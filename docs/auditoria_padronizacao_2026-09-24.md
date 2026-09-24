# Auditoria de padronização — Presidente, Senador e Governador (24/09/2026)

Pedido: garantir que a pesquisa individual (busca na internet) dos candidatos a Presidente, Senador e Governador
está padronizada e coerente. Ordem: Presidente → Senador → Governador (estados mais populosos primeiro).

**Estado: tudo local, nada commitado nem publicado.** As alterações estão em `data/reference/*.json`
(e no parquet regenerado). Para descartar tudo: `git checkout data/reference`.

## Como a auditoria foi feita

1. **Checagem automática** de todos os registros (script de auditoria, sem internet):
   nota gravada × nota recalculada pelas tabelas de `pipeline/pesos.py`; achados sem fonte; texto do `motivo`
   citando pesos diferentes das categorias; palavras suspeitas na descrição (ex.: "arquivado" numa categoria de
   investigação em curso; "réu" numa categoria de simples citação); caciques do círculo político comparados com a
   **composição oficial da coligação no TSE** (`DS_COMPOSICAO_COLIGACAO` do `consulta_cand_2026`); a mesma pessoa
   com pendências diferentes em registros diferentes.
2. **Checagem na web** só onde a auditoria achou divergência ou dúvida de status (não foi refeita a pesquisa de
   todos os 534 candidatos).
3. Correções aplicadas com as mesmas categorias de `pesos.py`; cada registro alterado ganhou prefixo
   `AUDITORIA 2026-09-24:` ou `PADRONIZADO em 2026-09-24` no `motivo`, com a nota antiga → nova.

---

## 1. Regra dos caciques (círculo político) — afeta os três cargos

### Problema encontrado

A mesma regra ("presidente do próprio partido + presidentes dos partidos da coligação") foi aplicada de três
jeitos diferentes:

| Cargo | Federações listadas na coligação | Partidos aliados diretos |
|---|---|---|
| Governador | contadas em 70 de 78 casos | quase sempre contados |
| Senador | contadas em 9 de 140 casos | **frequentemente esquecidos** (ex.: Deltan Dallagnol sem o PL; Angelo Coronel sem PL, PP e União; Simone Tebet sem PT/PDT/REDE; Elizeu Aguiar registrado "sem coligação", mas o TSE mostra NOVO/AVANTE) |
| Presidente | não contadas (Lula) | PDT de Lula e AGIR de Augusto Cury esquecidos; **DC de Clariana Barão esquecido** (presidente do DC tem condenação confirmada, −4) |

Além disso, **o mesmo presidente de partido tinha pendências diferentes** conforme o registro:

| Partido (presidente) | Como estava | Padronizado para | Por quê |
|---|---|---|---|
| PSD (Kassab) | réu −2 em 34 registros; "condenação confirmada" −4 em 11 (Governador) | réu em ação penal, −2 | a condenação por improbidade (precatórios de 2006) é de 1ª instância (2014), desfecho do recurso não localizado; a outra ação de precatórios terminou em absolvição mantida pelo TJSP (2019). Não há condenação confirmada localizada. |
| MDB (Baleia Rossi) | investigado −1 em 23; "não verificado" 0 em 21 (Governador) | investigado sem denúncia, −1 | é citado em inquérito sigiloso no STF desde 2018; o caso Alba Branca foi arquivado |
| PSDB (Aécio Neves) | 0 em 24; −1 em 9 | investigação arquivada sem denúncia, −1 | mesmo critério de Edinho Silva/PT (inquérito trancado = −1, pela tabela `PESOS_CACIQUE`); Aécio teve o INQ 4830 arquivado (2024) e foi absolvido no caso J&F (TRF-3, unânime). O "precedente 0" contrariava a tabela. |
| MISSÃO (Renan Santos) | −1, −2 (condenação civil) e −2 (réu ação civil) | ação civil em curso, −1 | a condenação dele é cível por danos morais (R$ 4 mil), não improbidade; a ação do MPF está em curso |
| PODE (Renata Abreu) | −1 em 33; 0 em 1 | investigado, −1 | — |
| PRD | Leonardo Avalanche (que é do PRTB!) em 2 registros de Senador; "não verificado" nos demais | Marcus Vinícius Neskau, investigado −1 | erro de pessoa; Neskau foi afastado da presidência do PTB por Alexandre de Moraes (INQ 4874, 2022) — pesquisado agora |
| PCdoB | "não verificado" | Nádia Campeão (presidente em exercício), nada encontrado, 0 | Luciana Santos (licenciada, ministra) tem condenação por improbidade em 1ª instância (2019, em recurso) — anotada, não contada por estar licenciada |
| CIDADANIA | "presidência em disputa", 0 | Roberto Freire (restituído pela Justiça), não verificado, 0 | — |
| PL (Valdemar) | dois rótulos diferentes, ambos −4 | condenação criminal confirmada, −4 | só rótulo |

