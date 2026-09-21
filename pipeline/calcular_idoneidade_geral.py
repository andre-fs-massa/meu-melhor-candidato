"""Calcula o indicador Idoneidade Geral: média entre a idoneidade pessoal
do candidato (enriquecer_idoneidade.py) e a idoneidade do seu círculo
político -- vice, coligação, lideranças partidárias e padrinho político
(enriquecer_circulo_politico.py).

Só é calculado quando AMBOS os componentes existem para o candidato; não
presume nota a partir de um único componente nem para quem não foi
pesquisado em nenhuma das duas camadas.
"""
import sys

import pandas as pd

from . import config

INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")


def calcular(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ambos_presentes = df["nota_idoneidade"].notna() & df["nota_circulo_politico"].notna()
    df["nota_idoneidade_geral"] = pd.NA
    df.loc[ambos_presentes, "nota_idoneidade_geral"] = (
        df.loc[ambos_presentes, "nota_idoneidade"] + df.loc[ambos_presentes, "nota_circulo_politico"]
    ) / 2
    return df


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.enriquecer_circulo_politico` primeiro.")

    df = pd.read_parquet(INPUT_PATH)
    if "nota_idoneidade" not in df.columns or "nota_circulo_politico" not in df.columns:
        sys.exit(
            "Colunas nota_idoneidade/nota_circulo_politico ausentes -- rode "
            "enriquecer_idoneidade e enriquecer_circulo_politico primeiro."
        )

    resultado = calcular(df)

    n = resultado["nota_idoneidade_geral"].notna().sum()
    print(f"{n} candidatos com Idoneidade Geral calculada")
    print(
        resultado[resultado["nota_idoneidade_geral"].notna()]
        .sort_values(["cargo", "nota_idoneidade_geral"])[
            ["nome_urna", "cargo", "nota_idoneidade", "nota_circulo_politico", "nota_idoneidade_geral"]
        ]
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
