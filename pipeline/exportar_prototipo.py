"""Exporta os dados do protótipo do eleitor (site/dados.js) a partir do funil de recomendação.

Uma única fonte da verdade: as recomendações vêm de `pipeline.recomendar.recomendar`, com o corte do cargo e a
política de não avaliados padrão (corte 6,0, e 8,5 para deputados; só recomenda quem tem idoneidade geral verificada). Para cada
cargo/UF com pelo menos um candidato verificado, exporta TODOS os candidatos com a situação de cada um
(fora da disputa, abaixo do corte, segue, recomendado) e os motivos estruturados das notas. Cargo/UF sem
nenhum candidato verificado exporta só as contagens, e a página mostra "ainda sem verificação".

Formato: `site/dados.js` é só o índice; cada cargo/UF com candidatos vai para `site/dados/<cargo>_<uf>.js`, carregado
sob demanda pelo site.

Uso: python -m pipeline.exportar_prototipo
"""
import hashlib
import json
import shutil
from collections import Counter
from datetime import date

import pandas as pd

from . import config
from .cruzar_bases_oficiais import BASES, SAIDA as CSV_BASES_OFICIAIS
from .enriquecer_circulo_politico import ROTULO_LIGACAO
from .pesos import PESOS_ACHADO
from .recomendar import (
    CORTE_IDONEIDADE_PADRAO, CORTE_POR_CARGO, INPUT_PATH, LIMIAR_QUADRANTE, MARGEM_FRONTEIRA, NOME_QUADRANTE, REF_DIR,
    VAGAS_POR_QUADRANTE, preparar, recomendar,
)

RAIZ = config.RAW_DIR.parent.parent
SAIDAS = [RAIZ / "site" / "dados.js"]
ROTULO_CARGO = {
    "PRESIDENTE": "Presidente", "GOVERNADOR": "Governador", "SENADOR": "Senador",
    "DEPUTADO FEDERAL": "Deputado federal", "DEPUTADO ESTADUAL": "Deputado estadual", "DEPUTADO DISTRITAL": "Deputado distrital",
}
ROTULO_ACHADO = {
    "inelegibilidade_vigente": "Inelegível (Ficha Limpa vigente)",
    "condenacao_criminal_pena_cumprida": "Condenação criminal com pena cumprida (inclui prisão)",
    "condenacao_confirmada_sem_reversao": "Condenação confirmada, sem reversão",
    "condenacao_1a_instancia_recorrivel": "Condenação de 1ª instância (cabe recurso)",
    "condenacao_revertida": "Condenação revertida em instância superior",
    "cassacao_de_mandato": "Cassação de mandato",
    "sancao_institucional_confirmada": "Sanção institucional confirmada (não criminal)",
    "reu_acao_penal": "Réu em ação penal",
    "investigacao_ou_acao_civil_em_curso": "Investigação ou ação civil em curso",
    "registro_indeferido": "Registro de candidatura indeferido",
    "registro_contestado_sub_judice": "Registro contestado, aguardando decisão",
    "contas_irregulares_com_ressarcimento": "Contas julgadas irregulares (com ressarcimento)",
    "contas_com_ressalva_ou_multa_eleitoral": "Contas com ressalva ou multa eleitoral",
    "infracao_eleitoral_leve": "Infração eleitoral leve",
    "acusacao_anulada_ou_absolvida": "Acusação anulada ou absolvição",
    "citado_ou_apuracao_preliminar": "Citado ou em apuração preliminar",
    "acao_civil_dano_moral": "Ação cível por dano moral",
    "controversia_administrativa": "Controvérsia administrativa",
    "infracao_administrativa_ambiental": "Infração ambiental (autos do Ibama abaixo de R$ 1 mi)",
}
CURTO_QUADRANTE = {"LIBERTARIO": "Libertário", "DIREITA": "Direita conservadora", "ESQUERDA": "Esquerda progressista",
                   "AUTORITARIO": "Estatista-autoritário"}


def num(x, casas=None):
    """Número JSON-seguro (NaN vira None)."""
    if x is None or pd.isna(x):
        return None
    x = float(x)
    return round(x, casas) if casas is not None else x


def _achados(reg: dict) -> list:
    return [{"categoria": a["categoria"], "rotulo": ROTULO_ACHADO[a["categoria"]],
             "peso": PESOS_ACHADO[a["categoria"]] * a.get("quantidade", 1), "quantidade": a.get("quantidade", 1),
             "descricao": a["descricao"]} for a in reg.get("achados", [])]


