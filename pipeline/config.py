"""Configuração central do pipeline de ingestão de candidatos do TSE."""
from pathlib import Path

ANO_ELEICAO = 2026

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

DATASET_ZIP_URL = (
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/"
    f"consulta_cand_{ANO_ELEICAO}.zip"
)
DATASET_PAGE_URL = f"https://dadosabertos.tse.jus.br/dataset/candidatos-{ANO_ELEICAO}"

ZIP_PATH = RAW_DIR / f"consulta_cand_{ANO_ELEICAO}.zip"
EXTRACT_DIR = RAW_DIR / f"consulta_cand_{ANO_ELEICAO}"
OUTPUT_PARQUET = PROCESSED_DIR / f"candidatos_{ANO_ELEICAO}.parquet"
OUTPUT_CSV = PROCESSED_DIR / f"candidatos_{ANO_ELEICAO}.csv"

# Cargos de interesse do projeto (Presidente, Governadores, Senadores,
# Deputados Federais e Deputados Estaduais/Distritais em todos os estados).
CARGOS_DE_INTERESSE = {
    "PRESIDENTE",
    "GOVERNADOR",
    "SENADOR",
    "DEPUTADO FEDERAL",
    "DEPUTADO ESTADUAL",
    "DEPUTADO DISTRITAL",
}

# Encoding e delimitador tradicionalmente usados pelo TSE nos arquivos
# consulta_cand_*.csv (ciclos 2020/2022/2024 seguiram este padrão).
CSV_ENCODING = "latin-1"
CSV_DELIMITER = ";"
