# Busca na web dos deputados finalistas (fase 2) — 2026-09-25

Pedido do usuário: buscar na web os deputados finalistas, estados mais populosos primeiro, e salvar os resultados
para leitura. Depois do primeiro estado, o usuário escolheu pesquisar o **bloco inteiro de empatados** e pediu que a
busca e a avaliação fossem padronizadas e justas. Decisões do usuário (25/09): **publicar estado por estado**, à
medida que cada um fecha; **confirmada** a mudança dos caciques dos deputados (abaixo); **mantidas** as regras da
auditoria de 24/09 (ordem de retirada de propaganda −1; AIJE/cassação eleitoral pendente −2).

## Por que o bloco de empatados

Quase todos os finalistas de deputado empatam na última vaga do quadrante (91 de 161 quadrantes; em SP, 9,25 com
4 a 11 empatados). Pesquisar só os 18 finalistas de cada estado não funciona: qualquer desconto, mesmo −1, tira o
pesquisado da lista e põe no lugar um empatado que ninguém pesquisou, e o sorteio de desempate muda quando o grupo
muda. Em SP, depois da primeira rodada, 8 dos 18 finalistas não tinham sido pesquisados. Ser pesquisado virava
desvantagem, que é o que o funil foi feito para evitar.

**Regra adotada:** em cada quadrante, pesquisar todo candidato com qualificação geral maior ou igual à do último
recomendado e repetir depois de recalcular, até que os 3 recomendados de cada quadrante tenham sido pesquisados e
nenhum não pesquisado empate com a última vaga. Um estado só é dado como fechado nessa condição.

## Método de busca (igual para todos)

- **1 busca por candidato**, sempre com o mesmo modelo: `"nome de urna" + cargo atual + cidade/UF + processo OR
  investigado OR condenado`.
- **Confirmação:** abrir a página da fonte (sem nova busca) só para conferir um achado que daria desconto. Quando a
  busca aponta um achado grave possível sem confirmar de quem é (nome omitido na matéria, página fora do ar), **uma**
  busca extra de confirmação. Se ainda assim não confirmar, **não desconta** e fica marcado "a confirmar".
- Nota 10 continua querendo dizer "nada encontrado numa busca rápida", não atestado. A profundidade do candidato passa
  de "Verificação estrutural" para "Pesquisa rápida" (exceção por candidato em `profundidade_pesquisa.json`).
- Os achados das bases oficiais (TCU, CEIS/CNEP, Ibama) continuam somados aos da busca.

## Regras de classificação (tabela fechada de `pipeline/pesos.py`)

| Situação encontrada | Categoria | Desconto |
|---|---|---|
| Condenação criminal ou por improbidade confirmada em 2ª instância | `condenacao_confirmada_sem_reversao` | −4 |
| Réu em ação penal | `reu_acao_penal` | −3 por processo |
| Registro de candidatura impugnado pelo MPE, pendente | `registro_contestado_sub_judice` | −2 |
| Inquérito aberto ou ação de improbidade/civil pública em curso (recente) | `investigacao_ou_acao_civil_em_curso` | −2 |
| Condenação de 1ª instância revertida no recurso (inclusive cassação eleitoral revertida) | `condenacao_revertida` | −2 |
| Condenação por improbidade cuja instância não se confirmou | `condenacao_1a_instancia_recorrivel` | −2 |
| Mandato cassado ou suspenso por decisão confirmada (casa legislativa ou TSE) | `cassacao_de_mandato` | −2 |
| Ação penal extinta por prescrição, sem condenação | `acusacao_anulada_ou_absolvida` | −1 |
| Ação de improbidade julgada improcedente / absolvição | `acusacao_anulada_ou_absolvida` | −1 |
| Investigação, representação ou apuração arquivada; citado em apuração sem ser alvo | `citado_ou_apuracao_preliminar` | −1 |
| Processo antigo (mais de 3 anos) sem desfecho encontrado — marcado "a confirmar" | `citado_ou_apuracao_preliminar` | −1 |
| Condenação ou acordo por dano moral / crime contra a honra | `acao_civil_dano_moral` | −1 |
| Contas de campanha desaprovadas | `contas_com_ressalva_ou_multa_eleitoral` | −1 |
| Multa ou ordem de retirada por propaganda irregular, antecipada ou negativa (critério da auditoria de 24/09, mantido pelo usuário) | `infracao_eleitoral_leve` | −1 |
| Advertência ou censura de conselho de ética | `controversia_administrativa` | −0,5 |
| Processo disciplinar por fala ou decoro, arquivado ou sem sanção | — | 0 |
| Ser autor ou vítima de processo; resultado de homônimo | — | 0 |
| Pedido de perda de mandato por infidelidade partidária (troca de partido) | — | 0 |
| Processos de parentes (cônjuge, pai), sem o candidato como alvo | — | 0 (entram no círculo político só dos majoritários) |