### Regra única aplicada

- Caciques = presidente **nacional** de cada partido da coligação **segundo o TSE**, **incluindo os membros das
  federações** listadas na coligação e da federação do próprio candidato (federação atua como um partido só na
  eleição). Continua o teto de −4 para a soma dos caciques.
- Pendência de cada presidente: **uma linha por partido**, agora gravada em `liderancas_partidarias.json`
  (campo `cacique`), igual em todos os registros.
- Partido que estava no registro mas **não está na coligação oficial** fica listado com `contado: false`
  (ex.: PODE no registro de Eduardo Paes; NOVO/PODE/PSDB no de Tarcísio).
- Presidente de partido que já está na chapa (Kassab vice de Caiado; Suêd Haidar vice de Grassi) não é contado duas vezes.
- Quando o **próprio candidato preside o partido** (Rui Costa Pimenta, Renan Santos, Avalanche, Edmilson Costa,
  Aécio), o círculo recebe o mesmo desconto de cacique que qualquer candidato do partido. Isso substitui descontos
  "adicionais" feitos à mão que variavam de −2 a −8.
- Removidos os descontos adicionais de "contas rejeitadas do PCO" (−2/−3 em 4 governadores e Rui): contas do
  partido não descontam de nenhum outro partido (PSTU teve DRAPs negados por contas e nunca descontou).
  Mantidos os −2 de instabilidade de chapa (Garotinho, Policial Edjane), que estão na regra escrita.
- Mantido de propósito: Washington Reis (presidente estadual do MDB-RJ e irmão da vice) no círculo de Eduardo Paes
  (não muda a nota, que já está no teto).

**Efeito: 284 registros de círculo reescritos, 164 com nota diferente** (lista completa na seção 6). A maior parte
é Senador caindo para 6 (teto de caciques) porque as coligações grandes quase sempre incluem PL, DC, PSD ou REDE.

⚠ **Decisão sua:** a inclusão dos membros de federação foi a escolha mais coerente com o que Governador já fazia
e com a lei (federação = um partido). Se preferir o contrário (não contar federação):
`python -m pipeline.padronizar_caciques --aplicar --sem-federacao` refaz tudo com a outra regra (a simulação dá
111 notas de círculo diferentes do estado atual).

⚠ **Deputados não foram mexidos** (fora do pedido), mas a tabela deles (`circulo_partidos_estrutural.json`) ainda
tem os valores antigos para PSDB (0), MISSÃO (−2), PRD e PCdoB (não verificados). Para ficar coerente com os
majoritários seria preciso atualizá-la (muda círculo de deputados do PSDB, PRD e MISSÃO).

---

## 2. Presidente (14 candidatos)

Todos os 14 têm idoneidade; 13 têm círculo (Marçal fora da disputa). Profundidade de pesquisa: aprofundada.

### Idoneidade pessoal

| Candidato | Nota | Mudança |
|---|---|---|
| Leonardo Avalanche (PRTB) | 4 → **5** | Os três crimes (associação criminosa, violência política de gênero, dados falsos) estão **numa única denúncia do MP-SP** e numa só ação penal; a regra conta réu **por processo** (−3), não por crime. A investigação da PF sobre desvio de R$ 750 mil do fundo eleitoral, que estava só no texto, virou achado próprio (−2). |
| Rui Costa Pimenta (PCO) | 6 → **8** | As contas rejeitadas do PCO (partido) descontavam −2 na nota pessoal dele; a categoria de contas é para contas de campanha do candidato e nenhum outro dirigente/candidato é descontado por contas do partido. Fica a investigação da PF (−2). |
| Flávio Bolsonaro (PL) | 7 (igual) | Só texto: o motivo dizia −3 para a investigação do caso Master, mas a categoria vale −2. |

Sem mudança: Lula (5), Caiado (6), Zema (8), Renan Santos (7), Marçal (3, fora da disputa) e os seis com nota 10
(Edmilson Costa, Augusto Cury, Hertz Dias, Samara, Wilson Grassi, Clariana Barão — "nada encontrado", não atestado).

Status de registro conferido: o TSE indeferiu Marçal (11/09); os demais seguem na disputa.

### Círculo político

| Candidato | Nota | Motivo |
|---|---|---|
| Lula (PT) | 4 → **1** | Coligação oficial: PSB, PDT, Federação Brasil da Esperança (PT/PCdoB/PV), Federação PSOL-REDE. Entram Lupi/PDT (−1) e Lamac/REDE (−2) além de Edinho (−1) e Dirceu (padrinho, −5). |
| Clariana Barão (DC) | 10 → **6** | Faltava o presidente do próprio partido: João Caldas (DC), condenação por improbidade confirmada (−4). |
| Avalanche (PRTB) | 2 → **8** | Tinha um desconto adicional de −8 que repetia a nota pessoal; agora recebe o desconto de cacique do PRTB (−2), igual a qualquer candidato do PRTB. |
| Rui Costa Pimenta (PCO) | 7 → **9** | Adicional de −3 (contas do PCO) substituído pelo cacique do PCO (−1). |
| Renan Santos (MISSÃO) | 7 → **9** | Adicional de −3 substituído pelo cacique da MISSÃO (−1). |

