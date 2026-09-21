"""Tabela única de pesos da nota de idoneidade PESSOAL (data/reference/idoneidade.json).

Cada achado verificado de um candidato é classificado em UMA categoria fechada e o
desconto vem daqui, nunca digitado à mão. Assim candidatos com o mesmo tipo de achado
recebem o mesmo desconto, e a nota gravada pode ser conferida por `calcular_nota`.

A escala descende do "_leiame" original de idoneidade.json (parte de 10 e desconta por
achado VERIFICADO, nunca por suposição). Categorias marcadas com [EXT] foram
explicitadas em 2026-09-21 porque a escala original não as cobria e cada caso vinha
sendo pontuado no olho.
"""

PESOS_ACHADO = {
    # Gravidade máxima
    "inelegibilidade_vigente": 6,                    # Ficha Limpa vigente e não revertida
    "condenacao_criminal_pena_cumprida": 5,          # inclui prisão, mesmo se anulada depois por vício processual
    # Condenações
    "condenacao_confirmada_sem_reversao": 4,         # [EXT] improbidade/criminal confirmada em 2ª instância ou transitada, sem prisão
    "condenacao_1a_instancia_recorrivel": 2,         # [EXT] condenação de 1ª instância ainda recorrível
    "condenacao_revertida": 2,                       # improbidade/inelegibilidade revertida em instância superior, sem prisão
    "cassacao_de_mandato": 2,                        # [EXT] sanção política por decisão de casa legislativa
    # Processos e investigações em curso
    "reu_acao_penal": 3,                             # por processo; a soma de processos penais é limitada a 6
    "investigacao_ou_acao_civil_em_curso": 2,        # inquérito/operação sem denúncia, réu em ação civil (improbidade/ACP)
    # Registro de candidatura (administrativo, não é crime nem Ficha Limpa)
    "registro_indeferido": 3,                        # [EXT] indeferido de forma definitiva ou já substituído
    "registro_contestado_sub_judice": 2,             # [EXT] contestado pelo MPE ou indeferido e em recurso
    # Contas e infrações eleitorais
    "contas_irregulares_com_ressarcimento": 2,       # [EXT] TCU/órgão de controle, com ressarcimento e multa
    "contas_com_ressalva_ou_multa_eleitoral": 1,     # contas rejeitadas/aprovadas com ressalva; multa por conduta vedada
    "infracao_eleitoral_leve": 1,                    # [EXT] ex.: propaganda antecipada
    # Leves
    "acusacao_anulada_ou_absolvida": 1,              # acusação anulada ou absolvição, nunca condenado nem preso
    "citado_ou_apuracao_preliminar": 1,              # [EXT] citado em delação/inquérito sem ser alvo, ou apuração preliminar
    "acao_civil_dano_moral": 1,                      # por caso; a soma é limitada a 3
    "controversia_administrativa": 0.5,              # [EXT] decisão administrativa questionável, sem ilícito
}

# Limites por categoria (soma dos descontos daquela categoria)
TETOS_POR_CATEGORIA = {"reu_acao_penal": 6, "acao_civil_dano_moral": 3}


# Peso do CACIQUE (presidente do partido do candidato ou de partido aliado), por natureza da pendência.
# Menor que o peso da mesma pessoa como candidato/vice/padrinho, porque a ligação com a candidatura é mais
# fraca. A soma dos caciques de uma mesma chapa é limitada a TETO_CACIQUES (em enriquecer_circulo_politico).
PESOS_CACIQUE = {
    "condenacao_criminal_confirmada": 4,
    "condenacao_civil": 2,
    "reu_acao_penal": 2,
    "reu_acao_civil": 2,
    "investigado_sem_denuncia": 1,
    "delatado_sem_denuncia": 1,
    "investigacao_arquivada_sem_denuncia": 1,
    "acao_civil_em_curso": 1,
    "nenhuma_encontrada": 0,
    "nao_verificado": 0,
}


def soma_descontos(achados: list) -> float:
    """Soma dos pesos (com tetos por categoria) de uma lista de achados; usada para vice e padrinho."""
    por_categoria = {}
    for a in achados:
        cat = a["categoria"]
        if cat not in PESOS_ACHADO:
            raise KeyError(f"categoria de achado desconhecida: {cat}")
        por_categoria[cat] = por_categoria.get(cat, 0) + PESOS_ACHADO[cat] * a.get("quantidade", 1)
    total = sum(min(v, TETOS_POR_CATEGORIA.get(k, v)) for k, v in por_categoria.items())
    return int(total) if float(total).is_integer() else total


def calcular_nota(achados: list) -> float:
    """Nota 0-10 = 10 - soma dos pesos dos achados, respeitando os tetos por categoria.

    Cada achado pode trazer 'quantidade' (padrão 1) quando há vários casos idênticos."""
    nota = max(0, 10 - soma_descontos(achados))
    return int(nota) if float(nota).is_integer() else nota


def formatar_achados(achados: list) -> str:
    """Texto legível dos achados com o peso de cada um."""
    return " | ".join(
        f"{a['categoria']}"
        + (f" x{a['quantidade']}" if a.get("quantidade", 1) != 1 else "")
        + f" [-{PESOS_ACHADO[a['categoria']]}{' cada' if a.get('quantidade', 1) != 1 else ''}]: {a['descricao']}"
        for a in achados
    )
