# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Utilitários
# MAGIC Funções compartilhadas: auditoria de qualidade (`dq_check` / `dq_flush`), perfis de nulos,
# MAGIC chaves duplicadas, constraints e a transformação/validação dos calendários (past e future).
# MAGIC
# MAGIC Uso: `%run ./00_config` e depois `%run ./00_utils`, cada um em sua própria célula.

# COMMAND ----------

from datetime import datetime
from pyspark.sql import functions as F, Window

# COMMAND ----------

# MAGIC %md
# MAGIC ## Auditoria de qualidade
# MAGIC `dq_check` registra cada regra. `dq_flush` grava tudo em `audit.dq_results` e **falha** se alguma regra
# MAGIC com severidade `error` tiver linhas com problema. Regras `warn` só avisam.

# COMMAND ----------

_DQ_RESULTS = []


def dq_check(layer, table, rule, failing_rows, severity="error"):
    failing_rows = int(failing_rows)
    passed = failing_rows == 0
    _DQ_RESULTS.append((datetime.now(), layer, table, rule, failing_rows, severity, passed))
    status = "OK  " if passed else ("FAIL" if severity == "error" else "WARN")
    print(f"[{status}] {table} | {rule} | linhas com problema: {failing_rows}")


def dq_flush():
    if not _DQ_RESULTS:
        return
    schema = (
        "run_ts timestamp, layer string, table_name string, rule string, "
        "failing_rows long, severity string, passed boolean"
    )
    results = spark.createDataFrame(_DQ_RESULTS, schema)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.audit")
    results.write.format("delta").mode("append").saveAsTable(f"{CATALOG}.audit.dq_results")

    errors = [r for r in _DQ_RESULTS if (not r[6]) and r[5] == "error"]
    _DQ_RESULTS.clear()
    if errors:
        detail = "; ".join(f"{e[2]}: {e[3]}" for e in errors)
        raise AssertionError(f"{len(errors)} regra(s) com erro -> {detail}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Helpers genéricos

# COMMAND ----------

def null_profile(df):
    """Contagem e % de nulos por coluna, em formato longo (uma linha por coluna)."""
    total = df.count()
    row = df.select([F.sum(F.col(c).isNull().cast("int")).alias(c) for c in df.columns]).first().asDict()
    data = [(c, int(n or 0), round(100.0 * int(n or 0) / total, 1) if total else 0.0) for c, n in row.items()]
    return spark.createDataFrame(data, "column string, nulls long, pct double").orderBy(F.desc("nulls"))


def duplicates_by_key(df, keys):
    """Chaves repetidas na granularidade informada."""
    return df.groupBy(*keys).count().filter(F.col("count") > 1)


def any_out_of_range(cols, lo=None, hi=None):
    """Condição verdadeira se alguma coluna estiver abaixo de lo ou acima de hi (nulos são ignorados)."""
    cond = F.lit(False)
    for c in cols:
        if lo is not None:
            cond = cond | (F.col(c) < lo)
        if hi is not None:
            cond = cond | (F.col(c) > hi)
    return cond


def add_check(table, name, expr):
    """CHECK constraint do Delta, idempotente (remove e recria)."""
    spark.sql(f"ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {name}")
    spark.sql(f"ALTER TABLE {table} ADD CONSTRAINT {name} CHECK ({expr})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Calendários (past e future compartilham o mesmo schema)
# MAGIC Observação: a granularidade é **anúncio x mês**. A coluna `date` da bronze é o primeiro dia do mês,
# MAGIC por isso na silver ela vira `month_start`. No future, `occupancy`/`reserved_days` são apenas o que já estava
# MAGIC reservado na data da extração (`snapshot_date`), não uma projeção de demanda.

# COMMAND ----------

CALENDAR_COLUMNS = [
    "listing_id", "month_start", "period_type", "snapshot_date", "days_in_month",
    "vacant_days", "reserved_days", "occupancy",
    "revenue", "rate_avg", "booked_rate_avg",
    "booking_lead_time_avg", "length_of_stay_avg", "min_nights_avg",
    "native_booked_rate_avg", "native_rate_avg", "native_revenue",
    "has_bookings", "stay_metrics_available",
]


def transform_calendar(df, period_type):
    """Bronze -> silver para past/future. period_type: 'past' ou 'future'."""
    return (
        df.withColumnRenamed("date", "month_start")
        .withColumn("snapshot_date", F.to_date("_source_modified_at"))
        .withColumn("period_type", F.lit(period_type))
        .withColumn("days_in_month", F.dayofmonth(F.last_day("month_start")))
        .withColumn("has_bookings", F.col("reserved_days") > 0)
        # lead time e tempo de estadia só existem quando há reservas
        .withColumn(
            "stay_metrics_available",
            F.col("booking_lead_time_avg").isNotNull() & F.col("length_of_stay_avg").isNotNull(),
        )
        .select(*CALENDAR_COLUMNS)
    )


def validate_calendar(df, table, bronze_table):
    n_bronze = spark.table(bronze_table).count()
    dq_check("silver", table, "contagem == bronze", abs(df.count() - n_bronze))
    dq_check("silver", table, "chave única (listing_id, month_start)",
             duplicates_by_key(df, ["listing_id", "month_start"]).count())
    dq_check("silver", table, "month_start é dia 1",
             df.filter(F.dayofmonth("month_start") != 1).count())
    dq_check("silver", table, "ocupação entre 0 e 1",
             df.filter(any_out_of_range(["occupancy"], 0, 1)).count())
    dq_check("silver", table, "dias e valores monetários >= 0",
             df.filter(any_out_of_range(
                 ["vacant_days", "reserved_days", "revenue", "native_revenue", "rate_avg", "native_rate_avg"], 0
             )).count())

    # Regras que eu não consegui confirmar nos dados: começam como aviso.
    dq_check("silver", table, "vacant_days + reserved_days = dias do mês",
             df.filter(F.col("vacant_days") + F.col("reserved_days") != F.col("days_in_month")).count(),
             severity="warn")
    total_days = F.col("vacant_days") + F.col("reserved_days")
    dq_check("silver", table, "ocupação = reservados / (vagos + reservados)",
             df.filter((total_days > 0) &
                       (F.abs(F.col("occupancy") - F.col("reserved_days") / total_days) > 0.005)).count(),
             severity="warn")
    dq_check("silver", table, "booked_rate_avg nulo somente quando não há reservas",
             df.filter(F.col("has_bookings") == F.col("booked_rate_avg").isNull()).count(),
             severity="warn")
