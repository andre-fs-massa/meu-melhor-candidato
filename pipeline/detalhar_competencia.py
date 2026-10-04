"""Explica, frente a frente, de onde veio a nota de competência de cada candidato (para o painel do site).

A nota de cada uma das 4 competências do cargo (pipeline/competencias.py) é a MAIOR entre (pipeline/pesos_competencia.py):
  - "c": mandato no mesmo poder do cargo pretendido (pipeline/enriquecer_experiencia.py);
  - "x": mandato no outro poder, que transfere em parte (idem);
  - "p": experiência profissional pesquisada, com motivo escrito (pipeline/enriquecer_competencia_transferivel.py);
  - "o": ocupação declarada ao TSE, pela matriz de competências por profissão (pipeline/mapear_competencias.py).
Aqui as fontes são recalculadas e a vencedora é conferida contra a coluna score_<competência> já gravada no parquet;
divergência vira aviso (sinal de que o pipeline e esta explicação saíram de sincronia).

Em empate, mostra a fonte mais informativa: mandato antes da ocupação; a pesquisa profissional só aparece quando subiu
a nota (é a mesma regra da etapa que a aplica).
"""
import json

import pandas as pd

from . import competencia_dimensoes as cd
from . import competencias
from .enriquecer_competencia_transferivel import REFERENCE_PATH as REF_PROFISSIONAL
from .enriquecer_experiencia import cargos_exercidos, carregar_referencia
from .pesos_competencia import FATOR_OCUPACAO, FATOR_PESQUISA, notas_por_mandatos

ROTULO_CARGO_ANTERIOR = {
    "PRESIDENTE": "Presidente", "GOVERNADOR": "Governador", "VICE-GOVERNADOR": "Vice-governador",
    "PREFEITO": "Prefeito", "VICE-PREFEITO": "Vice-prefeito", "SENADOR": "Senador",
    "DEPUTADO FEDERAL": "Deputado federal", "DEPUTADO ESTADUAL": "Deputado estadual",
    "DEPUTADO DISTRITAL": "Deputado distrital", "VEREADOR": "Vereador",
}


def rotulos_por_cargo() -> dict:
    """cargo -> nomes curtos das 4 frentes, na ordem usada em `detalhar` (vai uma vez só no índice do site)."""
    return {cargo: [rotulo for rotulo, _ in comp.values()] for cargo, comp in competencias.COMPETENCIAS_POR_CARGO.items()}


def _texto_mandato(cargo: str, registro: dict | None) -> str:
    texto = ROTULO_CARGO_ANTERIOR.get(cargo, cargo.capitalize())
    do_cargo = [c for c in (registro or {}).get("cargos_anteriores", []) if c["cargo"] == cargo]
    if not do_cargo:  # veio do título declarado como ocupação
        return texto + " (ocupação declarada ao TSE; mandato não localizado nos registros)"
    extra = ", ".join(x for x in (do_cargo[-1].get("local"), do_cargo[-1].get("periodo")) if x and x != "?")
    return texto + (f" ({extra})" if extra else "")


class Detalhador:
    def __init__(self):
        self.experiencia = carregar_referencia()["candidatos"]
        self.profissional = json.loads(REF_PROFISSIONAL.read_text(encoding="utf-8"))["candidatos"]
        self.divergencias = []

    def detalhar(self, r: pd.Series) -> list | None:
        """Lista [nota, fonte, texto] por frente, na ordem de COMPETENCIAS_POR_CARGO[cargo]. Para a fonte "o" o texto
        fica vazio (o site usa a ocupação do candidato, exportada uma vez só)."""
        cargo, sq = r["cargo"], r["sq_candidato"]
        if cargo not in competencias.COMPETENCIAS_POR_CARGO:
            return None
        arquetipo = cd.classificar_ocupacao(r["ocupacao"])
        matriz = cd.ARQUETIPOS["generico" if arquetipo.startswith("politico_") else arquetipo]
        registro = self.experiencia.get(sq)
        mandatos = notas_por_mandatos(cargo, cargos_exercidos(registro, r["ocupacao"]))
        prof = self.profissional.get(sq, {}).get("competencias", {})
        frentes = []
        for chave, (v_mandato, exercido, mesmo) in zip(competencias.COMPETENCIAS_POR_CARGO[cargo], mandatos):
            nota, fonte, texto = FATOR_OCUPACAO * matriz[cd.CARGO_COMPETENCIA_DIMENSAO[cargo][chave]], "o", ""
            if exercido and v_mandato >= nota:
                nota, fonte, texto = v_mandato, "c" if mesmo else "x", _texto_mandato(exercido, registro)
            if chave in prof and FATOR_PESQUISA * prof[chave]["nota"] > nota:
                nota, fonte, texto = FATOR_PESQUISA * prof[chave]["nota"], "p", prof[chave]["motivo"]
            gravado = r.get(f"score_{chave}")
            if gravado is not None and not pd.isna(gravado) and abs(float(gravado) - nota) > 1e-9:
                self.divergencias.append(f"{r['nome_urna']} ({cargo}) {chave}: explicação {nota} x parquet {gravado}")
            frentes.append([round(nota, 2), fonte, texto])
        return frentes


def texto_ocupacao(ocupacao) -> str | None:
    return ocupacao.capitalize() if isinstance(ocupacao, str) and ocupacao else None


def texto_escolaridade(escolaridade) -> str | None:
    return escolaridade.capitalize() if isinstance(escolaridade, str) and escolaridade else None