Correção de texto: condenação de Jair Bolsonaro datada "11/09/2026" → **11/09/2025**.

---

## 3. Senador (319 candidatos, 27 UFs)

314 com idoneidade (os 5 sem nota são duplicados/fora da disputa, como já registrado); Comandante Ribeiro Afonso (RJ)
tem só idoneidade (registro indeferido). Profundidade: rápida (1–2 buscas por candidato).

### Círculo político

É onde a padronização mais mexeu: **a maioria das notas de Senador caiu** porque os presidentes dos partidos
aliados não tinham sido contados (seção 1). Exemplos: Simone Tebet 10 → 6, Deltan Dallagnol 10 → 6 (PL na
coligação), Angelo Coronel 10 → 6, Aécio Neves 10 → 8, Helder 5 → 2, Ciro Nogueira 10 → 6. Candidatos da MISSÃO
subiram de 8 para 9 (cacique padronizado em −1). Lista completa na seção 6.

Checagem cruzada da mesma pessoa em vários registros (vices, suplentes, padrinhos): **sem divergência**
(a única diferença, Jair Bolsonaro contado para Flávio e não contado para Tarcísio, é intencional e explicada).

Observação sem correção: suplentes só foram pesquisados quando apareceram "de graça" na busca — a maioria tem
"nada encontrado". É uma assimetria de método (vice de Governador foi pesquisado sempre), não de peso.

### Idoneidade pessoal — casos parecidos com pesos diferentes (corrigidos)

| Candidato | Nota | O que mudou |
|---|---|---|
| **Wilson Lima (UNIÃO/AM)** | 8 → **5** | A busca rasa registrou só a busca e apreensão de 2021 "sem desfecho conhecido", mas ele é **réu no STJ desde 20/09/2021** (APn 993, respiradores comprados de loja de vinhos: organização criminosa, fraude em licitação, peculato); em set/2026 o STJ ainda julga recursos processuais. |
| Eduardo Gomes (PL/TO) | 8 → 9 | A PF **pediu** abertura de inquérito, sem notícia de abertura. Mesmo critério de Alfredo Gaspar e Renato Casagrande: pedido de inquérito = apuração preliminar (−1); inquérito aberto = −2. |
| Cid Gomes (PSB/CE) | 9 → 8 | Alvo de busca da PF (Colosseum, 2021) sem denúncia nem arquivamento conhecido = investigação em curso (−2), como Rose de Freitas, Ciro Nogueira, Mauro Mendes. O "−1 pela idade" era exceção fora da tabela (Ciro Gomes/Governador recebe a mesma correção). |
| Guilherme Derrite (PP/SP) | 8 → 9 | Os inquéritos por mortes em operações da ROTA não viraram denúncia: investigação encerrada = −1 (como Fufuca, Chico Rodrigues, Humberto Costa), não −2 de investigação em curso. |
| Capitão Wagner (UNIÃO/CE) | 7 → 8 | Ordem judicial para remover vídeos sem provas é infração eleitoral leve (−1), como Manuela D'Ávila e Eli Borges — não investigação (−2). |
| Manuela D'Ávila (PCdoB/RS) | 8 (igual) | Só rótulo (remoção de desinformação: "infração eleitoral leve"). |
| Acir Gurgacz (PDT/RO) | 4 → **0** | Faltava a própria condenação: 4 anos e 6 meses pelo STF (2018), pena cumprida em semiaberto (−5, como Lula e João Rodrigues). Já estava fora do funil pela inelegibilidade. |

### Status de registro atualizado (web)

| Candidato | Nota | Situação |
|---|---|---|
| Helder (MDB/PA) | 8 (igual) | O TRE-PA **deferiu** o registro por unanimidade em 14/09 (a pesquisa só tinha o pedido da Procuradoria) → sai o "registro contestado" (−2). Entraram os 2 inquéritos da pandemia (respiradores, Para Bellum) **arquivados** pelo STJ (−1 cada), que a busca rasa não pegou. |
| Deltan Dallagnol (NOVO/PR) | 8 (igual) | Segue sub judice: TSE confirmou a suspensão da campanha por 5×2 (21/09); TRE-PR manteve o registro nos embargos (23/09); TSE deve julgar o mérito até 25/09. **Reconferir.** |

### Amostra de incumbentes com nota 10 (limite da busca rasa)

Conferi 4 nomes experientes de estados grandes com nota 10; **3 tinham achados que faltavam**:

