"""Gera uma página estática por cargo/UF (site/<cargo>/<uf>/index.html) e o site/sitemap.xml, para o Google indexar.

O site é uma página única que monta tudo por JavaScript; o buscador vê pouco texto e um único endereço. Aqui cada
cargo/UF vira uma cópia de site/index.html com título, descrição e endereço próprios, o grupo já escolhido
(data-grupo no <body>, lido pelo app.js), a lista de todos os candidatos em texto (item "lista única" de "Todos os
candidatos") e uma linha discreta de links para os grupos vizinhos. A página inicial ganha o índice com links para
todas as páginas.

O modelo é o próprio site/index.html: só as regiões entre os marcadores <!-- seo:head -->, <!-- seo:conteudo --> e
<!-- seo:lista --> são reescritas, então rodar de novo é idempotente. Roda sozinho no fim de pipeline.exportar_prototipo.

Uso: python -m pipeline.gerar_paginas_seo
"""
import json
import re
import shutil
import unicodedata
from decimal import ROUND_HALF_UP, Decimal
from html import escape

from . import config

RAIZ = config.RAW_DIR.parent.parent
SITE = RAIZ / "site"
URL = "https://meu-melhor-candidato.afsm.me"

UF_NOME = {
    "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá", "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal",
    "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul",
    "MT": "Mato Grosso", "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco", "PI": "Piauí", "PR": "Paraná",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RO": "Rondônia", "RR": "Roraima", "RS": "Rio Grande do Sul",
    "SC": "Santa Catarina", "SE": "Sergipe", "SP": "São Paulo", "TO": "Tocantins",
}
# "no Rio de Janeiro", "na Bahia", "em São Paulo"
UF_PREP = {**{u: "em" for u in UF_NOME}, **{u: "no" for u in "AC AP AM CE DF ES MA MT MS PA PR PI RJ RN RS TO".split()},
           "BA": "na", "PB": "na"}
SITUACAO = {"recomendado": "Recomendado", "segue": "Continua na disputa", "abaixo_do_corte": "Abaixo do corte",
            "fora_da_disputa": "Fora da disputa", "nao_avaliado": "Sem verificação"}
MINUSC = {"da", "de", "do", "das", "dos", "e"}

DESCRICAO_HOME = "Encontre o candidato político com mais integridade, competência e alinhamento ideológico com você!"
TITULO_HOME = "Meu melhor candidato"


def tc(s: str) -> str:
    """Mesmo "Title Case" do app.js."""
    return " ".join(w if i and w in MINUSC else w[:1].upper() + w[1:] for i, w in enumerate(s.lower().split(" ")))


def fmt(x) -> str:
    """Como o fmt do app.js (toLocaleString): meio para cima sobre o valor binário exato (9,25 → 9,3)."""
    return "n/d" if x is None else str(Decimal(x).quantize(Decimal("0.1"), ROUND_HALF_UP)).replace(".", ",")


def ordem(s: str) -> str:
    """Chave de ordenação alfabética que ignora acentos (Pará, Paraíba, Paraná)."""
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def url_grupo(cargo: str, uf: str) -> str:
    return "/" + cargo.lower().replace(" ", "-") + "/" + ("" if uf == "BR" else uf.lower() + "/")


def onde(uf: str) -> str:
    return "" if uf == "BR" else f" {UF_PREP[uf]} {UF_NOME[uf]}"


def ler_js(caminho, prefixo: str):
    t = caminho.read_text(encoding="utf-8")
    i = t.index(prefixo) + len(prefixo)
    return json.loads(t[i:t.rindex(";")])


def cabecalho(titulo: str, descricao: str, url: str, extra: str = "") -> str:
    t, d, u = escape(titulo), escape(descricao), escape(URL + url)
    return f"""<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Meu melhor candidato">
<meta property="og:url" content="{u}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Meu melhor candidato: encontre o candidato com mais integridade, competência e alinhamento ideológico com você.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{URL}/og-image.png">
{extra}"""


def json_ld(obj: dict) -> str:
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>\n"


def juntar(itens) -> str:
    return " · ".join(f'<a href="{u}">{escape(r)}</a>' for u, r in itens)


def bloco_nav(resumo: str, linhas: list) -> str:
    """Links para outras páginas, recolhidos acima do rodapé. O buscador lê e segue links dentro de <details> fechado."""
    return ('<nav class="seo-nav" aria-label="Outras páginas do site">\n<details class="expansor">'
            f"<summary>{escape(resumo)}</summary>\n" + "\n".join(f"<p>{x}</p>" for x in linhas) + "\n</details>\n</nav>")


def lista_texto(cands: list) -> str:
    """Itens da "lista única" de "Todos os candidatos": uma linha de texto por candidato, na ordem da lista paginada.
    O app.js monta o mesmo texto (listaUnica) quando o eleitor troca de grupo: mudou aqui, mude lá."""
    ordenados = sorted(cands, key=lambda c: (-(c["qualificacao_geral"] if c["qualificacao_geral"] is not None else -1),
                                             ordem(c["nome_urna"])))
    linhas = []
    for c in ordenados:
        nome = tc(c["nome_urna"])
        completo = tc(c["nome_completo"]) if c.get("nome_completo") and c["nome_completo"] != c["nome_urna"] else ""
        linhas.append(f"<li><strong>{escape(nome)}</strong>" + (f" ({escape(completo)})" if completo else "")
                      + f", {escape(c['partido'])} {escape(c['numero'])}: qualificação {fmt(c['qualificacao_geral'])}, "
                      f"idoneidade {fmt(c['idoneidade_geral'])}, competência {fmt(c['competencia_geral'])}. "
                      f"{SITUACAO.get(c['situacao'], '')}.</li>")
    return "\n".join(linhas)


