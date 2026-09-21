"""Extrai o zip de candidatos do TSE, filtra os cargos de interesse e
normaliza em uma tabela única (parquet + csv) para uso pelo resto do
projeto.

O layout de colunas abaixo segue o padrão usado pelo TSE nos arquivos
consulta_cand_* desde o ciclo 2020. Se o TSE tiver mudado alguma coluna
em 2026, rode `python -m pipeline.parse_candidatos --inspect` primeiro
para conferir os nomes reais antes de confiar no resultado normalizado.
"""
import argparse
import sys
import zipfile

import pandas as pd

from . import config

# Nome da coluna no CSV do TSE -> nome amigável na tabela normalizada.
COLUNAS_RENOMEADAS = {
    "ANO_ELEICAO": "ano_eleicao",
    "SG_UF": "uf",
    "DS_CARGO": "cargo",
    "SQ_CANDIDATO": "sq_candidato",
    "NR_CANDIDATO": "numero",
    "NM_CANDIDATO": "nome_completo",
    "NM_URNA_CANDIDATO": "nome_urna",
    "NM_SOCIAL_CANDIDATO": "nome_social",
    "NR_CPF_CANDIDATO": "cpf",
    "SG_PARTIDO": "partido",
    "NR_PARTIDO": "numero_partido",
    "NM_PARTIDO": "nome_partido",
    "SG_FEDERACAO": "federacao",
    "NM_COLIGACAO": "coligacao",
    "DS_GENERO": "genero",
    "DS_GRAU_INSTRUCAO": "escolaridade",
    "DS_COR_RACA": "raca_cor",
    "DS_OCUPACAO": "ocupacao",
    "DS_ESTADO_CIVIL": "estado_civil",
    "DT_NASCIMENTO": "data_nascimento",
    "DS_SIT_TOT_TURNO": "situacao_totalizacao",
}

# ATENÇÃO: DS_SITUACAO_CANDIDATURA/CD_SITUACAO_CANDIDATURA (situação de
# deferimento da candidatura) foi descontinuado pelo TSE a partir do ciclo
# 2024 -- o leiame.pdf do próprio zip diz "Aplicável somente para os
# registros das eleições até 2022". No arquivo 2026 ele vem sempre #NE/-3,
# então NÃO dá pra usar esse campo para saber se a candidatura foi
# deferida/indeferida.
# ST_REELEICAO e ST_DECLARAR_BENS também não existem mais no layout 2026.
#
# Decisão de produto (2026-09-20): já que faltam ~2 semanas para o 1º turno
# e o registro fechou em 15/08, tratamos a mera presença de um candidato
# neste arquivo (consulta_cand_2026) como proxy de "candidatura ativa" --
# indeferimentos/cassações já deveriam ter removido o registro do cadastro
# corrente. Não confirmamos status judicial individual (isso exigiria
# DivulgaCandContas por candidato, que fica atrás do mesmo bloqueio de bot
# do CDN e não escala para ~20 mil candidatos).


def extrair_zip() -> list:
    if not config.ZIP_PATH.exists():
        sys.exit(
            f"Arquivo não encontrado: {config.ZIP_PATH}\n"
            "Rode `python -m pipeline.download` primeiro (ou baixe manualmente)."
        )

    config.EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(config.ZIP_PATH) as zf:
        nomes_csv = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        zf.extractall(config.EXTRACT_DIR, members=nomes_csv)

    arquivos = sorted(config.EXTRACT_DIR.glob("consulta_cand_*.csv"))
    if not arquivos:
        sys.exit(f"Nenhum consulta_cand_*.csv encontrado dentro de {config.ZIP_PATH}")
    return arquivos


def carregar_bruto(arquivos) -> pd.DataFrame:
    partes = []
    for caminho in arquivos:
        df = pd.read_csv(
            caminho,
            sep=config.CSV_DELIMITER,
            encoding=config.CSV_ENCODING,
            dtype=str,
            low_memory=False,
        )
        partes.append(df)
    return pd.concat(partes, ignore_index=True)


def inspecionar(arquivos) -> None:
    df = pd.read_csv(
        arquivos[0],
        sep=config.CSV_DELIMITER,
        encoding=config.CSV_ENCODING,
        dtype=str,
        nrows=5,
    )
    print(f"Arquivo de exemplo: {arquivos[0].name}")
    print(f"{len(df.columns)} colunas:")
    for col in df.columns:
        faltando = "" if col in COLUNAS_RENOMEADAS else "  <-- sem mapeamento"
        print(f"  {col}{faltando}")


def normalizar(df_bruto: pd.DataFrame) -> pd.DataFrame:
    if "DS_CARGO" not in df_bruto.columns:
        sys.exit(
            "Coluna DS_CARGO não encontrada. Rode com --inspect para ver as "
            "colunas reais do arquivo e ajuste COLUNAS_RENOMEADAS."
        )

    cargo_normalizado = df_bruto["DS_CARGO"].str.strip().str.upper()
    filtrado = df_bruto[cargo_normalizado.isin(config.CARGOS_DE_INTERESSE)].copy()

    colunas_presentes = [c for c in COLUNAS_RENOMEADAS if c in filtrado.columns]
    ausentes = [c for c in COLUNAS_RENOMEADAS if c not in filtrado.columns]
    if ausentes:
        print(f"Aviso: colunas ausentes no arquivo de origem: {ausentes}", file=sys.stderr)

    resultado = filtrado[colunas_presentes].rename(columns=COLUNAS_RENOMEADAS)

    if "sq_candidato" in resultado.columns:
        resultado = resultado.drop_duplicates(subset="sq_candidato")

    return resultado.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Só mostra as colunas do CSV de origem, sem processar tudo.",
    )
    args = parser.parse_args()

    arquivos = extrair_zip()
    print(f"{len(arquivos)} arquivo(s) CSV extraído(s) de {config.ZIP_PATH.name}")

    if args.inspect:
        inspecionar(arquivos)
        return

    bruto = carregar_bruto(arquivos)
    print(f"{len(bruto):,} linhas brutas carregadas (todos os cargos, todas as UFs)")

    normalizado = normalizar(bruto)
    print(
        f"{len(normalizado):,} candidatos após filtrar para "
        f"{sorted(config.CARGOS_DE_INTERESSE)}"
    )
    if "cargo" in normalizado.columns:
        print(normalizado["cargo"].value_counts().to_string())

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    normalizado.to_parquet(config.OUTPUT_PARQUET, index=False)
    normalizado.to_csv(config.OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nSalvo em:\n  {config.OUTPUT_PARQUET}\n  {config.OUTPUT_CSV}")


if __name__ == "__main__":
    main()
