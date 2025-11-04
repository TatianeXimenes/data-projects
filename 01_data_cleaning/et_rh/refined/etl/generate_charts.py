import pandas as pd
import matplotlib.pyplot as plt
from connections.conecta_via_SQLAlchemy import get_engine
import os

# CONFIG
OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
engine = get_engine()


# CONSULTAS SQL
queries = {
    # Turnover por satisfação
    "turnover_by_satisfaction": """
        SELECT job_satisfaction,
               COUNT(*) FILTER (WHERE attrition = 'Yes')::float / COUNT(*) AS turnover_rate
        FROM tabela_rh_textual
        GROUP BY job_satisfaction
        ORDER BY CASE job_satisfaction
                     WHEN 'Low' THEN 1
                     WHEN 'Medium' THEN 2
                     WHEN 'High' THEN 3
                 END;
    """,

    # OverTime por Trabalho Remoto
    "overtime_vs_remote": """
        SELECT remote_work,
               COUNT(*) FILTER (WHERE overtime='Yes') * 100.0 / COUNT(*) AS pct_overtime
        FROM tabela_rh_textual
        GROUP BY remote_work;
    """,

    # Média de Promoções por Nível
    "avg_promotions_by_level": """
        SELECT job_level, AVG(number_of_promotions) AS avg_promotions
        FROM tabela_rh_textual
        GROUP BY job_level;
    """,

    # Tempo médio por nível
    "avg_years_by_level": """
        SELECT job_level, AVG(years_at_company) AS avg_years
        FROM tabela_rh_textual
        GROUP BY job_level;
    """,

    # Distribuição por Cargo
    "distribution_by_role": """
        SELECT job_role, COUNT(*) AS total
        FROM tabela_rh_textual
        GROUP BY job_role;
    """,

    # Turnover por Área
    "turnover_by_role": """
        SELECT job_role,
               COUNT(*) FILTER (WHERE attrition='Left') * 100.0 / COUNT(*) AS pct_left
        FROM tabela_rh_textual
        GROUP BY job_role;
    """,

    # Salário médio por Área
    "avg_income_by_role": """
        SELECT job_role, AVG(monthly_income) AS avg_income
        FROM tabela_rh_textual
        GROUP BY job_role;
    """,

    # Satisfação média por área
    "avg_satisfaction_by_role": """
        SELECT job_role, 
                AVG(
                    CASE job_satisfaction
                        WHEN 'Low' THEN 1
                        WHEN 'Medium' THEN 2
                        WHEN 'High' THEN 3
                    END
                 ) AS avg_satisfaction
        FROM tabela_rh_textual
        GROUP BY job_role;
    """,

   # Performance média por nível
    "avg_performance_by_level": """
        SELECT job_level,
               AVG(
                   CASE performance_rating
                       WHEN 'Low' THEN 1
                       WHEN 'Medium' THEN 2
                       WHEN 'High' THEN 3
                   END
               ) AS avg_performance
        FROM tabela_rh_textual
        GROUP BY job_level
        ORDER BY job_level;
    """,

    # Turnover por Estado Civil
    "turnover_by_marital": """
        SELECT marital_status,
               COUNT(*) FILTER (WHERE attrition='Left') * 100.0 / COUNT(*) AS pct_left
        FROM tabela_rh_textual
        GROUP BY marital_status;
    """,

    # Oportunidade de liderança
    "leadership_opportunities": """
        SELECT leadership_opportunities, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tabela_rh_textual) AS pct
        FROM tabela_rh_textual
        GROUP BY leadership_opportunities;
    """,

    # Distribuição por Educação
    "education_distribution": """
        SELECT education_level, COUNT(*) AS total
        FROM tabela_rh_textual
        GROUP BY education_level;
    """
}

# FUNÇÃO PARA CRIAÇÃO DOS GRÁFICOS
def create_chart(df, x, y, title, filename, chart_type="bar"):
    plt.figure(figsize=(8,5))

    if chart_type == "bar":
        plt.bar(df[x], df[y])
    elif chart_type == "pie":
        plt.pie(df[y], labels=df[x], autopct='%1.1f%%')
    else:
        return

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{filename}.png", dpi=300)
    plt.close()

# EXECUÇÃO DAS QUERIES E GERAÇÃO DOS ARQUIVOS
for name, query in queries.items():
    print(f"🔎 Executando: {name}")
    df = pd.read_sql(query, engine)

    # se for contagem simples salva em csv
    if df.shape[1] == 1:
        df.to_csv(f"{OUTPUT_DIR}/{name}.csv", index=False)
        continue

    x, y = df.columns[0], df.columns[1]

    # Definição do tipo de gráfico
    if "distribution" in name or "education" in name or "role" in name:
        chart_type = "pie" if df[x].nunique() <= 6 else "bar"
    else:
        chart_type = "bar"

    create_chart(df, x, y, name.replace("_", " ").title(), name, chart_type)

print(f"\n Gráficos prontos e salvos em: {OUTPUT_DIR}/\n")

