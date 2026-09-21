"""Pontuação heurística de competência a partir da ocupação declarada.

Isso é um PROXY, não uma avaliação real de competência: a única informação
usada é DS_OCUPACAO (ocupação autodeclarada no registro de candidatura,
vocabulário controlado do TSE -- 211 valores distintos nos dados de 2026).
Não há verificação de histórico, desempenho ou veracidade da ocupação
declarada. Trate os escores como um sinal fraco para ordenar/agrupar
candidatos, não como nota de prova.

Modelo em duas camadas, pra ficar administrável com 211 ocupações:
  1) cada ocupação é classificada em 1 de ~20 arquétipos profissionais;
  2) cada arquétipo tem uma pontuação (0-10) em 9 "dimensões" genéricas;
  3) cada competência nomeada de cada cargo (ver competencias.py) aponta
     para uma dessas 9 dimensões.
"""
import unicodedata

# As 9 dimensões genéricas que cobrem todas as competências nomeadas de
# todos os cargos (ver CARGO_COMPETENCIA_DIMENSAO abaixo).
DIMENSOES = [
    "gestao_administrativa",
    "macro_financas",
    "processo_legislativo",
    "fiscalizacao_controle",
    "articulacao_politica",
    "representacao_social_regional",
    "relacoes_internacionais",
    "infraestrutura_urbana",
    "servicos_basicos",
]

# Pontuação (0-10) de cada arquétipo profissional nas 9 dimensões, na mesma
# ordem de DIMENSOES. Escala normalizada em 2026-09-21 (era 0-5; valores
# aqui são o dobro dos originais para manter a mesma ordinalidade relativa).
_ARQUETIPOS_VETOR = {
    "politico_legislativo_atual":  [4, 4, 10, 8, 8, 6, 2, 2, 2],
    "politico_executivo_atual":    [10, 8, 4, 2, 8, 4, 4, 6, 6],
    "juridico":                    [4, 2, 8, 8, 4, 4, 2, 0, 2],
    "financeiro":                  [6, 10, 2, 8, 2, 2, 2, 0, 0],
    "gestao_empresarial":          [8, 8, 0, 2, 4, 2, 2, 2, 0],
    "seguranca_publica_militar":   [6, 2, 0, 6, 2, 4, 0, 2, 6],
    "saude":                       [4, 0, 0, 0, 2, 6, 0, 0, 10],
    "educacao":                    [4, 0, 2, 0, 4, 6, 0, 0, 8],
    "engenharia_infraestrutura":   [6, 2, 0, 0, 2, 2, 0, 10, 2],
    "comunicacao":                 [2, 0, 0, 2, 8, 6, 0, 0, 0],
    "servidor_publico":            [8, 4, 2, 6, 2, 2, 0, 2, 4],
    "rural_agropecuaria":          [2, 2, 0, 0, 2, 8, 0, 2, 4],
    "ciencias_sociais_humanas":    [4, 0, 2, 2, 8, 8, 2, 0, 2],
    "diplomacia_ri":               [6, 4, 2, 2, 6, 0, 10, 0, 0],
    "estudante":                   [0, 0, 0, 0, 2, 6, 0, 0, 0],
    "do_lar_aposentado":           [2, 0, 0, 0, 0, 4, 0, 0, 2],
    "trabalhador_manual":          [0, 0, 0, 0, 2, 8, 0, 2, 4],
    "arte_cultura_esporte":        [0, 0, 0, 0, 6, 6, 0, 0, 0],
    "religioso":                   [2, 0, 0, 0, 6, 8, 0, 0, 2],
    "tecnico_ti":                  [4, 2, 0, 2, 0, 2, 0, 2, 0],
    "generico":                    [2, 2, 2, 2, 2, 2, 2, 2, 2],
}
ARQUETIPOS = {
    nome: dict(zip(DIMENSOES, vetor)) for nome, vetor in _ARQUETIPOS_VETOR.items()
}

