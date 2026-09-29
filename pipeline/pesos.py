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
    "condenacao_criminal_confirmada": 5,             # [EXT] 2026-09-29 (revisão de justiça, item 3): condenação CRIMINAL
                                                      # confirmada em 2ª instância, por tribunal colegiado ou transitada,
                                                      # sem reversão. Antes ficava em condenacao_confirmada_sem_reversao
                                                      # (-4), abaixo de uma condenação criminal já ANULADA com pena
                                                      # cumprida (-5).
    "condenacao_confirmada_sem_reversao": 4,         # [EXT] improbidade/criminal confirmada em 2ª instância ou transitada, sem prisão
                                                      # 2026-09-29: passa a cobrir só condenação NÃO criminal (improbidade,
                                                      # abuso de poder/AIJE eleitoral); a criminal vai para a categoria acima.
    "condenacao_1a_instancia_recorrivel": 3,         # [EXT] condenação de 1ª instância ainda recorrível
                                                      # 2026-09-29 (item 1): 2 -> 3. Com 2 pesava menos que ser só réu em
                                                      # ação penal (-3). Não somar com reu_acao_penal no MESMO processo.
    "condenacao_revertida": 2,                       # improbidade/inelegibilidade revertida em instância superior, sem prisão
                                                      # 2026-09-29 (item 2): mantido em 2 (regra do usuário de 26/09: "houve
                                                      # investigação, já é indício"); fica abaixo da condenação de pé (-3).
    "cassacao_de_mandato": 3,                        # [EXT] sanção política por decisão de casa legislativa
                                                      # 2026-09-29 (item 9): 2 -> 3. Perda de mandato decretada e mantida
                                                      # (casa legislativa ou Justiça Eleitoral). Suspensão temporária do
                                                      # mandato é sancao_institucional_confirmada (-2).
    "sancao_institucional_confirmada": 2,            # [EXT] 2026-09-22: achado final e confirmado sobre CONDUTA no
                                                      # exercício de função pública (não crime, não Ficha Limpa),
                                                      # reconhecido por órgão competente (ex.: STF, CNJ, tribunal de
                                                      # contas) -- peso institucional comparável a cassação de
                                                      # mandato, não a uma condenação por corrupção/improbidade.
                                                      # Caso de origem: suspeição/parcialidade de juiz confirmada
                                                      # pelo STF (peso ajustado de 4 para 2 a pedido do usuário,
                                                      # que achou o peso de condenação confirmada desproporcional
                                                      # a um achado que não é condenação criminal nem Ficha Limpa).
    # Processos e investigações em curso
    "reu_acao_penal": 3,                             # por processo; a soma de processos penais é limitada a 6
    "investigacao_ou_acao_civil_em_curso": 2,        # inquérito/operação sem denúncia, réu em ação civil (improbidade/ACP)
    # Registro de candidatura (administrativo, não é crime nem Ficha Limpa)
    "registro_indeferido": 0,                        # [EXT] indeferido de forma definitiva ou já substituído
    "registro_contestado_sub_judice": 0,             # [EXT] contestado pelo MPE ou indeferido e em recurso
                                                      # 2026-09-29 (item 4): ambos 3/2 -> 0. O registro em si não diz nada
                                                      # sobre a conduta (muitos casos são papelada do partido: DRAP, convenção,
                                                      # certidão) e o indeferido já sai do funil na etapa 0. Quando a causa é
                                                      # conduta pessoal, a CAUSA entra como achado próprio (AIJE pendente =
                                                      # investigacao_ou_acao_civil_em_curso, contas rejeitadas, condenação),
                                                      # e o registro fica só como marcador (sai do funil / aviso sub judice).
    # Contas e infrações eleitorais
    "contas_irregulares_com_ressarcimento": 2,       # [EXT] TCU/órgão de controle, com ressarcimento e multa
    "contas_rejeitadas": 2,                          # [EXT] 2026-09-29 (item 5): contas de gestão rejeitadas (Câmara, TCE,
                                                      # TCM) ou contas de campanha desaprovadas, em geral com devolução.
    "contas_com_ressalva_ou_multa_eleitoral": 1,     # contas rejeitadas/aprovadas com ressalva; multa por conduta vedada
                                                      # 2026-09-29 (item 5): passa a cobrir só MULTA (conduta vedada, doação
                                                      # acima do limite, multa de tribunal de contas); contas rejeitadas e
                                                      # aprovadas com ressalva ganharam categorias próprias.
    "contas_aprovadas_com_ressalva": 0.5,            # [EXT] 2026-09-29 (item 5): contas aprovadas com ressalva, sem multa
    "infracao_eleitoral_leve": 1,                    # [EXT] ex.: propaganda antecipada
    # Leves
    "acordo_de_nao_persecucao": 2,                   # [EXT] 2026-09-29 (item 8): ANPP (penal) ou ANPC (improbidade) firmado
                                                      # para encerrar o caso. O ANPP exige confissão formal; antes era tratado
                                                      # como citado (-1). Fica abaixo da condenação de 1ª instância (-3) porque
                                                      # só cabe para crime sem violência com pena mínima abaixo de 4 anos e
                                                      # não há sentença.
    "acusacao_anulada_ou_absolvida": 1,              # acusação anulada ou absolvição, nunca condenado nem preso
                                                      # 2026-09-29 (item 6): passa a cobrir só o que caiu SEM exame do fato
                                                      # (provas anuladas, incompetência, prescrição, extinção ou arquivamento
                                                      # sem motivo conhecido); o exame do fato a favor vai para a categoria abaixo.
    "absolvido_no_merito": 0.5,                      # [EXT] 2026-09-29 (item 6): absolvição, denúncia/queixa rejeitada ou
                                                      # arquivamento por falta de provas ou de crime, ação eleitoral ou
                                                      # impugnação julgada improcedente. Não é zero porque houve acusação
                                                      # formal, mas pesa metade da acusação que caiu por vício processual.
    "citado_ou_apuracao_preliminar": 1,              # [EXT] citado em delação/inquérito sem ser alvo, ou apuração preliminar
                                                      # 2026-09-29 (item 7): soma limitada a 2 (TETOS_POR_CATEGORIA), para não
                                                      # punir quem tem décadas de cargo por acúmulo de menções.
    "acao_civil_dano_moral": 1,                      # por caso; a soma é limitada a 3
    "controversia_administrativa": 0.5,              # [EXT] decisão administrativa questionável, sem ilícito
    "infracao_administrativa_ambiental": 1,          # [EXT] 2026-09-24: auto(s) de infração do Ibama, todos abaixo de R$ 1 mi
                                                      # (a partir de R$ 1 mi vale sancao_institucional_confirmada, -2).
                                                      # Um achado por candidato, qualquer que seja o número de autos.
                                                      # Definido a pedido do usuário, que decidiu penalizar autos pequenos
                                                      # (antes só apareciam no painel, sem desconto).
}

# Limites por categoria (soma dos descontos daquela categoria)
TETOS_POR_CATEGORIA = {"reu_acao_penal": 6, "acao_civil_dano_moral": 3, "citado_ou_apuracao_preliminar": 2}


# Peso do CACIQUE (presidente do partido do candidato ou de partido aliado), por natureza da pendência.
# Menor que o peso da mesma pessoa como candidato/vice/padrinho, porque a ligação com a candidatura é mais
# fraca. A soma dos caciques de uma mesma chapa é limitada a TETO_CACIQUES (em enriquecer_circulo_politico).
PESOS_CACIQUE = {
    "condenacao_criminal_confirmada": 4,
    "condenacao_confirmada_sem_reversao": 4,  # [EXT] mesmo peso do achado equivalente em PESOS_ACHADO;
                                               # improbidade/criminal confirmada em 2ª instância ou
                                               # transitada, sem prisão.
    "condenacao_civil": 2,
    "condenacao_1a_instancia_recorrivel": 2,  # [EXT] mesmo peso do achado equivalente em PESOS_ACHADO;
                                               # usado quando a instância final ainda não está clara.
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