## Correção feita antes da busca: caciques dos deputados

A tabela do círculo político dos deputados (`circulo_partidos_estrutural.json`) ainda usava notas de cacique
anteriores à auditoria de 24/09, enquanto os majoritários já usavam a pendência canônica (campo `cacique` de
`liderancas_partidarias.json`). Isso inflava o círculo de PSDB e PRD e os punha no bloco do topo. Agora
`gerar_estrutural_deputados --derivar-tabela` lê o campo canônico quando ele existe. Mudanças de nota: **PSDB 0 → −1**
(Aécio, inquérito arquivado), **PRD 0 → −1** (Neskau, investigado sem denúncia), **MISSÃO −2 → −1** (ação civil em
curso). Mudaram só rótulos, sem efeito na nota: PL, PCdoB, Cidadania. Era uma das decisões pendentes da auditoria;
aplicada porque o pedido foi de avaliação padronizada e **confirmada pelo usuário em 25/09**. Vale para os deputados
de todos os estados, não só os já pesquisados.

## Resultados por estado

### SP

Pesquisados: 64 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **LUCAS CARDOSO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 4, geral 7: condenação criminal confirmada em 2ª instância pelo TJSP (estelionato e sonegação de documento) e pedido de impugnação da candidatura pelo MPE, pendente no TRE-SP.
- **ALEX MANENTE** (CIDADANIA, Deputado Federal), idoneidade pessoal 7, geral 8.5: multa por propaganda antecipada em 2022 e dois processos listados em 2016 (inquérito eleitoral e ação de improbidade) sem desfecho encontrado (a confirmar).
- **BRUNA FURLAN** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: condenação de 1ª instância (só multa) por uso da máquina na campanha de 2012 em Barueri, revertida no recurso.
- **KIKO BELONI** (CIDADANIA, Deputado Estadual), idoneidade pessoal 8, geral 9: cassação de 1ª instância por fraude à cota de gênero, revertida pelo TRE-SP.
- **IVAN SILVA** (PODE, Deputado Estadual), idoneidade pessoal 8, geral 8.5: inquérito civil do MP-SP por nepotismo no gabinete (2024), sem desfecho encontrado.
- **ALBERTO BARRETO** (PRD, Deputado Estadual), idoneidade pessoal 9, geral 9: o MP-SP moveu ação de improbidade contra ele como presidente da Câmara de Taubaté e pediu o afastamento; a Justiça negou a ação em junho de 2026.
- **ANA CAROLINA SERRA** (PSDB, Deputado Estadual), idoneidade pessoal 9, geral 9: AIJE de 2022 por abuso de poder na campanha, sem desfecho encontrado (a confirmar).
- **KEIT LIMA** (PSOL, Deputado Estadual), idoneidade pessoal 9, geral 9.5: processo por crime contra a honra de uma colega, encerrado com acordo e retratação.
- **TABATA AMARAL** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: condenação civil por danos morais a Ricardo Nunes, ainda recorrível.
- **ERIKA HILTON** (PSOL, Deputado Federal), idoneidade pessoal 9, geral 9.5: apuração sobre uso de assessores como maquiadores, arquivada pela PGR em agosto de 2026.
- **TOME ABDUCH** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: contas de campanha de 2022 desaprovadas, com devolução de R$ 95 mil.
- **SÔNIA GUAJAJARA** (PSOL, Deputado Federal), idoneidade pessoal 9, geral 9.5: inquérito por críticas ao governo federal (2021), trancado pela Justiça Federal.
- **ORLANDO SILVA** (PCDOB, Deputado Federal), idoneidade pessoal 9, geral 9.5: apuração de 2011 como ministro do Esporte, arquivada pela Comissão de Ética da Presidência por falta de provas (o acusador foi condenado por calúnia).
- **HIGOR DIEGO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: citado em apurações preliminares (pedido de comissão processante sobre o transporte e apuração do MP sobre emendas), sem desfecho encontrado.
- **JULINHO FUZARI** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenação civil por danos morais a Luiz Marinho (2021).
- **CARLOS GIANNAZI** (PSOL, Deputado Estadual), idoneidade pessoal 9, geral 9.5: inquérito por suposta agressão a outro deputado (2018), arquivado pelo TJSP em 2020.
- **PARRA** (PODE, Deputado Estadual), idoneidade pessoal 9, geral 9: gabinete citado em inquérito do MP de 2019 sobre indicações políticas na Fundação do ABC.
- **RAFAEL DE ANGELI** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9.5, geral 9.75: advertência do Conselho de Ética da Câmara de Araraquara por conversa vazada.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ANA CAROLINA SERRA (PSDB, Deputado Estadual): AIJE de 2022 por abuso de poder na campanha, sem desfecho encontrado (a confirmar).
- ALEX MANENTE (CIDADANIA, Deputado Federal): multa por propaganda antecipada em 2022 e dois processos listados em 2016 (inquérito eleitoral e ação de improbidade) sem desfecho encontrado (a confirmar).
- EDGAR DOURADO (PSDB, Deputado Estadual): nada confirmado. Um resultado do TCE-SP fala de ex-presidente da Câmara de Andradina condenado por irregularidade, sem nome legível; ele presidiu a Câmara em 2025, e a página do TCE não abriu. A confirmar.
- JHONY SASAKI (PODE, Deputado Estadual): nada confirmado. Em junho de 2026 o MP pediu, em ação de improbidade, a condenação de um vereador de São Vicente que presidiu a Câmara em 2021-2022 por rachadinha (R$ 285 mil); as reportagens não dão o nome e não confirmei se é ele. A confirmar com prioridade.
- LEANDRO BASSON (PODE, Deputado Estadual): nada confirmado. O nome aparece em cerca de 40 processos (é policial civil) e há um processo "Justiça Pública x Leandro Jeronimo Basson" de 2025 no TJSP (comarca de Jundiaí), mas não consegui ver a classe nem o papel dele. A confirmar com prioridade.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: LEONARDO DE SIQUEIRA LIMA (NOVO 3060), EDUARDO BORGO (NOVO 3003), CRIS MONTEIRO (NOVO 3011)
- Deputado Federal · Direita conservadora: MARIA ROSAS (REPUBLICANOS 1022), ALTAIR MORAES (REPUBLICANOS 1033), DANI GALDINO (REPUBLICANOS 1040) — sorteio entre 8 empatados
- Deputado Federal · Esquerda progressista: PROFESSORA LUCIENE CAVALCANTE (PSOL 5089), SÂMIA BOMFIM (PSOL 5000), KEIKO OTA (PSB 4096)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: CARLOS ABRANCHES (CIDADANIA 23456), MARIA AMÉLIA (PSDB 45333), FABIANA CAMARINHA (PODE 20123) — sorteio entre 16 empatados
- Deputado Estadual · Direita conservadora: RUI ALVES (REPUBLICANOS 10111), GILMACI SANTOS (REPUBLICANOS 10123), ELTON CARVALHO (REPUBLICANOS 10192) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: MONICA DAS PRETAS (PSOL 50900), MARIANA CONTI (PSOL 50100), DÉBORA CAMILO (PSOL 50500) — sorteio entre 6 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### MG

