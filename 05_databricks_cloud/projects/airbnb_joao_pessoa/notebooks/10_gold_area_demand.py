# Databricks notebook source
# MAGIC %md
# MAGIC # 10 - Gold: onde mais se aluga
# MAGIC Responde à pergunta do projeto por área (`area_cell`), usando só o calendário **passado** e anúncios `in_scope`.
# MAGIC
# MAGIC Métricas de demanda:
# MAGIC - `median_adjusted_occupancy`: mediana da ocupação ajustada (desconta dias bloqueados) dos anúncios da área
# MAGIC - `occupancy_raw`: noites reservadas / noites listadas no calendário (bloqueios contam como vagos)
# MAGIC - `reserved_nights_per_listing`: noites reservadas por anúncio
# MAGIC - `reviews_per_listing`: reviews no período por anúncio (proxy de estadias)
# MAGIC - `adr_brl`: diária média das noites reservadas, em reais (`native_revenue` / noites reservadas)
# MAGIC
# MAGIC Áreas com menos de `MIN_LISTINGS_PER_AREA` anúncios aparecem na tabela, mas **sem ranking**.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./00_utils

# COMMAND ----------

fact = spark.table(GOLD_TABLES["fact_calendar_monthly"])
dim = spark.table(GOLD_TABLES["dim_listing"]).filter("in_scope")
past = fact.filter((F.col("period_type") == "past") & F.col("in_scope"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo por área

# COMMAND ----------

area_cal = (
    past.groupBy("area_cell")
    .agg(
        F.countDistinct("listing_id").alias("n_listings"),
        F.sum("reserved_days").alias("reserved_nights"),
        F.sum(F.col("reserved_days") + F.col("vacant_days")).alias("listed_nights"),
        F.sum("native_revenue").alias("revenue_brl"),
    )
    .withColumn("occupancy_raw", F.col("reserved_nights") / F.col("listed_nights"))
    .withColumn("adr_brl", F.when(F.col("reserved_nights") > 0, F.col("revenue_brl") / F.col("reserved_nights")))
    .withColumn("reserved_nights_per_listing", F.col("reserved_nights") / F.col("n_listings"))
)

area_dim = dim.groupBy("area_cell").agg(
    F.avg(F.col("latitude").cast("double")).alias("center_lat"),
    F.avg(F.col("longitude").cast("double")).alias("center_lon"),
    F.percentile_approx("ttm_adjusted_occupancy", 0.5).alias("median_adjusted_occupancy"),
    F.avg("rating_overall").alias("avg_rating"),
    F.sum("reviews_in_period").alias("reviews_in_period"),
)

summary = (
    area_cal.join(area_dim, "area_cell")
    .withColumn("reviews_per_listing", F.col("reviews_in_period") / F.col("n_listings"))
    .withColumn("is_reliable", F.col("n_listings") >= MIN_LISTINGS_PER_AREA)
)

# Ranking só entre áreas confiáveis
w = Window.orderBy(F.desc("median_adjusted_occupancy"), F.desc("reserved_nights_per_listing"))
ranked = summary.filter("is_reliable").withColumn("demand_rank", F.dense_rank().over(w))
unranked = summary.filter("NOT is_reliable").withColumn("demand_rank", F.lit(None).cast("int"))
summary = ranked.unionByName(unranked)

# COMMAND ----------

(summary.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLES["area_demand_summary"]))

display(spark.table(GOLD_TABLES["area_demand_summary"]).orderBy(F.col("demand_rank").asc_nulls_last()))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sazonalidade por área (passado)

# COMMAND ----------

monthly = (
    past.groupBy("area_cell", "month_start")
    .agg(
        F.countDistinct("listing_id").alias("n_listings"),
        F.sum("reserved_days").alias("reserved_nights"),
        F.sum(F.col("reserved_days") + F.col("vacant_days")).alias("listed_nights"),
        F.sum("native_revenue").alias("revenue_brl"),
    )
    .withColumn("occupancy_raw", F.col("reserved_nights") / F.col("listed_nights"))
    .withColumn("adr_brl", F.when(F.col("reserved_nights") > 0, F.col("revenue_brl") / F.col("reserved_nights")))
)

(monthly.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLES["area_monthly_demand"]))

# COMMAND ----------

s = spark.table(GOLD_TABLES["area_demand_summary"])
dq_check("gold", GOLD_TABLES["area_demand_summary"], "area_cell única", duplicates_by_key(s, ["area_cell"]).count())
dq_check("gold", GOLD_TABLES["area_demand_summary"], "ocupação bruta entre 0 e 1",
         s.filter(any_out_of_range(["occupancy_raw"], 0, 1)).count())
dq_check("gold", GOLD_TABLES["area_demand_summary"], "soma de n_listings == anúncios in_scope",
         abs(s.agg(F.sum("n_listings")).first()[0] - dim.count()))
dq_flush()

