"""Confere cada candidato de 2026 em bases oficiais e grava o resultado, base a base.

Bases (arquivos baixados em data/raw/, ver `BASES`): TCU (contas irregulares com implicação eleitoral), TSE 2022
(motivos de indeferimento/cassação), CEIS, CNEP, CEAF (Portal da Transparência) e autos de infração do Ibama.

Saída: data/processed/verificacao_bases_oficiais.csv, uma linha por candidato x base:
  resultado = "consta"       -> há registro (CPF completo + nome parecido)
              "a_confirmar"  -> só casou por nome + 6 dígitos do meio do CPF (CEAF traz CPF mascarado)
              "nada_consta"  -> base consultada, sem correspondência
  (o TSE 2022 só é "consultado" para quem já tinha candidatura em 2022; para os demais a linha não existe)

É SINAL DE CORROBORAÇÃO e de triagem: não altera nota. "Nada consta" só vale para o que a base cobre.

Uso: python -m pipeline.cruzar_bases_oficiais
"""
import difflib
import glob
import zipfile
from datetime import date

import pandas as pd

from pipeline import config
from pipeline.cruzar_motivos_tse import PESSOAL, SIMILARIDADE_MIN, _norm
from pipeline.cruzar_motivos_tse import cruzar as cruzar_tse_2022
from pipeline.cruzar_tcu_eleitoral import cruzar as cruzar_tcu
from pipeline.recomendar import INPUT_PATH

RAW = config.RAW_DIR
EST = RAW / "estruturadas"
SAIDA = INPUT_PATH.parent / "verificacao_bases_oficiais.csv"
HOJE = pd.Timestamp(date.today())

# rótulo mostrado ao eleitor, o que a base cobre e a data do arquivo baixado
BASES = {
    "tcu_eleitoral": ("TCU: contas julgadas irregulares (implicação eleitoral)", "2026-09-24"),
    "tse_2022": ("TSE: motivos de indeferimento/cassação em 2022", "2026-09-24"),
    "ceis": ("CEIS: empresas e pessoas sancionadas (Portal da Transparência)", "2026-09-23"),
    "cnep": ("CNEP: punições da Lei Anticorrupção (Portal da Transparência)", "2026-09-23"),
    "ceaf": ("CEAF: servidores expulsos do serviço público federal", "2026-09-23"),
    "ibama": ("Ibama: autos de infração ambiental", "2026-09-24"),
}


def _cpf(s: pd.Series) -> pd.Series:
    return s.astype(str).str.replace(r"\D", "", regex=True)


def _candidatos() -> pd.DataFrame:
    p = pd.read_parquet(INPUT_PATH)
    p["cpf"] = _cpf(p.cpf)
    return p[["sq_candidato", "cargo", "uf", "nome_urna", "nome_completo", "cpf"]]


def _casar_cpf_completo(p: pd.DataFrame, base: pd.DataFrame, nome_col: str) -> pd.DataFrame:
    m = p.merge(base, on="cpf")
    m["sim"] = [difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio() for a, b in zip(m.nome_completo, m[nome_col])]
    return m[m.sim >= SIMILARIDADE_MIN]


def _lista_sancoes(nome: str, p: pd.DataFrame, arquivo: str, csv: str) -> pd.DataFrame:
    d = pd.read_csv(zipfile.ZipFile(EST / arquivo).open(csv), sep=";", encoding="latin-1", dtype=str)
    d = d[d["TIPO DE PESSOA"] == "F"].copy()
    d["cpf"] = _cpf(d["CPF OU CNPJ DO SANCIONADO"])
    m = _casar_cpf_completo(p, d, "NOME DO SANCIONADO")
    fim = pd.to_datetime(m.filter(like="DATA FINAL").iloc[:, 0], format="%d/%m/%Y", errors="coerce")
    inicio = m.filter(like="DATA IN").iloc[:, 0]
    vigencia = ["vigente" if pd.isna(f) or f >= HOJE else "encerrada" for f in fim]
    cat = m.filter(like="CATEGORIA").iloc[:, 0]
    return pd.DataFrame({
        "sq_candidato": m.sq_candidato.values, "base": nome, "resultado": "consta",
        "detalhe": [f"{c} (início {i}, {v})" for c, i, v in zip(cat, inicio, vigencia)],
        "referencia": "https://portaldatransparencia.gov.br/sancoes/consulta"})


def _ceaf(p: pd.DataFrame) -> pd.DataFrame:
    d = pd.read_csv(zipfile.ZipFile(EST / "ceaf_20260923.zip").open("20260923_Expulsoes.csv"), sep=";",
                    encoding="latin-1", dtype=str)
    d = d[d["TIPO DE PESSOA"] == "F"].copy()
    d["meio"] = _cpf(d["CPF OU CNPJ DO SANCIONADO"])  # "***.603.193-**" -> "603193"
    d["nome_n"] = d["NOME DO SANCIONADO"].map(_norm)
    p = p.assign(meio=p.cpf.str[3:9], nome_n=p.nome_completo.map(_norm))
    m = p.merge(d, on=["meio", "nome_n"])  # nome IGUAL + 6 dígitos do meio
    cat = m.filter(like="CATEGORIA").iloc[:, 0]
    return pd.DataFrame({
        "sq_candidato": m.sq_candidato.values, "base": "ceaf", "resultado": "a_confirmar",
        "detalhe": [f"{c} (casou por nome + 6 dígitos do CPF; confirmar identidade)" for c in cat],
        "referencia": "https://portaldatransparencia.gov.br/sancoes/consulta"})


