"""Tabela única de pesos da nota de competência no cargo (decisão do usuário de 04/10/2026).

Princípio: a nota mede as competências transferíveis que o candidato acumulou. Para cada uma das 4 frentes do
cargo pretendido (pipeline/competencias.py), vale a MAIOR entre três fontes:

  1. Experiência pública no MESMO poder do cargo pretendido (Executivo ou Legislativo): quem já exerceu já pôs em
     prática as habilidades do cargo, então vale igual nas 4 frentes, conforme a esfera (NOTA_POR_DISTANCIA_ESFERA).
  2. Experiência pública no OUTRO poder: a mesma tabela, multiplicada pelo quanto cada frente se transfere
     (TRANSFERENCIA_OUTRO_PODER), com teto TETO_OUTRO_PODER para nunca igualar quem exerceu o mesmo poder.
  3. Experiência profissional: a matriz de competências por profissão (pipeline/competencia_dimensoes.py) × FATOR_OCUPACAO
     ou, quando a biografia foi pesquisada, a nota pesquisada × FATOR_PESQUISA. Os fatores mantêm a profissão abaixo
     da experiência pública no mesmo poder.

A nota no cargo é a média das 4 frentes. Detalhes e simulação em docs/auditoria_competencia_2026-10-04.md
(seção "Proposta 2").
"""

# Cargo eletivo -> (poder, esfera). Esfera: 3 federal, 2 estadual, 1 municipal.
PODER_ESFERA = {
    "PRESIDENTE": ("executivo", 3),
    "GOVERNADOR": ("executivo", 2),
    "VICE-GOVERNADOR": ("executivo", 2),
    "PREFEITO": ("executivo", 1),
    "VICE-PREFEITO": ("executivo", 1),
    "SENADOR": ("legislativo", 3),
    "DEPUTADO FEDERAL": ("legislativo", 3),
    "DEPUTADO ESTADUAL": ("legislativo", 2),
    "DEPUTADO DISTRITAL": ("legislativo", 2),
    "VEREADOR": ("legislativo", 1),
}
VICES = {"VICE-GOVERNADOR", "VICE-PREFEITO"}
DESCONTO_VICE = 2  # vice substitui, não governa: vale 2 a menos que o titular

# Esferas que o cargo exercido está ABAIXO do pretendido -> nota. Mesma esfera ou acima = 10.
NOTA_POR_DISTANCIA_ESFERA = {0: 10, 1: 8, 2: 6}

# Quanto de cada frente do cargo pretendido se transfere da experiência no outro poder, na ordem de
# COMPETENCIAS_POR_CARGO[cargo]. Ex.: quem governou já executou orçamento (1,0), mas não legislou (0,7).
TRANSFERENCIA_OUTRO_PODER = {
    # administração federal, macroeconomia, articulação nacional, relações internacionais
    "PRESIDENTE": [0.5, 0.6, 1.0, 0.4],
    # administração, finanças, processo legislativo, articulação política
    "GOVERNADOR": [0.5, 0.6, 1.0, 1.0],
    # processo legislativo, fiscalização do Executivo, representação, orçamento/emendas
    "SENADOR": [0.7, 0.8, 1.0, 1.0],
    "DEPUTADO FEDERAL": [0.7, 0.8, 1.0, 1.0],
    "DEPUTADO ESTADUAL": [0.7, 0.8, 1.0, 1.0],
    "DEPUTADO DISTRITAL": [0.7, 0.8, 1.0, 1.0],
}
TETO_OUTRO_PODER = 8

FATOR_OCUPACAO = 0.6   # matriz por profissão (0-10) -> no máximo 6
FATOR_PESQUISA = 0.7   # biografia pesquisada (0-10) -> no máximo 7

# Ocupação declarada ao TSE que é um título político: não é profissão. Se nenhum mandato for localizado nos registros,
# conta como mandato desse cargo ("DEPUTADO" não diz a esfera; fica a estadual, a mais conservadora).
TITULO_COMO_MANDATO = {
    "VEREADOR": "VEREADOR",
    "DEPUTADO": "DEPUTADO ESTADUAL",
    "SENADOR": "SENADOR",
    "GOVERNADOR": "GOVERNADOR",
    "PREFEITO": "PREFEITO",
}


def nota_mandato(cargo_pretendido: str, cargo_exercido: str) -> tuple:
    """(mesmo_poder, nota antes da transferência) de um mandato exercido, ou None se o cargo não tiver peso."""
    if cargo_exercido not in PODER_ESFERA or cargo_pretendido not in PODER_ESFERA:
        return None
    poder_alvo, esfera_alvo = PODER_ESFERA[cargo_pretendido]
    poder, esfera = PODER_ESFERA[cargo_exercido]
    nota = NOTA_POR_DISTANCIA_ESFERA[max(0, esfera_alvo - esfera)]
    if cargo_exercido in VICES:
        nota -= DESCONTO_VICE
    return poder == poder_alvo, nota


def notas_por_mandatos(cargo_pretendido: str, cargos_exercidos: list) -> list:
    """Por frente do cargo pretendido: (nota, cargo exercido que a deu, mesmo_poder), ou (0, None, None) sem mandato."""
    melhores = [(0, None, None)] * len(TRANSFERENCIA_OUTRO_PODER[cargo_pretendido])
    for exercido in cargos_exercidos:
        r = nota_mandato(cargo_pretendido, exercido)
        if r is None:
            continue
        mesmo, nota = r
        for i, fator in enumerate(TRANSFERENCIA_OUTRO_PODER[cargo_pretendido]):
            v = nota if mesmo else min(TETO_OUTRO_PODER, nota * fator)
            # empate: prefere o mesmo poder (é a evidência mais direta)
            if v > melhores[i][0] or (v == melhores[i][0] and v > 0 and mesmo and not melhores[i][2]):
                melhores[i] = (v, exercido, mesmo)
    return melhores