Pesquisados: 44 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **EUCLYDES PETTERSEN** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 2, geral 6: Busca rápida na internet (1 busca, fonte conferida): réu em duas ações penais e indiciado pela PF no escândalo dos descontos do INSS; o MPF pediu que ele apresente certidões criminais para o registro.
- **LUIZ FERNANDO** (UNIÃO, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca, fonte conferida): réu em ação penal da Lava Jato desde 2018 e denúncia por organização criminosa rejeitada em 2021, com recurso no STF.
- **NEWTON CARDOSO JR** (MDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: ação de improbidade de 2020 (assessores da Câmara em serviço doméstico) sem desfecho encontrado (a confirmar) e absolvição no STF em 2018 (crime ambiental e falsidade ideológica).
- **FRANCO CARTAFINA** (PODE, Deputado Federal), idoneidade pessoal 9, geral 9: absolvido em julho de 2026 na queixa-crime por calúnia movida por Eduardo Cunha.
- **BRAULIO LARA** (NOVO, Deputado Federal), idoneidade pessoal 9, geral 9.5: propaganda eleitoral irregular apontada pelo TRE-MG.
- **DUDA SALABERT** (PSOL, Deputado Federal), idoneidade pessoal 9, geral 9.5: alvo de representação de adversário à PF, sem notícia de inquérito aberto.
- **FLAVIO MARRA** (PRD, Deputado Estadual), idoneidade pessoal 9, geral 9: multa por propaganda eleitoral negativa (2024). Um pedido de cassação por agressão foi arquivado pela Câmara em 2026 (sem sanção, não desconta).
- **WANDERLEY PORTO** (PRD, Deputado Estadual), idoneidade pessoal 9, geral 9: processo de 2020 por difamação (hashtag no caso Mariana Ferrer) sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- NEWTON CARDOSO JR (MDB, Deputado Federal): ação de improbidade de 2020 (assessores da Câmara em serviço doméstico) sem desfecho encontrado (a confirmar) e absolvição no STF em 2018 (crime ambiental e falsidade ideológica).
- FLÁVIA BORJA (PODE, Deputado Estadual): nada que desconte. Ação de perda de mandato por infidelidade partidária (movida por suplente, com parecer favorável do MP) não é achado de idoneidade; um inquérito por falas consideradas transfóbicas foi citado por adversário em audiência, sem confirmação. A confirmar.
- WANDERLEY PORTO (PRD, Deputado Estadual): processo de 2020 por difamação (hashtag no caso Mariana Ferrer) sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: TIRZAH (NOVO 3036), FRANCO CARTAFINA (PODE 2030), RONALDO TANNÚS (PODE 2010) — sorteio entre 5 empatados
- Deputado Federal · Direita conservadora: GILBERTO ABRAMO (REPUBLICANOS 1010), RODRIGO DE CASTRO (UNIÃO 4450), PINHEIRINHO (PP 1122) — sorteio entre 6 empatados
- Deputado Federal · Esquerda progressista: CÉLIA XAKRIABÁ (PSOL 5088), LOHANNA (PV 4350), REGINALDO LOPES (PT 1312)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: RIAN PEREIRA (NOVO 30000), MARCELA TRÓPIA (NOVO 30400), OSVALDO LOPES (PODE 20123) — sorteio entre 5 empatados
- Deputado Estadual · Direita conservadora: MAURO TRAMONTE (REPUBLICANOS 10800), CHARLES SANTOS (REPUBLICANOS 10100), JOSE CARLOS GOMES (AGIR 36777) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: TIAGO SANTANA (PCDOB 65653), IRENE MELO FRANCO (PV 43222), IZA LOURENÇA (PSOL 50099) — sorteio entre 8 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### RJ

Pesquisados: 43 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **DANIELA DO WAGUINHO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 7, geral 8.5: ação por nepotismo arquivada (2018), apuração do MP sobre gráficas da campanha de 2022 sem desfecho encontrado (a confirmar) e multa por propaganda irregular no dia da eleição. O marido, Waguinho, é alvo da PF (não entra na nota pessoal).
- **LUIZ MARTINS** (PSDB, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e 1 de confirmação): réu na Operação Furna da Onça por associação criminosa e corrupção passiva, com prisão preventiva em 2018; processo suspenso pelo STJ.
- **MAICON CRUZ** (PV, Deputado Estadual), idoneidade pessoal 7, geral 8.5: mandato cassado pelo TSE em 2024 por fraude à cota de gênero da chapa e inquérito de 2022 arquivado.
- **MAX** (UNIÃO, Deputado Federal), idoneidade pessoal 7, geral 8: condenação por improbidade como ex-prefeito de Queimados (tratada como de 1ª instância por não ter confirmado a instância) e multa por propaganda negativa mantida pelo TSE. A perda de mandato por infidelidade partidária (2021) foi revista pelo TRE-RJ e não conta.
- **BERNARDO ROSSI** (UNIÃO, Deputado Federal), idoneidade pessoal 7, geral 8: alvo de busca e apreensão da PF no caso Refit (2026) e AIJE de 2020 sem desfecho encontrado (a confirmar).
- **GLAUBER BRAGA** (PSOL, Deputado Federal), idoneidade pessoal 8, geral 9: suspensão do mandato por 6 meses pela Câmara por agressão física a um militante dentro da Casa.
- **PROF. JOSEMAR** (PSOL, Deputado Estadual), idoneidade pessoal 8, geral 9: multa eleitoral por santinhos no dia da eleição e condenação por danos morais a policial federal.
- **JULIO LOPES** (PP, Deputado Federal), idoneidade pessoal 8, geral 8.5: alvo de busca e apreensão e investigado na Lava Jato por atos como secretário de Transportes, sem desfecho encontrado.
- **BANDEIRA DE MELLO** (PV, Deputado Federal), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e 1 de confirmação): ação penal do incêndio no Ninho do Urubu extinta para ele por prescrição em 2025, sem julgamento de mérito.
- **ALEXANDRE FREITAS** (NOVO, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenação a danos morais coletivos por post racista, em recurso. Foi expulso do Novo em 2021 (questão partidária, não conta).
- **YURI MOURA** (PSOL, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenação por injúria em ação movida por Cláudio Castro, com recurso em julgamento.
- **DR. LUIZINHO** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: citado no caso do laboratório de parentes que infectou transplantados com HIV, sem ser alvo formal encontrado.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- DANIELA DO WAGUINHO (REPUBLICANOS, Deputado Federal): ação por nepotismo arquivada (2018), apuração do MP sobre gráficas da campanha de 2022 sem desfecho encontrado (a confirmar) e multa por propaganda irregular no dia da eleição. O marido, Waguinho, é alvo da PF (não entra na nota pessoal).
- BERNARDO ROSSI (UNIÃO, Deputado Federal): alvo de busca e apreensão da PF no caso Refit (2026) e AIJE de 2020 sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: LUIZ LIMA (NOVO 3030), RENAN FERREIRINHA (PSD 5521), ANNA FEIO (NOVO 3006) — sorteio entre 8 empatados
- Deputado Federal · Direita conservadora: ROSANGELA GOMES (REPUBLICANOS 1033), FABIANO GONÇALVES (REPUBLICANOS 1012), RODRIGO VIZEU (MDB 1555) — sorteio entre 2 empatados
- Deputado Federal · Esquerda progressista: TALÍRIA PETRONE (PSOL 5077), JÚLIA CASAMASSO (PSOL 5007), PASTOR HENRIQUE VIEIRA (PSOL 5001) — sorteio entre 4 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: THIAGO MOURA (PSDB 45045), DIOGO TALENTO (PRD 25000), SIDNEY DINHO (PRD 25028)
- Deputado Estadual · Direita conservadora: CARLOS MACEDO (REPUBLICANOS 10100), LIBRELON (REPUBLICANOS 10000), JULIO ROCHA (AGIR 36036)
- Deputado Estadual · Esquerda progressista: LILIAN BEHRING (PCDOB 65656), DANI BALBI (PCDOB 65123), FLAVIO SERAFINI (PSOL 50123) — sorteio entre 7 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### BA

Pesquisados: 29 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ROBERTO CARLOS** (PV, Deputado Estadual), idoneidade pessoal 6, geral 8: Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado pelo TJ-BA em 2024 a 6 anos e 5 meses por rachadinha na Assembleia; ele diz que o caso está encerrado e que não é inelegível, sem explicar como (a confirmar).
- **ADOLFO VIANA** (PSDB, Deputado Federal), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca, fontes conferidas): citado em documentos apreendidos pela PF em duas apurações (obras superfaturadas com emendas dele, 2025; lista na casa de Ciro Nogueira, 2026), sem ser investigado formalmente; investigação eleitoral de 2018 arquivada.
- **MAURICIO TRINDADE** (PSDB, Deputado Federal), idoneidade pessoal 9, geral 9: Busca rápida na internet (1 busca e 1 de confirmação): réu por tráfico de influência em denúncia recebida pelo STF (fato de 1997, como vereador de Salvador), sem desfecho encontrado (a confirmar).
- **DUDA DE ALAN SANCHES** (PSDB, Deputado Federal), idoneidade pessoal 9, geral 9: denúncia anônima ao MP-BA por suposta compra de votos e uso de espaço público arquivada por falta de indícios (2026). Um assessor foi preso numa operação contra o tráfico e exonerado; o vereador não é alvo (sem desconto).
- **DANIEL** (PCDOB, Deputado Federal), idoneidade pessoal 9, geral 9.5: alvo de inquérito da Lava Jato no STF (delação da Odebrecht, 2017), sem desfecho encontrado (a confirmar). Reportagem de 2025 sobre emendas dele que beneficiaram a Contag (caso dos descontos do INSS) não o aponta como investigado (sem desconto).
- **MARIO NEGROMONTE JR** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca, fonte conferida): inquérito da Lava Jato (indiciamento pela PF em 2016) arquivado pelo STF em 2018. A ação penal por corrupção no STF é contra o pai, o ex-ministro Mário Negromonte (sem desconto).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- MAURICIO TRINDADE (PSDB, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): réu por tráfico de influência em denúncia recebida pelo STF (fato de 1997, como vereador de Salvador), sem desfecho encontrado (a confirmar).
- DANIEL (PCDOB, Deputado Federal): alvo de inquérito da Lava Jato no STF (delação da Odebrecht, 2017), sem desfecho encontrado (a confirmar). Reportagem de 2025 sobre emendas dele que beneficiaram a Contag (caso dos descontos do INSS) não o aponta como investigado (sem desconto).
- ROBERTO CARLOS (PV, Deputado Estadual): Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado pelo TJ-BA em 2024 a 6 anos e 5 meses por rachadinha na Assembleia; ele diz que o caso está encerrado e que não é inelegível, sem explicar como (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: ABILIO SANTANA (PSDB 4533), PROF. LEANDRO SANSON (NOVO 3044), MARTA SANTOS (NOVO 3011)
- Deputado Federal · Direita conservadora: KEL TORRES (REPUBLICANOS 1080), LÉO PRATES (REPUBLICANOS 1044), MÁRCIO MARINHO (REPUBLICANOS 1010)
- Deputado Federal · Esquerda progressista: LIDICE DA MATA (PSB 4040), OLIVIA (PCDOB 6550), SANDRO OLIVEIRA (PSOL 5012) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: ANDERSON NINHO (PSDB 45300), JORDAVIO RAMOS (PSDB 45555), ALEX DA PIATÃ (PSD 55000)
- Deputado Estadual · Direita conservadora: MILITÃO DOURADO (REPUBLICANOS 10155), CHARLIANE SOUSA (REPUBLICANOS 10888), JOSÉ DE ARIMATEIA (REPUBLICANOS 10456) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: FABRÍCIO (PCDOB 65333), HILTON COELHO (PSOL 50150), EDUARDO SALLES (PV 43222) — sorteio entre 5 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### PR

Pesquisados: 39 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **RENATO FREITAS** (PT, Deputado Federal), idoneidade pessoal 4, geral 6.5: Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado em 2024 a 3 meses (convertidos em serviços comunitários) por pichação em protesto, com recurso; cassação de vereador em 2022 revertida pelo STF; réu por crimes contra a honra no TJ-PR; parecer do Conselho de Ética da Assembleia pela cassação em 2026 (briga com manobrista), resultado do plenário não encontrado (a confirmar).
- **BETO RICHA** (PSDB, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): foi réu em 8 ações penais e teve prisões preventivas em 2018 e 2019; o STF anulou os atos da Lava Jato contra ele (2023) e manteve a extinção de quatro ações em 2026, sem condenação; o destino das demais não foi confirmado (a confirmar). Condenado em 2ª instância em ação popular a ressarcir diárias de viagem a Paris (2015).
- **ALEXANDRE GUIMARÃES** (PDT, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca, fontes conferidas): condenado em 1ª instância por improbidade (promoção pessoal com verba da Assembleia, 2020), recurso sem desfecho encontrado; alvo de busca do Gaeco por esquema de alvarás em Campo Largo, sem desfecho encontrado (a confirmar).
- **LUCIANO DUCCI** (PSB, Deputado Federal), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca, fonte conferida): condenado em 2ª instância (TJ-PR, 2015) a ressarcir R$ 79 mil à prefeitura por promoção pessoal com o telemarketing e o site da prefeitura; desfecho do recurso não encontrado (a confirmar).
- **BRUNO SECCO** (NOVO, Deputado Estadual), idoneidade pessoal 8, geral 9: perdeu o mandato de vereador quando o TRE-PR cassou a chapa do PMB de 2024 por fraude à cota de gênero; disse que recorreria.
- **EDER BORGES** (NOVO, Deputado Estadual), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca, fonte conferida): condenação por difamação contra o sindicato dos professores extinta por prescrição antes do trânsito em julgado (a perda de mandato de 2022 foi desfeita); representação por nepotismo arquivada pelo Conselho de Ética. O processo de ética por gesto de arma em plenário e fala contra professores é de decoro (sem desconto).
- **ANGELO VANHONI** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: alvo de representação na Câmara de Curitiba por uso de veículo oficial em manifestação política, sem desfecho encontrado.
- **PROFESSORA ANA LÚCIA** (PDT, Deputado Federal), idoneidade pessoal 9, geral 9: alvo de processo de cassação na Câmara de Maringá por denúncia de ex-assessor (desvio de função e pressão por contribuições partidárias); a comissão processante concluiu pela improcedência e o plenário ainda ia votar.
- **ZECA DIRCEU** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: inquérito da Lava Jato aberto no STF em 2016 e enviado à Justiça Eleitoral do PR como possível caixa dois, sem desfecho encontrado (a confirmar).
- **TANIA MAION** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9.5, geral 9.75: suspensão de 30 dias do mandato aprovada pela Câmara por quebra de decoro (2025), com efeitos suspensos por liminar da Justiça; desfecho final não encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- BETO RICHA (PSDB, Deputado Federal): Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): foi réu em 8 ações penais e teve prisões preventivas em 2018 e 2019; o STF anulou os atos da Lava Jato contra ele (2023) e manteve a extinção de quatro ações em 2026, sem condenação; o destino das demais não foi confirmado (a confirmar). Condenado em 2ª instância em ação popular a ressarcir diárias de viagem a Paris (2015).
- LUCIANO DUCCI (PSB, Deputado Federal): Busca rápida na internet (1 busca, fonte conferida): condenado em 2ª instância (TJ-PR, 2015) a ressarcir R$ 79 mil à prefeitura por promoção pessoal com o telemarketing e o site da prefeitura; desfecho do recurso não encontrado (a confirmar).
- TANIA MAION (REPUBLICANOS, Deputado Estadual): suspensão de 30 dias do mandato aprovada pela Câmara por quebra de decoro (2025), com efeitos suspensos por liminar da Justiça; desfecho final não encontrado (a confirmar).
- ALEXANDRE GUIMARÃES (PDT, Deputado Estadual): Busca rápida na internet (1 busca, fontes conferidas): condenado em 1ª instância por improbidade (promoção pessoal com verba da Assembleia, 2020), recurso sem desfecho encontrado; alvo de busca do Gaeco por esquema de alvarás em Campo Largo, sem desfecho encontrado (a confirmar).
- RENATO FREITAS (PT, Deputado Federal): Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado em 2024 a 3 meses (convertidos em serviços comunitários) por pichação em protesto, com recurso; cassação de vereador em 2022 revertida pelo STF; réu por crimes contra a honra no TJ-PR; parecer do Conselho de Ética da Assembleia pela cassação em 2026 (briga com manobrista), resultado do plenário não encontrado (a confirmar).
- ZECA DIRCEU (PT, Deputado Federal): inquérito da Lava Jato aberto no STF em 2016 e enviado à Justiça Eleitoral do PR como possível caixa dois, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: GUILHERME LIVOTI (NOVO 3043), INDIARA BARBOSA (NOVO 3003), EVANDRO ROMAN (CIDADANIA 2322)
- Deputado Federal · Direita conservadora: PEDRO LUPION (REPUBLICANOS 1000), MARCIO PACHECO (REPUBLICANOS 1077), HERMES FRANGÃO PARCIANELLO (UNIÃO 4440)
- Deputado Federal · Esquerda progressista: OMAR PICHETH (PSB 4077), CAMILLA GONDA (PSB 4000), LUCIANA RAFAGNIN (PT 1323) — sorteio entre 2 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: AMÁLIA TORTATO (NOVO 30234), TOTO (NOVO 30444), SAMUEL PINHEIRO (PODE 20012) — sorteio entre 2 empatados
- Deputado Estadual · Direita conservadora: JASSON GOULART (REPUBLICANOS 10789), CANTORA MARA LIMA (REPUBLICANOS 10456), NEY LEPREVOST (REPUBLICANOS 10669) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: GERALDO STOCCO (PV 43777), MISS PRETA (PT 13123), ROBERTO DE SOUZA (PT 13456) — sorteio entre 9 empatados
- Deputado Estadual · Estatista-autoritário: vazio


