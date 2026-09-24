"""Cruza os candidatos de 2026 com os motivos de indeferimento/cassação do TSE em 2022, por CPF + nome.

Entradas (baixadas manualmente do portal de dados abertos do TSE, em data/raw/):
  - consulta_cand_2022/  (SQ_CANDIDATO -> CPF)
  - motivo_cassacao_2022/ (SQ_CANDIDATO -> fundamento legal do julgamento; inclui 2 processos da suplementar de RR/2026)
Saída: data/processed/sinais_tse_motivos_2022.csv, uma linha por candidato de 2026 e motivo.

Isto é SINAL DE TRIAGEM, não nota: o arquivo lista os fundamentos citados no julgamento de 2022, não a
decisão final (pode ter sido revertida depois). Nada aqui altera idoneidade.json automaticamente.

Uso: python -m pipeline.cruzar_motivos_tse
"""
import difflib
import glob
import re
import unicodedata

import pandas as pd

from pipeline import config
from pipeline.recomendar import INPUT_PATH

RAW = config.RAW_DIR
SAIDA = INPUT_PATH.parent / "sinais_tse_motivos_2022.csv"

# Motivos que dizem respeito à conduta ou elegibilidade DA PESSOA.
PESSOAL = {
    "Ficha limpa (LC 64/90)", "Abuso de poder político", "Abuso de poder (LC 64/90)", "Abuso de poder econômico",
    "Conduta vedada (Lei 9.504/97).", "Compra de voto (Lei 9.504/97).", "Captação ilícita de sufrágio",
    "Gasto ilícito de recursos (Lei 9.504/97).", "Uso indevido de meios de comunicação",
    "Ausência de desincompatibilização (LC 64/90)", "Outras fraudes",
}
# Motivos formais ou do partido/chapa (documentação, DRAP, federação): não são achado individual.
FORMAL = {
    "Ausência de requisito de registro", "Indeferimento de partido, federação ou coligação.",
    "Partido ou federação Invalidado.", "Fraude à cota de gênero no DRAP",
}
SIMILARIDADE_MIN = 0.8  # nome completo 2026 x 2022; CPFs do TSE às vezes vêm repetidos/errados


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z ]", "", s).strip()


def _ler(pasta: str, prefixo: str, excluir_agregados: bool = False) -> pd.DataFrame:
    arquivos = glob.glob(str(RAW / pasta / f"{prefixo}_*.csv"))
    if excluir_agregados:
        arquivos = [f for f in arquivos if not f.endswith(("_BR.csv", "_BRASIL.csv"))]
        arquivos.append(str(RAW / pasta / f"{prefixo}_BRASIL.csv"))
    return pd.concat([pd.read_csv(f, sep=";", encoding="latin-1", dtype=str) for f in arquivos])


def cruzar() -> pd.DataFrame:
    d22 = _ler("consulta_cand_2022", "consulta_cand_2022", True).drop_duplicates("SQ_CANDIDATO")
    d22["cpf"] = d22.NR_CPF_CANDIDATO.str.replace(r"\D", "", regex=True)
    nomes_por_cpf = d22.groupby("cpf").NM_CANDIDATO.nunique()
    cpfs_suspeitos = set(nomes_por_cpf[nomes_por_cpf > 1].index)  # mesmo CPF em vários nomes = dado ruim

    mot = _ler("motivo_cassacao_2022", "motivo_cassacao_2022").drop_duplicates(["SQ_CANDIDATO", "NR_PROCESSO", "DS_MOTIVO"])
    mot["DS_MOTIVO"] = mot.DS_MOTIVO.str.strip()
    # O arquivo mistura a eleição geral de 2022 com a suplementar de governador de RR em 2026 (mesmo rótulo de ano);
    # o número do processo e DS_ELEICAO mostram qual é qual.
    mot["eleicao_do_motivo"] = mot.DS_ELEICAO.map(lambda x: "suplementar_2026" if "Suplementar" in x else "geral_2022")
    mot = mot[["SQ_CANDIDATO", "NR_PROCESSO", "DS_MOTIVO", "eleicao_do_motivo"]]  # UF, ano etc. vêm do consulta_cand
    j = mot.merge(d22, on="SQ_CANDIDATO", how="left")

    p = pd.read_parquet(INPUT_PATH)
    p["cpf"] = p.cpf.astype(str).str.replace(r"\D", "", regex=True)
    m = p.merge(j[["cpf", "NR_PROCESSO", "DS_MOTIVO", "eleicao_do_motivo", "NM_CANDIDATO", "DS_CARGO", "SG_UF", "SG_PARTIDO", "DS_SIT_TOT_TURNO"]],
                on="cpf", suffixes=("", "_2022"))
    m["similaridade_nome"] = [difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()
                              for a, b in zip(m.nome_completo, m.NM_CANDIDATO)]
    m = m[(m.similaridade_nome >= SIMILARIDADE_MIN) & (~m.cpf.isin(cpfs_suspeitos))].copy()
    m["natureza"] = m.DS_MOTIVO.map(lambda x: "pessoal" if x in PESSOAL else "formal_ou_partidario" if x in FORMAL else "desconhecida")
    cols = ["sq_candidato", "cargo", "uf", "nome_urna", "partido", "DS_CARGO", "SG_UF", "SG_PARTIDO", "DS_SIT_TOT_TURNO",
            "DS_MOTIVO", "eleicao_do_motivo", "natureza", "NR_PROCESSO", "similaridade_nome"]
    return m[cols].rename(columns={"DS_CARGO": "cargo_2022", "SG_UF": "uf_2022", "SG_PARTIDO": "partido_2022",
                                   "DS_SIT_TOT_TURNO": "resultado_2022", "DS_MOTIVO": "motivo",
                                   "NR_PROCESSO": "processo"}).sort_values(["cargo", "uf", "nome_urna"])


def main() -> None:
    df = cruzar()
    df.to_csv(SAIDA, index=False, encoding="utf-8-sig")
    print(f"{df.sq_candidato.nunique()} candidatos de 2026 com motivo em 2022 ({len(df)} linhas). Salvo em {SAIDA}")
    print(df.groupby(["cargo", "natureza"]).sq_candidato.nunique().unstack(fill_value=0).to_string())
    desconhecidas = sorted(set(df[df.natureza == "desconhecida"].motivo))
    if desconhecidas:
        print("Aviso: motivos sem classificação:", desconhecidas)


if __name__ == "__main__":
    main()
