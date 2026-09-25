"""Gera a seção de uma UF do relatório da busca dos deputados finalistas (markdown), a partir dos dados gravados.
Uso: python secao_uf.py SP"""
import json
import sys

import pandas as pd

RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # raiz do repositório
sys.path.insert(0, RAIZ)
from pipeline.recomendar import preparar, recomendar  # noqa: E402

uf = sys.argv[1]
idon = json.load(open(RAIZ + r"\data\reference\idoneidade.json", encoding="utf-8"))["candidatos"]
df = preparar(pd.read_parquet(RAIZ + r"\data\processed\candidatos_2026_competencias_enriquecido.parquet"))
df["sq_candidato"] = df["sq_candidato"].astype(str)
d = df[df.uf.eq(uf) & df.cargo.str.startswith("DEPUTADO")].set_index("sq_candidato")
busca = {sq: r for sq, r in idon.items() if r.get("origem") == "busca_finalistas" and sq in d.index}

Q = {"LIBERTARIO": "Libertário", "DIREITA": "Direita conservadora", "ESQUERDA": "Esquerda progressista", "AUTORITARIO": "Estatista-autoritário"}
L = [f"### {uf}", "", f"Pesquisados: {len(busca)} candidatos (1 busca cada, mais confirmações quando houve sinal grave).", ""]

estr = json.load(open(RAIZ + r"\data\processed\estrutural_idoneidade.json", encoding="utf-8"))["candidatos"]
com = [(sq, r) for sq, r in busca.items() if len(r["achados"]) > len(estr[sq].get("achados", []))]
L.append("**Achados que descontaram na busca:**")
L.append("")
for sq, r in sorted(com, key=lambda x: x[1]["nota"]):
    x = d.loc[sq]
    L.append(f"- **{r['nome_urna']}** ({x.partido}, {x.cargo.title()}), idoneidade pessoal {r['nota']:g}, geral {x.nota_idoneidade_geral:g}: {r['motivo'].replace('Busca rápida na internet (1 busca): ', '')}")
L.append("")
conf = [(sq, r) for sq, r in busca.items() if "A confirmar" in r["motivo"] or "a confirmar" in r["motivo"]]
if conf:
    L.append("**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**")
    L.append("")
    for sq, r in conf:
        x = d.loc[sq]
        L.append(f"- {r['nome_urna']} ({x.partido}, {x.cargo.title()}): {r['motivo'].replace('Busca rápida na internet (1 busca): ', '')}")
    L.append("")
L.append("**Finalistas depois da busca** (todos pesquisados):")
L.append("")
for cargo in ("DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "DEPUTADO DISTRITAL"):
    if not ((df.cargo == cargo) & (df.uf == uf)).any():
        continue
    res = recomendar(df, cargo, uf)
    for q, nome in Q.items():
        rs = [r for r in res["recomendados"] if r["quadrante"] == q]
        if not rs:
            L.append(f"- {cargo.title()} · {nome}: vazio")
            continue
        nomes = ", ".join(f"{r['nome_urna']} ({r['partido']} {r['numero']})" for r in rs)
        emp = rs[-1]["empatados_na_ultima_vaga"]
        L.append(f"- {cargo.title()} · {nome}: {nomes}" + (f" — sorteio entre {emp} empatados" if emp else ""))
L.append("")
print("\n".join(L))
