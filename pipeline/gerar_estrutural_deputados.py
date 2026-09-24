"""Gera, SEM busca na internet, as camadas de círculo político e experiência política de Deputado Federal, Estadual e Distrital.

Para Deputado (eleição proporcional) não há vice nem padrinho identificável em massa; a pesquisa manual dos
majoritários (Presidente, Governador, Senador) mostra que o círculo é dominado pelo presidente do próprio
partido. Aqui usamos só ele, com a MESMA convenção dos majoritários: federações e coligações não entram.
A experiência política vem dos arquivos de candidatos do TSE (consulta_cand_AAAA em data/raw/): quem já foi
ELEITO para um cargo, casado por TÍTULO ELEITORAL + nome (o CPF vem mascarado a partir de 2024).

Saídas (data/processed/, regeneráveis, no mesmo formato dos JSONs manuais de data/reference/):
  estrutural_circulo_politico.json       -> lido por enriquecer_circulo_politico.py
  estrutural_experiencia_politica.json   -> lido por enriquecer_experiencia.py
Os JSONs manuais têm precedência sobre estes se um candidato aparecer nos dois.

Tabela de caciques por partido: data/reference/circulo_partidos_estrutural.json (versionada, editável).
Ela é DERIVADA das pesquisas manuais de círculo (`--derivar-tabela`); revisar quando o presidente de um
partido mudar ou surgir pendência nova.

Honestidade sobre cobertura: a camada "experiência política" só conta como pesquisada (e só entra em
`camadas_pesquisadas`) quando TODOS os anos de ANOS_ESPERADOS estão em data/raw/. Com anos faltando, os
cargos encontrados ainda sobem a nota de competência (regra não regressiva), mas a camada fica "não pesquisada".

Uso:
  python -m pipeline.gerar_estrutural_deputados --derivar-tabela   # (re)gera a tabela de caciques
  python -m pipeline.gerar_estrutural_deputados                    # gera os dois arquivos
"""
import argparse
import collections
import datetime
import difflib
import glob
import json

import pandas as pd

from . import config
from .cruzar_motivos_tse import SIMILARIDADE_MIN, _norm
from .pesos import PESOS_CACIQUE

REF = config.RAW_DIR.parent / "reference"
TABELA_PATH = REF / "circulo_partidos_estrutural.json"
SAIDA_CIRCULO = config.PROCESSED_DIR / "estrutural_circulo_politico.json"
SAIDA_EXPERIENCIA = config.PROCESSED_DIR / "estrutural_experiencia_politica.json"

