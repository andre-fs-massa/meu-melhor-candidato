"""Ajusta as pontuações de competência com base em experiência PROFISSIONAL
real (biografia: carreira, formação, histórico militar/empresarial/sindical/
acadêmico), pesquisada manualmente e registrada em
data/reference/experiencia_profissional.json.

Diferente de pipeline/enriquecer_experiencia.py (que só considera CARGOS
ELETIVOS anteriores), aqui o sinal é qualquer experiência profissional
relevante -- inclusive não-política -- avaliada competência a competência,
com justificativa específica de por que aquela experiência transfere (ou
não). Ver o campo "_leiame" do JSON para a metodologia completa. Só é
preenchido para os candidatos efetivamente pesquisados; os demais ficam
inalterados.

Regra: a pontuação final de cada competência é o MAIOR valor entre (a) o
que já estava no parquet (proxy de ocupação + boosts anteriores) e (b) a
nota pesquisada de competência transferível. Ou seja, experiência
profissional real só pode subir a nota, nunca baixar um score que já
existia por outro motivo.
"""
import json
import sys

import pandas as pd

from . import config

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "experiencia_profissional.json"
INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")


def aplicar(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    for col in ("motivo_competencia_transferivel", "fontes_competencia_transferivel"):
        if col not in df.columns:
            df[col] = pd.NA

    df = df.set_index("sq_candidato", drop=False)

    for sq, registro in referencia["candidatos"].items():
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({registro['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)
            continue

        motivos_aplicados = []
        for chave_competencia, dado in registro["competencias"].items():
            col = f"score_{chave_competencia}"
            if col not in df.columns:
                print(f"Aviso: coluna {col} não existe (candidato {registro['nome_urna']})", file=sys.stderr)
                continue
            valor_atual = df.at[sq, col]
            valor_atual = 0 if pd.isna(valor_atual) else valor_atual
            nota_pesquisada = dado["nota"]
            if nota_pesquisada > valor_atual:
                df.at[sq, col] = nota_pesquisada
                motivos_aplicados.append(f"{chave_competencia}: {valor_atual}->{nota_pesquisada} ({dado['motivo']})")
            else:
                motivos_aplicados.append(f"{chave_competencia}: sem mudança ({valor_atual} já >= {nota_pesquisada})")

        df.at[sq, "motivo_competencia_transferivel"] = " | ".join(motivos_aplicados)
        df.at[sq, "fontes_competencia_transferivel"] = "; ".join(registro.get("fontes", []))

    return df.reset_index(drop=True)


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode o pipeline de competências/experiência/idoneidade primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    df = pd.read_parquet(INPUT_PATH)
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    resultado = aplicar(df, referencia)

    n_pesquisados = resultado["motivo_competencia_transferivel"].notna().sum()
    print(f"{n_pesquisados} candidatos com competência transferível aplicada")
    print(
        resultado[resultado["motivo_competencia_transferivel"].notna()]
        .sort_values(["cargo", "nome_urna"])[["nome_urna", "cargo"]]
        .to_string()
    )
    print(f"\nPesquisados sem alteração justificada (ver _leiame): {list(referencia.get('pesquisados_sem_alteracao', {}).keys())}")

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
