"""Aplica a nota de idoneidade do círculo político
(data/reference/circulo_politico.json) ao dataset de candidatos.

Distinta da nota de idoneidade pessoal (enriquecer_idoneidade.py): aqui
avaliamos vice/cabeça de chapa, coligação e lideranças partidárias
("caciques"), não o candidato em si. Ver o campo "_leiame" de
circulo_politico.json para a metodologia, e liderancas_partidarias.json
para a referência reutilizável de lideranças de partido.
"""
import json
import sys

import pandas as pd

from . import config
from .pesos import PESOS_CACIQUE, soma_descontos

REFERENCE_PATH = config.RAW_DIR.parent / "reference" / "circulo_politico.json"
INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
OUTPUT_PARQUET = INPUT_PATH
OUTPUT_CSV = INPUT_PATH.with_suffix(".csv")

# Tipos de ligação entre um apoiador e o candidato (ver "_leiame" do JSON).
ROTULO_LIGACAO = {
    "vice_de_chapa": "vice na chapa",
    "suplente_de_chapa": "suplente na chapa",  # 2026-09-23: Senador não tem vice, tem 1º/2º suplente
    "presidente_do_partido_do_candidato": "presidente do partido do candidato",
    "presidente_de_partido_aliado": "presidente de partido aliado (coligação)",
    "padrinho_politico": "padrinho político (escolheu/controla/financia a candidatura)",
    "apoio_externo": "apoio externo (endossa, sem controle da chapa)",
}
# Só estes tipos entram no teto de desconto por "caciques da coligação".
TIPOS_CACIQUE = {"presidente_do_partido_do_candidato", "presidente_de_partido_aliado"}
TETO_CACIQUES = 4


def calcular_nota(registro: dict):
    """Nota = 10 - descontos, com os caciques da coligação somados e limitados a
    TETO_CACIQUES. Devolve None quando o registro não tem decomposição completa
    (algum desconto contado sem valor), caso em que a nota gravada é aceita como está.
    """
    if "apoiadores" not in registro:
        return None
    caciques = outros = 0
    for a in registro["apoiadores"]:
        if not a.get("contado", True):
            continue
        if a["desconto"] is None:
            return None
        if a["tipo_ligacao"] in TIPOS_CACIQUE:
            caciques += a["desconto"]
        else:
            outros += a["desconto"]
    outros += sum(d["desconto"] for d in registro.get("descontos_adicionais", []))
    return max(0, 10 - min(caciques, TETO_CACIQUES) - outros)


def formatar_apoiadores(registro: dict) -> str:
    """Texto legível: quem é, qual a ligação com o candidato, a pendência e o desconto."""
    partes = []
    for a in registro.get("apoiadores", []):
        nome = a["nome"] + (f" ({a['partido']})" if a.get("partido") else "")
        ligacao = ROTULO_LIGACAO.get(a["tipo_ligacao"], a["tipo_ligacao"])
        if a.get("ligacao_detalhe"):
            ligacao += f": {a['ligacao_detalhe']}"
        if not a.get("contado", True):
            desconto = "não contado"
        elif a["desconto"] is None:
            desconto = "desconto não decomposto"
        else:
            desconto = f"-{a['desconto']}" if a["desconto"] else "sem desconto"
        partes.append(f"{nome} — {ligacao} — {a['pendencia']} [{desconto}]")
    for d in registro.get("descontos_adicionais", []):
        partes.append(f"{d['motivo']} [-{d['desconto']}]")
    caciques = sum(
        a["desconto"] or 0
        for a in registro.get("apoiadores", [])
        if a.get("contado", True) and a["tipo_ligacao"] in TIPOS_CACIQUE
    )
    if caciques > TETO_CACIQUES:
        partes.append(f"Teto: os caciques somam -{caciques}, limitados a -{TETO_CACIQUES} no cálculo da nota")
    return " | ".join(partes)


IDONEIDADE_PATH = config.RAW_DIR.parent / "reference" / "idoneidade.json"


