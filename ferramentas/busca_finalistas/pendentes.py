"""Lista quem falta pesquisar no bloco do topo de cada quadrante (deputados) de uma UF.

Bloco = candidatos elegíveis (dentro da disputa e acima do corte) com qualificação geral >= a do último
recomendado do quadrante. A UF está fechada quando todo recomendado já tem busca na web (origem busca_finalistas)
e nenhum não pesquisado empata com a última vaga.
Uso: python pendentes.py SP
"""
import json
import sys

import pandas as pd

RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # raiz do repositório
sys.path.insert(0, RAIZ)
from pipeline.recomendar import preparar, recomendar  # noqa: E402

uf = sys.argv[1]
idon = json.load(open(RAIZ + r"\data\reference\idoneidade.json", encoding="utf-8"))["candidatos"]
feitos = {sq for sq, r in idon.items() if r.get("origem") == "busca_finalistas"}
df = preparar(pd.read_parquet(RAIZ + r"\data\processed\candidatos_2026_competencias_enriquecido.parquet"))
df["sq_candidato"] = df["sq_candidato"].astype(str)
pend = []
for cargo in ("DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "DEPUTADO DISTRITAL"):
    if not ((df.cargo == cargo) & (df.uf == uf)).any():
        continue
    res = recomendar(df, cargo, uf)
    for q in ("LIBERTARIO", "DIREITA", "ESQUERDA", "AUTORITARIO"):
        rec = [r for r in res["recomendados"] if r["quadrante"] == q]
        if not rec:
            continue
        lim = min(r["qualificacao_geral"] for r in rec)
        U = df[(df.cargo == cargo) & (df.uf == uf) & (df.quadrante == q) & df.fora_da_disputa.isna()
               & (df.nota_idoneidade_geral >= res["corte"]) & (df.nota_qualificacao_geral >= lim - 1e-9)]
        falta = U[~U.sq_candidato.isin(feitos)]
        ok = sum(str(r["sq"]) in feitos for r in rec)
        print(f"# {cargo[9:]} {q[:3]}: corte da vaga {lim:.2f}, bloco {len(U)}, finalistas pesquisados {ok}/{len(rec)}, faltam {len(falta)}")
        for _, x in falta.iterrows():
            pend.append(x.sq_candidato)
            print(f"{x.sq_candidato} | {cargo[9:12]} | {x.nome_urna} | {x.nome_completo} | {x.partido} {x.numero} | "
                  f"{x.ocupacao} | cargos: {x.cargos_anteriores_resumo}")
print(f"TOTAL pendentes {uf}: {len(pend)}")
