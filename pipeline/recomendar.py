"""Funil de recomendação: do universo de candidatos ao 'melhor candidato' por quadrante.

Passo a passo (ver docs/funil_recomendacao.md):
  0. Remover quem está fora da disputa (registro indeferido ou inelegibilidade vigente).
  1. Filtrar pela idoneidade geral (`nota_idoneidade_geral`): sai quem tem nota abaixo do corte.
  2. Classificar cada candidato num quadrante do diagrama de Nolan (eixo econômico x eixo pessoal).
  3. Em cada quadrante, escolher por `nota_qualificacao_geral` (média simples de `nota_competencia_geral`
     e `nota_idoneidade_geral`, decisão do usuário em 2026-09-22 -- antes era só competência geral, com
     idoneidade geral entrando apenas como desempate):
       - Presidente, Governador, Senador: 1 candidato por quadrante;
       - Deputados (federal, estadual, distrital): 3 por quadrante, para o eleitor escolher.

Decisões de desenho (todas parametrizáveis e listadas na saída):
  * Quem NÃO tem idoneidade geral pesquisada não pode ser filtrado. Se passasse direto, ser pesquisado
    viraria desvantagem (só os pesquisados podem ser reprovados). Por padrão, portanto, só quem foi
    avaliado pode ser recomendado (`nao_avaliados="excluir"`); os demais aparecem numa lista à parte.
  * Posição no diagrama: pesquisa individual quando existe; sem ela, o baseline do PARTIDO
    (regra do fallback), marcado como tal. Perto do centro (+-0,5) o candidato é marcado 'fronteira'.
  * Empate na última vaga de um quadrante: desempate por competência geral (a metade "menos redundante"
    da qualificação geral), idoneidade geral, competência bruta e escolaridade; se ainda empatar, sorteio
    com semente fixa (reprodutível), e o tamanho do empate é informado. Nenhum candidato é favorecido por
    ordem alfabética.
"""
import argparse
import json
import random
import sys

import pandas as pd

from . import config

INPUT_PATH = (
    config.PROCESSED_DIR / f"candidatos_{config.ANO_ELEICAO}_competencias_enriquecido.parquet"
)
REF_DIR = config.RAW_DIR.parent / "reference"
OUTPUT_CSV = config.PROCESSED_DIR / f"recomendacoes_{config.ANO_ELEICAO}.csv"

CORTE_IDONEIDADE_PADRAO = 6.0  # definido pelo usuário em 2026-09-21; a recomendação é muito sensível a ele
# Deputados têm corte próprio (2026-09-24, decisão do usuário): a nota deles vem de bases oficiais e do partido,
# sem pesquisa individual na web, então o corte é mais alto (8,0 e depois 8,5 no mesmo dia). Como o círculo de um
# deputado é só o presidente do partido, com círculo 6 (PL, DC) a idoneidade geral máxima é 8,0: o partido inteiro cai.
CORTE_POR_CARGO = {"DEPUTADO FEDERAL": 8.5, "DEPUTADO ESTADUAL": 8.5, "DEPUTADO DISTRITAL": 8.5}


def corte_do_cargo(cargo: str) -> float:
    return CORTE_POR_CARGO.get(cargo, CORTE_IDONEIDADE_PADRAO)
LIMIAR_QUADRANTE = 5.0
MARGEM_FRONTEIRA = 0.5
SEMENTE_PADRAO = 2026
VAGAS_POR_QUADRANTE = {
    "PRESIDENTE": 1,
    "GOVERNADOR": 1,
    "SENADOR": 1,
    "DEPUTADO FEDERAL": 3,
    "DEPUTADO ESTADUAL": 3,
    "DEPUTADO DISTRITAL": 3,
}
NOME_QUADRANTE = {
    "LIBERTARIO": "Libertário (economia livre, costumes liberais)",
    "DIREITA": "Direita conservadora (economia livre, costumes conservadores)",
    "ESQUERDA": "Esquerda progressista (mais Estado na economia, costumes liberais)",
    "AUTORITARIO": "Estatista-autoritário (mais Estado na economia, costumes conservadores)",
}
# Achados de idoneidade que tiram o candidato da disputa (registro indeferido ou inelegível)
CATEGORIAS_FORA_DA_DISPUTA = {"registro_indeferido", "inelegibilidade_vigente"}