# Cada tupla é (palavras-chave, arquétipo). Testadas em ordem contra a
# ocupação normalizada (maiúscula, sem acento); a primeira que bater
# (qualquer palavra-chave como substring) decide o arquétipo. Ordem importa
# para casos ambíguos (ex.: "SERVIDOR PUBLICO" antes de regras genéricas).
_REGRAS = [
    (["DEPUTADO", "VEREADOR", "SENADOR"], "politico_legislativo_atual"),
    (["GOVERNADOR", "PREFEITO", "MINISTRO DE ESTADO"], "politico_executivo_atual"),
    (["DIPLOMATA"], "diplomacia_ri"),
    (["ADVOGADO", "MAGISTRADO", "MINISTERIO PUBLICO", "TABELIAO",
      "SERVENTUARIO DE JUSTICA", "DESPACHANTE"], "juridico"),
    (["ECONOMISTA", "CONTADOR", "BANCARIO", "CAPITALISTA DE ATIVOS",
      "CORRETOR DE IMOVEIS", "TECNICO CONTABILIDADE"], "financeiro"),
    (["EMPRESARIO", "ADMINISTRADOR", "DIRETOR DE EMPRESAS", "INDUSTRIAL",
      "GERENTE", "COMERCIANTE", "COMERCIARIO", "REPRESENTANTE COMERCIAL",
      "VENDEDOR"], "gestao_empresarial"),
    (["POLICIAL", "BOMBEIRO", "FORCAS ARMADAS", "MILITAR", "VIGILANTE",
      "DETETIVE PARTICULAR", "FISCAL"], "seguranca_publica_militar"),
    (["MEDICO", "ENFERMEIRO", "ODONTOLOGO", "PSICOLOGO", "FISIOTERAPEUTA",
      "NUTRICIONISTA", "FARMACEUTICO", "BIOMEDICO", "FONOAUDIOLOGO",
      "VETERINARIO", "AGENTE DE SAUDE", "TERAPEUTA"], "saude"),
    (["PROFESSOR", "PEDAGOGO", "DIRETOR DE ESTABELECIMENTO DE ENSINO"],
     "educacao"),
    (["ENGENHEIRO", "ARQUITETO", "AGRONOMO", "GEOLOGO", "TECNICO EM EDIFICACOES",
      "TECNICO DE OBRAS CIVIS", "TECNICO EM AGRONOMIA", "GEOFISICO"],
     "engenharia_infraestrutura"),
    (["JORNALISTA", "RADIALISTA", "LOCUTOR", "PUBLICITARIO",
      "RELACOES-PUBLICAS", "COMUNICOLOGO", "ESCRITOR", "FOTOGRAFO"],
     "comunicacao"),
    (["SERVIDOR PUBLICO", "AGENTE ADMINISTRATIVO", "OCUPANTE DE CARGO EM COMISSAO",
      "AUXILIAR DE ESCRITORIO", "SECRETARIO E DATILOGRAFO", "AGENTE POSTAL"],
     "servidor_publico"),
    (["AGRICULTOR", "PECUARISTA", "PRODUTOR AGROPECUARIO", "TRABALHADOR RURAL",
      "PESCADOR", "ZOOTECNISTA", "GARIMPEIRO", "AGENCIADOR"],
     "rural_agropecuaria"),
    (["CIENTISTA POLITICO", "SOCIOLOGO", "HISTORIADOR", "ANTROPOLOGO",
      "ASSISTENTE SOCIAL", "GEOGRAFO", "ARQUEOLOGO"], "ciencias_sociais_humanas"),
    (["SACERDOTE"], "religioso"),
    (["ANALISTA DE SISTEMAS", "TECNICO EM INFORMATICA", "PROGRAMADOR DE COMPUTADOR",
      "OPERADOR DE COMPUTADOR", "DIGITADOR", "BIOLOGO", "FISICO", "QUIMICO",
      "ASTRONOMO", "ESTATISTICO", "TECNICO DE QUIMICA", "TECNICO DE BIOLOGIA"],
     "tecnico_ti"),
    (["ESTUDANTE"], "estudante"),
    (["DONA DE CASA", "APOSENTADO", "GOVERNANTA"], "do_lar_aposentado"),
    (["MUSICO", "CANTOR", "ATOR ", "ARTISTA", "ESCULTOR", "ATLETA",
      "COREOGRAFO", "BAILARINO", "MODELO", "PINTOR"], "arte_cultura_esporte"),
    (["OUTROS", "NAO DIVULGAVEL"], "generico"),
]

