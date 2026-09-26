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
| Condenação de 1ª instância revertida no recurso; cassação ou perda de mandato **decretada e depois anulada ou revertida** (no recurso, nos embargos ou pelo próprio tribunal), inclusive por infidelidade partidária (decisão do usuário, 26/09: houve apuração e decisão contra o candidato, o que já é indício) | `condenacao_revertida` | −2 |
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
| Perda de mandato por infidelidade partidária **decretada e mantida** (decisão do usuário, 25/09) | `cassacao_de_mandato` | −2 |
| Pedido de cassação ou de perda de mandato ainda não decidido ou negado (nunca decretado) | — | 0 |
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
- **MAX** (UNIÃO, Deputado Federal), idoneidade pessoal 5 (era 7 até 26/09): condenação por improbidade como ex-prefeito de Queimados (tratada como de 1ª instância por não ter confirmado a instância) e multa por propaganda negativa mantida pelo TSE. A perda de mandato por infidelidade partidária decretada pelo TRE-RJ (2020-2021) e depois revista pelo próprio tribunal passou a contar como condenação revertida (−2) pela regra de 26/09.
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

Pesquisados: 44 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **RENATO FREITAS** (PT, Deputado Federal), idoneidade pessoal 4, geral 6.5: Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado em 2024 a 3 meses (convertidos em serviços comunitários) por pichação em protesto, com recurso; cassação de vereador em 2022 revertida pelo STF; réu por crimes contra a honra no TJ-PR; parecer do Conselho de Ética da Assembleia pela cassação em 2026 (briga com manobrista), resultado do plenário não encontrado (a confirmar).
- **BETO RICHA** (PSDB, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): foi réu em 8 ações penais e teve prisões preventivas em 2018 e 2019; o STF anulou os atos da Lava Jato contra ele (2023) e manteve a extinção de quatro ações em 2026, sem condenação; o destino das demais não foi confirmado (a confirmar). Condenado em 2ª instância em ação popular a ressarcir diárias de viagem a Paris (2015).
- **THAIS TAKAHASHI** (CIDADANIA, Deputado Federal), idoneidade pessoal 6, geral 8: condenação por apropriação indébita contra uma cliente idosa (retenção de benefício previdenciário) confirmada em 2ª instância pelo TJ-PR em 2025. Também presidiu a sessão de 01/01/2025 da Câmara de Cornélio Procópio, anulada pela Justiça por impedir o registro de uma chapa (sem desconto: decisão sobre o ato da Mesa, não sobre ela).
- **ALEXANDRE GUIMARÃES** (PDT, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca, fontes conferidas): condenado em 1ª instância por improbidade (promoção pessoal com verba da Assembleia, 2020), recurso sem desfecho encontrado; alvo de busca do Gaeco por esquema de alvarás em Campo Largo, sem desfecho encontrado (a confirmar).
- **LUCIANO DUCCI** (PSB, Deputado Federal), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca, fonte conferida): condenado em 2ª instância (TJ-PR, 2015) a ressarcir R$ 79 mil à prefeitura por promoção pessoal com o telemarketing e o site da prefeitura; desfecho do recurso não encontrado (a confirmar).
- **BRUNO SECCO** (NOVO, Deputado Estadual), idoneidade pessoal 8, geral 9: perdeu o mandato de vereador quando o TRE-PR cassou a chapa do PMB de 2024 por fraude à cota de gênero; disse que recorreria.
- **EDER BORGES** (NOVO, Deputado Estadual), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca, fonte conferida): condenação por difamação contra o sindicato dos professores extinta por prescrição antes do trânsito em julgado (a perda de mandato de 2022 foi desfeita); representação por nepotismo arquivada pelo Conselho de Ética. O processo de ética por gesto de arma em plenário e fala contra professores é de decoro (sem desconto).
- **EVANDRO ROMAN** (CIDADANIA, Deputado Federal), idoneidade pessoal 8, geral 9: perdeu o mandato de deputado federal por decisão do TSE em 2021 (4 a 3), por infidelidade partidária ao trocar o PSD pelo Patriota sem justa causa. Por decisão do usuário (25/09), perda de mandato decretada e mantida conta como cassação (−2); pedido de perda ainda não decidido ou revertido não conta.
- **ANGELO VANHONI** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: alvo de representação na Câmara de Curitiba por uso de veículo oficial em manifestação política, sem desfecho encontrado.
- **PROFESSORA ANA LÚCIA** (PDT, Deputado Federal), idoneidade pessoal 9, geral 9: alvo de processo de cassação na Câmara de Maringá por denúncia de ex-assessor (desvio de função e pressão por contribuições partidárias); a comissão processante concluiu pela improcedência e o plenário ainda ia votar.
- **ZECA DIRCEU** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: inquérito da Lava Jato aberto no STF em 2016 e enviado à Justiça Eleitoral do PR como possível caixa dois, sem desfecho encontrado (a confirmar).
- **HOMERO MARCHESE** (NOVO, Deputado Federal), idoneidade pessoal 9, geral 9.5: alvo de bloqueio de redes sociais no inquérito das fake news (2022), sem ser investigado formalmente segundo as reportagens.
- **TANIA MAION** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9.5, geral 9.75: suspensão de 30 dias do mandato aprovada pela Câmara por quebra de decoro (2025), com efeitos suspensos por liminar da Justiça; desfecho final não encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- BETO RICHA (PSDB, Deputado Federal): Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): foi réu em 8 ações penais e teve prisões preventivas em 2018 e 2019; o STF anulou os atos da Lava Jato contra ele (2023) e manteve a extinção de quatro ações em 2026, sem condenação; o destino das demais não foi confirmado (a confirmar). Condenado em 2ª instância em ação popular a ressarcir diárias de viagem a Paris (2015).
- LUCIANO DUCCI (PSB, Deputado Federal): Busca rápida na internet (1 busca, fonte conferida): condenado em 2ª instância (TJ-PR, 2015) a ressarcir R$ 79 mil à prefeitura por promoção pessoal com o telemarketing e o site da prefeitura; desfecho do recurso não encontrado (a confirmar).
- TANIA MAION (REPUBLICANOS, Deputado Estadual): suspensão de 30 dias do mandato aprovada pela Câmara por quebra de decoro (2025), com efeitos suspensos por liminar da Justiça; desfecho final não encontrado (a confirmar).
- ALEXANDRE GUIMARÃES (PDT, Deputado Estadual): Busca rápida na internet (1 busca, fontes conferidas): condenado em 1ª instância por improbidade (promoção pessoal com verba da Assembleia, 2020), recurso sem desfecho encontrado; alvo de busca do Gaeco por esquema de alvarás em Campo Largo, sem desfecho encontrado (a confirmar).
- RENATO FREITAS (PT, Deputado Federal): Busca rápida na internet (1 busca, 1 de confirmação e fontes conferidas): condenado em 2024 a 3 meses (convertidos em serviços comunitários) por pichação em protesto, com recurso; cassação de vereador em 2022 revertida pelo STF; réu por crimes contra a honra no TJ-PR; parecer do Conselho de Ética da Assembleia pela cassação em 2026 (briga com manobrista), resultado do plenário não encontrado (a confirmar).
- ZECA DIRCEU (PT, Deputado Federal): inquérito da Lava Jato aberto no STF em 2016 e enviado à Justiça Eleitoral do PR como possível caixa dois, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: GUILHERME LIVOTI (NOVO 3043), INDIARA BARBOSA (NOVO 3003), RENAN CESCHIN (PODE 2022) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: PEDRO LUPION (REPUBLICANOS 1000), MARCIO PACHECO (REPUBLICANOS 1077), HERMES FRANGÃO PARCIANELLO (UNIÃO 4440)
- Deputado Federal · Esquerda progressista: OMAR PICHETH (PSB 4077), CAMILLA GONDA (PSB 4000), LUCIANA RAFAGNIN (PT 1323) — sorteio entre 2 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: AMÁLIA TORTATO (NOVO 30234), TOTO (NOVO 30444), SAMUEL PINHEIRO (PODE 20012) — sorteio entre 2 empatados
- Deputado Estadual · Direita conservadora: JASSON GOULART (REPUBLICANOS 10789), CANTORA MARA LIMA (REPUBLICANOS 10456), NEY LEPREVOST (REPUBLICANOS 10669) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: GERALDO STOCCO (PV 43777), MISS PRETA (PT 13123), ROBERTO DE SOUZA (PT 13456) — sorteio entre 9 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### RS