| Candidato | Nota | Achado que faltava |
|---|---|---|
| Jaques Wagner (PT/BA) | 10 → 9 | Operação Cartão Vermelho (busca da PF em 2018, Arena Fonte Nova) — arquivada em fev/2025 sem denúncia. |
| Eduardo da Fonte (PP/PE) | 10 → 8 | Réu na Lava Jato em 2018 e absolvido pelo Plenário do STF em 2022; outra denúncia rejeitada em 2016. |
| Pedro Paulo (PSD/RJ) | 10 → 9 | Inquérito por agressão à então esposa, arquivado em 2016 a pedido da PGR. |
| Esperidião Amin (PP/SC) | 10 (igual) | Nada encontrado. |

⚠ Isso confirma que **nota 10 de Senador é "nada encontrado em 1–2 buscas"**, não ficha limpa. Os três achados
acima são leves (acusações encerradas a favor deles), mas mostram que faltam coisas. Há ~35 incumbentes/ex-ocupantes
de cargo com nota 10 em Senador (lista no script de auditoria); se quiser, dá para passar todos numa segunda rodada.

Casos deixados como estão, com dúvida registrada: Petecão/AC (ação penal por peculato AP 542 remetida à 1ª instância,
andamento não localizado — contada como −2 e não como réu −3); Vanderlei Luxemburgo/TO (acusação do MPF de 2000 por
sonegação, desfecho não localizado, −1).

---

## 4. Governador (201 candidatos)

198 com idoneidade (3 sem pesquisa: registro duplicado de Sargento Laudicério/MT, Cleber Rabelo/PA substituído, Pedro
Brito/CE desistente); os 7 sem círculo estão fora da disputa. Profundidade: padrão em 14 UFs, rápida em 13.
A classificação de Governador estava, no geral, **mais coerente que a de Senador** (arquivamentos = −1,
investigação formal = −2, AIJE pendente = −2 aplicados de forma estável). Divergências corrigidas:

| Candidato | Nota | O que mudou |
|---|---|---|
| **Delcídio Amaral (PRD/MS)** | 3 → **6** | A prisão de 2015 foi **preventiva** e ele foi **absolvido** em 2018 no processo de obstrução (junto com Lula). "Condenação com pena cumprida" (−5) exige condenação — a prisão preventiva de Marconi Perillo, por exemplo, não foi contada assim. Passa a "acusação absolvida" (−1); entra a condenação cível por danos morais a Lula (−1); segue a cassação do mandato (−2). |
| Ciro Gomes (PSDB/CE) | 6 → 5 | Operação Colosseum volta a −2 (investigação em curso), como Cid Gomes e os demais alvos de busca da PF sem desfecho conhecido. |
| Allyson (UNIÃO/RN) e Álvaro Dias (PL/RN) | 8 → **6** cada | Há AIJEs pendentes no TRE-RN nos dois sentidos (confirmadas na web). Em todos os outros estados AIJE pendente = registro contestado (−2); no RN elas estavam "não contadas". |
| Mateus Simões (PSD/MG) | 10 → 8 | Amostragem de incumbentes com nota 10: duas ordens do TRE-MG para retirar conteúdo de campanha (vídeo na UTI de hospital público, 29/08; vídeo com acusação falsa ao vice de Cleitinho, 22/09), −1 cada — mesmo critério de Catan e Capitão Wagner. |
| Wellington Fagundes (PL/MT) | 3 (igual) | Só rótulo: condenação por improbidade estava como "contas irregulares"; passa a "condenação de 1ª instância" (mesmo peso). |

Amostragem de incumbentes com nota 10 sem achado novo: Jerônimo Rodrigues (BA) e Sandro Alex (PR).

Registros contestados reconferidos (seguem sub judice, nada muda): Izadora Dias/PCO-SP (DRAP negado, em recurso),
Roberto Rocha/MA (indeferido pelo TRE-MA em 14/09, recurso ao TSE), Elizeu Aguiar/PI (impugnação do MPE ainda sem
julgamento), Roberto Cidade/AM (Procuradoria deu parecer pela cassação em 20/09 em mais uma ação; TRE-AM não julgou).

Deixados como estão, com observação: Gelson Merísio/SC (apuração do MPF de 2018 sem desfecho, −1 — mantido como
"apuração" porque não há sinal de operação/inquérito formal, diferente da Colosseum); João Henrique Catan/MS (vídeo no
hospital conta −2 porque há pedido de cassação pendente, equivalente a AIJE).

---

## 5. Efeito no funil (recomendações por quadrante)

Calculado localmente com `pipeline/recomendar.py` (corte 6,0), comparando com o que está publicado hoje.

