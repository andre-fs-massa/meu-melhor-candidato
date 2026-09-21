"""Gera, para cada candidato, a pontuação (0-10) nas 4 competências do seu
cargo, a partir da ocupação declarada (DS_OCUPACAO).

IMPORTANTE: isso é um proxy heurístico baseado só na ocupação
autodeclarada no registro de candidatura -- não é avaliação de
desempenho, histórico legislativo real nem verificação de veracidade.
Ver docstring de pipeline/competencia_dimensoes.py.
"""
import sys

import pandas as pd

from . import competencia_dimensoes as cd
from . import competencias, config

OUTPUT_PARQUET = config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias.parquet"
OUTPUT_CSV = config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias.csv"


def gerar_pontuacoes(df: pd.DataFrame) -> pd.DataFrame:
    cargos_sem_framework = set(df["cargo"].unique()) - set(
        competencias.COMPETENCIAS_POR_CARGO
    )
    if cargos_sem_framework:
        sys.exit(f"Cargo(s) sem framework de competências definido: {cargos_sem_framework}")

    df = df.copy()
    df["ocupacao_arquetipo"] = df["ocupacao"].apply(cd.classificar_ocupacao)

    dimensoes_por_ocupacao = {
        arquetipo: dict(vetor) for arquetipo, vetor in cd.ARQUETIPOS.items()
    }
    scores_dimensao = df["ocupacao_arquetipo"].map(dimensoes_por_ocupacao)

    for cargo, competencias_cargo in competencias.COMPETENCIAS_POR_CARGO.items():
        mascara_cargo = df["cargo"] == cargo
        if not mascara_cargo.any():
            continue
        mapa_dimensao = cd.CARGO_COMPETENCIA_DIMENSAO[cargo]
        for chave_competencia in competencias_cargo:
            dimensao = mapa_dimensao[chave_competencia]
            nome_coluna = f"score_{chave_competencia}"
            if nome_coluna not in df.columns:
                df[nome_coluna] = pd.NA
            df.loc[mascara_cargo, nome_coluna] = scores_dimensao[mascara_cargo].apply(
                lambda d, dim=dimensao: d[dim]
            )

    return df


def main() -> None:
    if not config.OUTPUT_PARQUET.exists():
        sys.exit(
            f"{config.OUTPUT_PARQUET} não existe. "
            "Rode `python -m pipeline.parse_candidatos` primeiro."
        )

    df = pd.read_parquet(config.OUTPUT_PARQUET)
    print(f"{len(df):,} candidatos carregados")

    resultado = gerar_pontuacoes(df)

    colunas_score = [c for c in resultado.columns if c.startswith("score_")]
    print(f"\nColunas de competência geradas: {colunas_score}")
    print("\nMédia de cada competência por cargo:")
    print(
        resultado.groupby("cargo")[colunas_score].mean().round(2).to_string()
    )

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
