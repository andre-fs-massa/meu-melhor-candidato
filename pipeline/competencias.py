"""Framework de atribuições/competências por cargo eletivo.

Cada cargo tem 4 competências centrais, derivadas do que a Constituição e
as leis efetivamente atribuem à função (não são "qualidades" genéricas de
um bom político, são as frentes de trabalho específicas do cargo).

Prefeito está incluído para completude do framework, mas não faz parte do
escopo de dados de 2026 deste projeto (eleição municipal é em 2028) -- ver
[[projeto_melhor_politico]] na memória.
"""

COMPETENCIAS_POR_CARGO = {
    "PRESIDENTE": {
        "administracao_federal_politicas_publicas": (
            "Administração Federal e Políticas Públicas",
            "Capacidade de gerir a máquina federal e conduzir políticas "
            "públicas nacionais (saúde, educação, segurança, etc.).",
        ),
        "macroeconomia": (
            "Macroeconomia",
            "Condução da política econômica nacional: fiscal, monetária, "
            "câmbio, dívida pública, relação com Banco Central.",
        ),
        "articulacao_nacional": (
            "Articulação Nacional",
            "Capacidade de construir e manter maioria no Congresso e "
            "coalizões com governadores e partidos.",
        ),
        "relacoes_internacionais": (
            "Relações Internacionais/Diplomacia",
            "Condução da política externa, tratados, comércio "
            "internacional e representação do país no exterior.",
        ),
    },
    "GOVERNADOR": {
        "administracao": (
            "Administração",
            "Gestão da máquina estadual e das políticas públicas de "
            "competência estadual (segurança, saúde, educação estaduais).",
        ),
        "financas": (
            "Finanças",
            "Gestão fiscal do estado: orçamento, dívida estadual, "
            "arrecadação (ICMS), relação com a União.",
        ),
        "processo_legislativo": (
            "Processo Legislativo",
            "Relação com a Assembleia Legislativa: envio de projetos, "
            "sanção/veto, negociação de pauta.",
        ),
        "articulacao_politica": (
            "Articulação Política",
            "Construção de base na Assembleia e com prefeitos/lideranças "
            "regionais para governabilidade.",
        ),
    },
    "PREFEITO": {
        "gestao_urbana_infraestrutura": (
            "Gestão Urbana e Infraestrutura",
            "Planejamento urbano, mobilidade, obras e infraestrutura "
            "municipal.",
        ),
        "financas_municipais": (
            "Finanças Municipais",
            "Orçamento municipal, arrecadação (IPTU/ISS), dependência de "
            "transferências (FPM) e capacidade de investimento.",
        ),
        "prestacao_servicos_basicos": (
            "Prestação de Serviços Básicos",
            "Entrega direta de saúde básica, educação infantil/fundamental, "
            "saneamento, coleta de lixo, transporte público.",
        ),
        "articulacao_local": (
            "Articulação Local (Câmara e Comunidade)",
            "Relação com a Câmara Municipal e com a comunidade/bairros na "
            "condução da gestão.",
        ),
    },
    "SENADOR": {
        "processo_legislativo": (
            "Processo Legislativo (Revisão Federativa)",
            "Papel de casa revisora: análise e emenda de projetos vindos da "
            "Câmara, PECs, tratados internacionais.",
        ),
        "fiscalizacao_executivo": (
            "Fiscalização do Executivo (Sabatinas e CPIs)",
            "Sabatina de indicados (ministros do STF, diretores de "
            "agências), CPIs, controle externo do Executivo federal.",
        ),
        "defesa_interesses_estado": (
            "Defesa de Interesses do Estado",
            "Representação do estado (não da população proporcionalmente) "
            "no Senado -- pauta de interesse regional/estadual.",
        ),
        "alocacao_orcamentaria": (
            "Alocação Orçamentária",
            "Atuação na Comissão de Orçamento e em emendas ao orçamento "
            "federal.",
        ),
    },
    "DEPUTADO FEDERAL": {
        "processo_legislativo": (
            "Processo Legislativo (Criação de Leis/PECs)",
            "Autoria e tramitação de projetos de lei e PECs na Câmara.",
        ),
        "fiscalizacao_executivo": (
            "Fiscalização do Executivo da União",
            "CPIs, requerimentos de informação, controle externo do "
            "governo federal.",
        ),
        "representacao_bases": (
            "Representação de Bases Ideológicas/Demográficas",
            "Representação proporcional de correntes ideológicas, "
            "categorias profissionais, grupos demográficos/identitários.",
        ),
        "alocacao_recursos": (
            "Alocação de Recursos (Emendas Federais)",
            "Emendas parlamentares individuais/de bancada destinando "
            "recursos federais a municípios/estados.",
        ),
    },
    "DEPUTADO ESTADUAL": {
        "processo_legislativo_estadual": (
            "Processo Legislativo Estadual",
            "Autoria e tramitação de leis estaduais na Assembleia "
            "Legislativa.",
        ),
        "fiscalizacao_executivo_estadual": (
            "Fiscalização do Executivo Estadual/TCE",
            "Controle externo do governo estadual, em conjunto com o "
            "Tribunal de Contas do Estado.",
        ),
        "representacao_regional": (
            "Representação Regional",
            "Representação de regiões/municípios específicos dentro do "
            "estado.",
        ),
        "alocacao_recursos_estaduais": (
            "Alocação de Recursos Estaduais",
            "Emendas parlamentares estaduais destinando recursos a "
            "municípios/regiões.",
        ),
    },
}

# Deputado Distrital exerce, no DF, competências análogas às de Deputado
# Estadual (a Câmara Legislativa do DF acumula competências estaduais e
# municipais -- art. 32 da Constituição).
COMPETENCIAS_POR_CARGO["DEPUTADO DISTRITAL"] = COMPETENCIAS_POR_CARGO[
    "DEPUTADO ESTADUAL"
]