## Situação e próximos passos

- **Estados fechados (5 de 27):** SP (64 pesquisados), MG (44), RJ (43), BA (29), PR (39). Total: 219 candidatos, 54
  com achado que descontou e 19 marcados "a confirmar". Nos cinco, todos os finalistas foram pesquisados e nenhum
  empatado ficou de fora.
- **Regra de infidelidade aplicada a um finalista:** Evandro Roman/PR (finalista do Libertário federal) perdeu o
  mandato de deputado federal por decisão do TSE em 2021 por trocar de partido sem justa causa; pela tabela, troca
  de partido não desconta (é sanção partidária, não de conduta).
- **Achados mais graves:** Euclydes Pettersen/MG (2 ações penais e indiciamento no caso do INSS, nota 2), Lucas
  Cardoso/SP (condenação por estelionato confirmada pelo TJSP e registro impugnado, nota 4), Luiz Fernando Faria/MG
  (réu na Lava Jato, nota 6), Renato Freitas/PR (condenação por pichação com recurso, cassação de 2022 revertida,
  réu por crime contra a honra e parecer de cassação em 2026, nota 4), Beto Richa/PR (8 ações penais extintas ou sem
  desfecho e condenação em ação popular, nota 6), Roberto Carlos/BA (condenado pelo TJ-BA por rachadinha, nota 6), Luiz Martins/RJ (réu na
  Furna da Onça, nota 7). Todos saíram da lista de finalistas.
