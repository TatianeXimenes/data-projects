from sqlalchemy import create_engine
import pandas as pd


df = pd.read_csv("/home/tatiane/data-projects/01_data_cleaning/et_rh/refined/data/clean_transformed_rh.csv")

usuario = "postgres"
senha = "senha"
host = "localhost"
banco = "rh_db"
porta = "5432"

engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")

df.to_sql("tabela_rh", engine, if_exists="replace", index=False)

print("Dados carregados com sucesso!")
