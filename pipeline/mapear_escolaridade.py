"""Calcula uma nota 0-10 de grau de instrução a partir do campo oficial do
TSE `DS_GRAU_INSTRUCAO` (coluna `escolaridade` após parse_candidatos.py).

Diferente das camadas de idoneidade/círculo político/posicionamento
ideológico/competência transferível, isso NÃO é pesquisa -- é uma
transformação determinística de um campo que já vem preenchido pelo TSE
para todo mundo (autodeclarado pelo candidato no registro de candidatura).
Por isso cobre os 20.060 candidatos de uma vez, não só um recorte de cargo.

Escala: os 8 níveis oficiais do TSE, na ordem crescente do próprio
dicionário de dados do TSE, mapeados linearmente para 0-10. "NÃO
DIVULGÁVEL" (ou qualquer valor fora da lista) fica com nota ausente (NaN),
não é tratado como grau mais baixo -- é dado faltante, não analfabetismo.
"""
import sys

import pandas as pd

from . import config

INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")

# Ordem oficial crescente do TSE (dicionário de dados do consulta_cand),
# mapeada linearmente para 0-10.
NIVEIS_ESCOLARIDADE = [
    "ANALFABETO",
    "LÊ E ESCREVE",
    "ENSINO FUNDAMENTAL INCOMPLETO",
    "ENSINO FUNDAMENTAL COMPLETO",
    "ENSINO MÉDIO INCOMPLETO",
    "ENSINO MÉDIO COMPLETO",
    "SUPERIOR INCOMPLETO",
    "SUPERIOR COMPLETO",
]
NOTA_POR_NIVEL = {
    nivel: round(i * 10 / (len(NIVEIS_ESCOLARIDADE) - 1), 2)
    for i, nivel in enumerate(NIVEIS_ESCOLARIDADE)
}


def calcular(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["nota_escolaridade"] = df["escolaridade"].map(NOTA_POR_NIVEL)

    nao_mapeados = sorted(
        set(df.loc[df["nota_escolaridade"].isna(), "escolaridade"].dropna().unique())
    )
    if nao_mapeados:
        print(
            f"Aviso: {len(nao_mapeados)} valor(es) de escolaridade fora do dicionário "
            f"oficial, ficaram sem nota: {nao_mapeados}",
            file=sys.stderr,
        )
    return df


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.enriquecer_posicionamento_ideologico` primeiro.")

    df = pd.read_parquet(INPUT_PATH)
    resultado = calcular(df)

    n = resultado["nota_escolaridade"].notna().sum()
    print(f"{n:,} de {len(resultado):,} candidatos com nota de escolaridade calculada")
    print("\nDistribuição por nível:")
    print(
        resultado.groupby("escolaridade")["nota_escolaridade"]
        .agg(["first", "count"])
        .rename(columns={"first": "nota"})
        .sort_values("nota")
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
