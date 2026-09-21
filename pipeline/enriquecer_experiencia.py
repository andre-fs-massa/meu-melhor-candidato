"""Ajusta as pontuações de competência com base em experiência política real
(cargos eletivos já ocupados), pesquisada manualmente e registrada em
data/reference/experiencia_politica.json.

Diferente de pipeline/mapear_competencias.py (que só usa DS_OCUPACAO como
proxy para todo mundo), aqui usamos um sinal mais forte -- cargo realmente
já ocupado -- mas só para os candidatos que já foram pesquisados (ver
_leiame do JSON). Para os demais, nada muda.

Regra: a pontuação final de cada competência é o MAIOR valor entre (a) o
proxy por ocupação já calculado e (b) a pontuação implícita pelos cargos
anteriores reais. Ou seja, experiência real só pode subir a nota, nunca
baixar um score que o proxy de ocupação já acertou por outro motivo.
"""
import json
import sys

import pandas as pd

from . import competencia_dimensoes as cd
from . import competencias, config

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "experiencia_politica.json"
OUTPUT_PARQUET = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_CSV = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.csv"
)

# Pontuação (0-10) que a experiência REAL em cada cargo anterior implica nas
# 9 dimensões genéricas (mesma ordem de cd.DIMENSOES). Cargos executivos
# (Presidente/Governador/Prefeito) puxam gestão/finanças/articulação;
# cargos legislativos puxam processo legislativo/fiscalização/articulação.
# Escala normalizada em 2026-09-21 (era 0-5; valores aqui são o dobro dos
# originais para manter a mesma ordinalidade relativa e a mesma escala de
# pipeline/competencia_dimensoes.py).
_BOOST_VETOR = {
    "PRESIDENTE":         [10, 10, 6, 4, 10, 4, 10, 4, 4],
    "GOVERNADOR":         [8, 8, 4, 4, 8, 4, 2, 6, 6],
    "PREFEITO":           [6, 4, 2, 2, 6, 4, 0, 8, 8],
    "SENADOR":            [4, 4, 8, 8, 6, 4, 4, 0, 0],
    "DEPUTADO FEDERAL":   [2, 2, 8, 6, 6, 4, 0, 0, 0],
    "DEPUTADO ESTADUAL":  [2, 2, 6, 4, 4, 6, 0, 0, 0],
    "DEPUTADO DISTRITAL": [2, 2, 6, 4, 4, 6, 0, 0, 0],
    "VEREADOR":           [2, 2, 4, 2, 4, 6, 0, 2, 4],
}
BOOST_POR_CARGO_ANTERIOR = {
    cargo: dict(zip(cd.DIMENSOES, vetor)) for cargo, vetor in _BOOST_VETOR.items()
}


def _boost_por_dimensao(cargos_anteriores: list) -> dict:
    """Máximo, por dimensão, entre todos os cargos anteriores do candidato."""
    boost = {dim: 0 for dim in cd.DIMENSOES}
    for cargo in cargos_anteriores:
        vetor_cargo = BOOST_POR_CARGO_ANTERIOR.get(cargo["cargo"])
        if vetor_cargo is None:
            continue
        for dim, valor in vetor_cargo.items():
            boost[dim] = max(boost[dim], valor)
    return boost


def enriquecer(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    df["teve_cargo_eletivo"] = pd.NA
    df["cargos_anteriores_resumo"] = pd.NA
    df["fontes_experiencia"] = pd.NA
    df["experiencia_pesquisada_em"] = pd.NA

    df = df.set_index("sq_candidato", drop=False)

    for sq, registro in referencia["candidatos"].items():
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({registro['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)
            continue

        cargo_pretendido = registro["cargo_pretendido"]
        mapa_dimensao = cd.CARGO_COMPETENCIA_DIMENSAO[cargo_pretendido]
        boost = _boost_por_dimensao(registro["cargos_anteriores"])

        for chave_competencia, dimensao in mapa_dimensao.items():
            col = f"score_{chave_competencia}"
            if col not in df.columns:
                continue
            valor_atual = df.at[sq, col]
            valor_atual = 0 if pd.isna(valor_atual) else valor_atual
            df.at[sq, col] = max(valor_atual, boost[dimensao])

        df.at[sq, "teve_cargo_eletivo"] = registro["teve_cargo_eletivo"]
        df.at[sq, "cargos_anteriores_resumo"] = "; ".join(
            f"{c['cargo']} ({c.get('local', '?')}, {c.get('periodo', '?')})"
            for c in registro["cargos_anteriores"]
        ) or "nenhum"
        df.at[sq, "fontes_experiencia"] = "; ".join(registro.get("fontes", []))
        df.at[sq, "experiencia_pesquisada_em"] = registro["pesquisado_em"]

    return df.reset_index(drop=True)


def main() -> None:
    if not config.OUTPUT_PARQUET.exists():
        sys.exit("Rode `python -m pipeline.mapear_competencias` primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    caminho_scores = (
        config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias.parquet"
    )
    df = pd.read_parquet(caminho_scores)
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    resultado = enriquecer(df, referencia)

    n_pesquisados = resultado["teve_cargo_eletivo"].notna().sum()
    print(f"{n_pesquisados} candidatos com experiência política pesquisada e aplicada")
    print(
        resultado[resultado["teve_cargo_eletivo"].notna()][
            ["nome_urna", "teve_cargo_eletivo", "cargos_anteriores_resumo"]
        ].to_string()
    )

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