- **Presidente:** nenhuma recomendação muda.
- **Governador:** só o ES muda (sai Ricardo Ferraço, entra Breno Barcelos na Direita — o círculo de Ferraço caiu
  com AGIR/PDT/Cidadania/PSDB da coligação). Ficam abaixo do corte: Patrus Ananias e Alexandre Kalil (MG),
  Ciro Gomes (CE), Álvaro Dias (RN).
- **Senador:** muda em 19 das 27 UFs. Ficam abaixo do corte: Marília Arraes (PE), Helder (PA), Eduardo Braga (AM),
  André Moura (SE).

Detalhe por UF:

```
## PRESIDENTE
## SENADOR
- SP: sai ['GUILHERME DERRITE (DIREITA)', 'SIMONE TEBET (LIBERTARIO)'] | entra ['SALLES (DIREITA)', 'SONINHA FRANCINE (LIBERTARIO)']
- MG: sai ['AÉCIO NEVES (LIBERTARIO)', 'ÁUREA CAROLINA (ESQUERDA)'] | entra ['MARCO ANTÔNIO SUPERMAN (LIBERTARIO)', 'VICTÓRIA MELLO VIC (ESQUERDA)']
- RJ: sai ['MONICA BENICIO (ESQUERDA)'] | entra ['MICHELLY XAVIER (ESQUERDA)']
- BA: sai ['ANGELO CORONEL (DIREITA)', 'JAQUES WAGNER (ESQUERDA)'] | entra ['CARLOS SODRÉ (DIREITA)', 'RUI COSTA (ESQUERDA)']
- RS: sai ['PIMENTA (ESQUERDA)', 'RIGOTTO (DIREITA)'] | entra ['DANIELA MULHERES SOCIA**Presidente (5):** BR Lula 4→1; BR Clariana Barao 10→6; BR Renan Santos 7→9; BR Rui Costa Pimenta 7→9; BR Leonardo Avalanche 2→8

**Senador (134):** SP Guilherme Derrite 9→6; SP Guto Schiavetto 8→9; SP Guto Schiavetto 8→9; SP Marina Silva 8→6; SP Simone Tebet 10→6; SP Soninha Francine 10→9; MG Aécio Neves 10→8; MG Marcelo Aro 9→8; MG Marília Campos 8→6; MG Áurea Carolina 10→7; RJ Benedita Da Silva 9→6; RJ Helio Secco 8→9; RJ Monica Benicio 10→8; RJ Pedro Paulo 8→6; BA Angelo Coronel 10→6; BA Jaques Wagner 9→6; BA Professora Delliana 10→8; BA Rui Costa 9→6; PR Alexandre Curi 10→6; PR Cristina Graeml 8→6; PR Deltan Dallagnol 10→6; PR Dr Rosinha 9→6; PR Gleisi 9→6; PR Karen Guerreiro 8→9; RS Frederico Antunes 8→6; RS Manuela D Ávila 10→6; RS Marcel Van Hattem 10→6; RS Milton Cardoso 10→9; RS Pimenta 9→6; RS Renato Jaguarão 10→9; RS Rigotto 9→6; PE Eduardo Da Fonte 9→6; PE Humberto Costa 9→6; PE Marília Arraes 9→6; PE Túlio Gadêlha 8→6; CE Capitão Wagner 9→6; CE Cid Gomes 10→6; CE Luizianne 8→6; PA Chicão 9→6; PA Conti 10→8; PA Gizelle Freitas 10→8; PA Helder 5→2; PA Livia Noronha 9→8; SC Afrânio Boppré 10→6; SC Décio Lima 9→6; SC Esperidião Amin 9→6; SC Lunelli 9→6; SC Túlio De Amorim Pfuetzenreiter 8→9; GO Cintia Dias 10→6; GO Ernesto Roller 10→6; GO Gracinha Caiado 9→8; GO Isaura Lemos 10→6; GO Iure Castro 10→6; AM Eduardo Braga 9→6; AM Plinio Valério 10→9; AM Professora Evany 10→8; AM Wilson Lima 9→7; ES Evair De Melo 10→6; ES Rose De Freitas 9→6; ES Renato Casagrande 10→6; ES Professor Fabian 10→8; PB Nabor 10→6; PB André Gadelha 9→6; PB Veneziano 9→6; PB Joao Azevêdo 10→6; RN Rafael Motta 9→8; RN Samanda De Lula 9→8; RN Styvenson Valentim 9→6; RN Tércio Tinôco 9→6; RN Sandro Pimentel 10→8; RN Sonia Godeiro 10→8; RN Zenaide Maia 8→6; MT Margareth Buzetti 9→6; MT Janaina Riva 9→6; MT Pedro Taques 10→6; MT Mauro Mendes 9→6; MT Fávaro 8→6; AL Arthur Lira 9→6; AL Renan 9→6; AL Dr. Wanderley 9→6; AL Marina Jhc 10→6; PI Ciro Nogueira 10→6; PI Marcelo Castro 9→6; PI Antônio Barros 10→8; PI Jorge Lopes 10→9; PI Francinaldo Leão 10→8; PI Maria Madalena Nunes 10→8; PI Júlio César O Julim Do Lula 8→6; DF Leila Do Vôlei 9→6; DF Erika Kokay 9→6; DF Guto Felício Dos Santos 10→9; MS Vander Loubet 9→8; MS Valter Da Comagran 10→8; MS Soraya 10→8; MS Beto Do Movimento 10→8; SE Eduardo Amorim 10→8; SE Delegado André David 10→8; SE Rogerio Carvalho 9→6; SE André Moura 9→6; SE Iran Barbosa 10→8; RO Mariana Carvalho 10→8; RO Sílvia Cristina 9→8; RO Acir Gurgacz 9→8; RO Engenheiro Thulio 8→9; RO Aires Mota 10→9; RO Luis Fernando 8→6; TO Gaguim 9→8; TO Alexandre Guimarães 8→7; TO Paulo Mourão 7→6; TO Professor Osvaldo 10→8; MA Roseana Sarney 8→6; MA Weverton Rocha 8→6; MA Fufuca 9→7; MA Eliziane Gama 9→7; MA Dr.Hilton Gonçalo 10→8; MA Enilton Rodrigues 9→7; AC Petecão 8→6; AC Eduardo Velloso 9→7; AC Jorge Viana 9→8; AC Mara Rocha 8→6; AC Professor Inacio Moreira 10→8; AP Randolfe 8→6; AP Alliny Serrão 8→6; AP Lucas Barreto 7→6; AP Rayssa Furlan 5→4; RR Teresa Surita 9→8; RR Chico Rodrigues 10→9; RR Hiperion De Oliveira 10→9; RR Márcio Junqueira 10→9; RR Helena Da Asatur 7→6; RR Pastor Isamar 7→6; RR Hilton Xavier 8→6; RR Mario Rocha 10→8; RR Bartô Macuxi 10→8

**Governador (25):** RJ William Siri 10→8; RJ Luan Monteiro 8→9; SP Fernando Haddad 1→0; SP Izadora Dias 8→9; MG Patrus Ananias 3→1; MG Alexandre Kalil 7→6; MG Henrique Áreas 8→9; PI Elizeu Aguiar 10→8; PI Dra. Lúcia Santos 10→9; MS Delcidio Amaral 9→8; RS Marcelo Maranata 10→9; MA Orleans Brandão 9.5→5.5; MA Felipe Camarão 9→7; SC Ralf Zimmer 9→8; SC Marcelo Brigadeiro 8→9; GO Luis Cesar Bueno 9→6; ES Ricardo Ferraço 7→6; ES Breno Barcelos 8→9; MT Rafaell Milas 8→9; DF Leandro Grass 9→6; RO Pedro Abib 9→8; TO Vicentinho Júnior 9→8; AC Tião Bocalom 8→7; AC Thor Dantas 6→8; RR Farah Mesquita 9→8S (ESQUERDA)', 'SANDERSON (DIREITA)']
- PE: sai ['HUMBERTO COSTA (ESQUERDA)'] | entra ['PAULO RUBEM SANTIAGO (ESQUERDA)']
    PE: agora abaixo do corte 6,0: ['MARÍLIA ARRAES']
- CE: sai ['CID GOMES (ESQUERDA)'] | entra ['REGINALDO (ESQUERDA)']
- PA: sai ['CHICÃO (DIREITA)'] | entra ['EDLAINE RODRIGUES (DIREITA)']
    PA: agora abaixo do corte 6,0: ['HELDER']
- SC: sai ['AFRÂNIO BOPPRÉ (ESQUERDA)'] | entra ['MARCOS DORVAL (ESQUERDA)']
- GO: sai ['ERNESTO ROLLER (LIBERTARIO)', 'ISAURA LEMOS (ESQUERDA)'] | entra ['GUILHERME DARQUES (ESQUERDA)', 'GUSTAVO MENDANHA (LIBERTARIO)']
- AM: sai ['PROFESSORA EVANY (ESQUERDA)'] | entra ['ISMAEL MUNDURUKU (ESQUERDA)']
    AM: agora abaixo do corte 6,0: ['EDUARDO BRAGA']
- ES: sai ['EVAIR DE MELO (DIREITA)'] | entra ['RODNEY MIRANDA (DIREITA)']
- RN: sai ['TÉRCIO TINÔCO (DIREITA)'] | entra ['GARI WENDELL BATISTA (DIREITA)']
- MT: sai ['FÁVARO (LIBERTARIO)'] | entra ['GALVAN (LIBERTARIO)']
- AL: sai ['RENAN (DIREITA)'] | entra ['DAVI DAVINO FILHO (DIREITA)']
- PI: sai ['MARIA MADALENA NUNES (ESQUERDA)'] | entra ['DANNIEL ROCHA (ESQUERDA)']
- DF: sai ['GUTO FELÍCIO DOS SANTOS (LIBERTARIO)'] | entra ['SEBASTIÃO COELHO (LIBERTARIO)']
    SE: agora abaixo do corte 6,0: ['ANDRÉ MOURA']
- RO: sai ['MARIANA CARVALHO (DIREITA)'] | entra ['ENGENHEIRO THULIO (DIREITA)']
- AC: sai ['MARA ROCHA (DIREITA)'] | entra ['DR. JUNIOR FEITOSA (DIREITA)']
## GOVERNADOR
    MG: agora abaixo do corte 6,0: ['PATRUS ANANIAS', 'ALEXANDRE KALIL']
    CE: agora abaixo do corte 6,0: ['CIRO GOMES']
- ES: sai ['RICARDO FERRAÇO (DIREITA)'] | entra ['BRENO BARCELOS (DIREITA)']
    RN: agora abaixo do corte 6,0: ['ÁLVARO DIAS']
```

