# Databricks notebook source
# MAGIC %md
# MAGIC # 08 - Gold: dimensão de anúncios
# MAGIC Uma linha por anúncio, com:
# MAGIC - `area_cell`: célula espacial (H3 se disponível no cluster; senão grade de lat/lon arredondada)
# MAGIC - flags de cobertura: `months_in_past_calendar`, `has_future_calendar`, `is_full_year`
# MAGIC - `reviews_in_period`: reviews no período do calendário (proxy de estadias)
# MAGIC - `in_scope`: imóvel inteiro + dentro da área de estudo + 12 meses de calendário
# MAGIC
# MAGIC `host_name` não é levado para a gold (dado pessoal).

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %run ./00_utils

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD}")

listings = spark.table(SILVER_TABLES["listings"])
past = spark.table(SILVER_TABLES["past_rates"])
future = spark.table(SILVER_TABLES["future_rates"])
reviews = spark.table(SILVER_TABLES["reviews"])

# COMMAND ----------

past_cov = past.groupBy("listing_id").agg(F.count("*").alias("months_in_past_calendar"))
future_ids = future.select("listing_id").distinct().withColumn("has_future_calendar", F.lit(True))
review_agg = reviews.groupBy("listing_id").agg(F.sum("num_reviews").alias("reviews_in_period"))

dim = (
    listings
    .join(past_cov, "listing_id", "left")
    .join(future_ids, "listing_id", "left")
    .join(review_agg, "listing_id", "left")
    .withColumn("has_future_calendar", F.coalesce("has_future_calendar", F.lit(False)))
    .withColumn("reviews_in_period", F.coalesce("reviews_in_period", F.lit(0)))
    .withColumn("is_full_year", F.col("months_in_past_calendar") == 12)
    .withColumn("is_entire_home", F.col("room_type") == "entire_home")
    .withColumn("in_scope", F.col("is_entire_home") & F.col("within_study_area") & F.col("is_full_year"))
    .drop("host_name")
)

# COMMAND ----------

def add_area_cell(df):
    """Tenta H3 (funções nativas do Databricks); se não estiver disponível, usa grade de lat/lon."""
    try:
        out = df.withColumn(
            "area_cell",
            F.expr(
                "h3_h3tostring(h3_longlatash3("
                f"CAST(longitude AS DOUBLE), CAST(latitude AS DOUBLE), {H3_RESOLUTION}))"
            ),
        )
        out.limit(1).collect()  # força a execução para detectar erro de função/cluster
        return out, f"h3_res{H3_RESOLUTION}"
    except Exception as e:
        print(f"H3 indisponível ({type(e).__name__}); usando grade de {GRID_DECIMALS} casas decimais.")
        lat = F.round(F.col("latitude").cast("double"), GRID_DECIMALS).cast("string")
        lon = F.round(F.col("longitude").cast("double"), GRID_DECIMALS).cast("string")
        return df.withColumn("area_cell", F.concat_ws("_", lat, lon)), f"grid_{GRID_DECIMALS}dec"


dim, area_method = add_area_cell(dim)
dim = dim.withColumn("area_method", F.lit(area_method))
print("Método de área:", area_method)

# COMMAND ----------

(dim.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLES["dim_listing"]))

# COMMAND ----------

d = spark.table(GOLD_TABLES["dim_listing"])
dq_check("gold", GOLD_TABLES["dim_listing"], "listing_id único", duplicates_by_key(d, ["listing_id"]).count())
dq_check("gold", GOLD_TABLES["dim_listing"], "area_cell preenchida", d.filter(F.col("area_cell").isNull()).count())
dq_flush()

print("Anúncios no escopo:", d.filter("in_scope").count(), "de", d.count())
display(d.groupBy("room_type", "within_study_area", "is_full_year").count().orderBy("room_type"))