def _apoiadores(reg: dict) -> list:
    saida = [{"nome": a["nome"], "partido": a.get("partido"), "ligacao": ROTULO_LIGACAO.get(a["tipo_ligacao"], a["tipo_ligacao"]),
              "detalhe": a.get("ligacao_detalhe"), "pendencia": a["pendencia"], "desconto": a["desconto"],
              "contado": a.get("contado", True)} for a in reg.get("apoiadores", [])]
    saida += [{"nome": None, "partido": None, "ligacao": "Chapa/partido", "detalhe": None, "pendencia": d["motivo"],
               "desconto": d["desconto"], "contado": True} for d in reg.get("descontos_adicionais", [])]
    return saida


def _carregar_bases_oficiais() -> dict:
    """sq_candidato -> base -> {resultado, n, itens, ref}, a partir de data/processed/verificacao_bases_oficiais.csv."""
    if not CSV_BASES_OFICIAIS.exists():
        print(f"Aviso: {CSV_BASES_OFICIAIS.name} não existe; rode `python -m pipeline.cruzar_bases_oficiais`. "
              "O site sairá sem a conferência em bases oficiais.")
        return {}
    df = pd.read_csv(CSV_BASES_OFICIAIS, dtype=str, encoding="utf-8-sig").fillna("")
    saida: dict = {}
    for (sq, base), g in df.groupby(["sq_candidato", "base"], sort=False):
        resultados = set(g.resultado)
        resultado = "consta" if "consta" in resultados else "a_confirmar" if "a_confirmar" in resultados else "nada_consta"
        itens = list(dict.fromkeys(d for d in g.detalhe if d))  # mantém a ordem (Ibama vem do maior valor)
        refs = [r for r in g.referencia if r]
        saida.setdefault(sq, {})[base] = {"resultado": resultado, "n": len(itens), "itens": itens[:4],
                                          "ref": refs[0] if refs else None}
    return saida


def _nivel_profundidade(prof: dict, cargo: str, uf: str, sq: str) -> str:
    if sq in prof.get("excecoes", {}):
        return prof["excecoes"][sq]
    for regra in prof["regras"]:
        if regra["cargo"] == cargo and ("ufs" not in regra or uf in regra["ufs"]):
            return regra["nivel"]
    return "rapida"


def _verificacao(prof: dict, bases_of: dict, cargo: str, uf: str, sq: str) -> dict:
    """Profundidade da pesquisa manual + conferência em bases oficiais (aparece ao eleitor, sem alterar a nota)."""
    do_candidato = bases_of.get(sq, {})
    bases = []
    if bases_of:  # sem o CSV, não afirma nada sobre bases oficiais
        for chave in BASES:
            b = do_candidato.get(chave)
            if not b:
                bases.append({"id": chave, "resultado": "nao_se_aplica"})
            elif b["resultado"] == "nada_consta":
                bases.append({"id": chave, "resultado": "nada_consta"})
            else:
                bases.append({"id": chave, "resultado": b["resultado"], "n": b["n"], "itens": b["itens"], "ref": b["ref"]})
    return {"nivel": _nivel_profundidade(prof, cargo, uf, sq), "bases": bases}


def _com_estrutural(manual: str, estrutural: str) -> dict:
    dados = json.loads((REF_DIR / manual).read_text(encoding="utf-8"))["candidatos"]
    caminho = config.PROCESSED_DIR / estrutural
    if caminho.exists():
        dados = {**json.loads(caminho.read_text(encoding="utf-8"))["candidatos"], **dados}
    return dados