CARGOS = {"DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "DEPUTADO DISTRITAL"}
ANOS_ESPERADOS = (2014, 2016, 2018, 2020, 2022, 2024)
MIN_TITULO_VALIDO = 0.9  # fração mínima de linhas com título de 12 dígitos para o ano contar como coberto

# Cargo no arquivo do TSE (normalizado, sem acento) -> (nome em BOOST_POR_CARGO_ANTERIOR, tipo)
CARGO_ELETIVO = {
    "PRESIDENTE": ("PRESIDENTE", "executivo"),
    "GOVERNADOR": ("GOVERNADOR", "executivo"),
    "PREFEITO": ("PREFEITO", "executivo"),
    "SENADOR": ("SENADOR", "legislativo"),
    "DEPUTADO FEDERAL": ("DEPUTADO FEDERAL", "legislativo"),
    "DEPUTADO ESTADUAL": ("DEPUTADO ESTADUAL", "legislativo"),
    "DEPUTADO DISTRITAL": ("DEPUTADO DISTRITAL", "legislativo"),
    "VEREADOR": ("VEREADOR", "legislativo"),
}
CARGOS_MUNICIPAIS = {"PREFEITO", "VEREADOR"}
COLUNAS_HISTORICO = ["NR_TITULO_ELEITORAL_CANDIDATO", "NM_CANDIDATO", "DS_CARGO", "SG_UF", "NM_UE", "DS_SIT_TOT_TURNO", "SQ_CANDIDATO", "NR_TURNO"]


# ---------- tabela de caciques (presidente do partido) ----------
def derivar_tabela() -> dict:
    """Para cada partido, o desconto do presidente segundo a pesquisa manual MAIS RECENTE de círculo político.

    Regra: entre os apoiadores 'presidente do partido do candidato' contados, vale o par (tipo_pendencia,
    desconto) mais frequente na data de pesquisa mais recente daquele partido, considerando só as pesquisas cujo
    presidente é o do cache de lideranças; empate -> maior desconto.
    O texto público da pendência vem de liderancas_partidarias.json (sem anotações internas).
    """
    circulo = json.loads((REF / "circulo_politico.json").read_text(encoding="utf-8"))["candidatos"]
    liderancas = json.loads((REF / "liderancas_partidarias.json").read_text(encoding="utf-8"))["partidos"]
    por_partido = collections.defaultdict(list)
    for r in circulo.values():
        for a in r.get("apoiadores", []):
            if a["tipo_ligacao"] == "presidente_do_partido_do_candidato" and a.get("contado", True):
                por_partido[a["partido"]].append((r["pesquisado_em"], a["nome"], a["tipo_pendencia"], a["desconto"]))

    tabela = {}
    for partido, lider in liderancas.items():
        if partido in por_partido:
            registros = por_partido[partido]
            # só as pesquisas cujo presidente é o do cache de lideranças (nas manuais houve nome de outro partido
            # atribuído por engano, ex.: presidente do PRTB em entradas do PRD); sem nenhuma, usa todas
            primeiro = _norm(lider["presidente_nacional"]).split()[:1]
            do_presidente = [r for r in registros if _norm(r[1]).split()[:1] == primeiro]
            registros = do_presidente or registros
            ultima = max(r[0] for r in registros)
            recentes = [r for r in registros if r[0] == ultima]
            contagem = collections.Counter((r[2], r[3]) for r in recentes)
            (tipo, desconto), _ = max(contagem.items(), key=lambda kv: (kv[1], kv[0][1]))
            nome = next(r[1] for r in recentes if (r[2], r[3]) == (tipo, desconto))
            origem = f"pesquisa manual de círculo político de {ultima} ({sum(contagem.values())} candidatos)"
        else:
            tipo, desconto, nome, ultima = "nao_verificado", 0, lider["presidente_nacional"], lider["pesquisado_em"]
            origem = "sem apoiador correspondente nas pesquisas de círculo: presidente não verificado (desconto 0)"
        if PESOS_CACIQUE.get(tipo) != desconto:
            raise SystemExit(f"{partido}: desconto {desconto} não bate com PESOS_CACIQUE[{tipo}]={PESOS_CACIQUE.get(tipo)}")
        tabela[partido] = {
            "presidente": nome,
            "tipo_pendencia": tipo,
            "desconto": desconto,
            "pendencia": lider["pendencias"],
            "fontes": lider.get("fontes", []),
            "atualizado_em": ultima,
            "origem": origem,
        }
    return {
        "_leiame": (
            "Desconto do presidente do partido no círculo político de candidatos de eleição PROPORCIONAL (deputados), "
            "onde não há vice nem padrinho identificável em massa. Derivado de circulo_politico.json (pesquisa manual) por "
            "`python -m pipeline.gerar_estrutural_deputados --derivar-tabela`; pode ser editado à mão (o campo 'origem' "
            "avisa quando for edição manual). Mesma convenção dos majoritários: parceiros de federação e coligação não entram. "
            "'nao_verificado' com desconto 0 significa que a pendência do presidente NÃO foi pesquisada, não que não exista."
        ),
        "partidos": tabela,
    }


# ---------- histórico eleitoral (experiência política) ----------
def _arquivos_ano(ano: int) -> list:
    pasta = config.RAW_DIR / f"consulta_cand_{ano}"
    arquivos = [f for f in glob.glob(str(pasta / f"consulta_cand_{ano}_*.csv")) if not f.endswith(("_BR.csv", "_BRASIL.csv"))]
    for agregado in ("_BRASIL.csv", "_BR.csv"):
        alvo = pasta / f"consulta_cand_{ano}{agregado}"
        if alvo.exists():
            arquivos.append(str(alvo))
            break
    return arquivos


def carregar_historico() -> tuple:
    """Devolve (DataFrame de ELEITOS por título eleitoral, {ano: status}) com o que há em data/raw/."""
    partes, status = [], {}
    for ano in ANOS_ESPERADOS:
        arquivos = _arquivos_ano(ano)
        if not arquivos:
            status[ano] = "arquivo ausente"
            continue
        df = pd.concat(
            [pd.read_csv(f, sep=config.CSV_DELIMITER, encoding=config.CSV_ENCODING, dtype=str, usecols=COLUNAS_HISTORICO) for f in arquivos]
        )
        # quem vai ao 2º turno tem duas linhas: a do 1º diz só "2º TURNO"; vale a do último turno (eleito ou não)
        df = df.sort_values("NR_TURNO").drop_duplicates("SQ_CANDIDATO", keep="last")
        df["titulo"] = df.NR_TITULO_ELEITORAL_CANDIDATO.fillna("").str.replace(r"\D", "", regex=True)
        valido = df.titulo.str.len().between(10, 12) & ~df.titulo.str.fullmatch(r"0+")
        df["titulo"] = df.titulo.str.zfill(12)
        fracao = valido.mean()
        if fracao < MIN_TITULO_VALIDO:
            status[ano] = f"título eleitoral ausente/mascarado em {1 - fracao:.0%} das linhas: ano NÃO usado"
            continue
        status[ano] = f"ok ({len(df):,} candidaturas)"
        df = df[valido].copy()
        df["ano"] = ano
        partes.append(df)
    if not partes:
        return pd.DataFrame(), status
    todos = pd.concat(partes)
    # título ligado a mais de um nome no mesmo ano = dado ruim (mesmo critério de cruzar_motivos_tse para CPF)
    nomes = todos.groupby(["ano", "titulo"]).NM_CANDIDATO.nunique()
    ruins = set(nomes[nomes > 1].index)
    todos = todos[[(a, t) not in ruins for a, t in zip(todos.ano, todos.titulo)]]
    todos["cargo_norm"] = todos.DS_CARGO.map(_norm)
    eleitos = todos[todos.DS_SIT_TOT_TURNO.fillna("").map(_norm).str.startswith("ELEITO") & todos.cargo_norm.isin(CARGO_ELETIVO)]
    return eleitos, status


def experiencia(candidatos: pd.DataFrame, eleitos: pd.DataFrame, status: dict) -> dict:
    anos_ok = sorted(a for a, s in status.items() if s.startswith("ok"))
    completo = len(anos_ok) == len(ANOS_ESPERADOS)
    hoje = datetime.date.today().isoformat()
    por_titulo = {t: g for t, g in eleitos.groupby("titulo")}
    saida = {}
    for c in candidatos.itertuples():
        mandatos = []
        g = por_titulo.get(c.titulo)
        if g is not None:
            for r in g.itertuples():
                if difflib.SequenceMatcher(None, _norm(c.nome_completo), _norm(r.NM_CANDIDATO)).ratio() < SIMILARIDADE_MIN:
                    continue
                cargo, tipo = CARGO_ELETIVO[r.cargo_norm]
                local = f"{r.NM_UE.title()}/{r.SG_UF}" if r.cargo_norm in CARGOS_MUNICIPAIS else r.SG_UF
                mandatos.append({"cargo": cargo, "local": local, "periodo": f"{r.ano + 1}-{r.ano + 4}", "tipo": tipo})
        if not mandatos and not completo:
            continue  # cobertura parcial: só registra quem tem cargo achado (evita gravar "sem experiência" sem ter olhado tudo)
        mandatos.sort(key=lambda m: m["periodo"])
        saida[c.sq_candidato] = {
            "nome_urna": c.nome_urna,
            "cargo_pretendido": c.cargo,
            "teve_cargo_eletivo": bool(mandatos),
            "cargos_anteriores": mandatos,
            "notas": (
                f"Eleito segundo o TSE (consulta_cand {min(ANOS_ESPERADOS)} a {max(ANOS_ESPERADOS)}), casado por título eleitoral e nome; "
                "mandatos de eleições anteriores a essa janela não aparecem. 'Eleito' não garante o mandato inteiro: "
                "renúncia, cassação ou suplente convocado não aparecem aqui. Vice e suplente eleitos não contam como mandato."
            ),
            "fontes": [f"https://dadosabertos.tse.jus.br/dataset/candidatos-{a}" for a in anos_ok],
            "pesquisado_em": hoje if completo else None,
            "anos_cobertos": anos_ok,
            "origem": "estrutural",
        }
    return saida


# ---------- círculo político ----------
def carregar_titulos() -> dict:
    """sq_candidato -> título eleitoral (12 dígitos) de 2026, lido do CSV bruto (o parquet não guarda o título)."""
    partes = [
        pd.read_csv(f, sep=config.CSV_DELIMITER, encoding=config.CSV_ENCODING, dtype=str,
                    usecols=["SQ_CANDIDATO", "NR_TITULO_ELEITORAL_CANDIDATO"])
        for f in glob.glob(str(config.EXTRACT_DIR / f"consulta_cand_{config.ANO_ELEICAO}_*.csv"))
        if not f.endswith(("_BR.csv", "_BRASIL.csv"))
    ]
    t = pd.concat(partes).drop_duplicates("SQ_CANDIDATO")
    t["titulo"] = t.NR_TITULO_ELEITORAL_CANDIDATO.fillna("").str.replace(r"\D", "", regex=True).str.zfill(12)
    return dict(zip(t.SQ_CANDIDATO, t.titulo))


def circulo(candidatos: pd.DataFrame, tabela: dict) -> dict:
    saida = {}
    for c in candidatos.itertuples():
        t = tabela[c.partido]
        nota = max(0, 10 - t["desconto"])
        nao_verif = t["tipo_pendencia"] == "nao_verificado"
        saida[c.sq_candidato] = {
            "nome_urna": c.nome_urna,
            "cargo_pretendido": c.cargo,
            "nota": nota,
            "motivo": (
                f"Estrutural (sem busca por candidato): em eleição proporcional só conta o presidente do partido "
                f"({t['presidente']}, {c.partido}), mesma convenção dos majoritários; federações e coligações não entram. "
                + ("Pendência do presidente NÃO verificada (sem desconto)." if nao_verif else f"Desconto de {t['desconto']} pela pendência do presidente.")
            ),
            "vice": None,
            "padrinho_politico": None,
            "partidos_coligacao_relevantes": [],
            "fontes": t["fontes"],
            "pesquisado_em": t["atualizado_em"],
            "apoiadores": [
                {
                    "nome": t["presidente"],
                    "partido": c.partido,
                    "tipo_ligacao": "presidente_do_partido_do_candidato",
                    "ligacao_detalhe": f"presidente nacional do {c.partido}, partido do candidato",
                    "tipo_pendencia": t["tipo_pendencia"],
                    "pendencia": t["pendencia"],
                    "desconto": t["desconto"],
                    "contado": True,
                }
            ],
            "descontos_adicionais": [],
            "origem": "estrutural",
        }
    return saida


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--derivar-tabela", action="store_true", help="(re)gera data/reference/circulo_partidos_estrutural.json")
    args = ap.parse_args()

    if args.derivar_tabela:
        tabela = derivar_tabela()
        TABELA_PATH.write_text(json.dumps(tabela, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Tabela de caciques gravada em {TABELA_PATH} ({len(tabela['partidos'])} partidos)")
        for p, t in sorted(tabela["partidos"].items()):
            print(f"  {p:14s} {t['presidente'][:36]:36s} {t['tipo_pendencia']:38s} -{t['desconto']}  [{t['atualizado_em']}]")
        return

    tabela = json.loads(TABELA_PATH.read_text(encoding="utf-8"))["partidos"]
    df = pd.read_parquet(config.OUTPUT_PARQUET)
    df = df[df.cargo.isin(CARGOS)].copy()
    df["titulo"] = df.sq_candidato.map(carregar_titulos())
    faltam = sorted(set(df.partido) - set(tabela))
    if faltam:
        raise SystemExit(f"Partidos sem linha em {TABELA_PATH.name}: {faltam}. Rode --derivar-tabela.")

    eleitos, status = carregar_historico()
    print("Histórico eleitoral (data/raw/consulta_cand_AAAA):")
    for ano in ANOS_ESPERADOS:
        print(f"  {ano}: {status.get(ano)}")

    exp = experiencia(df, eleitos, status) if len(eleitos) else {}
    circ = circulo(df, tabela)
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cabecalho = {"_leiame": "Gerado por pipeline/gerar_estrutural_deputados.py; regenerável, não editar à mão."}
    SAIDA_CIRCULO.write_text(json.dumps({**cabecalho, "candidatos": circ}, ensure_ascii=False), encoding="utf-8")
    SAIDA_EXPERIENCIA.write_text(json.dumps({**cabecalho, "candidatos": exp}, ensure_ascii=False), encoding="utf-8")

    com_cargo = sum(1 for r in exp.values() if r["teve_cargo_eletivo"])
    completo = all(str(status.get(a, "")).startswith("ok") for a in ANOS_ESPERADOS)
    print(f"\n{len(df):,} candidatos de {', '.join(sorted(CARGOS))}")
    print(f"Círculo político: {len(circ):,} registros")
    print(f"Experiência política: {len(exp):,} registros, {com_cargo:,} com cargo eletivo achado; camada "
          + ("COMPLETA (todos os anos)" if completo else "PARCIAL: não conta como pesquisada até baixar todos os anos"))
    if com_cargo:
        cont = collections.Counter(m["cargo"] for r in exp.values() for m in r["cargos_anteriores"])
        print("  mandatos achados:", dict(cont.most_common()))


if __name__ == "__main__":
    main()
