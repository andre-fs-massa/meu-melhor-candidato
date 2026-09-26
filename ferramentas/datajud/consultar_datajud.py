"""Consulta a API pública do DataJud (CNJ) para CONFIRMAR processos já achados.

A API não traz nome nem CPF das partes: não serve para descobrir processos de um
candidato, só para ler classe, órgão julgador e andamentos oficiais de um processo
cujo número (ou classe + tribunal + período) já conhecemos.

Uso:
  python consultar_datajud.py processo 0600123-45.2025.6.06.0000
  python consultar_datajud.py processo 06001234520256060000 --tribunal tse
  python consultar_datajud.py buscar tre-ce --classe "Desfiliação Partidária" \
      --mov-desde 2026-06-29 --mov-ate 2026-06-30
  python consultar_datajud.py buscar tse --numero "*202260400*" --classe "Recurso Ordinário"
  (--todos mostra todos os andamentos, não só os decisivos; --json devolve o bruto)

Chave pública em https://datajud-wiki.cnj.jus.br/api-publica/acesso/ (o CNJ pode
trocá-la; se der 401, copiar a nova para DATAJUD_APIKEY ou para CHAVE_PADRAO).
STF não está no DataJud.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

CHAVE_PADRAO = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
URL = "https://api-publica.datajud.cnj.jus.br/api_publica_{}/_search"

# Código TR do número CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO) -> UF, igual para TJ e TRE.
UFS_TR = ["ac", "al", "ap", "am", "ba", "ce", "df", "es", "go", "ma", "mt", "ms", "mg",
          "pa", "pb", "pr", "pe", "pi", "rj", "rn", "rs", "ro", "rr", "sc", "se", "sp", "to"]

# Andamentos que mudam a situação do processo (o resto é expediente: juntada,
# conclusão, publicação...). Casamento por trecho do nome oficial da TPU/CNJ.
DECISIVOS = re.compile(
    r"proced|provimento|trânsito|transito|arquiv|extin|cassa|homolog|julgamento|"
    r"sentença|acórdão|acordao|recurso|remetidos|baixa|liminar|antecipação|"
    r"condena|absolvi|denúncia|denuncia|rejei|prescri|desist|embargos|"
    r"suspens|sobrestamento|decisão|decisao|admiss|inadmiss|pauta|anula|punibilidade",
    re.I)


def chave():
    return os.environ.get("DATAJUD_APIKEY", CHAVE_PADRAO)


def pesquisar(tribunal, corpo):
    req = urllib.request.Request(
        URL.format(tribunal), data=json.dumps(corpo).encode("utf-8"), method="POST",
        headers={"Authorization": "APIKey " + chave(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"DataJud respondeu {e.code} em {tribunal}: {e.read().decode('utf-8', 'replace')[:500]}")


def so_digitos(numero):
    d = re.sub(r"\D", "", numero)
    if len(d) != 20:
        sys.exit(f"Número CNJ deve ter 20 dígitos, veio {len(d)}: {numero}")
    return d


def formatar(d):
    return f"{d[:7]}-{d[7:9]}.{d[9:13]}.{d[13]}.{d[14:16]}.{d[16:]}"


def tribunal_do_numero(d):
    """Deduz o alias do tribunal pelos segmentos J e TR do número CNJ."""
    j, tr = d[13], int(d[14:16])
    if j == "8":
        return "tj" + UFS_TR[tr - 1]
    if j == "6":
        return "tse" if tr == 0 else "tre-" + UFS_TR[tr - 1]
    if j == "4":
        return f"trf{tr}"
    if j == "5":
        return "tst" if tr == 0 else f"trt{tr}"
    if j == "3":
        return "stj"
    sys.exit(f"Segmento de justiça {j} sem alias conhecido; passe --tribunal.")


def data_curta(s):
    if not s:
        return "?"
    if re.fullmatch(r"\d{8,14}", s):  # dataAjuizamento vem como AAAAMMDDhhmmss
        return f"{s[6:8]}/{s[4:6]}/{s[:4]}"
    return f"{s[8:10]}/{s[5:7]}/{s[:4]}"


def complementos(m):
    return "; ".join(c.get("nome", "") for c in m.get("complementosTabelados") or [] if c.get("nome"))


def imprimir(fonte, todos=False, mov_desde=None, mov_ate=None):
    d = fonte["numeroProcesso"]
    print(f"\n{fonte['tribunal']} {fonte.get('grau', '')}  {formatar(d) if len(d) == 20 else d}")
    print(f"  classe: {fonte.get('classe', {}).get('nome')}")
    assuntos = ", ".join(a.get("nome", "") for a in fonte.get("assuntos") or [] if isinstance(a, dict))
    if assuntos:
        print(f"  assuntos: {assuntos}")
    print(f"  órgão: {fonte.get('orgaoJulgador', {}).get('nome')}")
    print(f"  ajuizado: {data_curta(fonte.get('dataAjuizamento'))}   sigilo: {fonte.get('nivelSigilo')}"
          f"   atualizado: {data_curta(fonte.get('dataHoraUltimaAtualizacao'))}")
    movs = sorted(fonte.get("movimentos") or [], key=lambda m: m.get("dataHora", ""))
    for m in movs:
        dia = m.get("dataHora", "")[:10]
        marcado = (mov_desde and mov_desde <= dia <= (mov_ate or "9999"))
        if todos or DECISIVOS.search(m.get("nome", "")) or marcado:
            extra = complementos(m)
            print(f"  {'>' if marcado else ' '} {data_curta(m.get('dataHora'))}  {m.get('nome')}"
                  + (f"  [{extra}]" if extra else ""))
    if movs:
        u = movs[-1]
        print(f"  último andamento: {data_curta(u.get('dataHora'))} {u.get('nome')}")


def cmd_processo(a):
    d = so_digitos(a.numero)
    tribunais = [a.tribunal] if a.tribunal else [tribunal_do_numero(d)]
    achou = False
    for t in tribunais:
        r = pesquisar(t, {"size": 20, "query": {"match": {"numeroProcesso": d}}})
        for h in r["hits"]["hits"]:
            achou = True
            if a.json:
                print(json.dumps(h["_source"], ensure_ascii=False, indent=1))
            else:
                imprimir(h["_source"], a.todos)
    if not achou:
        print(f"Não encontrado em {', '.join(tribunais)} (pode ser sigiloso, de outro "
              "tribunal/grau, ou ainda não enviado ao DataJud).")


def cmd_buscar(a):
    filtros = []
    if a.classe:
        filtros.append({"match_phrase": {"classe.nome": a.classe}})
    if a.orgao:
        filtros.append({"match_phrase": {"orgaoJulgador.nome": a.orgao}})
    if a.assunto:
        filtros.append({"match_phrase": {"assuntos.nome": a.assunto}})
    if a.grau:
        filtros.append({"match": {"grau": a.grau}})
    if a.numero:
        filtros.append({"wildcard": {"numeroProcesso": a.numero}})
    if a.desde or a.ate:
        faixa = {}
        if a.desde:
            faixa["gte"] = a.desde.replace("-", "") + "000000"
        if a.ate:
            faixa["lte"] = a.ate.replace("-", "") + "235959"
        filtros.append({"range": {"dataAjuizamento": faixa}})
    if a.mov_desde or a.mov_ate:
        faixa = {}
        if a.mov_desde:
            faixa["gte"] = a.mov_desde
        if a.mov_ate:
            faixa["lte"] = a.mov_ate + "T23:59:59"
        filtros.append({"range": {"movimentos.dataHora": faixa}})
    if not filtros:
        sys.exit("Passe ao menos um filtro.")
    r = pesquisar(a.tribunal, {"size": a.limite, "query": {"bool": {"filter": filtros}},
                               "sort": [{"dataAjuizamento": "desc"}]})
    total = r["hits"]["total"]["value"]
    print(f"{total} processo(s) em {a.tribunal}; mostrando {len(r['hits']['hits'])}.")
    for h in r["hits"]["hits"]:
        if a.json:
            print(json.dumps(h["_source"], ensure_ascii=False, indent=1))
        else:
            imprimir(h["_source"], a.todos, a.mov_desde, a.mov_ate)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pp = sub.add_parser("processo", help="consulta por número CNJ")
    pp.add_argument("numero")
    pp.add_argument("--tribunal", help="alias (tjsp, tre-ce, tse...); padrão: deduz do número")
    pb = sub.add_parser("buscar", help="lista processos por classe/órgão/período")
    pb.add_argument("tribunal")
    pb.add_argument("--classe")
    pb.add_argument("--orgao")
    pb.add_argument("--assunto")
    pb.add_argument("--grau", help="G1, G2, SUP...")
    pb.add_argument("--numero", help="padrão do número só com dígitos e *, ex.: '*202260400*' "
                    "(recursos no TSE vindos do TRE-AM, eleição 2022)")
    pb.add_argument("--desde", help="ajuizado a partir de AAAA-MM-DD")
    pb.add_argument("--ate", help="ajuizado até AAAA-MM-DD")
    pb.add_argument("--mov-desde", help="com andamento a partir de AAAA-MM-DD")
    pb.add_argument("--mov-ate", help="com andamento até AAAA-MM-DD")
    pb.add_argument("--limite", type=int, default=20)
    for x in (pp, pb):
        x.add_argument("--todos", action="store_true", help="mostra todos os andamentos")
        x.add_argument("--json", action="store_true")
    a = p.parse_args()
    {"processo": cmd_processo, "buscar": cmd_buscar}[a.cmd](a)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