Pesquisados: 41 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **LUCIANA GENRO** (PSOL, Deputado Estadual), idoneidade pessoal 8, geral 9: denúncia por declarações sobre Gaza rejeitada pelo TJ-RS em 2026; denunciada em 2009 no caso da 'farra das passagens' da Câmara, sem desfecho encontrado (a confirmar).
- **RONALDO NOGUEIRA** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8.5, geral 9.25: Busca rápida na internet (1 busca e 1 de confirmação): alvo da Operação Gaveteiro da PF (2020) sobre desvio de R$ 50 milhões no Ministério do Trabalho, com pedido de prisão negado, sem desfecho encontrado (a confirmar); censura pública do CNDH (2019) por retrocessos no combate ao trabalho escravo.
- **FELIPE CAMOZZATO** (NOVO, Deputado Federal), idoneidade pessoal 9, geral 9.5: alvo de representação criminal de procurador da República por crimes contra a honra em críticas ao MPF (2026), sem denúncia encontrada.
- **FELIPE FALLER** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca, fonte conferida): processo criminal encerrado por prescrição da pretensão punitiva em 2026, sem condenação.
- **RAMIRO ROSÁRIO** (NOVO, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenado em 1ª instância por danos morais a cooperativas do MST por divulgar informação falsa sobre agrotóxico no arroz (2026). Processo na Comissão de Ética por ofender um juiz em plenário (fala, sem desconto).
- **RODRIGO D AVILA** (NOVO, Deputado Estadual), idoneidade pessoal 9, geral 9.5: pedido de cassação por advogar contra concessionárias do município, arquivado pela Câmara de Canoas.
- **BUSATO** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: Busca rápida na internet (1 busca e 1 de confirmação): citado em delação com áudios entregues ao MPF sobre supostas propinas em contratos de saúde de Canoas quando era prefeito, sem ser réu. A condenação por improbidade no caso do aeromóvel de Canoas é de outro ex-prefeito, Jairo Jorge (sem desconto).
- **MARIANA LESCANO** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: investigada pela PF por fala na tribuna da Câmara de Porto Alegre, sem denúncia encontrada. A nota de repúdio da Defensoria a declarações dela é crítica, não processo (sem desconto).
- **COVATTI FILHO** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: citado na Lava Jato pelo doleiro Alberto Youssef (PP-RS), sem desfecho encontrado (a confirmar). Acusação da imprensa (2021) de que a família manteria escritório político pago com verba de gabinete do suplente, sem apuração encontrada (sem desconto).
- **FERNANDA MIRANDA** (PSOL, Deputado Estadual), idoneidade pessoal 9.5, geral 9.75: parecer da Comissão de Ética por afastamento de 60 dias do mandato (abordagem com substância ilícita no Carnaval), ainda sem votação em plenário (a confirmar). Ela denunciou, e não é alvo, a apuração sobre exames citopatológicos.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- LUCIANA GENRO (PSOL, Deputado Estadual): denúncia por declarações sobre Gaza rejeitada pelo TJ-RS em 2026; denunciada em 2009 no caso da 'farra das passagens' da Câmara, sem desfecho encontrado (a confirmar).
- FERNANDA MIRANDA (PSOL, Deputado Estadual): parecer da Comissão de Ética por afastamento de 60 dias do mandato (abordagem com substância ilícita no Carnaval), ainda sem votação em plenário (a confirmar). Ela denunciou, e não é alvo, a apuração sobre exames citopatológicos.
- RONALDO NOGUEIRA (REPUBLICANOS, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): alvo da Operação Gaveteiro da PF (2020) sobre desvio de R$ 50 milhões no Ministério do Trabalho, com pedido de prisão negado, sem desfecho encontrado (a confirmar); censura pública do CNDH (2019) por retrocessos no combate ao trabalho escravo.
- ARTHUR SCHMIDT (MDB, Deputado Federal): nada confirmado. Em jul/2025 a Polícia Civil (Draco de São Leopoldo, Operação Dia D) fez buscas contra um ex-vereador de São Leopoldo por rachadinha em 2021-2022; as reportagens não dão o nome e o mandato registrado dele é 2017-2020, então não se confirmou que seja ele (1 busca extra de confirmação). A confirmar.
- COVATTI FILHO (PP, Deputado Federal): citado na Lava Jato pelo doleiro Alberto Youssef (PP-RS), sem desfecho encontrado (a confirmar). Acusação da imprensa (2021) de que a família manteria escritório político pago com verba de gabinete do suplente, sem apuração encontrada (sem desconto).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: CARLA DAITX (NOVO 3033), ADA MUNARETTO (NOVO 3000), SANDRA BONETTO (NOVO 3010)
- Deputado Federal · Direita conservadora: FRAN BAYER (REPUBLICANOS 1012), CARLOS GOMES (REPUBLICANOS 1010), RANZI (MDB 1555) — sorteio entre 7 empatados
- Deputado Federal · Esquerda progressista: JURANDIR SILVA (PSOL 5055), CRIS MORAES (PV 4343), ATENA (PSOL 5001) — sorteio entre 5 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: KAKÁ D´ÁVILA (PODE 20333), MOISÉS BARBOZA (PSDB 45900), BRUNA MOLZ (PODE 20510) — sorteio entre 5 empatados
- Deputado Estadual · Direita conservadora: MARCELO HARTEMINK (REPUBLICANOS 10000), ELIANA BAYER (REPUBLICANOS 10120), JOÃO UEZ (REPUBLICANOS 10603) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: MATHEUS GOMES (PSOL 50123), KAREN SANTOS (PSOL 50555), GIOVANI CULAU (PCDOB 65656) — sorteio entre 5 empatados
- Deputado Estadual · Estatista-autoritário: vazio


### PE

Pesquisados: 45 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **SILVIO COSTA FILHO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 4, geral 7: Busca rápida na internet (1 busca, 1 de confirmação e fonte conferida): réu em quatro ações criminais do caso dos 'shows fantasmas' da Empetur (2008-2009), abertas em 2023; situação atual não confirmada. Há absolvição antiga (TJPE, 2014) em outro processo.
- **ROMERO ALBUQUERQUE** (PSB, Deputado Estadual), idoneidade pessoal 4, geral 7: investigado por agressão, ameaça, invasão de domicílio e outros crimes num episódio de 2025 (caso remetido à 1ª instância em 2026); três multas por propaganda eleitoral irregular (2014 e outdoors da esposa); AIJE de 2018 por abuso de poder sem desfecho encontrado (a confirmar).
- **JOÃO PAULO DO PT** (PT, Deputado Estadual), idoneidade pessoal 5, geral 7: condenado em 1ª instância em ação penal pela contratação direta da Finatec como prefeito do Recife, recurso sem desfecho encontrado (a confirmar); TCE-PE mandou ressarcir R$ 18 milhões e aplicou multa por licitação irregular.
- **JUNIOR MATUTO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 6, geral 8: Busca rápida na internet (1 busca e 1 de confirmação): alvo de ação do MPPE sobre cessão irregular de terreno público em Paulista (2026, sem julgamento); inquérito do MPF sobre licitações arquivado em 2026; afastado do cargo de prefeito em 2020 em operações por lavagem e peculato e indiciado por fraude a licitação, sem desfecho encontrado (a confirmar).
- **EDUARDO MOURA** (NOVO, Deputado Federal), idoneidade pessoal 8, geral 9: condenado por danos morais por expor uma mulher em vídeo de fiscalização (2026) e indiciado por injúria e difamação contra um colega (2026). O pedido de cassação no Conselho de Ética pelo mesmo gesto é de decoro (sem desconto).
- **RAFAEL PREQUÉ** (PV, Deputado Federal), idoneidade pessoal 8, geral 9: condenado por danos morais por chamar o prefeito de 'ladrão'; autuado por desmatamento (multa de R$ 19 mil). A ação de perda de mandato por infidelidade partidária está pendente (sem desconto).
- **FERNANDO FILHO** (UNIÃO, Deputado Federal), idoneidade pessoal 8, geral 8.5: alvo da Operação Vassalos da PF (2026) sobre desvio de emendas e fraude em licitações em Petrolina, investigação em curso sem denúncia.
- **CLARISSA TÉRCIO** (PP, Deputado Federal), idoneidade pessoal 8, geral 8.5: inquérito sobre o 8 de janeiro arquivado pelo STF; condenada em 1ª instância por danos morais (transfobia) a um casal.
- **AUGUSTO COUTINHO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: auto de infração ambiental anulado pela Justiça Federal. Bases oficiais: 1 auto(s) de infração ambiental não cancelado(s) no Ibama, o maior de R$ 5.000,00, somando R$ 5.000,00.
- **RENILDO CALHEIROS** (PCDOB, Deputado Federal), idoneidade pessoal 9, geral 9.5: processado pelo MPPE desde 2017 por falta de prestação de contas de verba do FNDE como prefeito de Olinda, sem desfecho encontrado (a confirmar).
- **GILSON MACHADO FILHO** (PODE, Deputado Estadual), idoneidade pessoal 9, geral 9: condenado por danos morais por incitar 'linchamento virtual' de um internauta (2026). A prisão citada nas notícias é do pai, Gilson Machado (sem desconto).
- **JEFERSON TIMÓTEO** (PODE, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia de distribuição de comida no comitê de campanha enviada ao MP Eleitoral (2026), sem decisão encontrada.
- **KAIO MANIÇOBA** (PP, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia por falsidade ideológica rejeitada pelo STF.
- **SILENO** (PSB, Deputado Estadual), idoneidade pessoal 9, geral 9.5: multa do TRE-PE por impulsionamento de propaganda negativa.
- **BETINHO GOMES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: investigado em inquéritos da Lava Jato no STF (delação da Odebrecht, 2017), sem desfecho encontrado (a confirmar).
- **ANDREZA ROMERO** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: multa mantida pelo TRE-PE por propaganda antecipada em outdoors.
- **KARI SANTOS** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: multa da Justiça Eleitoral por propaganda contra Gilson Machado (2024). Outras ações de Gilson Machado e de Eduardo Moura contra ela estão sem decisão (sem desconto).
- **VINI CASTELLO** (PCDOB, Deputado Estadual), idoneidade pessoal 9, geral 9.5: ordem da Justiça Eleitoral para recolher e retirar material de campanha que omitia o vice (2024).
- **DANI PORTELA** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia ao MP de Contas sobre contratação de empresa ligada a parente, arquivada em 2025 sem irregularidade.
- **LETÍCIA BORBA** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: multa por conduta vedada (publicidade institucional acima do limite em ano eleitoral) mantida pelo TSE.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- RENILDO CALHEIROS (PCDOB, Deputado Federal): processado pelo MPPE desde 2017 por falta de prestação de contas de verba do FNDE como prefeito de Olinda, sem desfecho encontrado (a confirmar).
- JUNIOR MATUTO (REPUBLICANOS, Deputado Estadual): Busca rápida na internet (1 busca e 1 de confirmação): alvo de ação do MPPE sobre cessão irregular de terreno público em Paulista (2026, sem julgamento); inquérito do MPF sobre licitações arquivado em 2026; afastado do cargo de prefeito em 2020 em operações por lavagem e peculato e indiciado por fraude a licitação, sem desfecho encontrado (a confirmar).
- ROMERO ALBUQUERQUE (PSB, Deputado Estadual): investigado por agressão, ameaça, invasão de domicílio e outros crimes num episódio de 2025 (caso remetido à 1ª instância em 2026); três multas por propaganda eleitoral irregular (2014 e outdoors da esposa); AIJE de 2018 por abuso de poder sem desfecho encontrado (a confirmar).
- BETINHO GOMES (REPUBLICANOS, Deputado Federal): investigado em inquéritos da Lava Jato no STF (delação da Odebrecht, 2017), sem desfecho encontrado (a confirmar).
- JOÃO PAULO DO PT (PT, Deputado Estadual): condenado em 1ª instância em ação penal pela contratação direta da Finatec como prefeito do Recife, recurso sem desfecho encontrado (a confirmar); TCE-PE mandou ressarcir R$ 18 milhões e aplicou multa por licitação irregular.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: FELIPE ALECRIM (NOVO 3000), FERNANDO RODOLFO (PRD 2555), LUCIANO JUNIOR (PODE 2088)
- Deputado Federal · Direita conservadora: MARCELLY DA AQUARELA (REPUBLICANOS 1020), DELEGADO LESSA (REPUBLICANOS 1090), LULA DA FONTE (PP 1111)
- Deputado Federal · Esquerda progressista: RINALDO JÚNIOR (PSB 4013), LUCAS RAMOS (PSB 4011), CARLOS VERAS (PT 1314) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: RENATO ANTUNES (NOVO 30630), JOÃO DE DEUS (PODE 20615), FABRIZIO FERRAZ (PODE 20111)
- Deputado Estadual · Direita conservadora: ANTONIO COELHO (UNIÃO 44000), GLEIDE ÂNGELO (PP 11111), HENRIQUE FILHO (PP 11777) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: CAYO ALBINO (PSB 40400), SILENO (PSB 40040), DORIEL (PT 13123)
- Deputado Estadual · Estatista-autoritário: vazio


### CE

Pesquisados: 30 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **SARGENTO REGINAURO** (PSDB, Deputado Estadual), idoneidade pessoal 7, geral 8: réu em ação penal militar pelo motim da segurança pública do Ceará em 2020, em andamento.
- **ADAIL CARNEIRO** (PSDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: preso em 2020 com R$ 2 milhões em espécie e condenado em 1ª instância por lavagem de dinheiro; absolvido pelo TRF-5 em 2025.
- **ERIKA AMORIM** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: condenada pelo TRE-CE por conduta vedada (perseguição de servidores de Caucaia na campanha de 2018) e denunciada criminalmente pelo mesmo caso, sem desfecho encontrado (a confirmar).
- **JACQUELINE GOUVEIA** (MDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: ação eleitoral por suposto abuso de poder econômico (projeto de castração gratuita com o nome dela), com liminar do TRE-CE que suspendeu o projeto em 2026; pendente.
- **EDUARDO BISMARCK** (PV, Deputado Federal), idoneidade pessoal 8, geral 9: cassação e inelegibilidade decididas pelo TSE em 2024 (abuso de poder do prefeito de Baturité em seu favor), revertidas pelo próprio TSE no mesmo ano.
- **FELIPE VASQUES** (PSDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: alvo da Operação Aletheia do MPCE (2026) sobre fraude em licitações da Câmara de Juazeiro do Norte, afastado e depois reconduzido pelo TJCE; investigação em curso.
- **ROMEU ALDIGUERI** (PSB, Deputado Estadual), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca e fontes conferidas): condenado em 1ª instância por calúnia eleitoral (2018), com alegação de prescrição; registros policiais antigos (atropelamento com morte, agressão à ex-mulher, estupro) e ação por estelionato citados pela imprensa sem desfecho conhecido (a confirmar).
- **LEONARDO PINHEIRO** (PSB, Deputado Estadual), idoneidade pessoal 8, geral 9: réu em ação de improbidade do MPCE por suposta funcionária fantasma no gabinete (2023).
- **ROMEU ALDIGUERI** (PSB, Deputado Federal), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca e fontes conferidas, feitas para o registro dele a deputado estadual; o mesmo candidato tem também registro a federal): condenado em 1ª instância por calúnia eleitoral (2018), com alegação de prescrição; registros policiais antigos (atropelamento com morte, agressão à ex-mulher, estupro) e ação por estelionato citados pela imprensa sem desfecho conhecido (a confirmar).
- **LUKÃO** (CIDADANIA, Deputado Federal), idoneidade pessoal 9, geral 9.5: ação por fraude à cota de gênero da chapa que pedia a cassação dele rejeitada pelo TRE-CE em 2026.
- **MOSES RODRIGUES** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: conduzido pela PF para explicar aglomeração perto de seções eleitorais em Sobral (2024), sem desfecho encontrado.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ERIKA AMORIM (REPUBLICANOS, Deputado Federal): condenada pelo TRE-CE por conduta vedada (perseguição de servidores de Caucaia na campanha de 2018) e denunciada criminalmente pelo mesmo caso, sem desfecho encontrado (a confirmar).
- ROMEU ALDIGUERI (PSB, Deputado Estadual): Busca rápida na internet (1 busca e fontes conferidas): condenado em 1ª instância por calúnia eleitoral (2018), com alegação de prescrição; registros policiais antigos (atropelamento com morte, agressão à ex-mulher, estupro) e ação por estelionato citados pela imprensa sem desfecho conhecido (a confirmar).
- ROMEU ALDIGUERI (PSB, Deputado Federal): Busca rápida na internet (1 busca e fontes conferidas, feitas para o registro dele a deputado estadual; o mesmo candidato tem também registro a federal): condenado em 1ª instância por calúnia eleitoral (2018), com alegação de prescrição; registros policiais antigos (atropelamento com morte, agressão à ex-mulher, estupro) e ação por estelionato citados pela imprensa sem desfecho conhecido (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: WELLINGTON SABOIA (PODE 2026), LUKÃO (CIDADANIA 2323), CAROL SIEBRA (NOVO 3030) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: MICHEL LINS (REPUBLICANOS 1001), AJ ALBUQUERQUE (PP 1111), BENIGNO JUNIOR (REPUBLICANOS 1045)
- Deputado Federal · Esquerda progressista: RENATO ROSENO (PSOL 5050), ADRIANA GERÔNIMO (PSOL 5077), FERNANDO SANTANA (PT 1322)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: PASTOR JOÃO LUÍS (NOVO 30500), JULIO CESAR (PRD 25789), QUEIROZ FILHO (PSDB 45777) — sorteio entre 3 empatados
- Deputado Estadual · Direita conservadora: GARDEL ROLIM (REPUBLICANOS 10333), DAVID DURAND (REPUBLICANOS 10123), SILVIO NASCIMENTO (REPUBLICANOS 10000)
- Deputado Estadual · Esquerda progressista: GABRIEL BIOLOGIA (PSOL 50555), DR. LUCILVIO GIRÃO (PSB 40234), TIN GOMES (PSB 40600)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do CE: Romeu Aldigueri tem dois registros (deputado estadual e federal) e recebeu o mesmo resultado nos
dois. Gardel Rolim (finalista estadual) responde a ação de perda de mandato por infidelidade partidária com julgamento
marcado no TRE-CE para 29/06/2026; o resultado não foi encontrado. Pela regra de 25/09, se a perda tiver sido
decretada, vale −2 e ele sai da lista: **confirmar antes de 04/10**.


### PA

Pesquisados: 37 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **IRAN LIMA** (MDB, Deputado Estadual), idoneidade pessoal 4, geral 6.5: Busca rápida na internet (1 busca e fontes conferidas): condenado por improbidade dolosa como prefeito de Moju; o TSE negou o registro em 2019 e cassou o mandato de deputado estadual em 2020.
- **ANTONIO DOIDO** (MDB, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca e fontes conferidas): alvo da Operação Igapó da PF (dez/2025) por desvio de verbas, corrupção e lavagem; declarado inelegível pela Justiça Eleitoral em dez/2025 por abuso de poder nas eleições de 2024, com recurso.
- **ALEXANDRE GOMES** (PODE, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e fontes conferidas): denunciado pelo MPPA em set/2026 como chefe de esquema de desvio de R$ 21,7 milhões na Habitação de Ananindeua; empresa ligada a ele citada na apuração da mansão do ex-prefeito.
- **ADRIANO COELHO** (MDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: Busca rápida na internet (1 busca e fontes conferidas): a PF abriu investigação sobre a campanha dele e a do irmão depois de apreender R$ 2,5 milhões em espécie com pessoas ligadas a eles (set/2026).
- **HENDERSON PINTO** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: Busca rápida na internet (1 busca e 1 de confirmação): denunciado pelo MPPA em 2018 na Operação Perfuga (peculato e fraude em licitação na Câmara de Santarém, 2013-2014), com bens bloqueados; desfecho não encontrado (a confirmar).
- **OZORIO JUVENIL** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: absolvido em ação penal eleitoral por uso de documento falso nas contas da campanha de 2010.
- **DIANA BELO** (UNIÃO, Deputado Estadual), idoneidade pessoal 9, geral 9: como prefeita de Capitão Poço, respondeu a dois processos de cassação e inelegibilidade; desfecho não encontrado (a confirmar).
- **MARTINHO CARMONA** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: ação penal por fraude na contratação de estagiário rejeitada pelo Pleno do TJPA.
- **ELCIONE BARBALHO** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: pedido de cassação por desvio da cota feminina em 2018 rejeitado pelo TSE em 2022.
- **CILENE COUTO** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: ação de improbidade do MPPA (2012) pela fraude na folha da Alepa, sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- HENDERSON PINTO (UNIÃO, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): denunciado pelo MPPA em 2018 na Operação Perfuga (peculato e fraude em licitação na Câmara de Santarém, 2013-2014), com bens bloqueados; desfecho não encontrado (a confirmar).
- DIANA BELO (UNIÃO, Deputado Estadual): como prefeita de Capitão Poço, respondeu a dois processos de cassação e inelegibilidade; desfecho não encontrado (a confirmar).
- CILENE COUTO (MDB, Deputado Estadual): ação de improbidade do MPPA (2012) pela fraude na folha da Alepa, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: VAVÁ MARTINS (NOVO 3010), OLIVAL MARQUES (PODE 2000), DR. FERNANDO (NOVO 3020) — sorteio entre 4 empatados
- Deputado Federal · Direita conservadora: KENISTON BRAGA (MDB 1512), LU OGAWA (PP 1111), RENILCE NICODEMOS (MDB 1577)
- Deputado Federal · Esquerda progressista: DR. FLAVIO NOBRE (PSB 4080), PROF. THIAGO (PSB 4022), VIVI REIS (PSOL 5050) — sorteio entre 4 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: PATRICIA PERDIGÃO (PODE 20320), PR. JUNIOR BRAGA (NOVO 30123), NEYLA BRAGA (NOVO 30000)
- Deputado Estadual · Direita conservadora: ANDREIA XARÃO (MDB 15123), PAULA TITAN (PP 11777), DR. RENAN LAURIA (PP 11234) — sorteio entre 6 empatados
- Deputado Estadual · Esquerda progressista: MARINOR BRITO (PSOL 50555), LÍVIA DUARTE (PSOL 50123), GLEISSON (PV 43123) — sorteio entre 4 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do PA: Iran Lima volta a disputar depois de ter o registro negado (2019) e o mandato cassado (2020) pelo TSE
pela condenação por improbidade como prefeito de Moju; a inelegibilidade já venceu (ele foi eleito em 2022).


### SC

Pesquisados: 36 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ANDRÉ MOSER** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 7, geral 8.5: Busca rápida na internet (1 busca e 1 de confirmação): inelegibilidade por abuso de poder decretada em 1ª instância (2024) e revertida pelo TRE-SC (2025); condenado por dano moral a morador ofendido nas redes (2026).
- **JEAN KUHLMANN** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 7, geral 8.5: Busca rápida na internet (1 busca e 1 de confirmação): condenado em 1ª instância por improbidade (servidora fantasma na Alesc), com recurso sem resultado encontrado; ação civil pública de 2012 sem desfecho encontrado (a confirmar).
- **DARCI DE MATOS** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: multado por propaganda antecipada (outdoors) e alvo de representação eleitoral antiga do MP sobre a campanha a prefeito de Joinville, sem desfecho encontrado (a confirmar).
- **PROFESSORA NATÁLIA** (MDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: absolvida (TJSC, 2025) em processo iniciado em 2010 e AIJE julgada improcedente pelo TRE-SC, com multa anulada.
- **ANA PAULA LIMA** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: ação penal eleitoral baseada em delação da Odebrecht trancada pelo TRE-SC.
- **MARCELO ACHUTTI** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: representação ao MP (2025) por discurso contra moradores de rua, sem desfecho encontrado (a confirmar); ação de um shopping contra ele teve liminar negada.
- **MARCELO WERNER** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: pedido de cassação por participação em empresa contratada pela prefeitura arquivado pela Câmara de Itajaí.
- **FABIO SCHIOCHET** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: ações de cassação da campanha de 2022 julgadas improcedentes pelo TRE-SC e pelo TSE.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- DARCI DE MATOS (REPUBLICANOS, Deputado Federal): multado por propaganda antecipada (outdoors) e alvo de representação eleitoral antiga do MP sobre a campanha a prefeito de Joinville, sem desfecho encontrado (a confirmar).
- MARCELO ACHUTTI (MDB, Deputado Estadual): representação ao MP (2025) por discurso contra moradores de rua, sem desfecho encontrado (a confirmar); ação de um shopping contra ele teve liminar negada.
- JEAN KUHLMANN (REPUBLICANOS, Deputado Estadual): Busca rápida na internet (1 busca e 1 de confirmação): condenado em 1ª instância por improbidade (servidora fantasma na Alesc), com recurso sem resultado encontrado; ação civil pública de 2012 sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: GILSON MARQUES (NOVO 3050), KAUE OLIVEIRA (NOVO 3049), RODRIGO LIVRAMENTO (NOVO 3030) — sorteio entre 5 empatados
- Deputado Federal · Direita conservadora: JORGE GOETTEN (REPUBLICANOS 1001), GEOVANIA DE SÁ (REPUBLICANOS 1077), DARCI DE MATOS (REPUBLICANOS 1022)
- Deputado Federal · Esquerda progressista: EDUARDO ZANATTA (PT 1331), CAREN MACHADO (PT 1340), CARLA AYRES (PT 1344)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: MATHEUS CADORIN (NOVO 30000), NETO PETTERS DO NOVO (NOVO 30456), MARQUINHO KURTZ (PODE 20456)
- Deputado Estadual · Direita conservadora: LUCAS NEVES (REPUBLICANOS 10282), RAMOS POLICIAL (UNIÃO 44190), DR. VICENTE (UNIÃO 44000) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: CAMASÃO (PSOL 50500), MARQUITO (PSOL 50150), INGRID SATERÉ MAWÉ (PSOL 50180)
- Deputado Estadual · Estatista-autoritário: vazio

Observações de SC: o desconto de Darci de Matos (idoneidade 8) baixou a qualificação da última vaga da direita federal
de 9,25 para 9,00 e abriu uma rodada de reposição com 5 empatados; ele segue finalista. Ações civis de dano moral movidas contra vereadores por adversários ou empresas,
ainda sem decisão (Camasão, Marcelo Achutti), não descontam; só a condenação desconta (André Moser).


### GO

Pesquisados: 30 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **LÊDA BORGES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 6, geral 8: Busca rápida na internet (1 busca e fonte conferida): condenação por improbidade como prefeita de Valparaíso de Goiás (jornal pago com dinheiro público para promoção eleitoral), restabelecida pelo STJ.
- **IGOR FRANCO** (PODE, Deputado Federal), idoneidade pessoal 9, geral 9: ordem judicial para apagar vídeos com IA contra o prefeito de Goiânia; pedido antigo de perda de mandato por infidelidade sem efeito.
- **MARUSSA BOLDRIN** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: AIJE de 2022 assumida pelo MP Eleitoral por abuso de poder econômico (uso da Faeg/Senar), sem desfecho encontrado (a confirmar).
- **JOSE NELTO** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: queixa-crime por injúria e calúnia rejeitada pelo STF.
- **MUCIO SANTANA** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: ação por compra de votos em 2024 julgada improcedente pelo TRE-GO.
- **NIXON DAS CASINHAS** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: citado em auditoria da CGU sobre programa habitacional de Luziânia.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- MARUSSA BOLDRIN (REPUBLICANOS, Deputado Federal): AIJE de 2022 assumida pelo MP Eleitoral por abuso de poder econômico (uso da Faeg/Senar), sem desfecho encontrado (a confirmar).
- AAVA SANTIAGO (PSB, Deputado Federal): o TRE-GO decretou em jul/2026 a perda do mandato de vereadora por infidelidade partidária (saída do PSDB sem justa causa), com recurso ao TSE pendente e ela no cargo. Pela regra de 25/09 só desconta (−2) se a perda for mantida: a confirmar.
- VETER MARTINS (PSB, Deputado Estadual): um blog de resumos jurídicos diz que ele é investigado no STF por crime contra a administração pública, mas a busca de confirmação não achou fonte primária nem notícia. Não desconta; a confirmar.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: JOÃO DA LUZ (CIDADANIA 2323), LUCAS CALIL (PRD 2525), GLAUSTIN DA FOKUS (PODE 2026)
- Deputado Federal · Direita conservadora: LUCAS VERGÍLIO (MDB 1510), RICARDO QUIRINO (REPUBLICANOS 1010), BRUNO PEIXOTO (UNIÃO 4455)
- Deputado Federal · Esquerda progressista: CARMEM LUCIA (PSB 4012), TALES DE CASTRO (PSB 4015), AAVA SANTIAGO (PSB 4040)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: GCM ROMÁRIO POLICARPO (CIDADANIA 23153), WELTON LEMOS (NOVO 30100), LEANDRO VENTURA (NOVO 30333)
- Deputado Estadual · Direita conservadora: VIVIAN NAVES (REPUBLICANOS 10111), CABO SENNA (MOBILIZA 33190), EDINHO CARVALHO (AGIR 36789) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: WAGNER NETO (SOLIDARIEDADE 77123), KARLOS CABRAL (PSB 40456), VETER MARTINS (PSB 40123) — sorteio entre 4 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações de GO: Aava Santiago teve a perda do mandato de vereadora por infidelidade partidária decretada pelo
TRE-GO em jul/2026, com recurso ao TSE pendente; pela regra de 25/09 só desconta (−2) se a perda for mantida:
**confirmar antes de 04/10**. Veter Martins aparece como investigado no STF só num blog de resumos jurídicos, sem
confirmação (não desconta). Inquérito disciplinar da PM contra Cabo Senna por vídeos políticos, sem sanção, não desconta.


### MA

Pesquisados: 34 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **JUNIOR LOURENÇO** (MDB, Deputado Federal), idoneidade pessoal 2, geral 5.5: Busca rápida na internet (1 busca e fontes conferidas): réu em várias ações penais da gestão como prefeito de Miranda do Norte (TJMA e TRF-1) e denunciado na Operação Laços de Família.
- **NAGIB** (MDB, Deputado Estadual), idoneidade pessoal 4, geral 6.5: Busca rápida na internet (1 busca e fontes conferidas): contas irregulares no TCU (R$ 5,4 milhões, obra inacabada), condenação eleitoral de 2020 mantida pelo TRE-MA e investigação criminal da PGJ (2026) sobre contratos da prefeitura de Codó.
- **ERIC COSTA** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 6, geral 8: condenado pelo TCE-MA a devolver R$ 163 mil (2026) e réu em ação de improbidade do MPMA; ação do MPF e investigações da Seccor sem desfecho encontrado (a confirmar).
- **ANTONIO PEREIRA** (MDB, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e 1 de confirmação): réu em ação penal do MPF por desvio de recursos da Saúde (2011-2013), remetida ao TRF-1 em 2022; situação atual não confirmada.
- **CLEBER VERDE** (MDB, Deputado Federal), idoneidade pessoal 7, geral 8: investigação da PF sobre intermediação de emendas enviada ao STF; absolvido pelo STF em ação antiga sobre aposentadoria fraudulenta no INSS.
- **DANIELLA** (MDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: alvo de busca da PF na Operação Lei do Retorno (desvio de verbas da educação), suspeita de ser beneficiária.
- **EDILAZIO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: indiciado pela PF em 2025 na investigação sobre venda de sentenças no TJMA.
- **COROBA** (CIDADANIA, Deputado Federal), idoneidade pessoal 9, geral 9.5: alvo de procedimento preparatório do MPMA (2024) sobre falta de repasses à Câmara quando era prefeito.
- **ALUISIO MENDES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: relatório da PF de 2022 aponta indícios de peculato e lavagem na campanha (desdobramento da Sermão aos Peixes), sem desfecho encontrado (a confirmar).
- **OTHELINO NETO** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: processo por corrupção e peculato arquivado por habeas corpus; ação antiga por crime de licitação sem desfecho encontrado (a confirmar).
- **HILDO ROCHA** (MDB, Deputado Federal), idoneidade pessoal 9, geral 9: ações de improbidade antigas (contratação sem concurso como prefeito de Cantanhede) sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- FERNANDO FEITOSA (PODE, Deputado Federal): nada confirmado: há um pedido antigo do MPMA de afastamento de oito vereadores de Paço do Lumiar (por atos na cassação do vice-prefeito) em que não foi possível confirmar se ele estava; e críticas de blog à retirada do Diário Oficial do portal da Câmara que ele preside. Não desconta; a confirmar.
- ALUISIO MENDES (REPUBLICANOS, Deputado Federal): relatório da PF de 2022 aponta indícios de peculato e lavagem na campanha (desdobramento da Sermão aos Peixes), sem desfecho encontrado (a confirmar).
- OTHELINO NETO (PSB, Deputado Federal): processo por corrupção e peculato arquivado por habeas corpus; ação antiga por crime de licitação sem desfecho encontrado (a confirmar).
- ERIC COSTA (REPUBLICANOS, Deputado Estadual): condenado pelo TCE-MA a devolver R$ 163 mil (2026) e réu em ação de improbidade do MPMA; ação do MPF e investigações da Seccor sem desfecho encontrado (a confirmar).
- RODRIGO LAGO (PSB, Deputado Estadual): a busca menciona um procedimento investigatório criminal do MPMA no TJMA sem nenhum detalhe; não desconta, a confirmar.
- HILDO ROCHA (MDB, Deputado Federal): ações de improbidade antigas (contratação sem concurso como prefeito de Cantanhede) sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: RAFAEL NEVES (PRD 2512), PÁBLO LIMA (PRD 2533), JULIANA LEITE (PRD 2577) — sorteio entre 4 empatados
- Deputado Federal · Direita conservadora: MICAL DAMASCENO (REPUBLICANOS 1022), COLETIVO UNIÃO (UNIÃO 4467), PEDRO LUCAS FERNANDES (UNIÃO 4444) — sorteio entre 3 empatados
- Deputado Federal · Esquerda progressista: BIRA DO PINDARÉ (PT 1311), GREYSSON CARVALHO (PSB 4050), MARCELO POETA (PSB 4004) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: MANCHINHA (PRD 25111), LAURINDO FREITAS (NOVO 30138), ROBERT LEMOS (NOVO 30222)
- Deputado Estadual · Direita conservadora: ANDRÉ CAMPOS (REPUBLICANOS 10345), FLORENCIO NETO (MDB 15222), DAVI BRANDÃO (MDB 15789) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: RODRIGO LAGO (PSB 40222), CARLOS LULA (PSB 40789), DR. RUBENS (PCDOB 65555)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do MA: Júnior Lourenço (réu em várias ações penais e denunciado na Operação Laços de Família, nota 2) e
Aluísio Mendes saíram da direita federal e abriram uma rodada de reposição com 4 empatados. Francisco Nagib (nota 4)
tem, segundo a imprensa local, inelegibilidade até 2031 por contas irregulares no TCU, mas não está na lista do TCU
cruzada pelo pipeline (conferir o registro). Rodrigo Lago, finalista estadual, aparece com um procedimento
investigatório criminal do MPMA sem nenhum detalhe: **confirmar antes de 04/10**.


### AM

Pesquisados: 48 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **DR RAIONE CABRAL** (AVANTE, Deputado Federal), idoneidade pessoal 3, geral 5.5: Busca rápida na internet (1 busca, 1 de confirmação e fonte conferida): preso preventivamente em 2025, investigado por tentativa de estupro de uma cliente e por tergiversação; investigado por furto de combustível em Coari; presos em flagrante em 2024 por crime eleitoral e por desacato a juiz do TRE-AM.
- **SIDNEY LEITE** (PSD, Deputado Federal), idoneidade pessoal 4, geral 6: Busca rápida na internet (1 busca e 1 de confirmação): réu em ação penal por corrupção eleitoral no TRE-AM; denunciado em 2016 por estupro de vulnerável e tortura (2004), processo sigiloso sem desfecho encontrado (a confirmar); condenado por fake news e multado por propaganda irregular.
- **ABDALA FRAXE** (AVANTE, Deputado Estadual), idoneidade pessoal 6, geral 7: Busca rápida na internet (1 busca e 1 de confirmação): condenação por crime contra a ordem econômica (cartel de combustíveis) confirmada pelo TRF1, com pena em execução mantida pelo STJ.
- **SAULLO VIANNA** (MDB, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca e fontes conferidas): prisão temporária em 2018 com provas anuladas e inquéritos arquivados; alvo de duas operações (PF 2020 e MPAM 2021) sobre licitações em Presidente Figueiredo sem desfecho encontrado (a confirmar); condenado a indenizar o Estado por divulgar informação falsa.
- **ATILA LINS** (PSD, Deputado Federal), idoneidade pessoal 7, geral 7.5: cassação pelo TRE-AM (campanha de 2010) sem efeito, com contas aprovadas pelo TSE; ação civil pública por dano ao erário sem desfecho encontrado (a confirmar).
- **SILAS CÂMARA** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 7, geral 8.5: Busca rápida na internet (1 busca e fontes conferidas): mandato cassado pelo TRE-AM por gastos ilícitos na campanha de 2022, cassação depois anulada pelo próprio TRE-AM (decisão definitiva em 2024); ação penal por rachadinha no STF encerrada por acordo de não persecução penal.
- **PROFESSOR SINÉSIO** (PT, Deputado Estadual), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e fonte conferida): contas de campanha com devolução de R$ 220 mil determinada pelo TRE-AM (2022) e inquérito da PF sobre R$ 20 mil em espécie apreendidos com uma assessora (2024).
- **ADAIL FILHO** (MDB, Deputado Federal), idoneidade pessoal 7, geral 8: alvo principal da operação Dinastia do Lago da PF (set/2026), com inquérito no STF por corrupção e lavagem, e preso temporariamente em 2019 na operação Patrinus, sem desfecho encontrado (a confirmar).
- **ADJUTO AFONSO** (UNIÃO, Deputado Estadual), idoneidade pessoal 7, geral 8: multa definitiva por doação eleitoral acima do limite (2020), impugnação do registro rejeitada pelo TRE-AM (2026) e ordem para retirar 20 publicações da Assembleia (2026).
- **NATALIA** (PSOL, Deputado Federal), idoneidade pessoal 8, geral 9: condenada em ação civil pública do MPAM (inelegível em 2024, segundo a imprensa); instância não confirmada (a confirmar).
- **HISSA ABRAHÃO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca e fonte conferida): ordem do TRE-AM para suspender impulsionamento de vídeo negativo contra adversários (2026) e impugnação do registro em 2018 sem desfecho encontrado (a confirmar). O resumo do buscador citou contas julgadas irregulares no TCE-AM (2013-2014), sem fonte que confirme (não desconta).
- **RODRIGO GUEDES** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: Busca rápida na internet (1 busca e 1 de confirmação): réu por calúnia e difamação contra um colega de Câmara e alvo de outra queixa-crime por crimes contra a honra, ambos sem desfecho encontrado. Uma manchete fala em condenação depois de ele denunciar compra de votos, mas a fonte não pôde ser aberta (a confirmar).
- **JOANA DARC** (UNIÃO, Deputado Federal), idoneidade pessoal 8, geral 8.5: Busca rápida na internet (1 busca e 1 de confirmação): cassação de 1ª instância por fraude à cota de gênero da chapa do PR em 2016, suspensa pelo TRE-AM, sem desfecho encontrado (a confirmar). Pela regra de 26/09, cassação decretada conta mesmo que depois anulada.
- **FAUSTO JR** (UNIÃO, Deputado Federal), idoneidade pessoal 8, geral 8.5: condenado por danos morais ao senador Omar Aziz e multado por propaganda antecipada.
- **CARLINHOS BESSA** (UNIÃO, Deputado Estadual), idoneidade pessoal 8, geral 8.5: PIC do MP Eleitoral por suposta desobediência eleitoral (mesma categoria dos PICs de Roberto Cidade/AM e Tião Bocalom/AC).
- **BRENA DIANNÁ** (UNIÃO, Deputado Estadual), idoneidade pessoal 8, geral 8.5: multas por propaganda irregular e antecipada e pesquisa fraudulenta na campanha de 2024; beneficiária de abuso de poder de um secretário estadual condenado.
- **JOÃO PAULO JANJÃO** (AGIR, Deputado Estadual), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e fonte conferida): ação por fraude à cota de gênero da chapa do Agir em 2024, sem desfecho encontrado (a confirmar).
- **ZÉ RICARDO** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: Busca rápida na internet (1 busca e fonte conferida): ação por fraude à cota de gênero da chapa da federação em 2024, sem desfecho encontrado (a confirmar).
- **THAYSA LIPPY** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: pedido de cassação no TRE-AM rejeitado por unanimidade, com multa por má-fé para a autora (mesma categoria de Lukão/CE e Elcione Barbalho/PA).
- **DR. GOMES** (UNIÃO, Deputado Estadual), idoneidade pessoal 9, geral 9: apuração da Procuradoria Regional Eleitoral sobre consultas médicas com pedido de voto no gabinete, sem desfecho encontrado (a confirmar). A acusação de xenofobia feita pelo sindicato dos médicos em 2020 não virou processo encontrado (sem desconto).
- **RODRIGO SÁ** (PP, Deputado Estadual), idoneidade pessoal 9, geral 9: apuração preliminar do MPAM sobre promoção pessoal com recursos públicos (2026).
- **KENNEDY MARQUES PROTETOR** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: procedimento preparatório do MPAM por suposto nepotismo (2026).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ATILA LINS (PSD, Deputado Federal): cassação pelo TRE-AM (campanha de 2010) sem efeito, com contas aprovadas pelo TSE; ação civil pública por dano ao erário sem desfecho encontrado (a confirmar).
- SIDNEY LEITE (PSD, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): réu em ação penal por corrupção eleitoral no TRE-AM; denunciado em 2016 por estupro de vulnerável e tortura (2004), processo sigiloso sem desfecho encontrado (a confirmar); condenado por fake news e multado por propaganda irregular.
- NATALIA (PSOL, Deputado Federal): condenada em ação civil pública do MPAM (inelegível em 2024, segundo a imprensa); instância não confirmada (a confirmar).
- HISSA ABRAHÃO (REPUBLICANOS, Deputado Federal): Busca rápida na internet (1 busca e fonte conferida): ordem do TRE-AM para suspender impulsionamento de vídeo negativo contra adversários (2026) e impugnação do registro em 2018 sem desfecho encontrado (a confirmar). O resumo do buscador citou contas julgadas irregulares no TCE-AM (2013-2014), sem fonte que confirme (não desconta).
- JOÃO PAULO JANJÃO (AGIR, Deputado Estadual): Busca rápida na internet (1 busca e fonte conferida): ação por fraude à cota de gênero da chapa do Agir em 2024, sem desfecho encontrado (a confirmar).
- CATIANNE ALVES (REPUBLICANOS, Deputado Estadual): nada confirmado: o resumo do buscador citou abandono de cargo e condenação no STF, sem fonte que confirme (não desconta; a confirmar).
- RODRIGO GUEDES (REPUBLICANOS, Deputado Estadual): Busca rápida na internet (1 busca e 1 de confirmação): réu por calúnia e difamação contra um colega de Câmara e alvo de outra queixa-crime por crimes contra a honra, ambos sem desfecho encontrado. Uma manchete fala em condenação depois de ele denunciar compra de votos, mas a fonte não pôde ser aberta (a confirmar).
- ZÉ RICARDO (PT, Deputado Estadual): Busca rápida na internet (1 busca e fonte conferida): ação por fraude à cota de gênero da chapa da federação em 2024, sem desfecho encontrado (a confirmar).
- JOANA DARC (UNIÃO, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): cassação de 1ª instância por fraude à cota de gênero da chapa do PR em 2016, suspensa pelo TRE-AM, sem desfecho encontrado (a confirmar). Pela regra de 26/09, cassação decretada conta mesmo que depois anulada.
- ADAIL FILHO (MDB, Deputado Federal): alvo principal da operação Dinastia do Lago da PF (set/2026), com inquérito no STF por corrupção e lavagem, e preso temporariamente em 2019 na operação Patrinus, sem desfecho encontrado (a confirmar).
- SAULLO VIANNA (MDB, Deputado Federal): Busca rápida na internet (1 busca e fontes conferidas): prisão temporária em 2018 com provas anuladas e inquéritos arquivados; alvo de duas operações (PF 2020 e MPAM 2021) sobre licitações em Presidente Figueiredo sem desfecho encontrado (a confirmar); condenado a indenizar o Estado por divulgar informação falsa.
- DR. GOMES (UNIÃO, Deputado Estadual): apuração da Procuradoria Regional Eleitoral sobre consultas médicas com pedido de voto no gabinete, sem desfecho encontrado (a confirmar). A acusação de xenofobia feita pelo sindicato dos médicos em 2020 não virou processo encontrado (sem desconto).
- THIAGO ABRAHIM (MDB, Deputado Estadual): nada confirmado: há notícia de representação ao MP por suposta autopromoção em Itacoatiara, sem abertura de apuração encontrada (não desconta; a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: RICHARD STONE (NOVO 3067), JOELSON SILVA (AVANTE 7001), DRA. EUNICE NASCIMENTO (AVANTE 7077)
- Deputado Federal · Direita conservadora: JOÃO CARLOS (REPUBLICANOS 1033), AMOM MANDEL (REPUBLICANOS 1000), SAIMON BESSA (UNIÃO 4433)
- Deputado Federal · Esquerda progressista: JOAQUIM FELIPE (PSB 4044), CHRISTIANE MELCHIOR (PSB 4000), LUIS CARLOS VELHO (PT 1363)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: YOMARA LINS (PODE 20123), FELIPE SOUZA (PODE 20000), JONH SILVA (NOVO 30777) — sorteio entre 3 empatados
- Deputado Estadual · Direita conservadora: CATIANNE ALVES (REPUBLICANOS 10321), THIAGO ABRAHIM (MDB 15789), DR. GEORGE LINS (UNIÃO 44666) — sorteio entre 8 empatados
- Deputado Estadual · Esquerda progressista: ZÉ RICARDO (PT 13610), LUIZ CASTRO (PDT 12345), OTACÍLIO NEGREIROS (PDT 12012) — sorteio entre 3 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do AM: **regra nova do usuário (26/09): cassação ou perda de mandato decretada e depois anulada ou revertida
desconta** (`condenacao_revertida`, −2), porque houve apuração e decisão contra o candidato. Aplicada a todos os
registros: Max/RJ (perda de mandato por infidelidade decretada pelo TRE-RJ e revista em 2021, nota 7 → 5) e Silas Câmara (cassação anulada pelo próprio TRE-AM nos embargos, em definitivo em 2024) passou de
"condenação recorrível" para "condenação revertida", nota mantida em 7; Kiko Beloni/SP, Renato Freitas/PR, Eduardo
Bismarck/CE e Átila Lins/AM já estavam assim. Não mudaram: pedidos de cassação ou de perda de mandato nunca decretados
(Livoti/PR, Igor Franco/GO: o MP pediu e o TRE-GO não decretou; ações de cassação rejeitadas seguem −1 como acusação
rejeitada) e Eder Borges/PR, cuja perda de mandato de 2022 decorreu de uma certidão de trânsito emitida por erro na
mesma condenação por difamação que já desconta (contar de novo seria dobrar o mesmo fato). Duas rodadas de reposição
(os descontos de Hissa Abrahão, Janjão, Adail Filho e Saullo Vianna abriram vagas na direita): 48 pesquisados.
Raione Cabral (preso preventivamente em 2025 por tentativa de estupro, nota 3) e Abdala Fraxe (condenação por cartel
de combustíveis confirmada pelo TRF1, nota 6) eram do bloco do topo e saíram.

### ES

Pesquisados: 35 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **FABRÍCIO GANDINI** (PODE, Deputado Estadual), idoneidade pessoal 8, geral 8.5: Busca rápida na internet (1 busca e fontes conferidas): condenado por danos morais ao prefeito de Vitória e multado por conduta vedada (uso de publicidade da prefeitura) na campanha de 2020.
- **PABLO MURIBECA** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: várias multas eleitorais por propaganda antecipada, negativa e fake news, e ação sobre conteúdo falso na campanha de 2024 sem desfecho encontrado (a confirmar). A ordem para não entrar em unidades de saúde da Serra e a denúncia de ex-aliado à PF não descontam.
- **MANATO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: inquérito da PF de 2019 por suposto peculato e rachadinha no gabinete, sem desfecho encontrado (a confirmar). O episódio de extorsão de 2019 teve ele como vítima (sem desconto).
- **DR. VICTOR** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: pedido de cassação do MP Eleitoral em 2022 por uso de evento da Guarda Municipal, sem desfecho encontrado (a confirmar).
- **PAULO NETO** (PODE, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia de ex-assessora à Câmara por rachadinha e funcionários fantasmas (2026), sem desfecho encontrado (a confirmar).
- **KARLA COSER** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: multa por propaganda antecipada com informação falsa e ordem de remover postagem.
- **DAVI ESMAEL** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenação por danos morais a uma servidora revertida no recurso. A representação de 2018 na Corregedoria da Câmara de Vitória é de decoro (sem desconto).
- **ALCÂNTARO FILHO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: condenação por danos morais ao prefeito de Aracruz. Os ex-vereadores de Aracruz condenados por rachid são outros.
- **HILÁRIO ROEPKE GATINHA** (AGIR, Deputado Estadual), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e 1 de confirmação): réu desde 2017 por peculato como prefeito de Santa Maria de Jetibá, sem desfecho encontrado (a confirmar). Denúncia anônima de 2021 sobre perda de vacinas não desconta.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- MANATO (REPUBLICANOS, Deputado Federal): inquérito da PF de 2019 por suposto peculato e rachadinha no gabinete, sem desfecho encontrado (a confirmar). O episódio de extorsão de 2019 teve ele como vítima (sem desconto).
- DR. VICTOR (PSB, Deputado Federal): pedido de cassação do MP Eleitoral em 2022 por uso de evento da Guarda Municipal, sem desfecho encontrado (a confirmar).
- PAULO NETO (PODE, Deputado Estadual): denúncia de ex-assessora à Câmara por rachadinha e funcionários fantasmas (2026), sem desfecho encontrado (a confirmar).
- PABLO MURIBECA (REPUBLICANOS, Deputado Estadual): várias multas eleitorais por propaganda antecipada, negativa e fake news, e ação sobre conteúdo falso na campanha de 2024 sem desfecho encontrado (a confirmar). A ordem para não entrar em unidades de saúde da Serra e a denúncia de ex-aliado à PF não descontam.
- HILÁRIO ROEPKE GATINHA (AGIR, Deputado Estadual): Busca rápida na internet (1 busca e 1 de confirmação): réu desde 2017 por peculato como prefeito de Santa Maria de Jetibá, sem desfecho encontrado (a confirmar). Denúncia anônima de 2021 sobre perda de vacinas não desconta.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: SARGENTO ASSIS (NOVO 3090), GILSON DANIEL (PODE 2000), RENZO MENDES (PODE 2022)
- Deputado Federal · Direita conservadora: DA VITÓRIA (PP 1111), MARCELO SANTOS (UNIÃO 4456), ERICK MUSSO (REPUBLICANOS 1010)
- Deputado Federal · Esquerda progressista: TYAGO HOFFMANN (PSB 4040), FELIPE RIGONI (PSB 4044), LORENA VASQUES (PSB 4056) — sorteio entre 2 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: LEO PINDOBA (PODE 20001), ALEXANDRE XAMBINHO (PODE 20789), MARCOS MADUREIRA (PODE 20456) — sorteio entre 7 empatados
- Deputado Estadual · Direita conservadora: BISPO ALVES (REPUBLICANOS 10123), TONINHO DA EMATER (AGIR 36500), DENNINHO SILVA (UNIÃO 44444) — sorteio entre 3 empatados
- Deputado Estadual · Esquerda progressista: CAMILA VALADÃO (PSOL 50180), FABIO DUARTE (PDT 12789), BRUNO LAMAS (PSB 40011) — sorteio entre 2 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do ES: estado com poucos achados graves; nenhum finalista tem desconto. A rodada de reposição (6 da
direita estadual) veio dos descontos de Pablo Muribeca (multas eleitorais por fake news) e Paulo Neto. Hilário Roepke
(réu desde 2017 por peculato como prefeito, desfecho não encontrado) ficou com −1 "a confirmar", seguindo o precedente
de Beto Richa/PR; não é finalista. Três manchetes de condenação em Vila Velha e Viana eram de outros vereadores
(conferido nas fontes).

### PB

Pesquisados: 27 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ELIZA** (PP, Deputado Federal), idoneidade pessoal 5, geral 7: ré por incitação ao ódio contra a população LGBTQIA+ (denúncia do MPF recebida em 2025) e nova investigação por transfobia (2026).
- **ROMERO RODRIGUES** (PODE, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca e 1 de confirmação): réu na Operação Calvário por suposta propina para a campanha de 2016 em troca da gestão de hospitais municipais; denúncia antiga por declaração falsa ao fisco arquivada pelo TRF-5.
- **AGUINALDO RIBEIRO** (PP, Deputado Federal), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e 1 de confirmação): réu no 'quadrilhão do PP' com ação encerrada pelo STF em 2021 e condenação por improbidade (febre aftosa) cuja instância não se confirmou. Reportagem cita acusação de violência doméstica sem detalhe (a confirmar, não desconta); a TCU o isentou no caso da funcionária fantasma.
- **WILSON SANTIAGO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 7, geral 8.5: réu por corrupção passiva e organização criminosa na Operação Pés de Barro (obra da adutora Capivara).
- **RUY CARNEIRO** (PODE, Deputado Federal), idoneidade pessoal 8, geral 8.5: Busca rápida na internet (1 busca e 1 de confirmação): condenação no caso Desk (1ª instância em 2024, mantida pelo TJPB em 2025) anulada pelo STJ em abril de 2026 por incompetência do juízo.
- **HUGO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: citado por empresário condenado como beneficiário de propina em emenda (sem denúncia) e investigação sobre voo particular arquivada pelo STF (2026). Investigações de parentes não descontam.
- **ADRIANO GALDINO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: condenações por improbidade como prefeito de Pocinhos, instância não confirmada (a confirmar), entre 45 processos segundo a imprensa. A auditoria do TCE sobre salários da filha na Secretaria de Planejamento é sobre a filha (parente, sem desconto).
- **FELIPE LEITÃO** (MDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: condenação por compra de votos em 2008, com recurso sem desfecho encontrado (a confirmar). Pela regra de 26/09, conta mesmo que tenha sido revertida.
- **TIÃO GOMES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: citado em delação da Operação Calvário, sem indiciamento (a PF concluiu que não havia provas).
- **LUIZ COUTO** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: queixas-crime por calúnia rejeitadas pelo STF (mesma categoria de José Nelto/GO).
- **DANIELLE DO VALE** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: ordem do TRE-PB para retirar vídeo em ação por uso da máquina pública (2026).
- **LUCIANO CARTAXO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e 1 de confirmação): operação da PF sobre obras do Parque da Lagoa na gestão dele, sem denúncia ou desfecho confirmados (a confirmar). A ligação política com a Operação Calvário e a AIJE antiga não descontam sem achado pessoal.
- **WILSON FILHO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: inquérito civil do MPF de 2017 e bloqueio de bens junto com o pai em investigação no STF, sem desfecho encontrado (a confirmar).
- **RAONI MENDES** (PSD, Deputado Federal), idoneidade pessoal 9, geral 8.5: condenação eleitoral por doação ilegal em 2010, que levou o TRE-PB a barrar uma candidatura posterior.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- LUCIANO CARTAXO (REPUBLICANOS, Deputado Estadual): Busca rápida na internet (1 busca e 1 de confirmação): operação da PF sobre obras do Parque da Lagoa na gestão dele, sem denúncia ou desfecho confirmados (a confirmar). A ligação política com a Operação Calvário e a AIJE antiga não descontam sem achado pessoal.
- WILSON FILHO (REPUBLICANOS, Deputado Estadual): inquérito civil do MPF de 2017 e bloqueio de bens junto com o pai em investigação no STF, sem desfecho encontrado (a confirmar).
- AGUINALDO RIBEIRO (PP, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): réu no 'quadrilhão do PP' com ação encerrada pelo STF em 2021 e condenação por improbidade (febre aftosa) cuja instância não se confirmou. Reportagem cita acusação de violência doméstica sem detalhe (a confirmar, não desconta); a TCU o isentou no caso da funcionária fantasma.
- ADRIANO GALDINO (REPUBLICANOS, Deputado Estadual): condenações por improbidade como prefeito de Pocinhos, instância não confirmada (a confirmar), entre 45 processos segundo a imprensa. A auditoria do TCE sobre salários da filha na Secretaria de Planejamento é sobre a filha (parente, sem desconto).
- FELIPE LEITÃO (MDB, Deputado Estadual): condenação por compra de votos em 2008, com recurso sem desfecho encontrado (a confirmar). Pela regra de 26/09, conta mesmo que tenha sido revertida.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: DIEGO BRAYTNNER (NOVO 3030), RAONI MENDES (PSD 5533), RUY CARNEIRO (PODE 2030)
- Deputado Federal · Direita conservadora: RANIERY PAULINO (REPUBLICANOS 1015), TIÃO GOMES (REPUBLICANOS 1033), MURILO GALDINO (REPUBLICANOS 1044) — sorteio entre 2 empatados
- Deputado Federal · Esquerda progressista: GERVÁSIO MAIA (PCDOB 6565), FÁBIO CARNEIRO (SOLIDARIEDADE 7722), JAILMA CARVALHO (PSB 4045)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: vazio
- Deputado Estadual · Direita conservadora: DANIELLE DO VALE (REPUBLICANOS 10456), MICHEL HENRIQUE (PP 11011), WILSON FILHO (REPUBLICANOS 10110) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: CHICO MENDES (PSB 40456), CHIÓ (PV 43789), JÔ OLIVEIRA (PCDOB 65000)
- Deputado Estadual · Estatista-autoritário: vazio

Observações da PB: Ruy Carneiro continua finalista (Libertário federal) com nota 8: a condenação de 20 anos no caso
Desk, mantida pelo TJPB em dez/2025, foi anulada pelo STJ em abr/2026 por incompetência do juízo, e conta como
condenação revertida (−2). Saíram do topo Romero Rodrigues (réu na Operação Calvário, nota 6), Eliza Virgínia (ré por
incitação ao ódio contra a população LGBTQIA+, nota 5), Wilson Santiago (réu na Operação Pés de Barro, nota 7) e
Aguinaldo Ribeiro (condenação por improbidade de instância não confirmada, nota 7). Duas rodadas de reposição.

### MT

Pesquisados: 35 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ALTIR PERUZZO** (PT, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca e fonte conferida): condenação por improbidade como prefeito de Juína confirmada pelo TJMT; registro deferido em 2026 por falta de enriquecimento ilícito declarado.
- **FÁBIO GARCIA** (UNIÃO, Deputado Federal), idoneidade pessoal 7, geral 8: alvo da operação Heritage da PF (2026), com bloqueio de bens, e condenado por danos morais a Emanuel Pinheiro. A investigação de um assessor por atuar como falso terapeuta não é contra ele.
- **CAIO CORDEIRO** (NOVO, Deputado Federal), idoneidade pessoal 8, geral 9: condenação por danos morais revertida no recurso e recomendação do MP à Câmara para apurar decoro, sem desfecho encontrado (a confirmar).
- **ELIZEU NASCIMENTO** (NOVO, Deputado Estadual), idoneidade pessoal 8, geral 9: alvo da operação Emenda Oculta (2026) sobre desvio de emendas parlamentares, com dinheiro apreendido e bens bloqueados.
- **JUCA DO GUARANÁ** (PSDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: investigado pela Polícia Civil no caso dos kits agrícolas pagos com emendas (2024).
- **MAYSA LEÃO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: pedido de cassação e inquérito do MP arquivados; queixa-crime por crimes contra a honra extinta.
- **PROFESSORA ROSA NEIDE** (PT, Deputado Federal), idoneidade pessoal 8, geral 8.5: condenada por danos morais por fake news contra deputados; inquérito da Seduc suspenso pelo STF, com as provas anuladas.
- **MAGALY** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: notícia de fato do MPMT sobre contrato da secretaria que chefiava, arquivada sem indícios.
- **ANTERO** (PV, Deputado Federal), idoneidade pessoal 9, geral 9.5: multa por propaganda negativa antecipada e representação por publicações contra Mauro Mendes (2026).
- **VALDENIRIA DUTRA** (PODE, Deputado Estadual), idoneidade pessoal 9, geral 9: apuração do MPMT sobre possível conflito de interesses arquivada por falta de elementos.
- **CRISTIANO BICÔ** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: pedido de cassação por suposta rachadinha arquivado pela Câmara, com cópia enviada ao MP e à polícia (a confirmar).
- **WENDER MADUREIRA FILHO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: boletim de ocorrência por suspeita de violação de domicílio em fiscalização de maus-tratos a animais (2026), sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- CAIO CORDEIRO (NOVO, Deputado Federal): condenação por danos morais revertida no recurso e recomendação do MP à Câmara para apurar decoro, sem desfecho encontrado (a confirmar).
- CRISTIANO BICÔ (REPUBLICANOS, Deputado Estadual): pedido de cassação por suposta rachadinha arquivado pela Câmara, com cópia enviada ao MP e à polícia (a confirmar).
- WENDER MADUREIRA FILHO (REPUBLICANOS, Deputado Federal): boletim de ocorrência por suspeita de violação de domicílio em fiscalização de maus-tratos a animais (2026), sem desfecho encontrado (a confirmar).
- DR.. FLAVIANE RAMALHO (NOVO, Deputado Estadual): nada confirmado: registro deferido pelo TRE-MT sem certidões criminais positivas (vetado só o nome 'Flaviane do Bolsonaro'); um juiz que ela acusou de assédio (2018) afirmou tê-la condenado em 2010 a pagar R$ 60 mil, sem fonte que detalhe o processo (não desconta; a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: CORONEL ROVERI (PODE 2044), GISA BARROS (PODE 2050), DOUTORA DÉBORA (NOVO 3003) — sorteio entre 3 empatados
- Deputado Federal · Direita conservadora: EDUARDO MAGALHÃES (REPUBLICANOS 1023), CESAR LIMA (DEMOCRATA 3522), DR. LEONARDO (REPUBLICANOS 1000) — sorteio entre 3 empatados
- Deputado Federal · Esquerda progressista: JOSÉ ROBERTO (PSOL 5050), MARCELO TERRA (PDT 1222), ANDREIA SCHWARZ (PDT 1230) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: DRA. ANA ROSA JOB (NOVO 30030), MISSIONÁRIA ELAINE BELUSSI (NOVO 30555), DR.. FLAVIANE RAMALHO (NOVO 30022) — sorteio entre 4 empatados
- Deputado Estadual · Direita conservadora: SANDRA DONATO (REPUBLICANOS 10800), ADEMIR DEBORTOLI (REPUBLICANOS 10500), PAULO ARAÚJO (REPUBLICANOS 10456)
- Deputado Estadual · Esquerda progressista: DOUTOR JOSUÉ (PCDOB 65013), CARLOS WAGNER (PV 43456), ROSENWAL RODRIGUES (PV 43123) — sorteio entre 4 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do MT: saíram do topo Altir Peruzzo (improbidade confirmada pelo TJMT, nota 6), Fábio Garcia (alvo da
operação Heritage da PF em 2026, nota 7), Elizeu Nascimento (operação Emenda Oculta, 2026) e Juca do Guaraná
(investigação dos kits agrícolas pagos com emendas), entre outros; uma rodada de reposição com 14 empatados. Flaviane
Ramalho, finalista estadual, tem um "a confirmar" sem desconto (alegação de um juiz sobre condenação cível de 2010).

### RN

Pesquisados: 29 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ROBINSON FARIA** (PP, Deputado Federal), idoneidade pessoal 6, geral 7.5: inelegibilidade por abuso de poder em 2018 decretada pelo TRE-RN e revertida pelo TSE; condenação por improbidade por excesso de gastos com pessoal, instância não confirmada (a confirmar).
- **GALENO TORQUATO** (UNIÃO, Deputado Estadual), idoneidade pessoal 6, geral 7.5: condenação por improbidade confirmada pelo STJ (2026); acordo com confissão proposto para reverter a inelegibilidade.
- **BIANCA NEGREIROS** (UNIÃO, Deputado Federal), idoneidade pessoal 6, geral 7.5: Busca rápida na internet (1 busca e fonte conferida): condenação definitiva por estelionato qualificado na Justiça Federal, que barrou a candidatura a prefeita de Mossoró em 2020 (situação de elegibilidade atual a confirmar).
- **TAVEIRA JÚNIOR** (PSDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: condenação de 1ª instância por improbidade como servidor fantasma na Câmara de Parnamirim, com recurso.
- **JOÃO MAIA** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: denunciado pelo MPF em 2018 no caso do Dnit/BR-101, sem recebimento ou desfecho encontrados (a confirmar).
- **MARLEIDE CUNHA** (PT, Deputado Federal), idoneidade pessoal 9, geral 9: ação de cassação por fraude à cota rejeitada pelo TRE-RN (mesma categoria de Lukão/CE).
- **EZEQUIEL** (PSDB, Deputado Estadual), idoneidade pessoal 9, geral 9: absolvido pelo STF de corrupção passiva por falta de provas.
- **ROBSON CARVALHO** (UNIÃO, Deputado Estadual), idoneidade pessoal 9, geral 9: multa por propaganda antecipada mantida pelo TRE-RN.
- **UBALDO FERNANDES** (PV, Deputado Estadual), idoneidade pessoal 9, geral 9.5: multa por propaganda antecipada em outdoors. O pedido de perda de mandato por infidelidade (2019) foi negado pelo TRE-RN (sem desconto).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ROBINSON FARIA (PP, Deputado Federal): inelegibilidade por abuso de poder em 2018 decretada pelo TRE-RN e revertida pelo TSE; condenação por improbidade por excesso de gastos com pessoal, instância não confirmada (a confirmar).
- JOÃO MAIA (PP, Deputado Federal): denunciado pelo MPF em 2018 no caso do Dnit/BR-101, sem recebimento ou desfecho encontrados (a confirmar).
- ISOLDA DANTAS (PT, Deputado Estadual): nada que desconte: um blog questionou pagamentos da verba de gabinete a aliados na campanha de 2022 (recibos em vez de notas), sem apuração formal encontrada (a confirmar); a operação no Detran afastou um indicado dela, não ela.
- BIANCA NEGREIROS (UNIÃO, Deputado Federal): Busca rápida na internet (1 busca e fonte conferida): condenação definitiva por estelionato qualificado na Justiça Federal, que barrou a candidatura a prefeita de Mossoró em 2020 (situação de elegibilidade atual a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: RAPHAEL FERREIRA (NOVO 3000), APOLLIANE SOUZA (AVANTE 7010), DRA ROSEMARIA (PSDB 4566) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: JOÃO MAIA (PP 1111), BENES LEOCÁDIO (UNIÃO 4444), PAULINHA GALDINO (PP 1122) — sorteio entre 2 empatados
- Deputado Federal · Esquerda progressista: DR. BERNARDO (PV 4300), DRA GLEUCE LEITE (PSB 4013), RAPOSINHA (PCDOB 6513) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: CRISTIANE DANTAS (PSDB 45555), DRA KARINA PEREIRA (PSDB 45666), ERIKO JÁCOME (PSDB 45111)
- Deputado Estadual · Direita conservadora: KLEBER RODRIGUES (PP 11999), NEILTON DIÓGENES (PP 11111), CLOVIS JUNIOR (MDB 15000)
- Deputado Estadual · Esquerda progressista: UBALDO FERNANDES (PV 43222), DIVANEIDE BASÍLIO (PT 13613), ISOLDA DANTAS (PT 13123) — sorteio entre 4 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do RN: saíram do topo Robinson Faria (inelegibilidade de 2018 revertida pelo TSE e improbidade de instância
não confirmada, nota 6), Galeno Torquato (improbidade confirmada pelo STJ em 2026, nota 6) e Bianca Negreiros
(condenação definitiva por estelionato qualificado, nota 6). João Maia segue finalista com −1 "a confirmar" (denúncia
do MPF de 2018 no caso do Dnit sem recebimento ou desfecho encontrados): **confirmar antes de 04/10** se possível.

### PI

Pesquisados: 36 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **MERLONG SOLANO** (PT, Deputado Federal), idoneidade pessoal 5, geral 7: réu por peculato no caso das cisternas e condenado em 1ª instância por improbidade por contratações sem concurso, com recurso.
- **DR. GIL CARLOS** (PT, Deputado Estadual), idoneidade pessoal 6, geral 7.5: réu na operação Topique (transporte escolar) e acordo com o MP para encerrar apuração de improbidade como prefeito.
- **RUBENS VIEIRA** (PT, Deputado Estadual), idoneidade pessoal 7, geral 8: réu na Justiça Federal por fraude em licitação como prefeito de Cocal. Numa ação por calúnia ele foi a vítima.
- **GEORGIANO** (PSD, Deputado Federal), idoneidade pessoal 8, geral 8: réu em ação de improbidade de R$ 6,9 milhões ainda sem julgamento.
- **FLORENTINO NETO** (PT, Deputado Federal), idoneidade pessoal 8, geral 8.5: condenação por improbidade por contratações sem concurso na saúde, instância não confirmada (a confirmar).
- **FRANZÉ SILVA** (PT, Deputado Federal), idoneidade pessoal 8, geral 8.5: ação de improbidade do MPPI (2024) pela nomeação de um condenado por homicídio na Assembleia.
- **FÁBIO XAVIER** (PT, Deputado Estadual), idoneidade pessoal 8, geral 8.5: inquérito da PF por apropriação de verba de candidatura laranja em 2018.
- **JULIO ARCOVERDE** (PP, Deputado Federal), idoneidade pessoal 9, geral 9: mencionado em investigação da Polícia Civil enviada ao STF por foro, sem ser formalmente investigado.
- **GRACINHA MÃO SANTA** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: multa por conduta vedada na eleição municipal de 2024 em Parnaíba.
- **ANA PAULA** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia antiga do MP como ex-prefeita de Sebastião Leal, sem desfecho encontrado (a confirmar). No caso do relógio furtado ela é a vítima.
- **CEL CARLOS AUGUSTO** (MDB, Deputado Estadual), idoneidade pessoal 9, geral 9: ação de improbidade antiga por negar informações sobre licitações da PM, sem desfecho encontrado (a confirmar).
- **EVALDO GOMES** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: indiciado por falsificar documento nas contas de 2014, caso encerrado por acordo com o MP Eleitoral.
- **FÁBIO NOVO** (PT, Deputado Estadual), idoneidade pessoal 9, geral 9: inquérito da PF sobre a Secretaria de Cultura arquivado pelo TRF1.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- FLORENTINO NETO (PT, Deputado Federal): condenação por improbidade por contratações sem concurso na saúde, instância não confirmada (a confirmar).
- ANA PAULA (MDB, Deputado Estadual): denúncia antiga do MP como ex-prefeita de Sebastião Leal, sem desfecho encontrado (a confirmar). No caso do relógio furtado ela é a vítima.
- CEL CARLOS AUGUSTO (MDB, Deputado Estadual): ação de improbidade antiga por negar informações sobre licitações da PM, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: DRA. KARINE BONFIM (NOVO 3022), DRA. DANIELLE PESSOA (PODE 2026), DR. GILBERTO MOREIRA (PODE 2000)
- Deputado Federal · Direita conservadora: ALAN OSÓRIO (REPUBLICANOS 1099), MARCOS AURÉLIO (MDB 1511), CASTRO NETO (MDB 1515)
- Deputado Federal · Esquerda progressista: DR. FRANCISCO (PT 1313), FLÁVIO NOGUEIRA (PT 1312), ZÉ SANTANA (PT 1311)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: MARDEN MENEZES (PSD 55456), ANTÔNIO MUNIZ (PSDB 45666), ZÉ OSMAR (PSD 55777) — sorteio entre 3 empatados
- Deputado Estadual · Direita conservadora: SEVERO EULÁLIO (MDB 15101), PASTOR GESSIVALDO ISAIAS (MDB 15789), HENRIQUE PIRES (MDB 15123)
- Deputado Estadual · Esquerda progressista: FIRMINO PAULO (PT 13789), LIMMA (PT 13123), HÉLIO RODRIGUES (PT 13678) — sorteio entre 5 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do PI: estado com muitos achados no topo da esquerda (PT), que saíram da lista: Merlong Solano (réu por
peculato no caso das cisternas e improbidade de 1ª instância, nota 5), Dr. Gil Carlos (réu na operação Topique, nota 6),
Rubens Vieira (réu por fraude em licitação, nota 7), Florentino Neto, Franzé Silva e Fábio Xavier. Nenhum finalista tem
desconto.

### AL

Pesquisados: 29 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ISNALDO BULHÕES JR** (MDB, Deputado Federal), idoneidade pessoal 4, geral 6.5: Busca rápida na internet (1 busca e 1 de confirmação): réu por falso e desvio de verba da Assembleia; condenação por improbidade na Taturana de situação não confirmada (a confirmar); investigação no STF arquivada e citação no caso Master.
- **DR JOÃO NETO** (SOLIDARIEDADE, Deputado Federal), idoneidade pessoal 4, geral 6.5: condenação por violência doméstica mantida pelo TJAL e registro de candidatura indeferido pelo TRE-AL (2026).
- **MARX BELTRÃO** (UNIÃO, Deputado Federal), idoneidade pessoal 8, geral 8.5: absolvido pelo STF de falsidade ideológica e réu por calúnia contra o primo, sem desfecho encontrado.
- **RAFAEL BRITO** (MDB, Deputado Federal), idoneidade pessoal 8, geral 8.5: Busca rápida na internet (1 busca e 1 de confirmação): ação de cassação pelo Bolsa Escola 10 rejeitada pelo TRE-AL e ordem judicial contra fake news sobre o prefeito de Maceió. A ligação com a operação Capa Dura (livros didáticos) é sobre uma empresa, não sobre ele.
- **CHICO FILHO** (PSDB, Deputado Federal), idoneidade pessoal 9, geral 9: multa do TCE-AL como presidente da Câmara de Maceió (2026; multa de tribunal de contas = −1). A ação do antigo partido por infidelidade ainda não foi decidida (sem desconto).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ISNALDO BULHÕES JR (MDB, Deputado Federal): Busca rápida na internet (1 busca e 1 de confirmação): réu por falso e desvio de verba da Assembleia; condenação por improbidade na Taturana de situação não confirmada (a confirmar); investigação no STF arquivada e citação no caso Master.
- MESAQUE PADILHA (PP, Deputado Estadual): nada confirmado: o resumo do buscador citou contas de campanha de 2022 aprovadas com ressalvas e devolução de valor, sem fonte que confirme (não desconta; a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: CAL MOREIRA (PSDB 4577), KELMANN VIEIRA DE OLIVEIRA (PSDB 4545), JOÃO UCHÔA (NOVO 3003) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: DANIEL BARBOSA (PP 1155), DELEGADO FABIO COSTA (PP 1190), OLIVIA TENORIO (PP 1133)
- Deputado Federal · Esquerda progressista: HELO BEZERRA (SOLIDARIEDADE 7777), AFRANIO NETO (SOLIDARIEDADE 7717), NECO (PV 4343) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: CÉSAR FELIZARDO (PSDB 45999), LÉO LOUREIRO (PSDB 45222), LUCAS BARBOSA (PSDB 45888) — sorteio entre 2 empatados
- Deputado Estadual · Direita conservadora: DUDU RONALSA (MDB 15333), DAVID DO EMPREGO (UNIÃO 44555), INACIO LOIOLA (MDB 15345) — sorteio entre 5 empatados
- Deputado Estadual · Esquerda progressista: MARCOS BARBOSA (PT 13333), TARCIZO FREIRE (PV 43456), SILVIO CAMELO (PV 43123)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do AL: saíram do topo Isnaldo Bulhões Jr. (réu por falso e desvio de verba da Assembleia, condenação na
Taturana de situação não confirmada, nota 4) e Dr. João Neto (condenado por violência doméstica, registro indeferido
pelo TRE-AL, nota 4). **Correção no pipeline:** Afrânio de Mendonça Alves Neto (Solidariedade 7717) tem dois registros
no TSE e ocupava duas das três vagas da esquerda federal, porque um dos nomes completos tem espaço duplo e escapava da
remoção de pessoas duplicadas em `pipeline/recomendar.py`; a chave agora ignora espaços repetidos (só esse caso no país).

### DF

Pesquisados: 40 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **HERMETO** (MDB, Deputado Distrital), idoneidade pessoal 5, geral 7: indiciado por rachadinha pela PCDF; condenação por homofobia anulada pelo TJDFT; condenado a indenizar casal homoafetivo.
- **DANIEL DONIZET** (MDB, Deputado Federal), idoneidade pessoal 7, geral 8: Busca rápida na internet (1 busca e 1 de confirmação): denunciado pelo MPDFT por assédio sexual e obstrução de justiça (2025) e alvo de pedidos de cassação na CLDF sem desfecho encontrado.
- **WELLINGTON LUIZ** (MDB, Deputado Distrital), idoneidade pessoal 7, geral 8: absolvido de peculato pelo TJDFT e cassação de 2011 revertida pelo TSE (conta pela regra de 26/09).
- **ROLLEMBERG** (PSB, Deputado Federal), idoneidade pessoal 8, geral 9: multa por propaganda negativa em 2018 e ação de improbidade antiga sobre renúncia fiscal sem desfecho encontrado (a confirmar).
- **MATHEUS MILANEZ** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: acusado de violência doméstica, com medida protetiva concedida pelo TJDFT (2026); renunciou à candidatura em 15/08/2026 (ainda consta no arquivo do TSE usado pelo site).
- **WILKER LEÃO** (NOVO, Deputado Federal), idoneidade pessoal 9, geral 9.5: condenado por calúnia e difamação contra professor da UnB (crime contra a honra = −1).
- **RAFAEL PRUDENTE** (MDB, Deputado Federal), idoneidade pessoal 9, geral 9: ação de improbidade suspensa sobre programa de incentivo fiscal, sem desfecho encontrado (a confirmar). A menção a réu no caso Caixa de Pandora não se confirmou (pode ser do pai, Leonardo Prudente).
- **JULIO CESAR** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e 1 de confirmação): absolvido na operação Drácon (2025), com recurso do MP.
- **PROFESSOR ISRAEL** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: denúncia de desvio em emendas dele analisada pelo MPDFT, sem desfecho encontrado (a confirmar).
- **PROF. REGINALDO VERAS** (PV, Deputado Federal), idoneidade pessoal 9, geral 9.5: citado como réu por corrupção passiva em levantamento antigo sobre a CLDF, sem desfecho encontrado (a confirmar).
- **BISPO RENATO ANDRADE** (REPUBLICANOS, Deputado Distrital), idoneidade pessoal 9, geral 9.5: Busca rápida na internet (1 busca e 1 de confirmação): absolvido na operação Drácon (2025), com recurso do MP.
- **FRED LINHARES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: citado na operação Korban da PF por emendas a entidade investigada, sem ser alvo formal encontrado.
- **FÁBIO FELIX** (PSOL, Deputado Federal), idoneidade pessoal 9, geral 9.5: inquérito da PCDF arquivado por falta de provas. A prisão de uma assessora e a versão da PM sobre suposta interferência dele (2026) não geraram apuração encontrada contra ele.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- RAFAEL PRUDENTE (MDB, Deputado Federal): ação de improbidade suspensa sobre programa de incentivo fiscal, sem desfecho encontrado (a confirmar). A menção a réu no caso Caixa de Pandora não se confirmou (pode ser do pai, Leonardo Prudente).
- ROLLEMBERG (PSB, Deputado Federal): multa por propaganda negativa em 2018 e ação de improbidade antiga sobre renúncia fiscal sem desfecho encontrado (a confirmar).
- PROFESSOR ISRAEL (PSB, Deputado Federal): denúncia de desvio em emendas dele analisada pelo MPDFT, sem desfecho encontrado (a confirmar).
- PROF. REGINALDO VERAS (PV, Deputado Federal): citado como réu por corrupção passiva em levantamento antigo sobre a CLDF, sem desfecho encontrado (a confirmar).
- DAYSE AMARILIO (PSB, Deputado Distrital): nada confirmado: o TRE-DF apontou indícios preliminares de irregularidade nas contas da campanha de 2022; resultado do julgamento não confirmado (não desconta; a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: ROBERTO FREIRE (CIDADANIA 2323), MAYARA NORONHA (PODE 2027), WILKER LEÃO (NOVO 3000) — sorteio entre 4 empatados
- Deputado Federal · Direita conservadora: JULIO CESAR (REPUBLICANOS 1010), LUIZ EDUARDO (REPUBLICANOS 1000), REIS COLETIVO SEGURANÇAPRIVADA (DEMOCRATA 3577) — sorteio entre 4 empatados
- Deputado Federal · Esquerda progressista: ROLLEMBERG (PSB 4040), PROF. REGINALDO VERAS (PV 4343), CARLA GEHLEN (PSB 4007)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Distrital · Libertário: DRA.TÂNIA SOSTER (NOVO 30555), DR JACINTO (NOVO 30007), CRIS MOURÃO (NOVO 30303) — sorteio entre 8 empatados
- Deputado Distrital · Direita conservadora: DELEGADA DOUTORA JANE (REPUBLICANOS 10555), IOLANDO (MDB 15000), MARTINS MACHADO (REPUBLICANOS 10123)
- Deputado Distrital · Esquerda progressista: GABRIEL MAGNO (PT 13131), RICARDO VALE (PT 13013), JACY AFONSO (PT 13001) — sorteio entre 3 empatados
- Deputado Distrital · Estatista-autoritário: vazio

Observações do DF: a operação Drácon terminou em absolvição em 1ª instância (mar/2025) de Celina Leão, Julio Cesar e
Bispo Renato, com recurso do MP (−1 cada). Wellington Luiz teve a cassação de 2011 revertida pelo TSE e passa a
descontar pela regra de 26/09. Saíram do topo Hermeto (indiciado por rachadinha e condenação por homofobia anulada,
nota 5), Daniel Donizet (denunciado por assédio sexual, nota 7) e Matheus Milanez (medida protetiva por violência
doméstica; renunciou à candidatura em 15/08, mas ainda consta no arquivo do TSE). Reginaldo Veras segue finalista com
−1 "a confirmar" (apontado como réu por corrupção passiva em levantamento antigo).

### MS

Pesquisados: 37 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ZECA DO PT** (PT, Deputado Estadual), idoneidade pessoal 6, geral 7.5: condenação colegiada na 'Farra da Publicidade' com efeitos suspensos desde 2022. Ele também obteve indenização do Estado por conduta de promotores (vítima, sem desconto).
- **MAURICIO PICARELLI** (PRD, Deputado Federal), idoneidade pessoal 8, geral 8.5: condenação de 1ª instância por improbidade por acumular mandato e direção de TV. Dívidas e execuções privadas (inclusive com empresário que ele acusa de golpe) não descontam; a anulação da aposentadoria atingiu vários ex-deputados.
- **BETO PEREIRA** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 8, geral 9: contas de prefeito de Terenos julgadas irregulares pelo TCE-MS com ressarcimento (ressarcimento de tribunal de contas = −2).
- **CAMILA JARA** (PT, Deputado Federal), idoneidade pessoal 8, geral 8.5: ação por abuso de poder rejeitada pelo TRE-MS e multa por propaganda antecipada (2026). A representação no Conselho de Ética da Câmara pelo tumulto em plenário é de decoro (sem desconto).
- **CHICÃO VIANNA** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: réu em ação civil pública do MPMS com pedido de ressarcimento. A ação do PSB pelo mandato (infidelidade) foi extinta a pedido do próprio partido (sem desconto).
- **GERALDO RESENDE** (UNIÃO, Deputado Federal), idoneidade pessoal 9, geral 9: inquérito antigo da operação Uragano sobre propina em emendas, sem desfecho encontrado (a confirmar).
- **MARQUINHOS TRAD** (PV, Deputado Federal), idoneidade pessoal 9, geral 9.5: denunciado por crimes sexuais contra sete mulheres e absolvido (2022 e 2024).
- **HERCULANO BORGES** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 9, geral 9.5: citado em interceptações da operação Gutemberg, sem ser alvo formal encontrado.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- GERALDO RESENDE (UNIÃO, Deputado Federal): inquérito antigo da operação Uragano sobre propina em emendas, sem desfecho encontrado (a confirmar).
- ALAN GUEDES (PP, Deputado Federal): nada que desconte: contratos da gestão dele em Dourados com a editora investigada na operação Gutenberg estão sob apuração, mas os documentos não o apontam como investigado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: PROFESSOR JUARI (PSDB 4599), MIRIAM GIMENEZ (NOVO 3060), CESAR ALVES (PRD 2550)
- Deputado Federal · Direita conservadora: NETO SANTOS (REPUBLICANOS 1012), ALAN GUEDES (PP 1155), JURANDIR MACHADO (AGIR 3666) — sorteio entre 2 empatados
- Deputado Federal · Esquerda progressista: ANA SARAVY (PV 4300), MARQUINHOS TRAD (PV 4333), JEFFERSOM MARECCO (PDT 1234) — sorteio entre 4 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: EDUARDO ROCHA (PSDB 45123), WALKIRIA SILVA (NOVO 30999), THIAGO LOUREIRO (NOVO 30077) — sorteio entre 4 empatados
- Deputado Estadual · Direita conservadora: PEDROSSIAN NETO (REPUBLICANOS 10000), ANTONIO VAZ (REPUBLICANOS 10123), HERCULANO BORGES (REPUBLICANOS 10888) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: GILMAR GARCIA (PV 43123), LUIZA RIBEIRO (PT 13700), IDEVALDO CLAUDINO (PT 13300) — sorteio entre 4 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do MS: saíram do topo Zeca do PT (condenação colegiada na "Farra da Publicidade" com efeitos suspensos,
nota 6), Beto Pereira (contas irregulares no TCE-MS com ressarcimento), Maurício Picarelli e Chicão Vianna; uma rodada de
reposição com 16. Marquinhos Trad segue finalista com −1 (absolvido das acusações de crimes sexuais em 2022 e 2024) e
Herculano Borges com −1 (citado em interceptações da operação Gutemberg). Gilmar Garcia, finalista estadual, teria
desistido da candidatura segundo a imprensa, mas ainda consta no arquivo do TSE.

### SE

Pesquisados: 26 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **GUSTINHO RIBEIRO** (PP, Deputado Federal), idoneidade pessoal 5, geral 7: condenação por improbidade confirmada pelo TJSE (subvenções sociais a aliados), com acordo de não persecução cível em homologação provisória; impugnação do registro de 2026 rejeitada pelo TRE-SE.
- **LUCIANO BISPO** (PSD, Deputado Estadual), idoneidade pessoal 6, geral 7: condenação por improbidade confirmada em 2ª instância, que levou o TSE a negar o registro de 2018.
- **FÁBIO REIS** (PSD, Deputado Federal), idoneidade pessoal 8, geral 8: denúncia por desobediência eleitoral julgada improcedente pelo STF e apuração de 2020 sobre cota parlamentar sem desfecho encontrado (a confirmar).
- **THIAGO DE JOALDO** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9, geral 9.5: preso na operação Castelo de Cartas, processo arquivado em 2018.
- **ROBSON VIANA** (PSB, Deputado Federal), idoneidade pessoal 9, geral 9.5: réu por peculato em caso antigo da Câmara de Aracaju, sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- FÁBIO REIS (PSD, Deputado Federal): denúncia por desobediência eleitoral julgada improcedente pelo STF e apuração de 2020 sobre cota parlamentar sem desfecho encontrado (a confirmar).
- ROBSON VIANA (PSB, Deputado Federal): réu por peculato em caso antigo da Câmara de Aracaju, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: DRA. JEANNE LIMA (CIDADANIA 2333), DELEGADA KATARINA (PSD 5505), NETO BATALHA (PSD 5588)
- Deputado Federal · Direita conservadora: GRACINHA GARCEZ (REPUBLICANOS 1012), ALBERTO MACEDO (REPUBLICANOS 1044), THIAGO DE JOALDO (REPUBLICANOS 1011) — sorteio entre 2 empatados
- Deputado Federal · Esquerda progressista: ELBER BATALHA (PSB 4010), GLEIDOALDO (SOLIDARIEDADE 7766), WALDIR RODRIGUES (PCDOB 6513)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: MAISA MITIDIERI (PSD 55555), JORGINHO ARAUJO (PSD 55777), ADAILTON MARTINS (PSD 55123)
- Deputado Estadual · Direita conservadora: GEORGEO PASSOS (REPUBLICANOS 10777), NETINHO GUIMARÃES (UNIÃO 44777), ANDERSON DE TUCA (UNIÃO 44123) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: LINDA BRASIL (PSOL 50180), PAULO JR (PV 43777), KITTY LIMA (PSB 40400)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do SE: saíram do topo Gustinho Ribeiro (improbidade confirmada pelo TJSE, com acordo de não persecução cível
em homologação provisória, nota 5), Luciano Bispo (improbidade confirmada, registro negado pelo TSE em 2018, nota 6) e
Fábio Reis. Thiago de Joaldo segue finalista com −1 (preso na operação Castelo de Cartas, processo arquivado em 2018).

### RO

Pesquisados: 29 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **DRA ROSANGELLA CIPRIANNO** (PSB, Deputado Federal), idoneidade pessoal 4, geral 7: condenação criminal confirmada pelo TRF1 (crimes previdenciários) e registro indeferido pelo TRE-RO, com recurso anunciado ao TSE.
- **GISLAINE LEBRINHA** (PRD, Deputado Estadual), idoneidade pessoal 8, geral 8.5: denunciada por concussão e lavagem como prefeita, caso remetido ao STF.
- **RAFAEL FERA** (PODE, Deputado Federal), idoneidade pessoal 9, geral 9: multa por desinformação na campanha de 2024, mantida pelo TRE-RO.
- **DR SANTANA** (UNIÃO, Deputado Estadual), idoneidade pessoal 9, geral 9: pedidos de cassação por violência política de gênero (2026), sem desfecho encontrado (a confirmar). A disputa sobre a saída do PRD não desconta.
- **ADA DANTAS BOABAID** (PRD, Deputado Federal), idoneidade pessoal 9, geral 9: condenada por danos morais a uma professora, decisão confirmada pelo TJRO.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- AIRTON GURGACZ (PDT, Deputado Federal): nada confirmado: uma fonte antiga cita investigação da PF sobre o Detran quando ele era vice-governador e diretor do órgão, sem detalhe (não desconta; a confirmar).
- ADALTO DE BANDEIRANTES (REPUBLICANOS, Deputado Estadual): nada que desconte: segundo o advogado dele, não é réu na ação por fraude à cota de gênero do PSB em Porto Velho citada nas redes (a confirmar).
- DR SANTANA (UNIÃO, Deputado Estadual): pedidos de cassação por violência política de gênero (2026), sem desfecho encontrado (a confirmar). A disputa sobre a saída do PRD não desconta.

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: CRISTIANE LOPES (PODE 2022), ADRIANA MARTINS (NOVO 3030), RAFAEL FERA (PODE 2090)
- Deputado Federal · Direita conservadora: DRA AMÁLIA MILANI (UNIÃO 4455), MAURÍCIO CARVALHO (UNIÃO 4444), DRA. VERA PAIXÃO (REPUBLICANOS 1001) — sorteio entre 3 empatados
- Deputado Federal · Esquerda progressista: DRA POLLYANNA MAYARA (PSB 4030), AIRTON GURGACZ (PDT 1233), WELISON NUNES (SOLIDARIEDADE 7722) — sorteio entre 2 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: LUCAS FOLLADOR (NOVO 30300), PEDRO GEOVAR (NOVO 30234), JOAO MENDES (PODE 20022) — sorteio entre 4 empatados
- Deputado Estadual · Direita conservadora: ÉLITON COSTA (REPUBLICANOS 10800), ADALTO DE BANDEIRANTES (REPUBLICANOS 10500), RAFAEL LOPES (MDB 15123)
- Deputado Estadual · Esquerda progressista: CLÁUDIA DE JESUS (PT 13123), ANDRÉ DO SINDICATO (PT 13111), FRANCIMAR SIMÃO EFICAZ CONTAB (PT 13456)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do RO: saíram do topo Rosangela Cipriano (condenação por crimes previdenciários confirmada pelo TRF1 e
registro indeferido pelo TRE-RO, nota 4) e Gislaine Lebrinha (denunciada por concussão e lavagem, caso no STF). Rafael
Fera segue finalista com −1 (multa por desinformação na campanha de 2024). **Armadilha nova:** o resumo do buscador
repetiu, para vários candidatos sem relação entre si (Catianne/AM, Cristiane Lopes, Anderson Pereira, Dr. Gilber e
Pedro Geovar/RO), o mesmo texto sobre "abandono de cargo e condenação no STF por coação", sem fonte; foi descartado em
todos os casos.

### TO

Pesquisados: 30 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **RICARDO AYRES** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 5, geral 7.5: alvo da operação Fames-19 da PF (inquérito no STF), condenação do TCE anulada e pedido do MP Eleitoral de indeferimento do registro de 2026 sem desfecho encontrado (a confirmar).
- **NILTON FRANCO** (UNIÃO, Deputado Estadual), idoneidade pessoal 6, geral 7.5: condenação por improbidade desfeita pelo TJTO e alvo de operação da PF com R$ 900 mil em espécie apreendidos.
- **IVORY DE LIRA** (PCDOB, Deputado Estadual), idoneidade pessoal 6, geral 8: condenado em 1ª instância por lavagem de dinheiro (com recurso) e investigado na operação Fames-19.
- **PROFESSORA JANAD VALCARI** (PP, Deputado Federal), idoneidade pessoal 7, geral 8: inquérito civil do MPTO sobre a empresa dos Barões da Pisadinha e emendas (2024); AIJE de 2024 e processo antigo por fraude em licitação sem desfecho encontrado (a confirmar).
- **TOINHO ANDRADE** (PSDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: investigado por peculato (rachadinha) na Assembleia do Tocantins, com indiciamento em 2019 e quebra de sigilo recente.
- **JORGE FREDERICO** (PSDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: investigado na operação Fames-19, com veículos apreendidos.
- **OLYNTHO** (MDB, Deputado Estadual), idoneidade pessoal 8, geral 8.5: inquérito antigo sobre funcionários fantasmas sem desfecho encontrado (a confirmar) e absolvição no TRE-TO no caso dos R$ 500 mil.
- **IVANILSON MARINHO** (UNIÃO, Deputado Estadual), idoneidade pessoal 9, geral 9: denúncia anônima ao MPTO arquivada por falta de provas.

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- RICARDO AYRES (REPUBLICANOS, Deputado Federal): alvo da operação Fames-19 da PF (inquérito no STF), condenação do TCE anulada e pedido do MP Eleitoral de indeferimento do registro de 2026 sem desfecho encontrado (a confirmar).
- OLYNTHO (MDB, Deputado Estadual): inquérito antigo sobre funcionários fantasmas sem desfecho encontrado (a confirmar) e absolvição no TRE-TO no caso dos R$ 500 mil.
- PROFESSORA JANAD VALCARI (PP, Deputado Federal): inquérito civil do MPTO sobre a empresa dos Barões da Pisadinha e emendas (2024); AIJE de 2024 e processo antigo por fraude em licitação sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: GEOVANE DOS SANTOS (PSDB 4567), CRYS FRAGA (NOVO 3003), TIAGO DIMAS (PODE 2088)
- Deputado Federal · Direita conservadora: EULA ANGELIM (DEMOCRATA 3511), JOÃO DANTAS (DEMOCRATA 3535), FABIO VAZ (REPUBLICANOS 1020)
- Deputado Federal · Esquerda progressista: VIVI SOUZA (PSB 4033), CÉLIO MOURA (PT 1313), GABRIELLE BORGES (PDT 1221) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: SILVANEY RABELO (PRD 25111), PROFESSOR JUNIOR GEO (PSDB 45123), EDNA GOMES (NOVO 30321)
- Deputado Estadual · Direita conservadora: ELENIL DA PENHA (REPUBLICANOS 10115), DR. VINICIUS PIRES (REPUBLICANOS 10010), VALDEMAR JÚNIOR (MDB 15015) — sorteio entre 4 empatados
- Deputado Estadual · Esquerda progressista: LAMARCK (PV 43111), EDY CESAR (PT 13000), TERCILIANO GOMES (SOLIDARIEDADE 77123)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do TO: a operação Fames-19 (desvio de cestas básicas pagas com emendas na pandemia) atinge vários
deputados do bloco do topo; saíram Ricardo Ayres (alvo da PF, inquérito no STF, nota 5), Ivory de Lira (condenado em 1ª
instância por lavagem e investigado na Fames-19, nota 6), Nilton Franco (condenação por improbidade desfeita e R$ 900 mil
apreendidos pela PF, nota 6), Jorge Frederico, Toinho Andrade, Olyntho e Janad Valcari. Nenhum finalista tem desconto.

### AC

Pesquisados: 37 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ANTÔNIA LÚCIA** (MDB, Deputado Federal), idoneidade pessoal 4, geral 6.5: condenação por peculato confirmada pelo TRF-1 e registro de 2026 indeferido pelo TRE-AC.
- **FAGNER CALEGARIO** (UNIÃO, Deputado Estadual), idoneidade pessoal 6, geral 7.5: condenação de 1ª instância por plágio em concurso e ação civil pública ambiental. A PF não atribuiu a ele o dinheiro apreendido nas operações Ptolomeu IV e Umbra (2026), sem desconto.
- **CLODOALDO RODRIGUES** (PP, Deputado Estadual), idoneidade pessoal 7, geral 8: condenação de 1ª instância por compra de votos em 2022 (recorrível) e impugnação do registro de 2026 rejeitada pelo TRE-AC.
- **KELEN BOCALOM** (PSDB, Deputado Federal), idoneidade pessoal 9, geral 9: apuração preliminar do MPAC sobre a nomeação dela pelo marido prefeito (nepotismo), sem desfecho encontrado.
- **TCHÊ** (PDT, Deputado Estadual), idoneidade pessoal 9, geral 9: réu por compra de votos em 2010, denúncia recebida pelo TRE-AC em 2013, sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- TCHÊ (PDT, Deputado Estadual): réu por compra de votos em 2010, denúncia recebida pelo TRE-AC em 2013, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: FERNANDO MELO (PODE 2000), KELEN BOCALOM (PSDB 4545), DELEGADO JUDSON (NOVO 3079) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: SOCORRO NERI (PP 1101), CORONEL ULYSSES (UNIÃO 4422), FÁBIO ARAÚJO (MDB 1511)
- Deputado Federal · Esquerda progressista: ANDRÉ KAMAI (PT 1313), TAILON SILAS (PSB 4040), PERPÉTUA ALMEIDA (PCDOB 6513) — sorteio entre 3 empatados
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: EMERSON JARUDE (NOVO 30000), DR SILVANO SANTIAGO (NOVO 30700), BENÍCIO DIAS (NOVO 30852)
- Deputado Estadual · Direita conservadora: TADEU HASSEM (REPUBLICANOS 10456), MARIA ANTONIA (PP 11133), ANTONIA SALES (MDB 15122) — sorteio entre 12 empatados
- Deputado Estadual · Esquerda progressista: TCHÊ (PDT 12123), DR. MÁRCIO ANDRÉ (PDT 12555), EDNEY BATALHA (PDT 12333) — sorteio entre 3 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do AC: saíram Antônia Lúcia (peculato confirmado pelo TRF-1 e registro indeferido, nota 4), Fagner
Calegário (condenado em 1ª instância por plágio em concurso e réu em ação ambiental, nota 6) e Clodoaldo Rodrigues
(condenado em 1ª instância por compra de votos, nota 7). Dois finalistas têm desconto leve: Kelen Bocalom (apuração do
MPAC sobre a nomeação dela pelo marido prefeito, nota 9) e Tchê (denúncia por compra de votos de 2010 recebida em 2013,
sem desfecho encontrado, a confirmar antes de 04/10). A ação do MDB pelo mandato de Eber Machado (infidelidade) ainda
não foi decidida, sem desconto pela regra.

### AP

Pesquisados: 32 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **ROBERTO GÓES** (UNIÃO, Deputado Estadual), idoneidade pessoal 2, geral 5.5: condenação no STF com pena prescrita, condenação por peculato anulada pelo Plenário e ação de improbidade em curso.
- **MAX DA AABB** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 4, geral 7: condenação transitada no TSE por compra de votos em 2018, com inelegibilidade até 07/10/2026; desistiu da candidatura de 2026.
- **EDNA AUZIER** (PV, Deputado Estadual), idoneidade pessoal 5, geral 7.5: cassação por compra de votos em 2022 mantida no TSE, com efeitos suspensos por liminar do STF (set/2026), e registro de 2026 deferido.
- **ALINE GURGEL** (UNIÃO, Deputado Federal), idoneidade pessoal 6, geral 7.5: alvo da operação Cícero da PF por compra de votos (desfecho não encontrado, a confirmar), contas de 2018 desaprovadas e AIJE por abuso rejeitada.
- **ALDILENE SOUZA** (PDT, Deputado Estadual), idoneidade pessoal 7, geral 8: condenação por abuso de poder em 2018 anulada pelo STF (provas anuladas) e impugnação do registro de 2026 retirada pelo MP Eleitoral.
- **LEDA SADALA** (PSD, Deputado Federal), idoneidade pessoal 8, geral 8: AIJE por abuso de poder julgada improcedente e contas rejeitadas pelo TCE-PA como gestora em Parauapebas.
- **RAYFRAN BEIRÃO** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: alvo da operação Vinculum da PF (servidores fantasmas na Assembleia, 2025). Absolvição no TSE em processo de cassação citada só em rede social, sem desconto.
- **HILDEGARD GURGEL** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: alvo da operação Cícero da PF por compra de votos, sem desfecho encontrado (a confirmar).
- **DAYSE MARQUES** (REDE, Deputado Estadual), idoneidade pessoal 9, geral 8.5: investigada em AIJE do MP Eleitoral com a prefeita de Amapá, sem desfecho encontrado (a confirmar).

**A confirmar (sinal sem confirmação; não descontou ou descontou só o que se confirmou):**

- ALINE GURGEL (UNIÃO, Deputado Federal): alvo da operação Cícero da PF por compra de votos (desfecho não encontrado, a confirmar), contas de 2018 desaprovadas e AIJE por abuso rejeitada.
- HILDEGARD GURGEL (REPUBLICANOS, Deputado Estadual): alvo da operação Cícero da PF por compra de votos, sem desfecho encontrado (a confirmar).
- DAYSE MARQUES (REDE, Deputado Estadual): investigada em AIJE do MP Eleitoral com a prefeita de Amapá, sem desfecho encontrado (a confirmar).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: ALEXANDRE AZEVEDO (PODE 2055), LUIZ ALEX (PSD 5544), BETH GARCIA (NOVO 3065) — sorteio entre 2 empatados
- Deputado Federal · Direita conservadora: MEIRE SALVIANO (MISSÃO 1401), LUIZ CARLOS (UNIÃO 4456), CRISTIANO FURLAN (UNIÃO 4400) — sorteio entre 4 empatados
- Deputado Federal · Esquerda progressista: JESUS PONTES (PDT 1234), JOSENILDO (PDT 1212), PROFESSORA MARCIVÂNIA (PCDOB 6565)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: ELENICE (PODE 20200), R NELSON (PODE 20193), JOÃO MENDONÇA (PODE 20800)
- Deputado Estadual · Direita conservadora: TELMA NERY (REPUBLICANOS 10000), JAIME PEREZ (REPUBLICANOS 10789), CAROL MONTEIRO (MDB 15000) — sorteio entre 2 empatados
- Deputado Estadual · Esquerda progressista: PASTOR OLIVEIRA (PDT 12147), FABRICIO FURLAN (REDE 18000), JACK JK (PDT 12222)
- Deputado Estadual · Estatista-autoritário: vazio

Observações do AP: saíram Roberto Góes (condenado pelo STF com pena prescrita, condenação por peculato anulada e
improbidade em curso, nota 2), Max da AABB (inelegível até 07/10/2026 por compra de votos, desistiu da candidatura,
nota 4), Edna Auzier (cassação por compra de votos mantida no TSE e suspensa por liminar do STF, nota 5), Aline
Gurgel e o marido Hildegard Gurgel (alvos da operação Cícero da PF), Aldilene Souza (condenação de 2018 anulada),
Rayfran Beirão (operação Vinculum), Leda Sadala e Dayse Marques. Nenhum finalista tem desconto. Parentes com
problemas (irmãos Furlan, irmão de Jack JK) não descontam, pela regra.

### RR

Pesquisados: 32 candidatos (1 busca cada, mais confirmações quando houve sinal grave).

**Achados que descontaram na busca:**

- **CHICO MOZART** (PP, Deputado Estadual), idoneidade pessoal 6, geral 7.5: condenação por compra de votos confirmada pelo TRE-RR em 2023.
- **GENILSON COSTA** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 7, geral 8.5: cassação de 1ª instância por compra de votos em 2024 (em recurso) e ação penal por tráfico trancada pelo STJ.
- **ADJALMA** (PODE, Deputado Federal), idoneidade pessoal 8, geral 8.5: perda do mandato de vereador por infidelidade partidária decretada pelo TSE em 2024.
- **TAYLA PERES** (REPUBLICANOS, Deputado Estadual), idoneidade pessoal 8, geral 9: alvo da operação Testa de Ferro da PF por lavagem de dinheiro (2026).
- **GABRIEL MOTA** (UNIÃO, Deputado Federal), idoneidade pessoal 8.5, geral 8.75: condenação por danos morais em juizado especial e controvérsia sobre suposta funcionária fantasma no gabinete.
- **ROBERTA ACIOLY** (REPUBLICANOS, Deputado Federal), idoneidade pessoal 9.5, geral 9.75: gastos da cota parlamentar com empresas ligadas a aliados políticos. O marido é investigado pela PF por fraude na saúde (parente, sem desconto).

**Finalistas depois da busca** (todos pesquisados):

- Deputado Federal · Libertário: RAY KLEBER (PODE 2077), DRA. MAISE (PODE 2034), WELLINGTON BRASIL (NOVO 3030)
- Deputado Federal · Direita conservadora: MARCOS JORGE (REPUBLICANOS 1011), ROBERTA ACIOLY (REPUBLICANOS 1044), ZÉ HAROLDO CATHEDRAL (UNIÃO 4455) — sorteio entre 3 empatados
- Deputado Federal · Esquerda progressista: ROBERT DAGON (PSOL 5005), JANDERSON BARBOSA (PDT 1212), JOENIA WAPICHANA (PT 1333)
- Deputado Federal · Estatista-autoritário: vazio
- Deputado Estadual · Libertário: RENATO SILVA (PODE 20100), LEILA CASTRO (NOVO 30123), IURI BANCÁRIO (NOVO 30369)
- Deputado Estadual · Direita conservadora: DR. CLÁUDIO CIRURGIÃO (REPUBLICANOS 10111), IDAZIO DA PERFIL (UNIÃO 44115), JORGE EVERTON (UNIÃO 44444) — sorteio entre 7 empatados
- Deputado Estadual · Esquerda progressista: MARCELO NUNES (PDT 12345), DR. GEISEL (PV 43777), RÔMULO BRAZ (PT 13777) — sorteio entre 3 empatados
- Deputado Estadual · Estatista-autoritário: vazio

Observações do RR: saíram Chico Mozart (compra de votos confirmada pelo TRE-RR, nota 6), Genilson Costa (cassado em 1ª
instância por compra de votos, nota 7), Adjalma (perda do mandato de vereador por infidelidade decretada pelo TSE, nota
8), Tayla Peres (operação Testa de Ferro da PF) e Gabriel Mota. Uma finalista tem desconto leve: Roberta Acioly
(gastos da cota parlamentar com empresas de aliados, controvérsia sem apuração, nota 9,5). O deputado de Roraima com
cassação por compra de votos mantida pelo TSE em abr/2026 é Renan Bekel, que não está entre os pesquisados.

## Reconferência dos finalistas "a confirmar" (26/09, tarde)

Todos os finalistas do país com desconto ou sinal "a confirmar" foram reconferidos (1 a 2 buscas cada, mais DataJud
quando havia classe e tribunal conhecidos):

- **Aava Santiago/GO** (federal, Esquerda): a perda do mandato de vereadora por infidelidade foi decretada pelo TRE-GO
  (6 a 1, 27/07/2026) e está em recurso no TSE. Como a perda decretada vale −2 tanto se mantida (regra de 25/09) quanto
  se revertida (regra de 26/09), o desconto não depende do recurso: nota 10 → 8, saiu da lista. Entraram Adedy
  Santana (nada encontrado) e, no bloco, Rubens Otoni (multa por propaganda antecipada e citação no caso Cachoeira
  arquivada, nota 8).
- **Catianne Alves/AM**: o "abandono de cargo e condenação no STF" do resumo do buscador foi conferido e a página
  trata de outra pessoa; marcação "a confirmar" retirada (nota 10).
- **Aline e Hildegard Gurgel/AP** (não finalistas): a operação Cícero é de 2019-2020, então vale a regra de processo
  antigo sem desfecho (−1, a confirmar) em vez de investigação em curso (−2): notas 6 → 7 e 8 → 9.
- **Sem mudança (desfecho continua não encontrado):** Tchê/AC (denúncia de 2013 no TRE-AC; o DataJud não traz a ação
  originária), Kelen Bocalom/AC (apuração do MPAC sem notícia de desfecho), Zé Ricardo/AM (ação por fraude à cota de
  gênero ainda sem julgamento), Rollemberg/DF (improbidade de 2016), Reginaldo Veras/DF, João Maia/RN (denúncia da
  Via Trajana, 2018), Wilson Filho/PB, Veter Martins/GO (só um blog automático de resumos do STF; sem desconto),
  Rodrigo Lago/MA e Airton Gurgacz/RO (sem desconto), Roberta Acioly/RR (controvérsia de gastos, −0,5).

## 2ª rodada: busca pelo nome completo nos 10 estados mais populosos (26/09, em andamento)

Pedido do usuário (26/09): mais uma rodada de pesquisa individual dos finalistas, só nos 10 maiores estados (SP, MG,
RJ, BA, PR, RS, PE, CE, PA, SC), um estado depois do outro. Método: 1 busca nova por finalista, com o **nome completo**
do registro no TSE (a 1ª rodada usou o nome de urna) e termos diferentes (improbidade, ação civil, Ministério Público,
TCE, TRE, multa), mais confirmação quando aparece sinal. Os achados novos se **somam** aos da 1ª rodada
(`ferramentas/busca_finalistas/aplicar_rodada2.py`; o registro ganha `rodada2`). Para não punir só quem teve a busca
extra, quem entra na lista no lugar de um finalista também passa pelas duas rodadas antes de o estado fechar
(`finalistas.py UF --sem-rodada2` lista quem falta). As mesmas regras de classificação acima valem para a 2ª rodada.

- **SP** (18 finalistas na 2ª rodada + 17 empatados novos na 1ª): saíram Sâmia Bomfim (multa do TRE-SP por desinformação, set/2026, nota 9) e Cris Monteiro (denúncia por lesão corporal leve em juizado especial pela briga na Câmara, a confirmar, nota 9). No bloco de 23 empatados da Esquerda federal: Gilson de Souza (improbidade transitada, 6), Vicentinho e Paulo Teixeira (processos antigos sem desfecho e contas, 8), Raul Marcelo (crime contra a honra, 9), Zarattini (inquéritos arquivados/suspensos, 9), Alencar Santana (contas de 2022, 9). Entraram Alexis Fonteyne e Nabil Bonduki (nada nas duas rodadas).
- **MG** (18 finalistas na 2ª rodada + 1 empatado novo na 1ª): saiu Gilberto Abramo (citado pela PF como autor formal de
  emendas atribuídas a Eduardo Cunha, 2026, a confirmar, nota 9). Entrou Pedro Aihara (nada nas duas rodadas). Iza
  Lourença: o Jusbrasil lista processos no TRE-MG com o nome, sem nenhum processo ou sanção identificada (sem desconto).
- **RJ** (18 finalistas): nenhum achado novo; a lista não mudou. Luiz Lima, Júlia Casamasso, Pastor Henrique, Carlos
  Macedo, Librelon e Lilian Behring aparecem em listagens de processos (Jusbrasil/Escavador, a maioria eleitorais), sem
  nenhum processo ou sanção identificada (sem desconto).
- **BA** (18 finalistas): nenhum achado novo; a lista não mudou. Lídice da Mata (278 processos listados no Jusbrasil, a
  maioria no TRE-BA) e Militão Dourado aparecem em listagens de processos sem nenhum processo ou sanção identificada.
- **Faltam:** PR, RS, PE, CE, PA e SC.

## Situação e próximos passos

- **Estados fechados (27 de 27):** SP (64 pesquisados), MG (44), RJ (43), BA (29), PR (44), RS (41), PE (45), CE (30), PA (37),
  SC (36), GO (30), MA (34), AM (48), ES (35), PB (27), MT (35), RN (29), PI (36), AL (29), DF (40), MS (37), SE (26), RO (29), TO (30), AC (37), AP (32), RR (32). Total: 979 candidatos, 276 com achado que descontou e 102 marcados "a confirmar". Nos 27, todos os finalistas foram pesquisados e nenhum
  empatado ficou de fora.
- **Infidelidade partidária (decisão do usuário, 25/09):** Evandro Roman/PR perdeu o mandato de deputado federal por
  decisão do TSE em 2021 por trocar de partido sem justa causa. O usuário decidiu tratar a perda de mandato decretada e
  mantida como cassação (−2); pedidos não decididos ou negados continuam sem desconto; desde 26/09, perda decretada e
  depois revertida vale −2 como condenação revertida (Max/RJ: perda decretada pelo TRE-RJ em 2020-2021 e revista em
  ago/2021, nota 7 → 5) (Gilberto Abramo,
  Flávia Borja, Ronaldo Tannús/MG e Livoti/PR seguem como estavam).
- **Achados mais graves:** Euclydes Pettersen/MG (2 ações penais e indiciamento no caso do INSS, nota 2), Lucas
  Cardoso/SP (condenação por estelionato confirmada pelo TJSP e registro impugnado, nota 4), Luiz Fernando Faria/MG
  (réu na Lava Jato, nota 6), Renato Freitas/PR (condenação por pichação com recurso, cassação de 2022 revertida,
  réu por crime contra a honra e parecer de cassação em 2026, nota 4), Júnior Lourenço/MA (réu em várias ações penais da gestão como prefeito, nota 2), Francisco Nagib/MA (TCU,
  condenação eleitoral de 2020 e investigação da PGJ, nota 4), Iran Lima/PA (improbidade confirmada e mandato cassado pelo TSE em 2020, nota 4), Antônio Doido/PA (alvo da PF
  e declarado inelegível em 1ª instância, nota 6), Silvio Costa Filho/PE (réu em 4 ações
  criminais dos 'shows fantasmas', nota 4), Romero Albuquerque/PE (investigado por agressão e invasão de domicílio e 3
  multas eleitorais, nota 4), João Paulo/PE (condenação criminal de 1ª instância e ressarcimento de R$ 18 mi ao TCE,
  nota 5), Beto Richa/PR (8 ações penais extintas ou sem
  desfecho e condenação em ação popular, nota 6), Roberto Carlos/BA (condenado pelo TJ-BA por rachadinha, nota 6), Luiz Martins/RJ (réu na
  Furna da Onça, nota 7). Todos saíram da lista de finalistas.
- **A confirmar com prioridade** (sinal grave sem confirmação, sem desconto): Jhony Sasaki/SP (ação de rachadinha
  contra ex-presidente da Câmara de São Vicente) e Leandro Basson/SP (processo "Justiça Pública x" em 2025). Nenhum
  dos 10 "a confirmar" está entre os finalistas atuais, mas Sasaki e Basson estão no bloco empatado do Libertário
  estadual de SP: se o sorteio mudar e um deles entrar, confirmar antes de publicar.
- **Busca concluída nos 27 estados em 26/09/2026.** Próximo passo sugerido: reconferir, antes de 04/10, os
  finalistas com desconto "a confirmar" (ver as seções de cada estado).
- **Publicação por estado.** SP, MG e RJ publicados em 25/09, depois BA, PR, RS, PE, CE, PA, SC, GO, MA, AM, ES, PB, MT, RN, PI, AL, DF, MS, SE, RO, TO, AC, AP e RR (junto com a correção dos caciques, que vale para
  todos os estados). A cada estado novo: rodar `exportar_prototipo`, acrescentar a UF na frase de "Limites" em
  `site/app.js` ("Nos estados já concluídos (...)"), conferir numa cópia do site sem o GA e publicar.
- **Ferramentas para continuar:** `ferramentas/busca_finalistas/` (listar pendentes, gravar resultados, rodar o
  pipeline, gerar a seção do relatório).
