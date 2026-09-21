"""Marca, para cada candidato, quais camadas de avaliação foram PESQUISADAS de fato.

Existe para tornar as notas comparáveis com justiça: só uma parte dos ~20 mil candidatos
teve pesquisa individual. Sem essa marca, quem foi pesquisado (e recebeu boost de
experiência política, desconto de idoneidade etc.) seria comparado com quem tem apenas
o proxy automático de ocupação + escolaridade, e as duas situações pareceriam iguais.

Colunas geradas:
  camadas_pesquisadas  int 0-5  quantas das 5 camadas individuais têm pesquisa
  cobertura_pesquisa   texto    quais (e o nível de evidência do posicionamento)

As 5 camadas: idoneidade pessoal, círculo político, posicionamento ideológico,
experiência política e competência por experiência profissional. A nota de competência
(`nota_competencia`) só é comparável entre candidatos com a camada de experiência
política pesquisada; sem ela é um proxy que tende a SUBESTIMAR quem tem carreira eletiva.
"""
import json
import sys

import pandas as pd

from . import config

INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")
EXPERIENCIA_PROFISSIONAL_PATH = config.RAW_DIR.parent / "reference" / "experiencia_profissional.json"
CARGOS_PESQUISADOS = {"PRESIDENTE", "GOVERNADOR"}


def _marcar_transferivel(df: pd.DataFrame) -> pd.Series:
    """True para quem foi pesquisado em experiencia_profissional.json, com ou sem alteração de nota."""
    ref = json.loads(EXPERIENCIA_PROFISSIONAL_PATH.read_text(encoding="utf-8"))
    com_entrada = set(ref["candidatos"].keys())
    sem_alteracao = set(ref.get("pesquisados_sem_alteracao", {}).keys())
    return df["sq_candidato"].isin(com_entrada) | (
        df["cargo"].isin(CARGOS_PESQUISADOS) & df["nome_urna"].isin(sem_alteracao)
    )


def aplicar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    tem = {
        "idoneidade": df["nota_idoneidade"].notna(),
        "círculo político": df["nota_circulo_politico"].notna(),
        "posicionamento": df["eixo_economico"].notna(),
        "experiência política": df["experiencia_pesquisada_em"].notna(),
        "competência profissional": _marcar_transferivel(df),
    }
    df["camadas_pesquisadas"] = sum(m.astype(int) for m in tem.values())

    def texto(i: int) -> str:
        feitas = []
        for nome, mask in tem.items():
            if not mask.iat[i]:
                continue
            if nome == "posicionamento":
                ne, npess = df["nivel_eixo_economico"].iat[i], df["nivel_eixo_pessoal"].iat[i]
                feitas.append(f"posicionamento (econômico {ne}, pessoal {npess})")
            else:
                feitas.append(nome)
        return "; ".join(feitas) if feitas else "nenhuma (só proxy de ocupação + escolaridade)"

    df["cobertura_pesquisa"] = [texto(i) for i in range(len(df))]
    return df


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.calcular_competencia_geral` primeiro.")
    df = pd.read_parquet(INPUT_PATH)
    resultado = aplicar(df)

    resumo = (
        resultado.assign(completo=resultado["camadas_pesquisadas"] == 5, algum=resultado["camadas_pesquisadas"] > 0)
        .groupby("cargo")
        .agg(candidatos=("sq_candidato", "size"), com_alguma_camada=("algum", "sum"), com_as_5_camadas=("completo", "sum"))
    )
    print(resumo.to_string())

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
