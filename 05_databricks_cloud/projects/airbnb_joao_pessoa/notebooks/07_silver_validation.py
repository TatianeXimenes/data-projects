# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # 07 - Validação cruzada da camada Silver
# MAGIC Checagens que envolvem mais de uma tabela: integridade referencial e reconciliação entre
# MAGIC `listings` (métricas ttm) e o calendário mensal. Rode depois dos notebooks 03 a 06.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./00_utils

# COMMAND ----------

listings = spark.table(SILVER_TABLES["listings"])
past = spark.table(SILVER_TABLES["past_rates"])
future = spark.table(SILVER_TABLES["future_rates"])
reviews = spark.table(SILVER_TABLES["reviews"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Integridade referencial

# COMMAND ----------

ids = listings.select("listing_id")
for key, df in [("past_rates", past), ("future_rates", future), ("reviews", reviews)]:
    orphans = df.select("listing_id").distinct().join(ids, "listing_id", "left_anti")
    dq_check("silver", SILVER_TABLES[key], "listing_id existe em silver.listings", orphans.count())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reconciliação: métricas ttm de `listings` x soma do calendário mensal
# MAGIC Só faz sentido para anúncios com os 12 meses no calendário. Diferenças aparecem como **aviso**:
# MAGIC podem ser janela de datas ou câmbio diferentes, e a definição exata deve ser confirmada no dicionário de dados da fonte.

# COMMAND ----------

cal = past.groupBy("listing_id").agg(
    F.count("*").alias("cal_months"),
    F.sum("reserved_days").alias("cal_reserved_days"),
    F.sum("revenue").alias("cal_revenue"),
)

recon = (
    listings.select("listing_id", "ttm_reserved_days", "ttm_total_days", "ttm_revenue", "ttm_revpar")
    .join(cal, "listing_id", "left")
    .withColumn("reserved_days_diff", F.col("ttm_reserved_days") - F.col("cal_reserved_days"))
    .withColumn("revenue_diff_pct",
                F.when(F.col("cal_revenue") > 0,
                       F.abs(F.col("ttm_revenue") - F.col("cal_revenue")) / F.col("cal_revenue")))
    .withColumn("revpar_implied_revenue", F.col("ttm_revpar") * F.col("ttm_total_days"))
    .withColumn("revpar_diff_pct",
                F.when(F.col("ttm_revenue") > 0,
                       F.abs(F.col("revpar_implied_revenue") - F.col("ttm_revenue")) / F.col("ttm_revenue")))
)
full_year = recon.filter(F.col("cal_months") == 12)

T = SILVER_TABLES["listings"]
dq_check("silver", T, "ttm_reserved_days == soma de reserved_days do calendário",
         full_year.filter(F.col("reserved_days_diff") != 0).count(), severity="warn")
dq_check("silver", T, "ttm_revenue ≈ soma de revenue do calendário (±5%)",
         full_year.filter(F.col("revenue_diff_pct") > 0.05).count(), severity="warn")
dq_check("silver", T, "ttm_revpar x dias ≈ ttm_revenue (±5%)",
         full_year.filter(F.col("revpar_diff_pct") > 0.05).count(), severity="warn")

display(full_year.filter((F.col("revenue_diff_pct") > 0.05) | (F.col("revpar_diff_pct") > 0.05))
        .orderBy(F.desc("revenue_diff_pct")))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cobertura (informativo)

# COMMAND ----------

print("Anúncios sem future calendar:")
display(listings.join(future.select("listing_id").distinct(), "listing_id", "left_anti")
        .select("listing_id", "listing_name", "room_type"))

print("Anúncios com menos de 12 meses no past calendar:")
display(cal.filter(F.col("cal_months") < 12))

print("Anúncios sem nenhuma review:")
display(listings.join(reviews.select("listing_id").distinct(), "listing_id", "left_anti")
        .select("listing_id", "listing_name"))

# COMMAND ----------

diag = (
    listings.select("listing_id", "currency", "single_fee_structure", "cleaning_fee",
                    "ttm_revenue", "ttm_revpar", "ttm_total_days")
    .join(cal, "listing_id")
    .filter(F.col("cal_months") == 12)
    .withColumn("ratio_ttm_vs_calendar",
                F.when(F.col("cal_revenue") > 0, F.col("ttm_revenue") / F.col("cal_revenue")))
    .withColumn("ratio_ttm_vs_revpar",
                F.when(F.col("ttm_revpar") > 0,
                       F.col("ttm_revenue") / (F.col("ttm_revpar") * F.col("ttm_total_days"))))
)

display(diag.select("ratio_ttm_vs_calendar", "ratio_ttm_vs_revpar")
        .summary("min", "25%", "50%", "75%", "max"))

display(diag.groupBy("single_fee_structure")
        .agg(F.count("*").alias("n"),
             F.percentile_approx("ratio_ttm_vs_calendar", 0.5).alias("mediana_ratio")))

# COMMAND ----------

from dateutil.relativedelta import relativedelta

past_start = past.agg(F.min("month_start")).first()[0]
past_end = past.agg(F.max("month_start")).first()[0]
future_start = future.agg(F.min("month_start")).first()[0]

dq_check("silver", SILVER_TABLES["future_rates"], "future começa no mês seguinte ao fim do past",
         0 if future_start == past_end + relativedelta(months=1) else 1, severity="warn")

dq_check("silver", SILVER_TABLES["reviews"], "reviews dentro da janela do past calendar",
         reviews.filter((F.col("month_start") < past_start) | (F.col("month_start") > past_end)).count(),
         severity="warn")

rev_sum = reviews.groupBy("listing_id").agg(F.sum("num_reviews").alias("reviews_window"))
dq_check("silver", SILVER_TABLES["reviews"], "reviews na janela <= num_reviews total do anúncio",
         listings.select("listing_id", "num_reviews").join(rev_sum, "listing_id")
         .filter(F.col("reviews_window") > F.col("num_reviews")).count(),
         severity="warn")

# COMMAND ----------

dq_flush()