def quadrante(eco: float, pessoal: float) -> str:
    if eco >= LIMIAR_QUADRANTE:
        return "LIBERTARIO" if pessoal >= LIMIAR_QUADRANTE else "DIREITA"
    return "ESQUERDA" if pessoal >= LIMIAR_QUADRANTE else "AUTORITARIO"


def carregar_fora_da_disputa() -> dict:
    """sq_candidato -> motivo, para quem tem achado de registro indeferido ou inelegibilidade vigente."""
    caminho = REF_DIR / "idoneidade.json"
    if not caminho.exists():
        return {}
    dados = json.loads(caminho.read_text(encoding="utf-8"))["candidatos"]
    saida = {}
    for sq, reg in dados.items():
        for a in reg.get("achados", []):
            if a["categoria"] in CATEGORIAS_FORA_DA_DISPUTA:
                saida[sq] = f"{a['categoria']}: {a['descricao']}"
                break
    return saida


CHAVE_PESSOA = ["nome_completo", "cargo", "uf", "numero", "partido"]


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta posição final no diagrama (individual ou do partido), quadrante e flag de fronteira.

    Também remove pessoas registradas duas vezes no arquivo do TSE (mesmo nome completo, cargo, UF,
    número e partido, com `sq_candidato` diferentes -- ex.: 17 casos em 2026), para não recomendar
    a mesma pessoa em duplicidade. Fica o registro com mais camadas pesquisadas e, no empate, o mais recente.
    O dataset original não é alterado."""
    ideologia = json.loads((REF_DIR / "ideologia_partidaria.json").read_text(encoding="utf-8"))["partidos"]
    # Espaços repetidos no nome não distinguem pessoas (ex.: "MENDONÇA  ALVES" no registro duplicado de AL).
    chave = df[CHAVE_PESSOA].assign(nome_completo=df["nome_completo"].str.split().str.join(" "))
    ordem = df.sort_values(["camadas_pesquisadas", "sq_candidato"], ascending=[False, False]).index
    df = df.loc[ordem][~chave.loc[ordem].duplicated(keep="first")]
    base_eco = df["partido"].map(lambda p: ideologia[p]["eixo_economico"])
    base_pes = df["partido"].map(lambda p: ideologia[p]["eixo_pessoal"])
    df["eco_final"] = df["eixo_economico"].fillna(base_eco)
    df["pes_final"] = df["eixo_pessoal"].fillna(base_pes)
    df["posicao_fonte"] = df["eixo_economico"].notna().map({True: "pesquisa individual", False: "baseline do partido"})
    df["quadrante"] = [quadrante(e, p) for e, p in zip(df["eco_final"], df["pes_final"])]
    df["fronteira"] = ((df["eco_final"] - LIMIAR_QUADRANTE).abs() < MARGEM_FRONTEIRA) | (
        (df["pes_final"] - LIMIAR_QUADRANTE).abs() < MARGEM_FRONTEIRA
    )
    fora = carregar_fora_da_disputa()
    df["fora_da_disputa"] = df["sq_candidato"].map(fora)
    df["nota_qualificacao_geral"] = (df["nota_competencia_geral"] + df["nota_idoneidade_geral"]) / 2
    return df


def _escolher(grupo: pd.DataFrame, vagas: int, semente: int):
    """Escolhe `vagas` candidatos por qualificação geral (média de competência geral e idoneidade geral),
    com desempate explícito. Devolve (escolhidos, empatados_na_ultima_vaga)."""
    chaves = ["nota_qualificacao_geral", "nota_competencia_geral", "nota_idoneidade_geral", "nota_competencia", "nota_escolaridade"]
    g = grupo.copy()
    for c in chaves:
        g[f"_k_{c}"] = g[c].fillna(-1).round(6)
    g["_chave"] = list(zip(*[g[f"_k_{c}"] for c in chaves]))
    rng = random.Random(f"{semente}:{grupo['quadrante'].iloc[0]}:{grupo['uf'].iloc[0]}:{grupo['cargo'].iloc[0]}")
    escolhidos, restante, empate_ultima = [], vagas, 0
    for chave in sorted(g["_chave"].unique(), reverse=True):
        bloco = g[g["_chave"] == chave]
        if len(bloco) <= restante:
            escolhidos.append(bloco)
            restante -= len(bloco)
        else:
            indices = list(bloco.index)
            rng.shuffle(indices)
            escolhidos.append(bloco.loc[indices[:restante]])
            empate_ultima = len(bloco)
            restante = 0
        if restante == 0:
            break
    return pd.concat(escolhidos), empate_ultima


def recomendar(
    df: pd.DataFrame,
    cargo: str,
    uf: str,
    corte: float = None,
    nao_avaliados: str = "excluir",
    semente: int = SEMENTE_PADRAO,
) -> dict:
    """Roda o funil para um cargo e uma UF ('BR' para Presidente). `df` já passou por `preparar`.
    `corte=None` usa o corte do cargo (`corte_do_cargo`); um valor explícito vale para qualquer cargo."""
    assert nao_avaliados in ("excluir", "manter_sinalizado")
    corte = corte_do_cargo(cargo) if corte is None else corte
    universo = df[(df["cargo"] == cargo) & (df["uf"] == uf)]
    resultado = {"cargo": cargo, "uf": uf, "corte": corte, "nao_avaliados": nao_avaliados,
                 "n_inicial": len(universo), "removidos": [], "recomendados": []}

    fora = universo[universo["fora_da_disputa"].notna()]
    for _, r in fora.iterrows():
        resultado["removidos"].append({"sq": r["sq_candidato"], "nome": r["nome_urna"], "etapa": "etapa 0: fora da disputa",
                                       "situacao": "fora_da_disputa", "motivo": r["fora_da_disputa"]})
    universo = universo[universo["fora_da_disputa"].isna()]
    resultado["apos_etapa_0"] = len(universo)

    reprovados = universo[universo["nota_idoneidade_geral"].notna() & (universo["nota_idoneidade_geral"] < corte)]
    for _, r in reprovados.iterrows():
        resultado["removidos"].append({"sq": r["sq_candidato"], "nome": r["nome_urna"],
                                       "etapa": "etapa 1: idoneidade geral abaixo do corte", "situacao": "abaixo_do_corte",
                                       "motivo": f"{r['nota_idoneidade_geral']:.1f} < {corte:g}"})
    universo = universo.drop(reprovados.index)

    sem_nota = universo[universo["nota_idoneidade_geral"].isna()]
    resultado["nao_avaliados_lista"] = list(sem_nota["nome_urna"])
    resultado["nao_avaliados_sq"] = list(sem_nota["sq_candidato"])
    if nao_avaliados == "excluir":
        universo = universo.drop(sem_nota.index)
    resultado["apos_etapa_1"] = len(universo)

    vagas = VAGAS_POR_QUADRANTE[cargo]
    for q in NOME_QUADRANTE:
        grupo = universo[universo["quadrante"] == q]
        if grupo.empty:
            continue
        escolhidos, empate = _escolher(grupo, vagas, semente)
        for _, r in escolhidos.iterrows():
            resultado["recomendados"].append({
                "quadrante": q, "sq": r["sq_candidato"], "nome_urna": r["nome_urna"], "partido": r["partido"], "numero": r["numero"],
                "idoneidade_geral": r["nota_idoneidade_geral"], "competencia_geral": r["nota_competencia_geral"],
                "qualificacao_geral": r["nota_qualificacao_geral"],
                "posicao": f"({r['eco_final']:.1f}; {r['pes_final']:.1f}) {r['posicao_fonte']}",
                "fronteira": bool(r["fronteira"]), "camadas_pesquisadas": int(r["camadas_pesquisadas"]),
                "avaliado_em_idoneidade": pd.notna(r["nota_idoneidade_geral"]),
                "candidatos_no_quadrante": len(grupo), "empatados_na_ultima_vaga": empate,
            })
    return resultado


def formatar(res: dict) -> str:
    L = [f"== {res['cargo']} / {res['uf']} == corte de idoneidade geral: {res['corte']} | não avaliados: {res['nao_avaliados']}",
         f"Candidatos: {res['n_inicial']} -> após etapa 0 (fora da disputa): {res['apos_etapa_0']} -> após etapa 1 (idoneidade): {res['apos_etapa_1']}"]
    if res["removidos"]:
        L.append("Removidos:")
        L += [f"  - {x['nome']} [{x['etapa']}] {x['motivo'][:110]}" for x in res["removidos"]]
    if res["nao_avaliados_lista"]:
        L.append(f"Sem idoneidade geral pesquisada ({len(res['nao_avaliados_lista'])}): " + ", ".join(res["nao_avaliados_lista"][:12])
                 + (" ..." if len(res["nao_avaliados_lista"]) > 12 else ""))
    if not res["recomendados"]:
        L.append("Nenhum candidato recomendável com estes critérios.")
    for q in NOME_QUADRANTE:
        rs = [r for r in res["recomendados"] if r["quadrante"] == q]
        if not rs:
            L.append(f"[{NOME_QUADRANTE[q]}] -- nenhum candidato neste quadrante")
            continue
        L.append(f"[{NOME_QUADRANTE[q]}] ({rs[0]['candidatos_no_quadrante']} elegíveis)")
        for r in rs:
            idg = "n/d" if pd.isna(r["idoneidade_geral"]) else f"{r['idoneidade_geral']:.1f}"
            flags = []
            if r["fronteira"]:
                flags.append("FRONTEIRA")
            if not r["avaliado_em_idoneidade"]:
                flags.append("SEM IDONEIDADE")
            if r["empatados_na_ultima_vaga"]:
                flags.append(f"sorteado entre {r['empatados_na_ultima_vaga']} empatados")
            L.append(f"  * {r['nome_urna']} ({r['partido']} {r['numero']}) qualificação geral {r['qualificacao_geral']:.2f} "
                     f"(idoneidade {idg} | competência {r['competencia_geral']:.2f}) | "
                     f"posição {r['posicao']} | {r['camadas_pesquisadas']}/5 camadas" + (f" | {', '.join(flags)}" if flags else ""))
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cargo", default="PRESIDENTE")
    ap.add_argument("--uf", default="BR")
    ap.add_argument("--corte", type=float, default=None, help="vale para qualquer cargo; sem ele, cada cargo usa o seu (deputados 8, demais 6)")
    ap.add_argument("--nao-avaliados", choices=["excluir", "manter_sinalizado"], default="excluir")
    ap.add_argument("--csv", action="store_true", help="grava as recomendações de TODOS os cargos/UFs em data/processed")
    a = ap.parse_args()
    if not INPUT_PATH.exists():
        sys.exit("Rode o pipeline completo primeiro (até calcular_cobertura).")
    df = preparar(pd.read_parquet(INPUT_PATH))
    if a.csv:
        linhas = []
        for (cargo, uf), _ in df.groupby(["cargo", "uf"]):
            res = recomendar(df, cargo, uf, a.corte, a.nao_avaliados)
            linhas += [{"cargo": cargo, "uf": uf, "corte": res["corte"], "nao_avaliados": a.nao_avaliados, **r} for r in res["recomendados"]]
        pd.DataFrame(linhas).to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
        print(f"{len(linhas)} recomendações em {OUTPUT_CSV}")
        return
    print(formatar(recomendar(df, a.cargo.upper(), a.uf.upper(), a.corte, a.nao_avaliados)))


if __name__ == "__main__":
    main()