⚠ **Antes de publicar, vale você olhar a regra da federação (seção 1)**: é ela que produz a maior parte das trocas em
Senador. Um efeito colateral conhecido do método ficou mais visível: como candidatos de partido pequeno, sem coligação,
não perdem pontos de círculo, eles ganham quadrantes de candidatos de coligações grandes (ex.: SP Libertário passa de
Simone Tebet para Soninha; MG Libertário de Aécio para Marco Antônio Superman).

---

## 6. Lista completa das notas de círculo que mudaram

**Presidente (5):** BR Lula 4→1; BR Clariana Barao 10→6; BR Renan Santos 7→9; BR Rui Costa Pimenta 7→9; BR Leonardo Avalanche 2→8

**Senador (134):** SP Guilherme Derrite 9→6; SP Guto Schiavetto 8→9; SP Guto Schiavetto 8→9; SP Marina Silva 8→6; SP Simone Tebet 10→6; SP Soninha Francine 10→9; MG Aécio Neves 10→8; MG Marcelo Aro 9→8; MG Marília Campos 8→6; MG Áurea Carolina 10→7; RJ Benedita Da Silva 9→6; RJ Helio Secco 8→9; RJ Monica Benicio 10→8; RJ Pedro Paulo 8→6; BA Angelo Coronel 10→6; BA Jaques Wagner 9→6; BA Professora Delliana 10→8; BA Rui Costa 9→6; PR Alexandre Curi 10→6; PR Cristina Graeml 8→6; PR Deltan Dallagnol 10→6; PR Dr Rosinha 9→6; PR Gleisi 9→6; PR Karen Guerreiro 8→9; RS Frederico Antunes 8→6; RS Manuela D Ávila 10→6; RS Marcel Van Hattem 10→6; RS Milton Cardoso 10→9; RS Pimenta 9→6; RS Renato Jaguarão 10→9; RS Rigotto 9→6; PE Eduardo Da Fonte 9→6; PE Humberto Costa 9→6; PE Marília Arraes 9→6; PE Túlio Gadêlha 8→6; CE Capitão Wagner 9→6; CE Cid Gomes 10→6; CE Luizianne 8→6; PA Chicão 9→6; PA Conti 10→8; PA Gizelle Freitas 10→8; PA Helder 5→2; PA Livia Noronha 9→8; SC Afrânio Boppré 10→6; SC Décio Lima 9→6; SC Esperidião Amin 9→6; SC Lunelli 9→6; SC Túlio De Amorim Pfuetzenreiter 8→9; GO Cintia Dias 10→6; GO Ernesto Roller 10→6; GO Gracinha Caiado 9→8; GO Isaura Lemos 10→6; GO Iure Castro 10→6; AM Eduardo Braga 9→6; AM Plinio Valério 10→9; AM Professora Evany 10→8; AM Wilson Lima 9→7; ES Evair De Melo 10→6; ES Rose De Freitas 9→6; ES Renato Casagrande 10→6; ES Professor Fabian 10→8; PB Nabor 10→6; PB André Gadelha 9→6; PB Veneziano 9→6; PB Joao Azevêdo 10→6; RN Rafael Motta 9→8; RN Samanda De Lula 9→8; RN Styvenson Valentim 9→6; RN Tércio Tinôco 9→6; RN Sandro Pimentel 10→8; RN Sonia Godeiro 10→8; RN Zenaide Maia 8→6; MT Margareth Buzetti 9→6; MT Janaina Riva 9→6; MT Pedro Taques 10→6; MT Mauro Mendes 9→6; MT Fávaro 8→6; AL Arthur Lira 9→6; AL Renan 9→6; AL Dr. Wanderley 9→6; AL Marina Jhc 10→6; PI Ciro Nogueira 10→6; PI Marcelo Castro 9→6; PI Antônio Barros 10→8; PI Jorge Lopes 10→9; PI Francinaldo Leão 10→8; PI Maria Madalena Nunes 10→8; PI Júlio César O Julim Do Lula 8→6; DF Leila Do Vôlei 9→6; DF Erika Kokay 9→6; DF Guto Felício Dos Santos 10→9; MS Vander Loubet 9→8; MS Valter Da Comagran 10→8; MS Soraya 10→8; MS Beto Do Movimento 10→8; SE Eduardo Amorim 10→8; SE Delegado André David 10→8; SE Rogerio Carvalho 9→6; SE André Moura 9→6; SE Iran Barbosa 10→8; RO Mariana Carvalho 10→8; RO Sílvia Cristina 9→8; RO Acir Gurgacz 9→8; RO Engenheiro Thulio 8→9; RO Aires Mota 10→9; RO Luis Fernando 8→6; TO Gaguim 9→8; TO Alexandre Guimarães 8→7; TO Paulo Mourão 7→6; TO Professor Osvaldo 10→8; MA Roseana Sarney 8→6; MA Weverton Rocha 8→6; MA Fufuca 9→7; MA Eliziane Gama 9→7; MA Dr.Hilton Gonçalo 10→8; MA Enilton Rodrigues 9→7; AC Petecão 8→6; AC Eduardo Velloso 9→7; AC Jorge Viana 9→8; AC Mara Rocha 8→6; AC Professor Inacio Moreira 10→8; AP Randolfe 8→6; AP Alliny Serrão 8→6; AP Lucas Barreto 7→6; AP Rayssa Furlan 5→4; RR Teresa Surita 9→8; RR Chico Rodrigues 10→9; RR Hiperion De Oliveira 10→9; RR Márcio Junqueira 10→9; RR Helena Da Asatur 7→6; RR Pastor Isamar 7→6; RR Hilton Xavier 8→6; RR Mario Rocha 10→8; RR Bartô Macuxi 10→8

