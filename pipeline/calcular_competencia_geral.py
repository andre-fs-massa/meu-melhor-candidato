"""Calcula dois indicadores agregados a partir das colunas score_<competencia>
já existentes (proxy de ocupação + boost de experiência política + boost de
competência transferível, ver pipeline/enriquecer_competencia_transferivel.py):

  - nota_competencia: média das competências nomeadas do CARGO do candidato
    (4 competências por cargo, ver pipeline/competencias.py) -- um único
    número 0-10 resumindo as camadas de competência já calculadas.
  - nota_competencia_geral: média entre nota_competencia e nota_escolaridade
    (pipeline/mapear_escolaridade.py) -- só calculada quando ambos existem,
    não presume nota a partir de um único componente.

Cobre todos os cargos com framework de competência definido (não só
Presidente/Governador/Senador), já que nem este cálculo nem a nota de
escolaridade dependem de pesquisa individual por candidato.
"""
import sys

import pandas as pd

from . import competencias, config

INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")


def calcular(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["nota_competencia"] = pd.NA

    for cargo, competencias_cargo in competencias.COMPETENCIAS_POR_CARGO.items():
        mascara_cargo = df["cargo"] == cargo
        if not mascara_cargo.any():
            continue
        colunas_score = [
            f"score_{chave}" for chave in competencias_cargo if f"score_{chave}" in df.columns
        ]
        if not colunas_score:
            continue
        df.loc[mascara_cargo, "nota_competencia"] = df.loc[mascara_cargo, colunas_score].mean(
            axis=1, skipna=True
        )

    ambos_presentes = df["nota_competencia"].notna() & df["nota_escolaridade"].notna()
    df["nota_competencia_geral"] = pd.NA
    df.loc[ambos_presentes, "nota_competencia_geral"] = (
        df.loc[ambos_presentes, "nota_competencia"] + df.loc[ambos_presentes, "nota_escolaridade"]
    ) / 2

    df["nota_competencia"] = pd.to_numeric(df["nota_competencia"])
    df["nota_competencia_geral"] = pd.to_numeric(df["nota_competencia_geral"])

    return df


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.mapear_escolaridade` primeiro.")

    df = pd.read_parquet(INPUT_PATH)
    if "nota_escolaridade" not in df.columns:
        sys.exit("Coluna nota_escolaridade ausente -- rode `python -m pipeline.mapear_escolaridade` primeiro.")

    resultado = calcular(df)

    n = resultado["nota_competencia_geral"].notna().sum()
    print(f"{n:,} de {len(resultado):,} candidatos com Competência Geral calculada")
    print("\nMédia de Competência Geral por cargo:")
    print(
        resultado.groupby("cargo")[["nota_competencia", "nota_escolaridade", "nota_competencia_geral"]]
        .mean(numeric_only=True)
        .round(2)
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