def navegacao_grupo(g: dict, rotulos: dict, grupos: dict) -> str:
    """Links para os grupos vizinhos (ajudam o buscador a achar e ligar as páginas)."""
    cargo, uf = g["cargo"], g["uf"]
    partes = []
    if uf != "BR":
        outros = [(url_grupo(c, uf), rotulos[c]) for c in rotulos if c != cargo and f"{c}|{uf}" in grupos]
        if outros:
            partes.append(f"Outros cargos{escape(onde(uf))}: {juntar(outros)}")
        vizinhos = sorted(((url_grupo(cargo, u), UF_NOME[u]) for k in grupos
                           for c, u in [k.split("|")] if c == cargo and u != uf), key=lambda x: ordem(x[1]))
        if vizinhos:
            partes.append(f"{escape(rotulos[cargo])} em outros estados: {juntar(vizinhos)}")
    partes.append('<a href="/">Todos os cargos e estados</a>')
    return bloco_nav("Ver outros cargos e estados", partes)


def conteudo_home(rotulos: dict, grupos: dict) -> str:
    """Índice da página inicial: uma linha por cargo com links para todas as páginas."""
    partes = []
    for cargo, rot in rotulos.items():
        ufs = sorted((u for k in grupos for c, u in [k.split("|")] if c == cargo), key=lambda u: ordem(UF_NOME.get(u, "")))
        if ufs == ["BR"]:
            partes.append(f"{escape(rot)}: " + juntar([(url_grupo(cargo, "BR"), f"Candidatos a {rot.lower()}")]))
        elif ufs:
            partes.append(f"{escape(rot)}: " + juntar([(url_grupo(cargo, u), UF_NOME[u]) for u in ufs]))
    return bloco_nav("Ver as páginas de cada cargo e estado", partes)


def montar(modelo: str, head: str, conteudo: str, lista: str, grupo: str | None) -> str:
    t = re.sub(r"<!-- seo:head -->.*?<!-- /seo:head -->", lambda _: f"<!-- seo:head -->\n{head}<!-- /seo:head -->",
               modelo, count=1, flags=re.S)
    t = re.sub(r"<!-- seo:conteudo -->.*?<!-- /seo:conteudo -->",
               lambda _: f"<!-- seo:conteudo -->\n{conteudo}\n<!-- /seo:conteudo -->", t, count=1, flags=re.S)
    t = re.sub(r"<!-- seo:lista -->.*?<!-- /seo:lista -->",
               lambda _: f"<!-- seo:lista -->\n{lista}\n<!-- /seo:lista -->", t, count=1, flags=re.S)
    corpo = f'<body data-grupo="{escape(grupo)}">' if grupo else "<body>"
    return re.sub(r"<body[^>]*>", corpo, t, count=1)


def main() -> None:
    DADOS = ler_js(SITE / "dados.js", "const DADOS = ")
    rotulos = {c["codigo"]: c["rotulo"] for c in DADOS["cargos"]}
    grupos = {k: g for k, g in DADOS["grupos"].items() if g.get("arquivo") and g.get("status") != "sem_verificacao"}
    modelo = (SITE / "index.html").read_text(encoding="utf-8")
    for s in {url_grupo(c, "BR").strip("/") for c in rotulos}:  # o gerador é o dono destas pastas
        shutil.rmtree(SITE / s, ignore_errors=True)

    urls = ["/"]
    for chave, g in grupos.items():
        cargo, uf = g["cargo"], g["uf"]
        rot = rotulos[cargo].lower()
        dados_grupo = ler_js(SITE / g["arquivo"], "] = ")
        sigla = "" if uf == "BR" else f" ({uf})"
        titulo = f"Candidatos a {rot}{onde(uf)}{sigla} 2026: ranking e notas | Meu melhor candidato"
        descricao = (f"Compare os {milhar(g['n_total'])} candidatos a {rot}{onde(uf)} nas Eleições 2026 por idoneidade, "
                     f"competência e posição ideológica, e veja os recomendados em cada quadrante.")
        url = url_grupo(cargo, uf)
        migalhas = [{"@type": "ListItem", "position": 1, "name": "Meu melhor candidato", "item": URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": f"{rotulos[cargo]}{onde(uf)}", "item": URL + url}]
        head = cabecalho(titulo, descricao, url, json_ld({"@context": "https://schema.org", "@type": "BreadcrumbList",
                                                           "itemListElement": migalhas}))
        html = montar(modelo, head, navegacao_grupo(g, rotulos, grupos), lista_texto(dados_grupo["candidatos"]), chave)
        destino = SITE / url.strip("/") / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(html, encoding="utf-8", newline="\n")
        urls.append(url)

    head_home = cabecalho(TITULO_HOME, DESCRICAO_HOME, "/", json_ld({
        "@context": "https://schema.org", "@type": "WebSite", "name": "Meu melhor candidato", "url": URL + "/",
        "inLanguage": "pt-BR",
        "description": "Ferramenta gratuita e de código aberto que avalia candidatos das Eleições 2026 no Brasil por "
                       "integridade, competência e alinhamento ideológico."}))
    (SITE / "index.html").write_text(montar(modelo, head_home, conteudo_home(rotulos, grupos), "", None),
                                     encoding="utf-8", newline="\n")

    lastmod = DADOS["meta"]["gerado_em"]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{URL}{u}</loc><lastmod>{lastmod}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(urls) - 1} páginas de cargo/UF + página inicial; sitemap com {len(urls)} endereços")


if __name__ == "__main__":
    main()
