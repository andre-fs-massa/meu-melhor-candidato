"""Cruza os candidatos de 2026 com a lista do TCU de responsáveis com contas irregulares de possível implicação eleitoral.

Entrada (baixada manualmente de https://certidoes.apps.tcu.gov.br/lista-implicacao-eleitoral):
  data/raw/lista-responsaveis-fins-eleitorais.csv  (separador '|', CPF completo, trânsito em julgado e fim do prazo de 8 anos)
Saída: data/processed/sinais_tcu_eleitoral.csv, uma linha por candidato de 2026 e processo do TCU.

Isto é SINAL DE TRIAGEM, não nota. A lista é o que o TCU envia à Justiça Eleitoral: a inelegibilidade só existe se a
Justiça Eleitoral reconhecer irregularidade insanável com ato doloso de improbidade. Nada aqui altera idoneidade.json.

Uso: python -m pipeline.cruzar_tcu_eleitoral
"""
import difflib

import pandas as pd

from pipeline import config
from pipeline.cruzar_motivos_tse import SIMILARIDADE_MIN, _norm
from pipeline.recomendar import INPUT_PATH

ENTRADA = config.RAW_DIR / "lista-responsaveis-fins-eleitorais.csv"
SAIDA = INPUT_PATH.parent / "sinais_tcu_eleitoral.csv"
DIA_DA_ELEICAO = pd.Timestamp("2026-10-04")


def cruzar() -> pd.DataFrame:
    t = pd.read_csv(ENTRADA, sep="|", encoding="latin-1", skiprows=1, dtype=str)  # 1ª linha é "sep=|"
    t.columns = ["nome_tcu", "cpf", "uf_tcu", "municipio_tcu", "processo_tcu", "link_processo", "link_acordao",
                 "transito_em_julgado", "prazo_final"]
    t["cpf"] = t.cpf.str.replace(r"\D", "", regex=True)
    for c in ("transito_em_julgado", "prazo_final"):
        t[c] = pd.to_datetime(t[c], format="%d/%m/%Y", errors="coerce")

    p = pd.read_parquet(INPUT_PATH)
    p["cpf"] = p.cpf.astype(str).str.replace(r"\D", "", regex=True)
    m = p.merge(t, on="cpf")
    m["similaridade_nome"] = [difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()
                              for a, b in zip(m.nome_completo, m.nome_tcu)]
    m = m[m.similaridade_nome >= SIMILARIDADE_MIN].copy()
    m["prazo_vigente_na_eleicao"] = m.prazo_final >= DIA_DA_ELEICAO
    cols = ["sq_candidato", "cargo", "uf", "nome_urna", "partido", "municipio_tcu", "processo_tcu",
            "transito_em_julgado", "prazo_final", "prazo_vigente_na_eleicao", "link_acordao", "link_processo",
            "similaridade_nome"]
    return m[cols].sort_values(["cargo", "uf", "nome_urna", "transito_em_julgado"])


def main() -> None:
    df = cruzar()
    df.to_csv(SAIDA, index=False, encoding="utf-8-sig")
    print(f"{df.sq_candidato.nunique()} candidatos de 2026 na lista do TCU ({len(df)} processos). Salvo em {SAIDA}")
    print(df.groupby("cargo").sq_candidato.nunique().to_string())


if __name__ == "__main__":
    main()