# Exceções de correspondência exata: casos em que o casamento por substring
# das regras acima erraria (ex.: "APOSENTADO (EXCETO SERVIDOR PÚBLICO)"
# contém literalmente "SERVIDOR PÚBLICO" dentro da cláusula de exclusão e
# seria classificado como servidor público, o oposto do que a ocupação diz).
# Checadas antes de _REGRAS.
_EXCECOES_EXATAS = {
    "APOSENTADO (EXCETO SERVIDOR PUBLICO)": "do_lar_aposentado",
}


def _normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.upper().strip()


def classificar_ocupacao(ocupacao: str) -> str:
    """Retorna a chave do arquétipo mais próximo da ocupação declarada.

    Ocupações sem regra correspondente caem em 'trabalhador_manual' (perfil
    predominante da cauda longa de ocupações operacionais/manuais do
    catálogo do TSE), exceto valores vazios/nulos, que caem em 'generico'.
    """
    if not ocupacao or not isinstance(ocupacao, str):
        return "generico"

    normalizado = _normalizar(ocupacao)

    if normalizado in _EXCECOES_EXATAS:
        return _EXCECOES_EXATAS[normalizado]

    for palavras_chave, arquetipo in _REGRAS:
        if any(_normalizar(p) in normalizado for p in palavras_chave):
            return arquetipo
    return "trabalhador_manual"


def pontuar_ocupacao(ocupacao: str) -> dict:
    """Retorna {dimensao: score} para a ocupação declarada."""
    arquetipo = classificar_ocupacao(ocupacao)
    return dict(ARQUETIPOS[arquetipo])


# Mapa (cargo, chave_da_competencia) -> dimensão genérica. As chaves de
# competência vêm de competencias.py (COMPETENCIAS_POR_CARGO).
CARGO_COMPETENCIA_DIMENSAO = {
    "PRESIDENTE": {
        "administracao_federal_politicas_publicas": "gestao_administrativa",
        "macroeconomia": "macro_financas",
        "articulacao_nacional": "articulacao_politica",
        "relacoes_internacionais": "relacoes_internacionais",
    },
    "GOVERNADOR": {
        "administracao": "gestao_administrativa",
        "financas": "macro_financas",
        "processo_legislativo": "processo_legislativo",
        "articulacao_politica": "articulacao_politica",
    },
    "PREFEITO": {
        "gestao_urbana_infraestrutura": "infraestrutura_urbana",
        "financas_municipais": "macro_financas",
        "prestacao_servicos_basicos": "servicos_basicos",
        "articulacao_local": "articulacao_politica",
    },
    "SENADOR": {
        "processo_legislativo": "processo_legislativo",
        "fiscalizacao_executivo": "fiscalizacao_controle",
        "defesa_interesses_estado": "representacao_social_regional",
        "alocacao_orcamentaria": "macro_financas",
    },
    "DEPUTADO FEDERAL": {
        "processo_legislativo": "processo_legislativo",
        "fiscalizacao_executivo": "fiscalizacao_controle",
        "representacao_bases": "representacao_social_regional",
        "alocacao_recursos": "macro_financas",
    },
    "DEPUTADO ESTADUAL": {
        "processo_legislativo_estadual": "processo_legislativo",
        "fiscalizacao_executivo_estadual": "fiscalizacao_controle",
        "representacao_regional": "representacao_social_regional",
        "alocacao_recursos_estaduais": "macro_financas",
    },
}
CARGO_COMPETENCIA_DIMENSAO["DEPUTADO DISTRITAL"] = CARGO_COMPETENCIA_DIMENSAO[
    "DEPUTADO ESTADUAL"
]
