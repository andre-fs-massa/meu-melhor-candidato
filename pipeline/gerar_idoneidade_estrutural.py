"""Gera, SEM busca na internet, a idoneidade PESSOAL de Deputado Federal a partir das bases oficiais já cruzadas.

Entrada: data/processed/verificacao_bases_oficiais.csv (`python -m pipeline.cruzar_bases_oficiais`).
Saída:   data/processed/estrutural_idoneidade.json, no formato de data/reference/idoneidade.json, lido por
         enriquecer_idoneidade.py e exportar_prototipo.py (o JSON manual tem precedência).

Regra (decidida com o usuário em 2026-09-24), sempre com categorias de pipeline/pesos.py:
  * parte de 10 e desconta um achado por base, mesmo com vários registros na mesma base;
  * TCU, contas julgadas irregulares (lista com implicação eleitoral) ......... contas_irregulares_com_ressarcimento (-2)
  * CEIS/CNEP, sanção VIGENTE (as encerradas ficam só no painel) ............... sancao_institucional_confirmada (-2)
  * Ibama, algum auto individual >= R$ 1 mi ..................................... sancao_institucional_confirmada (-2)
  * Ibama, autos todos abaixo de R$ 1 mi ........................................ infracao_administrativa_ambiental (-1)
  * TSE 2022 (motivo pessoal) e CEAF (só nome + 6 dígitos do CPF) ............... só painel, sem desconto.
    O TSE 2022 cita o fundamento do julgamento do registro, não a decisão final (pode ter sido revertida).

LIMITE: as bases não cobrem processo criminal, improbidade, inquérito nem imprensa. Nota 10 aqui quer dizer
"nada consta nestas bases", não "ficha limpa"; o site marca estes candidatos como verificação estrutural.

Uso: python -m pipeline.gerar_idoneidade_estrutural
"""
import datetime
import json
import re

import pandas as pd

from . import config
from .cruzar_bases_oficiais import SAIDA as CSV_BASES
from .gerar_estrutural_deputados import CARGOS
from .pesos import calcular_nota, formatar_achados

SAIDA = config.PROCESSED_DIR / "estrutural_idoneidade.json"
LIMITE_IBAMA = 1_000_000  # autos a partir deste valor (um único auto) valem como sanção institucional
PADRAO_VALOR = re.compile(r"R\$ ([\d\.]+,\d{2})")


def _valor(detalhe: str):
    m = PADRAO_VALOR.search(detalhe)
    return float(m.group(1).replace(".", "").replace(",", ".")) if m else None


def _reais(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def achados_do_candidato(linhas: pd.DataFrame) -> tuple:
    """(achados, fontes) de um candidato, a partir das linhas 'consta' do CSV de verificação."""
    achados, fontes = [], []
    for base, g in linhas.groupby("base"):
        itens = list(dict.fromkeys(g.detalhe))
        refs = [r for r in dict.fromkeys(g.referencia) if isinstance(r, str) and r.startswith("http")]
        if base == "tcu_eleitoral":
            achados.append({"categoria": "contas_irregulares_com_ressarcimento", "descricao": (
                f"Lista do TCU de contas julgadas irregulares (implicação eleitoral): {len(itens)} processo(s). "
                + "; ".join(itens[:3]) + (f"; e mais {len(itens) - 3}" if len(itens) > 3 else "")
                + ". A lista não informa se houve ressarcimento; quem declara a inelegibilidade é a Justiça Eleitoral.")})
            fontes += refs[:1]
        elif base in ("ceis", "cnep"):
            vigentes = [i for i in itens if "vigente" in i]
            if vigentes:
                achados.append({"categoria": "sancao_institucional_confirmada", "descricao": (
                    f"{base.upper()} (Portal da Transparência): " + "; ".join(vigentes[:3]) + ".")})
                fontes += refs[:1]
        elif base == "ibama":
            valores = [_valor(i) for i in itens]
            conhecidos = [v for v in valores if v is not None]
            maior = max(conhecidos) if conhecidos else 0
            resumo = (f"{len(itens)} auto(s) de infração ambiental não cancelado(s) no Ibama, "
                      f"o maior de {_reais(maior)}, somando {_reais(sum(conhecidos))}" if conhecidos
                      else f"{len(itens)} auto(s) de infração ambiental não cancelado(s) no Ibama, valor não informado")
            categoria = "sancao_institucional_confirmada" if maior >= LIMITE_IBAMA else "infracao_administrativa_ambiental"
            achados.append({"categoria": categoria, "descricao": resumo + "."})
            fontes += refs[:1]
    return achados, list(dict.fromkeys(fontes))


def gerar() -> dict:
    if not CSV_BASES.exists():
        raise SystemExit(f"{CSV_BASES.name} não existe. Rode `python -m pipeline.cruzar_bases_oficiais` primeiro.")
    df = pd.read_parquet(config.OUTPUT_PARQUET)
    df = df[df.cargo.isin(CARGOS)]
    bases = pd.read_csv(CSV_BASES, dtype=str, encoding="utf-8-sig").fillna("")
    consta = bases[bases.resultado == "consta"]
    por_sq = {sq: g for sq, g in consta.groupby("sq_candidato")}
    hoje = datetime.date.today().isoformat()
    saida = {}
    for c in df.itertuples():
        achados, fontes = achados_do_candidato(por_sq[c.sq_candidato]) if c.sq_candidato in por_sq else ([], [])
        nota = calcular_nota(achados)
        so_painel = por_sq[c.sq_candidato].base.isin(["tse_2022"]).any() if c.sq_candidato in por_sq else False
        saida[c.sq_candidato] = {
            "nome_urna": c.nome_urna,
            "cargo_pretendido": c.cargo,
            "nota": nota,
            "motivo": (
                "Estrutural (sem busca na internet): parte de 10 e desconta só registros em bases oficiais (TCU, CEIS/CNEP, Ibama). "
                "Nota 10 quer dizer que nada consta nessas bases; NÃO inclui processos judiciais, inquéritos nem notícias."
                + (" Há também registro no painel de conferência (TSE 2022 ou CEAF) que não altera a nota." if so_painel else "")
            ),
            "achados": achados,
            "fontes": fontes,
            "pesquisado_em": hoje,
            "origem": "estrutural",
        }
        assert nota == calcular_nota(achados)
    return saida


def main() -> None:
    saida = gerar()
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(json.dumps({"_leiame": "Gerado por pipeline/gerar_idoneidade_estrutural.py; regenerável, não editar à mão.",
                                 "candidatos": saida}, ensure_ascii=False), encoding="utf-8")
    notas = pd.Series([r["nota"] for r in saida.values()]).value_counts().sort_index()
    print(f"{len(saida):,} candidatos; salvo em {SAIDA}")
    print("Nota pessoal estrutural:", notas.to_dict())
    com = [(r["nome_urna"], r["nota"], [a["categoria"] for a in r["achados"]]) for r in saida.values() if r["achados"]]
    print(f"{len(com)} com desconto. Primeiros:")
    for nome, nota, cats in sorted(com, key=lambda x: x[1])[:8]:
        print(f"  {nome}: {nota} {cats}")
    print("Formato de exemplo:", formatar_achados(next(r["achados"] for r in saida.values() if r["achados"]))[:200])


if __name__ == "__main__":
    main()