def _ibama(p: pd.DataFrame) -> pd.DataFrame:
    z = zipfile.ZipFile(EST / "ibama_auto_infracao.zip")
    usar = ["TP_PESSOA_INFRATOR", "NOME_INFRATOR", "CPF_CNPJ_INFRATOR", "VAL_AUTO_INFRACAO", "DAT_HORA_AUTO_INFRACAO", "UF",
            "SIT_CANCELADO"]
    partes = []
    for nome in z.namelist():
        d = pd.read_csv(z.open(nome), sep=";", encoding="utf-8", dtype=str, usecols=usar, on_bad_lines="skip")
        partes.append(d[(d.TP_PESSOA_INFRATOR == "PF") & (d.SIT_CANCELADO != "S")])
    d = pd.concat(partes)
    d["cpf"] = _cpf(d.CPF_CNPJ_INFRATOR)
    m = _casar_cpf_completo(p, d, "NOME_INFRATOR")
    m = m.assign(valor=pd.to_numeric(m.VAL_AUTO_INFRACAO.str.replace(",", "."), errors="coerce"),
                 data=pd.to_datetime(m.DAT_HORA_AUTO_INFRACAO, errors="coerce")).sort_values("valor", ascending=False)
    reais = lambda v: "valor não informado" if pd.isna(v) else "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    dia = lambda d: "data não informada" if pd.isna(d) else f"{d:%d/%m/%Y}"
    return pd.DataFrame({
        "sq_candidato": m.sq_candidato.values, "base": "ibama", "resultado": "consta",
        "detalhe": [f"Auto de infração de {reais(v)} em {dia(dt)} ({uf})" for v, dt, uf in zip(m.valor, m.data, m.UF)],
        "referencia": "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao"})


def verificar() -> pd.DataFrame:
    p = _candidatos()
    achados = []
    tcu = cruzar_tcu()
    achados.append(pd.DataFrame({
        "sq_candidato": tcu.sq_candidato, "base": "tcu_eleitoral", "resultado": "consta",
        "detalhe": [f"Contas julgadas irregulares, processo {pr}, trânsito em julgado em {t:%d/%m/%Y}, prazo até {f:%d/%m/%Y}"
                    for pr, t, f in zip(tcu.processo_tcu, tcu.transito_em_julgado, tcu.prazo_final)],
        "referencia": tcu.link_acordao}))
    tse = cruzar_tse_2022()
    tse = tse[tse.natureza == "pessoal"]  # motivos formais/de partido não são achado individual
    achados.append(pd.DataFrame({
        "sq_candidato": tse.sq_candidato, "base": "tse_2022", "resultado": "consta",
        "detalhe": [f"Fundamento citado no julgamento do registro: {m}" for m in tse.motivo],
        "referencia": "https://dadosabertos.tse.jus.br/dataset/candidatos-2022"}))
    achados.append(_lista_sancoes("ceis", p, "ceis_20260923.zip", "20260923_CEIS.csv"))
    achados.append(_lista_sancoes("cnep", p, "cnep_20260923.zip", "20260923_CNEP.csv"))
    achados.append(_ceaf(p))
    achados.append(_ibama(p))
    consta = pd.concat(achados).drop_duplicates()

    # quem já tinha candidatura em 2022 foi "consultado" na base do TSE (mesmo sem motivo); os demais não se aplica
    arqs = [f for f in glob.glob(str(RAW / "consulta_cand_2022" / "consulta_cand_2022_*.csv")) if not f.endswith(("_BR.csv", "_BRASIL.csv"))]
    cpfs22 = set(_cpf(pd.concat([pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, usecols=["NR_CPF_CANDIDATO"])
                                 for f in arqs]).NR_CPF_CANDIDATO))
    linhas = []
    for base in BASES:
        aplicaveis = p[p.cpf.isin(cpfs22)] if base == "tse_2022" else p
        com = consta[consta.base == base]
        sem = aplicaveis[~aplicaveis.sq_candidato.isin(com.sq_candidato)]
        linhas.append(pd.DataFrame({"sq_candidato": sem.sq_candidato, "base": base, "resultado": "nada_consta",
                                    "detalhe": "", "referencia": ""}))
    out = pd.concat([consta] + linhas)
    return out.merge(p[["sq_candidato", "cargo", "uf", "nome_urna"]], on="sq_candidato").sort_values(["cargo", "uf", "nome_urna", "base"], kind="stable")


def main() -> None:
    df = verificar()
    df.to_csv(SAIDA, index=False, encoding="utf-8-sig")
    print(f"Salvo em {SAIDA} ({len(df)} linhas)")
    print(df.groupby(["base", "resultado"]).sq_candidato.nunique().unstack(fill_value=0).to_string())
    maj = df[df.cargo.isin(["PRESIDENTE", "GOVERNADOR", "SENADOR"]) & (df.resultado != "nada_consta")]
    print("\nMajoritários com registro em alguma base (para conferir contra idoneidade.json):")
    print(maj[["cargo", "uf", "nome_urna", "base", "resultado", "detalhe"]].to_string(index=False))


if __name__ == "__main__":
    main()