- **A confirmar com prioridade** (sinal grave sem confirmação, sem desconto): Jhony Sasaki/SP (ação de rachadinha
  contra ex-presidente da Câmara de São Vicente) e Leandro Basson/SP (processo "Justiça Pública x" em 2025). Nenhum
  dos 10 "a confirmar" está entre os finalistas atuais, mas Sasaki e Basson estão no bloco empatado do Libertário
  estadual de SP: se o sorteio mudar e um deles entrar, confirmar antes de publicar.
- **Faltam 22 estados**, na ordem de população: RS, PE, CE, PA, SC, GO, MA, AM, ES, PB, MT, RN, PI, AL, DF,
  MS, SE, RO, TO, AC, AP, RR. Com o teto de ~200 buscas por sessão, cada sessão nova fecha ~3 a 4 estados grandes
  (SP levou 64 buscas, MG 44, RJ 43, mais confirmações). Estimativa: 6 a 8 sessões.
- **Anotado para o AM:** o deputado federal Adail Filho (MDB) foi alvo da PF em 16/09/2026 (Operação Dinastia do
  Lago: fraude em licitações, desvio, corrupção e lavagem) — apareceu por acaso numa busca de MG.
- **Publicação por estado.** SP, MG e RJ publicados em 25/09, depois BA e PR (junto com a correção dos caciques, que vale para
  todos os estados). A cada estado novo: rodar `exportar_prototipo`, acrescentar a UF na frase de "Limites" em
  `site/app.js` ("Nos estados já concluídos (...)"), conferir numa cópia do site sem o GA e publicar.
- **Ferramentas para continuar:** `ferramentas/busca_finalistas/` (listar pendentes, gravar resultados, rodar o
  pipeline, gerar a seção do relatório).
