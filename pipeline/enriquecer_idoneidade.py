"""Aplica a nota de idoneidade (data/reference/idoneidade.json) ao dataset
de candidatos já enriquecido com competências e experiência política.

A nota de idoneidade é pesquisada manualmente (processos judiciais, Ficha
Limpa, contas rejeitadas, sanções éticas) -- não vem do TSE e não é um
índice oficial. Ver o campo "_leiame" do JSON para a metodologia completa.
Só é preenchida para os candidatos efetivamente pesquisados; os demais
ficam com NA, não com uma nota presumida.
"""
import json
import sys

import pandas as pd

from . import config
from .pesos import calcular_nota, formatar_achados

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "idoneidade.json"
INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")


def aplicar(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    for col in (
        "nota_idoneidade",
        "motivo_idoneidade",
        "achados_idoneidade",
        "idoneidade_pesquisado_em",
    ):
        if col not in df.columns:
            df[col] = pd.NA

    df = df.set_index("sq_candidato", drop=False)

    for sq, registro in referencia["candidatos"].items():
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({registro['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)
            continue
        if "achados" not in registro:
            print(f"Aviso: {registro['nome_urna']} ({sq}) sem lista 'achados' -- nota não pode ser conferida", file=sys.stderr)
        else:
            calculada = calcular_nota(registro["achados"])
            if calculada != registro["nota"]:
                print(
                    f"Aviso: {registro['nome_urna']} ({sq}) tem nota {registro['nota']} mas os "
                    f"achados somam {calculada}",
                    file=sys.stderr,
                )
            df.at[sq, "achados_idoneidade"] = formatar_achados(registro["achados"]) or pd.NA
        df.at[sq, "nota_idoneidade"] = registro["nota"]
        df.at[sq, "motivo_idoneidade"] = registro["motivo"]
        df.at[sq, "idoneidade_pesquisado_em"] = registro["pesquisado_em"]

    return df.reset_index(drop=True)


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.enriquecer_experiencia` primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    df = pd.read_parquet(INPUT_PATH)
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    resultado = aplicar(df, referencia)

    n_pesquisados = resultado["nota_idoneidade"].notna().sum()
    print(f"{n_pesquisados} candidatos com nota de idoneidade aplicada")
    print(
        resultado[resultado["nota_idoneidade"].notna()]
        .sort_values("nota_idoneidade")[["nome_urna", "nota_idoneidade"]]
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