def construir(df: pd.DataFrame) -> dict:
    prof = json.loads((REF_DIR / "profundidade_pesquisa.json").read_text(encoding="utf-8"))
    bases_of = _carregar_bases_oficiais()
    # JSONs manuais (data/reference) + registros estruturais de deputados (data/processed); o manual tem precedência
    idn = _com_estrutural("idoneidade.json", "estrutural_idoneidade.json")
    circ = _com_estrutural("circulo_politico.json", "estrutural_circulo_politico.json")
    grupos = {}
    for (cargo, uf), g in df.groupby(["cargo", "uf"]):
        n_aval = int(g["nota_idoneidade_geral"].notna().sum())
        entrada = {"cargo": cargo, "uf": uf, "n_total": len(g), "n_avaliados": n_aval, "corte": CORTE_POR_CARGO.get(cargo, CORTE_IDONEIDADE_PADRAO)}
        if n_aval == 0:
            entrada["status"] = "sem_verificacao"
            grupos[f"{cargo}|{uf}"] = entrada
            continue
        res = recomendar(df, cargo, uf)
        situ = {x["sq"]: (x["situacao"], x["etapa"], x["motivo"]) for x in res["removidos"]}
        recs = {r["sq"]: r for r in res["recomendados"]}
        nao_aval = set(res["nao_avaliados_sq"])
        candidatos = []
        for _, r in g.iterrows():
            sq = r["sq_candidato"]
            if sq in recs:
                situacao, etapa, motivo = "recomendado", None, None
            elif sq in situ:
                situacao, etapa, motivo = situ[sq]
            elif sq in nao_aval:
                situacao, etapa, motivo = "nao_avaliado", "sem idoneidade geral pesquisada", None
            else:
                situacao, etapa, motivo = "segue", None, None
            ri, rc = idn.get(sq, {}), circ.get(sq, {})
            candidatos.append({
                "sq": sq, "nome_urna": r["nome_urna"], "nome_completo": r["nome_completo"], "partido": r["partido"],
                "numero": r["numero"], "situacao": situacao, "etapa": etapa, "motivo_saida": motivo,
                "idoneidade_pessoal": num(r["nota_idoneidade"]), "circulo": num(r["nota_circulo_politico"]),
                "idoneidade_geral": num(r["nota_idoneidade_geral"], 2), "competencia_geral": num(r["nota_competencia_geral"], 2),
                "qualificacao_geral": num(r["nota_qualificacao_geral"], 2),
                "competencia": num(r["nota_competencia"], 2), "escolaridade": num(r["nota_escolaridade"], 2),
                "eco": num(r["eco_final"], 2), "pes": num(r["pes_final"], 2), "posicao_fonte": r["posicao_fonte"],
                "nivel_eco": r["nivel_eixo_economico"] if pd.notna(r["nivel_eixo_economico"]) else "c",
                "nivel_pes": r["nivel_eixo_pessoal"] if pd.notna(r["nivel_eixo_pessoal"]) else "c",
                "quadrante": r["quadrante"], "fronteira": bool(r["fronteira"]), "camadas": int(r["camadas_pesquisadas"]),
                "cobertura": r["cobertura_pesquisa"],
                "achados": _achados(ri), "apoiadores": _apoiadores(rc),
                "fontes": list(dict.fromkeys(ri.get("fontes", []) + rc.get("fontes", []))),
                "verificacao": _verificacao(prof, bases_of, cargo, uf, sq),
                "empate": recs[sq]["empatados_na_ultima_vaga"] if sq in recs else 0,
            })
        candidatos.sort(key=lambda c: (c["idoneidade_geral"] is None, -(c["idoneidade_geral"] or 0), c["nome_urna"]))
        entrada.update({"status": "completo" if n_aval == len(g) else "parcial", "candidatos": candidatos,
                        "recomendados": [r["sq"] for r in res["recomendados"]]})
        grupos[f"{cargo}|{uf}"] = entrada
    return {
        "meta": {"gerado_em": date.today().isoformat(), "corte": CORTE_IDONEIDADE_PADRAO, "corte_deputados": max(CORTE_POR_CARGO.values()), "limiar": LIMIAR_QUADRANTE,
                 "margem_fronteira": MARGEM_FRONTEIRA, "politica_nao_avaliados": "excluir", "data_eleicao": "2026-10-04",
                 "total_candidatos": int(len(df))},
        "profundidade": prof["niveis"],
        "bases_oficiais": [{"id": k, "rotulo": r, "data": d} for k, (r, d) in BASES.items()],
        "quadrantes": [{"chave": k, "nome": v, "curto": CURTO_QUADRANTE[k]} for k, v in NOME_QUADRANTE.items()],
        "cargos": [{"codigo": c, "rotulo": ROTULO_CARGO[c], "vagas": VAGAS_POR_QUADRANTE[c]} for c in ROTULO_CARGO],
        "grupos": grupos,
    }


# Campos de candidato cujo valor se repete entre milhares de candidatos (mesmo partido, mesma conferência em bases).
CAMPOS_DEDUPLICADOS = ("apoiadores", "fontes", "verificacao", "cobertura", "posicao_fonte")
TAMANHO_MINIMO_DEDUP = 12  # não vale trocar por índice um valor menor que isto (ex.: "[]")


