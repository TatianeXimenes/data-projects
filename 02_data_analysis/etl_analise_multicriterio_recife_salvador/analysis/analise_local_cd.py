
"""
Análise multi-critério para escolher a melhor capital para abrir um Centro de Distribuição (CD).

Entradas:
- data/cidades_candidatas.csv
- data/tempos_viagem_rodoviarios.csv
- data/demanda_estadual.csv
- pesos_criterios.json

Saídas:
- resultados/ranking.csv
- resultados/diagnostico.csv
- figuras/ranking.png

Como usar:
1) Substitua os valores dos CSVs por dados reais (IBGE, DNIT, Google Distance Matrix, etc.).
2) Ajuste os pesos em pesos_criterios.json conforme sua estratégia.
3) Rode: python analise_local_cd.py
"""

import os, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
RES_DIR = os.path.join(BASE_DIR, "resultados")
FIG_DIR = os.path.join(BASE_DIR, "figuras")
os.makedirs(RES_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# === Utilidades ===
def min_max_normalize(series, invert=False, eps=1e-9):
    s = series.astype(float)
    if invert:
        s = -s
    mn, mx = np.nanmin(s), np.nanmax(s)
    if np.isclose(mx - mn, 0):
        return pd.Series(np.ones(len(s))*0.5, index=series.index)
    return (s - mn) / (mx - mn + eps)

def topsis(matrix, weights, benefit_flags):
    """
    matrix: pd.DataFrame (alternatives x criteria)
    weights: list/np.array (sums to 1)
    benefit_flags: list of booleans where True means "benefit" (higher is better)
    """
    X = matrix.copy().astype(float).values
    # normalização vetorial
    denom = np.sqrt((X**2).sum(axis=0))
    denom[denom==0] = 1.0
    R = X / denom
    W = np.array(weights)
    V = R * W  # matriz ponderada
    # solucao ideal e anti-ideal
    ideal = np.array([V[:,j].max() if benefit_flags[j] else V[:,j].min() for j in range(V.shape[1])])
    anti_ideal = np.array([V[:,j].min() if benefit_flags[j] else V[:,j].max() for j in range(V.shape[1])])
    # distâncias
    d_pos = np.sqrt(((V - ideal)**2).sum(axis=1))
    d_neg = np.sqrt(((V - anti_ideal)**2).sum(axis=1))
    score = d_neg / (d_pos + d_neg + 1e-12)
    return score

# === Carregar dados ===
cidades = pd.read_csv(os.path.join(DATA_DIR, "cidades_candidatas.csv"))
tempos = pd.read_csv(os.path.join(DATA_DIR, "tempos_viagem_rodoviarios.csv"))
demanda = pd.read_csv(os.path.join(DATA_DIR, "demanda_estadual.csv"))
with open(os.path.join(BASE_DIR, "pesos_criterios.json"), "r", encoding="utf-8") as f:
    pesos = json.load(f)

# === 1) Custo imobiliário composto ===
# Índice composto (quanto menor melhor): aluguel + terreno + mão de obra + tributos (padronizados)
cidades["custo_aluguel_norm"] = min_max_normalize(cidades["aluguel_m2_R$"], invert=False)
cidades["custo_terreno_norm"] = min_max_normalize(cidades["preco_terreno_indice"], invert=False)
cidades["custo_mao_obra_norm"] = min_max_normalize(cidades["custo_mao_obra_indice"], invert=False)
cidades["custo_tributario_norm"] = min_max_normalize(cidades["carga_tributaria_indice"], invert=False)
cidades["custo_composto"] = (
    0.50*cidades["custo_aluguel_norm"]
  + 0.20*cidades["custo_terreno_norm"]
  + 0.20*cidades["custo_mao_obra_norm"]
  + 0.10*cidades["custo_tributario_norm"]
)

# === 2) Tempos de entrega médios ponderados pela demanda de destino ===
# potencial de consumo estadual: população * renda_per_capita * consumo_indice (normalizado)
demanda["potencial_bruto"] = demanda["populacao_milhoes"] * demanda["renda_per_capita_R$"] * demanda["consumo_indice"]
demanda["potencial"] = min_max_normalize(demanda["potencial_bruto"], invert=False)

# juntar tempos com potenciais de destino
tmp = tempos.merge(demanda.rename(columns={"estado":"estado_destino"})[["estado_destino","potencial"]],
                   on="estado_destino", how="left")
# tempo médio ponderado (quanto menor, melhor)
def weighted_mean_time(df):
    w = df["potencial"].fillna(0.0).values
    t = df["tempo_horas"].values
    if np.sum(w)==0:
        return np.nan
    return np.average(t, weights=w)

tempo_medio = tmp.groupby("origem").apply(weighted_mean_time).rename("tempo_medio_ponderado_h").reset_index()
cidades = cidades.merge(tempo_medio, left_on="cidade", right_on="origem", how="left").drop(columns=["origem"])
cidades["tempo_norm"] = min_max_normalize(cidades["tempo_medio_ponderado_h"], invert=False)

# === 3) Captação de demanda (gravidade) ===
# Quanto maior o potencial acessível em até T horas, melhor. Usamos um decaimento exponencial por tempo.
TETA = 0.10  # sensibilidade ao tempo (ajuste conforme necessidade)
tmp["decay"] = np.exp(-TETA * tmp["tempo_horas"])
tmp["potencial_acessivel"] = tmp["potencial"] * tmp["decay"]
cap = tmp.groupby("origem")["potencial_acessivel"].sum().rename("captacao_demanda").reset_index()
cidades = cidades.merge(cap, left_on="cidade", right_on="origem", how="left").drop(columns=["origem"])
cidades["captacao_norm"] = min_max_normalize(cidades["captacao_demanda"], invert=False)  # benefício (maior melhor)

# === Consolidação dos critérios ===
# Importante: custo_composto e tempo_norm são "custo" (quanto menor, melhor). captacao_norm é "benefício" (maior, melhor).
criterios = cidades.set_index(["cidade","estado"])[["custo_composto","tempo_norm","captacao_norm"]].copy()

# invertendo custos para que maior seja melhor em todos os critérios (opcional para método aditivo)
criterios_benef = criterios.copy()
criterios_benef["custo_benef"] = 1 - criterios_benef["custo_composto"]
criterios_benef["tempo_benef"] = 1 - criterios_benef["tempo_norm"]
criterios_benef = criterios_benef[["custo_benef","tempo_benef","captacao_norm"]]

# Pesos
w_custos = float(pesos.get("peso_custos", 0.4))
w_tempos = float(pesos.get("peso_tempos_entrega", 0.35))
w_consumo = float(pesos.get("peso_potencial_consumo", 0.25))
w = np.array([w_custos, w_tempos, w_consumo], dtype=float)
w = w / (w.sum() if w.sum()>0 else 1.0)

# === Método 1: Soma ponderada (WSM) ===
wsm_score = (criterios_benef * w).sum(axis=1).rename("score_wsm")

# === Método 2: TOPSIS ===
mat = criterios.copy()
# para TOPSIS, definimos quais critérios são benefício (True) ou custo (False)
benef_flags = [False, False, True]  # custo_composto, tempo_norm, captacao_norm
topsis_score = topsis(mat, weights=w, benefit_flags=benef_flags).reshape(-1)
topsis_score = pd.Series(topsis_score, index=mat.index, name="score_topsis")

# === Ranking final (média dos dois métodos) ===
final_score = pd.concat([wsm_score, topsis_score], axis=1).mean(axis=1).rename("score_final")
ranking = final_score.sort_values(ascending=False).reset_index()
ranking["posicao"] = np.arange(1, len(ranking)+1)

# === Diagnóstico detalhado ===
diag = criterios.reset_index().merge(ranking[["cidade","estado","score_final","posicao"]], on=["cidade","estado"])
diag = diag.merge(cidades[["cidade","estado","aluguel_m2_R$","tempo_medio_ponderado_h","captacao_demanda"]],
                  on=["cidade","estado"], how="left")

# === Salvar ===
ranking_path = os.path.join(RES_DIR, "ranking.csv")
diag_path = os.path.join(RES_DIR, "diagnostico.csv")
ranking.to_csv(ranking_path, index=False, encoding="utf-8")
diag.to_csv(diag_path, index=False, encoding="utf-8")

# === Gráfico simples ===
plt.figure()
plt.bar(ranking["cidade"], ranking["score_final"])
plt.title("Ranking de capitais – Score final")
plt.ylabel("Score")
plt.xlabel("Cidade")
plt.tight_layout()
fig_path = os.path.join(FIG_DIR, "ranking.png")
plt.savefig(fig_path, dpi=180)
print(f"Arquivos gerados:\n- {ranking_path}\n- {diag_path}\n- {fig_path}")
