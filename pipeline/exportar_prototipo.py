"""Exporta os dados do protótipo do eleitor (prototipo/dados.js) a partir do funil de recomendação.

Uma única fonte da verdade: as recomendações vêm de `pipeline.recomendar.recomendar`, com o corte e a
política de não avaliados padrão (corte 6,0; só recomenda quem tem idoneidade geral verificada). Para cada
cargo/UF com pelo menos um candidato verificado, exporta TODOS os candidatos com a situação de cada um
(fora da disputa, abaixo do corte, segue, recomendado) e os motivos estruturados das notas. Cargo/UF sem
nenhum candidato verificado exporta só as contagens, e a página mostra "ainda sem verificação".

Uso: python -m pipeline.exportar_prototipo
"""
import json
from datetime import date

import pandas as pd

from . import config
from .enriquecer_circulo_politico import ROTULO_LIGACAO
from .pesos import PESOS_ACHADO
from .recomendar import (
    CORTE_IDONEIDADE_PADRAO, INPUT_PATH, LIMIAR_QUADRANTE, MARGEM_FRONTEIRA, NOME_QUADRANTE, REF_DIR,
    VAGAS_POR_QUADRANTE, preparar, recomendar,
)

SAIDA = config.RAW_DIR.parent.parent / "prototipo" / "dados.js"
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


def construir(df: pd.DataFrame) -> dict:
    idn = json.loads((REF_DIR / "idoneidade.json").read_text(encoding="utf-8"))["candidatos"]
    circ = json.loads((REF_DIR / "circulo_politico.json").read_text(encoding="utf-8"))["candidatos"]
    grupos = {}
    for (cargo, uf), g in df.groupby(["cargo", "uf"]):
        n_aval = int(g["nota_idoneidade_geral"].notna().sum())
        entrada = {"cargo": cargo, "uf": uf, "n_total": len(g), "n_avaliados": n_aval}
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
                "competencia": num(r["nota_competencia"], 2), "escolaridade": num(r["nota_escolaridade"], 2),
                "eco": num(r["eco_final"], 2), "pes": num(r["pes_final"], 2), "posicao_fonte": r["posicao_fonte"],
                "nivel_eco": r["nivel_eixo_economico"] if pd.notna(r["nivel_eixo_economico"]) else "c",
                "nivel_pes": r["nivel_eixo_pessoal"] if pd.notna(r["nivel_eixo_pessoal"]) else "c",
                "quadrante": r["quadrante"], "fronteira": bool(r["fronteira"]), "camadas": int(r["camadas_pesquisadas"]),
                "cobertura": r["cobertura_pesquisa"],
                "achados": _achados(ri), "apoiadores": _apoiadores(rc),
                "fontes": list(dict.fromkeys(ri.get("fontes", []) + rc.get("fontes", []))),
                "empate": recs[sq]["empatados_na_ultima_vaga"] if sq in recs else 0,
            })
        candidatos.sort(key=lambda c: (c["idoneidade_geral"] is None, -(c["idoneidade_geral"] or 0), c["nome_urna"]))
        entrada.update({"status": "completo" if n_aval == len(g) else "parcial", "candidatos": candidatos,
                        "recomendados": [r["sq"] for r in res["recomendados"]]})
        grupos[f"{cargo}|{uf}"] = entrada
    return {
        "meta": {"gerado_em": date.today().isoformat(), "corte": CORTE_IDONEIDADE_PADRAO, "limiar": LIMIAR_QUADRANTE,
                 "margem_fronteira": MARGEM_FRONTEIRA, "politica_nao_avaliados": "excluir", "data_eleicao": "2026-10-04",
                 "total_candidatos": int(len(df))},
        "quadrantes": [{"chave": k, "nome": v, "curto": CURTO_QUADRANTE[k]} for k, v in NOME_QUADRANTE.items()],
        "cargos": [{"codigo": c, "rotulo": ROTULO_CARGO[c], "vagas": VAGAS_POR_QUADRANTE[c]} for c in ROTULO_CARGO],
        "grupos": grupos,
    }


def main() -> None:
    df = preparar(pd.read_parquet(INPUT_PATH))
    dados = construir(df)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("// Gerado por pipeline/exportar_prototipo.py -- não editar à mão.\nconst DADOS = "
                     + json.dumps(dados, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    verif = [k for k, v in dados["grupos"].items() if v["status"] != "sem_verificacao"]
    print(f"{len(dados['grupos'])} grupos cargo/UF; {len(verif)} com verificação: {', '.join(verif)}")
    print(f"Salvo em {SAIDA} ({SAIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
