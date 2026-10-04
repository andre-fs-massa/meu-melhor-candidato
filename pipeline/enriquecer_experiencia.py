"""Ajusta as pontuações de competência com base em experiência política real
(cargos eletivos já ocupados), pesquisada manualmente e registrada em
data/reference/experiencia_politica.json (e, para deputados, nos registros
estruturais do TSE de 2014 a 2024).

Regra (2026-10-04, pipeline/pesos_competencia.py): mandato no MESMO poder do
cargo pretendido vale igual nas 4 frentes, conforme a esfera (10 / 8 / 6, vice
2 a menos); mandato no OUTRO poder vale a mesma tabela vezes a transferência de
cada frente, com teto 8. A pontuação final de cada frente é o MAIOR valor entre
o que já estava (profissão, pipeline/mapear_competencias.py) e o do mandato:
experiência real só pode subir a nota.

Quem declarou ao TSE um título político como ocupação (Vereador, Deputado...)
e não tem mandato localizado nos registros conta como tendo exercido aquele
cargo (TITULO_COMO_MANDATO).
"""
import json
import sys

import pandas as pd

from . import competencias, config
from .pesos_competencia import TITULO_COMO_MANDATO, notas_por_mandatos

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "experiencia_politica.json"
# Gerado sem pesquisa manual por pipeline/gerar_estrutural_deputados.py (deputados); o JSON manual tem precedência.
ESTRUTURAL_PATH = config.PROCESSED_DIR / "estrutural_experiencia_politica.json"
OUTPUT_PARQUET = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_CSV = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.csv"
)


def cargos_exercidos(registro: dict | None, ocupacao) -> list:
    """Cargos eletivos já exercidos; sem nenhum localizado, o título político declarado como ocupação."""
    cargos = [c["cargo"] for c in (registro or {}).get("cargos_anteriores", [])]
    if not cargos and ocupacao in TITULO_COMO_MANDATO:
        cargos = [TITULO_COMO_MANDATO[ocupacao]]
    return cargos


def enriquecer(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    df["teve_cargo_eletivo"] = pd.NA
    df["cargos_anteriores_resumo"] = pd.NA
    df["fontes_experiencia"] = pd.NA
    df["experiencia_pesquisada_em"] = pd.NA

    df = df.set_index("sq_candidato", drop=False)
    candidatos = referencia["candidatos"]
    for sq in candidatos:
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({candidatos[sq]['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)

    for sq, cargo, ocupacao in zip(df["sq_candidato"], df["cargo"], df["ocupacao"]):
        if cargo not in competencias.COMPETENCIAS_POR_CARGO:
            continue
        notas = notas_por_mandatos(cargo, cargos_exercidos(candidatos.get(sq), ocupacao))
        for chave, (nota, _, _) in zip(competencias.COMPETENCIAS_POR_CARGO[cargo], notas):
            col = f"score_{chave}"
            valor_atual = df.at[sq, col]
            valor_atual = 0 if pd.isna(valor_atual) else valor_atual
            df.at[sq, col] = max(valor_atual, nota)

    for sq, registro in candidatos.items():
        if sq not in df.index:
            continue
        df.at[sq, "teve_cargo_eletivo"] = registro["teve_cargo_eletivo"]
        df.at[sq, "cargos_anteriores_resumo"] = "; ".join(
            f"{c['cargo']} ({c.get('local', '?')}, {c.get('periodo', '?')})"
            for c in registro["cargos_anteriores"]
        ) or "nenhum"
        df.at[sq, "fontes_experiencia"] = "; ".join(registro.get("fontes", []))
        df.at[sq, "experiencia_pesquisada_em"] = registro["pesquisado_em"]

    return df.reset_index(drop=True)


def carregar_referencia() -> dict:
    """JSON manual de experiência política + registros estruturais de deputados (o manual tem precedência)."""
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    if ESTRUTURAL_PATH.exists():
        estrutural = json.loads(ESTRUTURAL_PATH.read_text(encoding="utf-8"))["candidatos"]
        print(f"{len(estrutural):,} registros estruturais (deputados) somados aos {len(referencia['candidatos']):,} manuais")
        # 2026-09-30: o registro manual tem precedência, mas ganha os mandatos do TSE (2014-2024) que não citava
        # (ex.: Marina Silva sem o mandato de deputada federal de 2023). Casa por cargo, sem duplicar.
        for sq, man in referencia["candidatos"].items():
            est = estrutural.get(sq)
            if not est or not est["cargos_anteriores"]:
                continue
            ja = {c["cargo"] for c in man["cargos_anteriores"]}
            novos = [c for c in est["cargos_anteriores"] if c["cargo"] not in ja]
            if novos:
                man["cargos_anteriores"] = man["cargos_anteriores"] + novos
                man["teve_cargo_eletivo"] = True
        referencia["candidatos"] = {**estrutural, **referencia["candidatos"]}
    return referencia


def main() -> None:
    if not config.OUTPUT_PARQUET.exists():
        sys.exit("Rode `python -m pipeline.mapear_competencias` primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    caminho_scores = (
        config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias.parquet"
    )
    df = pd.read_parquet(caminho_scores)
    referencia = carregar_referencia()

    resultado = enriquecer(df, referencia)

    n_pesquisados = resultado["teve_cargo_eletivo"].notna().sum()
    print(f"{n_pesquisados} candidatos com experiência política pesquisada e aplicada")
    print(
        resultado[resultado["teve_cargo_eletivo"].notna() & resultado["experiencia_pesquisada_em"].notna()][
            ["nome_urna", "teve_cargo_eletivo", "cargos_anteriores_resumo"]
        ].head(400).to_string()
    )

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
