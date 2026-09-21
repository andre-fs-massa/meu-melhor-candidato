"""Aplica o posicionamento ideológico individual
(data/reference/posicionamento_ideologico.json) ao dataset de candidatos.

Diferente da classificação de PARTIDO (usada como chute inicial em análises
anteriores), aqui os dois eixos do diagrama de Nolan (eixo_economico,
eixo_pessoal, ambos 0-10) são pesquisados por CANDIDATO -- plano de governo
registrado no TSE, entrevistas, sabatinas e pauta de campanha -- para captar
divergências reais entre o candidato e o rótulo genérico do partido (ex.:
liberal na economia mas conservador em costumes). Ver o campo "_leiame" do
JSON para a metodologia completa. Só é preenchido para os candidatos
efetivamente pesquisados; os demais ficam com NA, não com uma nota presumida.
"""
import json
import sys

import pandas as pd

from . import config

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "posicionamento_ideologico.json"
INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")
IDEOLOGIA_PARTIDARIA_PATH = config.RAW_DIR.parent / "reference" / "ideologia_partidaria.json"

# Nível de evidência de cada eixo (ver "_leiame" do JSON):
#   a = posição/proposta explícita do próprio candidato; b = proposta institucional ou programa do partido que
#   correlaciona com o eixo; c = baseline do PARTIDO (fallback sem sinal individual); d = centro (não usar como padrão).
NIVEIS_VALIDOS = {"a", "b", "c", "d"}
# nome do partido no arquivo do TSE -> chave em ideologia_partidaria.json
CHAVE_PARTIDO = {"PC DO B": "PCDOB", "PODE": "PODE", "PODEMOS": "PODE", "UNIÃO": "UNIÃO", "UNIAO": "UNIÃO"}


def validar_niveis(registro: dict, partido: str, ideologia: dict) -> list:
    """Nível 'c' tem que ser exatamente o baseline do partido; nível ausente/inválido é erro."""
    erros = []
    chave = CHAVE_PARTIDO.get(partido, partido)
    for eixo in ("economico", "pessoal"):
        nivel = registro.get(f"nivel_eixo_{eixo}")
        if nivel not in NIVEIS_VALIDOS:
            erros.append(f"nivel_eixo_{eixo} ausente ou inválido ({nivel!r})")
        elif nivel == "c":
            base = ideologia.get(chave, {}).get(f"eixo_{eixo}")
            if base is None:
                erros.append(f"nível c no eixo {eixo}, mas o partido {partido} não está em ideologia_partidaria.json")
            elif abs(base - registro[f"eixo_{eixo}"]) > 0.05:
                erros.append(f"nível c no eixo {eixo} deveria ser o baseline do {partido} ({base}), mas está {registro[f'eixo_{eixo}']}")
    return erros


def aplicar(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    for col in (
        "eixo_economico",
        "eixo_pessoal",
        "nivel_eixo_economico",
        "nivel_eixo_pessoal",
        "motivo_posicionamento_ideologico",
        "fontes_posicionamento_ideologico",
        "posicionamento_ideologico_pesquisado_em",
    ):
        if col not in df.columns:
            df[col] = pd.NA

    df = df.set_index("sq_candidato", drop=False)
    ideologia = {}
    if IDEOLOGIA_PARTIDARIA_PATH.exists():
        ideologia = json.loads(IDEOLOGIA_PARTIDARIA_PATH.read_text(encoding="utf-8"))["partidos"]

    for sq, registro in referencia["candidatos"].items():
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({registro['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)
            continue
        for erro in validar_niveis(registro, df.at[sq, "partido"], ideologia):
            print(f"Aviso: {registro['nome_urna']} ({sq}): {erro}", file=sys.stderr)
        df.at[sq, "eixo_economico"] = registro["eixo_economico"]
        df.at[sq, "eixo_pessoal"] = registro["eixo_pessoal"]
        df.at[sq, "nivel_eixo_economico"] = registro.get("nivel_eixo_economico", pd.NA)
        df.at[sq, "nivel_eixo_pessoal"] = registro.get("nivel_eixo_pessoal", pd.NA)
        df.at[sq, "motivo_posicionamento_ideologico"] = registro["motivo"]
        df.at[sq, "fontes_posicionamento_ideologico"] = "; ".join(registro.get("fontes", []))
        df.at[sq, "posicionamento_ideologico_pesquisado_em"] = registro["pesquisado_em"]

    return df.reset_index(drop=True)


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.calcular_idoneidade_geral` primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    df = pd.read_parquet(INPUT_PATH)
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    resultado = aplicar(df, referencia)

    n_pesquisados = resultado["eixo_economico"].notna().sum()
    print(f"{n_pesquisados} candidatos com posicionamento ideológico individual aplicado")
    print(
        resultado[resultado["eixo_economico"].notna()]
        .sort_values(["cargo", "eixo_economico"])[["nome_urna", "cargo", "eixo_economico", "eixo_pessoal"]]
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
