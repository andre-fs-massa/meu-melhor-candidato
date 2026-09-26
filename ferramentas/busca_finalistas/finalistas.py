"""Lista os finalistas atuais de deputado (recomendados por quadrante), com a nota de idoneidade e o motivo gravado.
Uso: python finalistas.py [UF ...] [--descontos] [--sem-rodada2]
(sem UF: todas; --descontos: só quem tem desconto ou "a confirmar"; --sem-rodada2: só quem ainda não teve a 2ª rodada)"""
import json
import sys

import pandas as pd

RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # raiz do repositório
sys.path.insert(0, RAIZ)
from pipeline.recomendar import preparar, recomendar  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
so_descontos = "--descontos" in sys.argv
sem_r2 = "--sem-rodada2" in sys.argv
idon = json.load(open(RAIZ + r"\data\reference\idoneidade.json", encoding="utf-8"))["candidatos"]
prof = json.load(open(RAIZ + r"\data\reference\profundidade_pesquisa.json", encoding="utf-8")).get("excecoes", {})
df = preparar(pd.read_parquet(RAIZ + r"\data\processed\candidatos_2026_competencias_enriquecido.parquet"))
df["sq_candidato"] = df["sq_candidato"].astype(str)
dep = df[df.cargo.str.startswith("DEPUTADO")]
ufs = args or sorted(dep.uf.unique())
nomes = dep.set_index("sq_candidato")["nome_completo"]

for uf in ufs:
    for cargo in ("DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "DEPUTADO DISTRITAL"):
        if not ((dep.cargo == cargo) & (dep.uf == uf)).any():
            continue
        for r in recomendar(df, cargo, uf)["recomendados"]:
            sq = str(r["sq"])
            reg = idon.get(sq, {})
            motivo = reg.get("motivo", "")
            desc = reg.get("nota", 10) < 10 or "confirmar" in motivo
            if so_descontos and not desc:
                continue
            if sem_r2 and reg.get("rodada2"):
                continue
            print(f"{uf} | {cargo[9:12]} | {r['quadrante'][:3]} | {sq} | {r['nome_urna']} | {nomes.get(sq, '')} | "
                  f"{r['partido']} | nota {reg.get('nota', '-')} | {prof.get(sq, '-')} | r2 {reg.get('rodada2', '-')} | {motivo[:160]}")
