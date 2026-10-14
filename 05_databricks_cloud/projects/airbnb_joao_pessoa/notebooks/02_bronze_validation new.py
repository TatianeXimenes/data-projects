# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # 02 - Validação da camada Bronze
# MAGIC Profiling feito **uma única vez**, lendo a bronze. Os notebooks silver só aplicam decisões e conferem o resultado.
# MAGIC As regras ficam registradas em `audit.dq_results`; regras com severidade `error` interrompem a execução.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./00_utils

# COMMAND ----------

bronze = {key: spark.table(table) for key, table in BRONZE_TABLES.items()}

# COMMAND ----------

# MAGIC %md
# MAGIC ## Volume e rastreio

# COMMAND ----------

for key, df in bronze.items():
    print(f"{key}: {df.count()} linhas, {len(df.columns)} colunas")
    df.select("_source_file", "_source_modified_at").distinct().show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Nulos por coluna (somente observação)
# MAGIC Nulos estruturais esperados: `guests`/`bedrooms` em quarto privado, `booked_rate_avg` e métricas de estadia em meses sem reserva.

# COMMAND ----------

for key, df in bronze.items():
    print(f"=== {key}")
    display(null_profile(df).filter("nulls > 0"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Regras

# COMMAND ----------

# Chave única na granularidade correta (listing x mês nas tabelas de série)
for key, keys in GRAIN.items():
    dq_check("bronze", BRONZE_TABLES[key], f"chave única {keys}", duplicates_by_key(bronze[key], keys).count())

# COMMAND ----------

# Integridade referencial: todo listing_id das tabelas filhas existe em listings
ids = bronze["listings"].select("listing_id").distinct()
for key in ["past_rates", "future_rates", "reviews"]:
    orphans = bronze[key].select("listing_id").distinct().join(ids, "listing_id", "left_anti")
    dq_check("bronze", BRONZE_TABLES[key], "listing_id existe em listings", orphans.count())

# COMMAND ----------

# Calendários
for key in ["past_rates", "future_rates"]:
    df = bronze[key]
    t = BRONZE_TABLES[key]
    days = F.dayofmonth(F.last_day("date"))
    total = F.col("vacant_days") + F.col("reserved_days")

    dq_check("bronze", t, "date é o primeiro dia do mês", df.filter(F.dayofmonth("date") != 1).count())
    dq_check("bronze", t, "ocupação entre 0 e 1", df.filter(any_out_of_range(["occupancy"], 0, 1)).count())
    dq_check("bronze", t, "dias e valores monetários >= 0",
             df.filter(any_out_of_range(
                 ["vacant_days", "reserved_days", "revenue", "native_revenue", "rate_avg", "native_rate_avg"], 0
             )).count())
    dq_check("bronze", t, "vacant_days + reserved_days = dias do mês",
             df.filter(total != days).count(), severity="warn")
    dq_check("bronze", t, "ocupação = reservados / (vagos + reservados)",
             df.filter((total > 0) & (F.abs(F.col("occupancy") - F.col("reserved_days") / total) > 0.005)).count(),
             severity="warn")
    # hipótese dos nulos estruturais: booked_rate_avg é nulo exatamente quando reserved_days = 0
    dq_check("bronze", t, "booked_rate_avg nulo somente quando reserved_days = 0",
             df.filter((F.col("reserved_days") == 0) == F.col("booked_rate_avg").isNotNull()).count(),
             severity="warn")

# COMMAND ----------

# Reviews
rv = bronze["reviews"]
dq_check("bronze", BRONZE_TABLES["reviews"], "num_reviews == tamanho de reviewers",
         rv.filter(F.col("num_reviews") != F.size("reviewers")).count())

# COMMAND ----------

# Listings
ls = bronze["listings"]
t = BRONZE_TABLES["listings"]
dq_check("bronze", t, "latitude/longitude preenchidas",
         ls.filter(F.col("latitude").isNull() | F.col("longitude").isNull()).count())
dq_check("bronze", t, "ocupações entre 0 e 1",
         ls.filter(any_out_of_range(["ttm_occupancy", "ttm_adjusted_occupancy",
                                     "l90d_occupancy", "l90d_adjusted_occupancy"], 0, 1)).count())
dq_check("bronze", t, "coordenadas dentro da área de estudo",
         ls.filter(~(F.col("latitude").cast("double").between(BBOX["lat_min"], BBOX["lat_max"]) &
                     F.col("longitude").cast("double").between(BBOX["lon_min"], BBOX["lon_max"]))).count(),
         severity="warn")

# COMMAND ----------

dq_flush()
