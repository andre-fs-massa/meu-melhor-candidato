"""Explica, frente a frente, de onde veio a nota de competência de cada candidato (para o painel do site).

A nota de cada uma das 4 competências do cargo (pipeline/competencias.py) é a MAIOR entre três fontes:
  - "o": ocupação declarada ao TSE (proxy por arquétipo, pipeline/mapear_competencias.py);
  - "c": cargo eletivo já exercido (pipeline/enriquecer_experiencia.py);
  - "p": experiência profissional pesquisada, com motivo escrito (pipeline/enriquecer_competencia_transferivel.py).
Aqui as três são recalculadas e a vencedora é conferida contra a coluna score_<competência> já gravada no parquet;
divergência vira aviso (sinal de que o pipeline e esta explicação saíram de sincronia).

Em empate, mostra a fonte mais informativa: cargo exercido antes da ocupação; a pesquisa profissional só aparece
quando subiu a nota (é a mesma regra da etapa que a aplica).
"""
import json

import pandas as pd

from . import competencia_dimensoes as cd
from . import competencias
from .enriquecer_competencia_transferivel import REFERENCE_PATH as REF_PROFISSIONAL
from .enriquecer_experiencia import BOOST_POR_CARGO_ANTERIOR, carregar_referencia

ROTULO_CARGO_ANTERIOR = {
    "PRESIDENTE": "Presidente", "GOVERNADOR": "Governador", "PREFEITO": "Prefeito", "SENADOR": "Senador",
    "DEPUTADO FEDERAL": "Deputado federal", "DEPUTADO ESTADUAL": "Deputado estadual",
    "DEPUTADO DISTRITAL": "Deputado distrital", "VEREADOR": "Vereador",
}


def rotulos_por_cargo() -> dict:
    """cargo -> nomes curtos das 4 frentes, na ordem usada em `detalhar` (vai uma vez só no índice do site)."""
    return {cargo: [rotulo for rotulo, _ in comp.values()] for cargo, comp in competencias.COMPETENCIAS_POR_CARGO.items()}


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
        proxy = cd.ARQUETIPOS[cd.classificar_ocupacao(r["ocupacao"])]
        cargos_ant = self.experiencia.get(sq, {}).get("cargos_anteriores", []) if sq in self.experiencia else []
        prof = self.profissional.get(sq, {}).get("competencias", {})
        frentes = []
        for chave in competencias.COMPETENCIAS_POR_CARGO[cargo]:
            dim = cd.CARGO_COMPETENCIA_DIMENSAO[cargo][chave]
            nota, fonte, texto = proxy[dim], "o", ""
            # cargo exercido que dá a maior nota nesta dimensão (empate com a ocupação: mostra o cargo)
            melhor = max(cargos_ant, key=lambda c: BOOST_POR_CARGO_ANTERIOR.get(c["cargo"], {}).get(dim, -1), default=None)
            if melhor is not None:
                v = BOOST_POR_CARGO_ANTERIOR.get(melhor["cargo"], {}).get(dim)
                if v is not None and v >= nota and v > 0:
                    nota, fonte = v, "c"
                    texto = ROTULO_CARGO_ANTERIOR.get(melhor["cargo"], melhor["cargo"].capitalize())
                    extra = ", ".join(x for x in (melhor.get("local"), melhor.get("periodo")) if x and x != "?")
                    texto += f" ({extra})" if extra else ""
            if chave in prof and prof[chave]["nota"] > nota:
                nota, fonte, texto = prof[chave]["nota"], "p", prof[chave]["motivo"]
            gravado = r.get(f"score_{chave}")
            if gravado is not None and not pd.isna(gravado) and abs(float(gravado) - nota) > 1e-9:
                self.divergencias.append(f"{r['nome_urna']} ({cargo}) {chave}: explicação {nota} x parquet {gravado}")
            frentes.append([nota, fonte, texto])
        return frentes


def texto_ocupacao(ocupacao) -> str | None:
    return ocupacao.capitalize() if isinstance(ocupacao, str) and ocupacao else None


def texto_escolaridade(escolaridade) -> str | None:
    return escolaridade.capitalize() if isinstance(escolaridade, str) and escolaridade else None
