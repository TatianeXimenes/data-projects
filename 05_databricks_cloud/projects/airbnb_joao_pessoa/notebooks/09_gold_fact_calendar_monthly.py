# Databricks notebook source
# MAGIC %md
# MAGIC # 09 - Gold: fato de calendário mensal
# MAGIC União de past e future (`period_type`), enriquecida com `area_cell` e `in_scope` da dimensão.
# MAGIC
# MAGIC Cuidado na análise: linhas `future` mostram só o que já estava reservado em `snapshot_date`.
# MAGIC Use-as para ritmo de reservas, não para comparar demanda com o passado.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./00_utils

# COMMAND ----------

past = spark.table(SILVER_TABLES["past_rates"])
future = spark.table(SILVER_TABLES["future_rates"])
dim = spark.table(GOLD_TABLES["dim_listing"]).select("listing_id", "area_cell", "in_scope")

fact = (
    past.unionByName(future)
    .join(dim, "listing_id", "inner")
    .withColumn("year_month", F.date_format("month_start", "yyyy-MM"))
)

# COMMAND ----------

(fact.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLES["fact_calendar_monthly"]))

# COMMAND ----------

f = spark.table(GOLD_TABLES["fact_calendar_monthly"])
T = GOLD_TABLES["fact_calendar_monthly"]
dq_check("gold", T, "linhas == past + future",
         abs(f.count() - (past.count() + future.count())))
dq_check("gold", T, "chave única (listing_id, month_start, period_type)",
         duplicates_by_key(f, ["listing_id", "month_start", "period_type"]).count())
dq_flush()

display(f.groupBy("period_type").agg(F.min("month_start").alias("de"), F.max("month_start").alias("ate"),
                                     F.countDistinct("listing_id").alias("listings")))