**Governador (25):** RJ William Siri 10→8; RJ Luan Monteiro 8→9; SP Fernando Haddad 1→0; SP Izadora Dias 8→9; MG Patrus Ananias 3→1; MG Alexandre Kalil 7→6; MG Henrique Áreas 8→9; PI Elizeu Aguiar 10→8; PI Dra. Lúcia Santos 10→9; MS Delcidio Amaral 9→8; RS Marcelo Maranata 10→9; MA Orleans Brandão 9.5→5.5; MA Felipe Camarão 9→7; SC Ralf Zimmer 9→8; SC Marcelo Brigadeiro 8→9; GO Luis Cesar Bueno 9→6; ES Ricardo Ferraço 7→6; ES Breno Barcelos 8→9; MT Rafaell Milas 8→9; DF Leandro Grass 9→6; RO Pedro Abib 9→8; TO Vicentinho Júnior 9→8; AC Tião Bocalom 8→7; AC Thor Dantas 6→8; RR Farah Mesquita 9→8

---

## 7. O que ficou para você decidir

1. **Federações contam como coligação?** Apliquei "sim" (seção 1). Se "não", reverto só essa parte.
2. **AIJE/pedido de cassação de adversário vale −2?** É a regra atual e agora está aplicada igual em todos os estados
   (inclusive RN). Mas significa que qualquer adversário que entra com AIJE derruba 2 pontos. Uma alternativa seria
   −1 (apuração preliminar) enquanto não houver decisão, e −2 só com decisão desfavorável ou pedido do Ministério Público.