def deduplicar(dados: dict) -> dict:
    """Guarda uma vez só (em dados['tabelas']) os valores repetidos de CAMPOS_DEDUPLICADOS e deixa no candidato o
    índice. O site (`expandirTabelas` em app.js) devolve cada índice ao valor original ao carregar; quem lê o
    JSON por fora deve fazer o mesmo. Valores que aparecem uma vez, ou pequenos, ficam no próprio candidato."""
    candidatos = [c for g in dados["grupos"].values() for c in g.get("candidatos", [])]
    ser = lambda v: json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    contagem = {campo: Counter(ser(c[campo]) for c in candidatos if campo in c) for campo in CAMPOS_DEDUPLICADOS}
    tabelas, indices = {}, {}
    for campo in CAMPOS_DEDUPLICADOS:
        # mais frequentes primeiro: índices menores (menos caracteres) para os valores mais usados
        comuns = [v for v, n in contagem[campo].most_common() if n >= 2 and len(v) > TAMANHO_MINIMO_DEDUP]
        indices[campo] = {v: i for i, v in enumerate(comuns)}
        tabelas[campo] = [json.loads(v) for v in comuns]
    for c in candidatos:
        for campo in CAMPOS_DEDUPLICADOS:
            if campo in c and ser(c[campo]) in indices[campo]:
                c[campo] = indices[campo][ser(c[campo])]
    dados["tabelas"] = tabelas
    return dados


def dividir_por_grupo(dados: dict) -> tuple:
    """Separa `dados` em (índice, {arquivo relativo: texto}). O índice (site/dados.js) fica leve: metadados, contagens e
    status de cada grupo, tabelas de valores repetidos. Cada cargo/UF com candidatos vira um arquivo próprio
    (site/dados/<cargo>_<uf>.js) que o site baixa só quando o eleitor escolhe aquele grupo."""
    arquivos, indice = {}, dict(dados)
    indice["grupos"] = {}
    for chave, g in dados["grupos"].items():
        if "candidatos" not in g:
            indice["grupos"][chave] = g
            continue
        nome = f"dados/{g['cargo'].lower().replace(' ', '_')}_{g['uf'].lower()}.js"
        corpo = {"candidatos": g["candidatos"], "recomendados": g["recomendados"]}
        arquivos[nome] = ("window.GRUPOS_CARREGADOS = window.GRUPOS_CARREGADOS || {};\nwindow.GRUPOS_CARREGADOS["
                          + json.dumps(chave) + "] = " + json.dumps(corpo, ensure_ascii=False, separators=(",", ":")) + ";\n")
        indice["grupos"][chave] = {k: v for k, v in g.items() if k not in corpo} | {"arquivo": nome}
    # versão do conteúdo: o site a põe na URL de cada arquivo (?v=), para ninguém ficar com um grupo antigo em cache
    resumo = hashlib.sha1(json.dumps(indice, sort_keys=True, ensure_ascii=False).encode())
    for nome in sorted(arquivos):
        resumo.update(arquivos[nome].encode())
    indice["versao"] = resumo.hexdigest()[:10]
    return indice, arquivos


def main() -> None:
    df = preparar(pd.read_parquet(INPUT_PATH))
    indice, arquivos = dividir_por_grupo(deduplicar(construir(df)))
    texto = ("// Gerado por pipeline/exportar_prototipo.py -- não editar à mão. Índice: cada cargo/UF tem o seu arquivo em dados/.\n"
             "const DADOS = " + json.dumps(indice, ensure_ascii=False, indent=1) + ";\n")
    for saida in SAIDAS:
        pasta = saida.parent / "dados"
        shutil.rmtree(pasta, ignore_errors=True)  # o exportador é o dono desta pasta: não sobram grupos antigos
        pasta.mkdir(parents=True, exist_ok=True)
        saida.write_text(texto, encoding="utf-8", newline="\n")
        for nome, corpo in arquivos.items():
            (saida.parent / nome).write_text(corpo, encoding="utf-8", newline="\n")
    verif = [k for k, v in indice["grupos"].items() if v["status"] != "sem_verificacao"]
    print(f"{len(indice['grupos'])} grupos cargo/UF; {len(verif)} com verificação (versão {indice['versao']})")
    for saida in SAIDAS:
        tam = [(saida.parent / n).stat().st_size for n in arquivos]
        print(f"Índice {saida} ({saida.stat().st_size / 1024:.0f} KB) + {len(arquivos)} arquivos em dados/ "
              f"(soma {sum(tam) / 1e6:.1f} MB, maior {max(tam) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
