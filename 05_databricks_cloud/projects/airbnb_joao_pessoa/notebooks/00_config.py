# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Config
# MAGIC Parâmetros compartilhados por todos os notebooks do projeto.
# MAGIC
# MAGIC Uso: em cada notebook, uma célula só com `%run ./00_config`.

# COMMAND ----------

CATALOG = "airbnb_joao_pessoa"
BRONZE = f"{CATALOG}.bronze"
SILVER = f"{CATALOG}.silver"
GOLD = f"{CATALOG}.gold"

# Ajuste para o caminho do Volume onde estão os parquets
RAW_PATH = f"/Volumes/{CATALOG}/bronze/raw_files"

SOURCE_FILES = {
    "listings": "Listings_Data.parquet",
    "past_rates": "Past_Calendar_Rates.parquet",
    "future_rates": "Future_Calendar_Rates.parquet",
    "reviews": "Reviews_Data.parquet",
}

BRONZE_TABLES = {
    "listings": f"{BRONZE}.listings",
    "past_rates": f"{BRONZE}.past_calendar_rates",
    "future_rates": f"{BRONZE}.future_calendar_rates",
    "reviews": f"{BRONZE}.reviews",
}

SILVER_TABLES = {
    "listings": f"{SILVER}.listings",
    "past_rates": f"{SILVER}.past_calendar_rates",
    "future_rates": f"{SILVER}.future_calendar_rates",
    "reviews": f"{SILVER}.reviews",
}

GOLD_TABLES = {
    "dim_listing": f"{GOLD}.dim_listing",
    "fact_calendar_monthly": f"{GOLD}.fact_calendar_monthly",
    "area_demand_summary": f"{GOLD}.area_demand_summary",
    "area_monthly_demand": f"{GOLD}.area_monthly_demand",
}

# Granularidade (chave única) de cada tabela na bronze
GRAIN = {
    "listings": ["listing_id"],
    "past_rates": ["listing_id", "date"],
    "future_rates": ["listing_id", "date"],
    "reviews": ["listing_id", "date"],
}

# Área de estudo (caixa aproximada de João Pessoa).
# ATENÇÃO: é uma aproximação. 
BBOX = {"lat_min": -7.22, "lat_max": -7.04, "lon_min": -34.95, "lon_max": -34.78}

# Agrupamento espacial para a gold
H3_RESOLUTION = 7        # ~5 km² por célula; com 100 listings, resolução maior deixa células vazias
GRID_DECIMALS = 2        # fallback sem H3: grade de ~1,1 km (arredondamento de lat/lon)
MIN_LISTINGS_PER_AREA = 3  # abaixo disso a área não entra no ranking