3. **Ordem judicial de retirada de propaganda** (−1 cada) é comum em campanha e a busca rasa só pega algumas — é o
   achado mais sujeito a cobertura desigual. Opções: manter, ou só contar quando houver multa/condenação.
4. **Deputados** (`circulo_partidos_estrutural.json`) ainda com os valores antigos de PSDB, MISSÃO, PRD e PCdoB.
5. **Segunda rodada de incumbentes com nota 10**: a amostra de 7 achou algo em 4. Há ~35 em Senador e ~20 em Governador.
6. Deltan Dallagnol (TSE julga até 25/09) e os demais sub judice: reconferir perto de 04/10.

## Como revisar / desfazer

- Script novo (não rastreado): `pipeline/padronizar_caciques.py` — aplica a regra única dos caciques; sem `--aplicar` só simula.
- Todas as mudanças: `git diff data/reference/` (arquivos `idoneidade.json`, `circulo_politico.json`,
  `liderancas_partidarias.json`). Cada registro alterado tem `auditado_em` / `padronizado_em` = `2026-09-24`.
- Pipeline rodado até `calcular_cobertura` sem nenhum "Aviso"; **`exportar_prototipo` NÃO foi rodado**, então
  `site/` continua igual ao publicado.
- Desfazer tudo: `git checkout data/reference` e rodar o pipeline de novo.
- Cerca de 45 buscas e 8 leituras de páginas na web nesta sessão.