def validar_apoiadores(registro: dict, idoneidade: dict) -> list:
    """Confere cada desconto contra a regra que o define; devolve a lista de divergências."""
    erros = []
    for a in registro.get("apoiadores", []):
        rotulo = f"{a['nome']} ({a['tipo_ligacao']})"
        if a["tipo_ligacao"] in TIPOS_CACIQUE and a["desconto"] is not None:
            esperado = PESOS_CACIQUE.get(a["tipo_pendencia"].split("+")[0])
            if esperado is None:
                erros.append(f"{rotulo}: tipo_pendencia '{a['tipo_pendencia']}' fora de PESOS_CACIQUE")
            elif esperado != a["desconto"]:
                erros.append(f"{rotulo}: desconto {a['desconto']} mas a tabela de caciques dá {esperado}")
        if "achados" in a and a["desconto"] is not None and soma_descontos(a["achados"]) != a["desconto"]:
            erros.append(f"{rotulo}: desconto {a['desconto']} mas os achados somam {soma_descontos(a['achados'])}")
        ref = a.get("idoneidade_ref")
        if ref and ref in idoneidade and a["desconto"] is not None and 10 - idoneidade[ref]["nota"] != a["desconto"]:
            erros.append(
                f"{rotulo}: desconto {a['desconto']} mas 10 - idoneidade de {idoneidade[ref]['nome_urna']} "
                f"({idoneidade[ref]['nota']}) = {10 - idoneidade[ref]['nota']}"
            )
    return erros


def aplicar(df: pd.DataFrame, referencia: dict) -> pd.DataFrame:
    df = df.copy()
    for col in (
        "nota_circulo_politico",
        "motivo_circulo_politico",
        "apoiadores_circulo_politico",
        "circulo_politico_pesquisado_em",
    ):
        if col not in df.columns:
            df[col] = pd.NA

    df = df.set_index("sq_candidato", drop=False)
    idoneidade = {}
    if IDONEIDADE_PATH.exists():
        idoneidade = json.loads(IDONEIDADE_PATH.read_text(encoding="utf-8"))["candidatos"]

    for sq, registro in referencia["candidatos"].items():
        if sq not in df.index:
            print(f"Aviso: sq_candidato {sq} ({registro['nome_urna']}) não encontrado no dataset atual", file=sys.stderr)
            continue
        for erro in validar_apoiadores(registro, idoneidade):
            print(f"Aviso: {registro['nome_urna']} ({sq}): {erro}", file=sys.stderr)
        calculada = calcular_nota(registro)
        if calculada is not None and calculada != registro["nota"]:
            print(
                f"Aviso: {registro['nome_urna']} ({sq}) tem nota {registro['nota']} mas os "
                f"apoiadores somam {calculada}",
                file=sys.stderr,
            )
        df.at[sq, "nota_circulo_politico"] = registro["nota"]
        df.at[sq, "motivo_circulo_politico"] = registro["motivo"]
        df.at[sq, "apoiadores_circulo_politico"] = formatar_apoiadores(registro) or pd.NA
        df.at[sq, "circulo_politico_pesquisado_em"] = registro["pesquisado_em"]

    return df.reset_index(drop=True)


def main() -> None:
    if not INPUT_PATH.exists():
        sys.exit("Rode `python -m pipeline.enriquecer_idoneidade` primeiro.")
    if not REFERENCE_PATH.exists():
        sys.exit(f"{REFERENCE_PATH} não existe.")

    df = pd.read_parquet(INPUT_PATH)
    referencia = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))

    resultado = aplicar(df, referencia)

    n_pesquisados = resultado["nota_circulo_politico"].notna().sum()
    print(f"{n_pesquisados} candidatos com nota de círculo político aplicada")
    print(
        resultado[resultado["nota_circulo_politico"].notna()]
        .sort_values(["cargo", "nota_circulo_politico"])[["nome_urna", "cargo", "nota_circulo_politico"]]
        .to_string()
    )

    resultado.to_parquet(OUTPUT_PARQUET, index=False)
    resultado.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {OUTPUT_PARQUET}\n  {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
