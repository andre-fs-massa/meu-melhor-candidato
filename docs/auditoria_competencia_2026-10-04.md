# Auditoria da competência geral (04/10/2026)

Avaliação crítica de todos os pesos que compõem a **competência geral**: os 21 arquétipos de ocupação
(`pipeline/competencia_dimensoes.py`), os pesos de cargo já exercido (`pipeline/enriquecer_experiencia.py`), a
experiência profissional pesquisada (`pipeline/enriquecer_competencia_transferivel.py`), a escala de escolaridade
(`pipeline/mapear_escolaridade.py`) e a média final (`pipeline/calcular_competencia_geral.py`). Números medidos nos
20.046 candidatos do arquivo do TSE e nos 702 recomendados publicados em 6d91674. **Nada foi alterado.**

## Por que isso importa mais do que parece

Entre os deputados acima do corte de idoneidade (17.190), a idoneidade geral quase não varia (desvio de **0,35**),
enquanto a competência varia muito (desvio de **1,71**) e a escolaridade também (**1,89**). Na prática, **quem decide
quais deputados são recomendados é a competência geral**, não a idoneidade.

Quem foi recomendado entre os 483 deputados, comparado com o total de candidatos a deputado:

| Ocupação declarada | Recomendados | Todos os candidatos |
|---|---|---|
| Deputado, vereador ou senador (título) | 65,4% | 8,4% |
| Advogado e afins | 16,1% | 8,1% |
| Finanças (inclui corretor de imóveis) | 10,4% | 2,3% |
| Empresário, comerciante | 3,3% | 20,0% |
| Saúde e educação | 0,8% | 13,0% |
| "Outros", estudante, aposentado, trabalhador manual | 0% | 25% |

Além disso, 97,7% dos recomendados têm superior completo, contra 57,6% do total.

## Achados

### 1. A ocupação declarada vale mais do que o mandato realmente exercido (grave)
O arquétipo "político legislativo atual" (ocupação DEPUTADO, VEREADOR ou SENADOR) pontua acima do peso do mandato real:

| Candidato a deputado federal | Competência no cargo |
|---|---|
| Declara ocupação "Vereador" (sem mandato de deputado) | **7,0** |
| Ex-deputado federal que declara a ocupação "Deputado" | 7,0 |
| Ex-deputado federal que declara outra ocupação | **5,9** |
| Mandato real de vereador (peso do cargo) | 3,5 |
| Mandato real de prefeito (peso do cargo) | 3,0, abaixo de um advogado (5,5) |

O mesmo mandato vale notas diferentes conforme a palavra escolhida no formulário do TSE. Um vereador vale tanto quanto
um senador. Para governador, a ocupação "Governador" dá 7,5, e o mandato real de governador dá 7,0.

### 2. Profissões de elite jurídica e financeira têm vantagem estrutural (grave)
Média das 4 frentes para Deputado ou Senador, só pela ocupação: advogado **5,5**, finanças **5,5**, servidor público
3,5, empresário 3,0, professor **2,0**, médico **1,5**, engenheiro **1,0**. As frentes de deputado (processo
legislativo, fiscalização, emendas) só reconhecem a formação jurídica e financeira; saúde e educação só pontuam em
"representação". Na prática, médicos, professores e engenheiros quase nunca chegam à recomendação de deputado.

### 3. A escolaridade conta em dobro (moderado)
A escolaridade tem metade do peso da competência geral, mas as ocupações que mais pontuam (advogado, economista,
contador) já exigem diploma. O diploma entra duas vezes: na ocupação e na escolaridade. A escala é linear em 8 degraus
(ensino médio completo = 7,1), e a Constituição não exige escolaridade para nenhum cargo além de saber ler e escrever.

### 4. Erros de classificação de ocupação (moderado, fácil de corrigir)
- **"ATOR "** perde o espaço na normalização (`.strip()`) e passa a casar com "LABOR**ATÓR**IO": 18 técnicos e
  auxiliares de laboratório viraram "artista".
- "Lanterneiro e pintor de veículos" virou artista ("PINTOR").
- "Agenciador de propaganda" virou rural ("AGENCIADOR").
- "Operador de aparelhos de produção industrial" virou empresário ("INDUSTRIAL"): 21 operários com nota de gestor.
- "Fiscal" virou segurança pública. "Despachante" virou jurídico, com 8 em processo legislativo.
- O corretor de imóveis e seguros (188 candidatos, 13 deles recomendados) recebe a mesma nota de economista e contador,
  com 10 em finanças.
- Biólogo, físico, químico e astrônomo estão no mesmo grupo de digitador e operador de computador.
- Ocupação sem regra cai em "trabalhador manual" (agente de viagem, supervisor de compras, desenhista).

### 5. Resposta pouco informativa recebe tratamento desigual (leve)
"Outros" (2.724 candidatos, 13% dos deputados) vale 2 em tudo. "Aposentado" e "dona de casa" valem menos ainda (0,5 a
1,0 na média), o que penaliza ex-políticos aposentados e mulheres que declaram "dona de casa", sem nenhuma informação
real sobre competência.

### 6. Pesquisa profissional: igual dentro de cada disputa (achado retirado após reconferência)
A primeira contagem só olhou os candidatos que tiveram a nota alterada (39) e deixou de fora a lista
`pesquisados_sem_alteracao` (166 nomes, indexada por nome de urna, não por código). Recontando: **Presidente 14 de 14**
e **Governador 192 de 200** foram pesquisados. Os 8 governadores sem pesquisa estão fora da disputa ou sem idoneidade
avaliada, ou seja, não concorrem à recomendação. Como o ranking compara só candidatos da mesma disputa, não há
desigualdade. Senador não tem pesquisa profissional (0 de 318), mas a regra vale igual para todos os candidatos ao
Senado. A consequência é que, ali, a competência depende só da ocupação e dos mandatos, e os achados 1 e 2 pesam mais.

### 7. Lacunas no peso dos cargos (leve)
- Vice-governador (5 casos) e vice-prefeito (3) estão nos registros, mas não têm peso: valem zero.
- O tempo de mandato não conta: um mandato vale o mesmo que seis.
- Para deputados, só entram mandatos de 2014 a 2024 (ponto cego já conhecido).
- Senador e deputado usam as mesmas 4 dimensões, então têm notas idênticas.

## Proposta de melhoria

| | Mudança | Por quê |
|---|---|---|
| **A** | **Hierarquia de evidência:** o título político declarado na ocupação deixa de pontuar sozinho; o mandato real (TSE ou pesquisa) passa a valer pelo menos o que o título valia. Vereador vale 0,8 de um deputado, prefeito vale 0,8 de um governador, vice vale de 0,5 a 0,6. | Corrige o achado 1: o mesmo mandato passa a ter a mesma nota. |
| **B** | **Comprimir a nota por ocupação para a faixa de 2 a 6** (2 + 0,4 × peso atual). | A ocupação é autodeclarada e é um sinal fraco. Diminui a distância entre advogado e médico (achado 2) e impede que ela supere um mandato exercido. |
| **C** | **Escolaridade com 25% do peso** (competência geral = 0,75 × competência no cargo + 0,25 × escolaridade). | Reduz a dupla contagem do diploma (achado 3). |
| **D** | **Corrigir as regras de ocupação** (lista do achado 4); "aposentado" e "dona de casa" passam a valer o mesmo que "outros". | Erros objetivos e penalidade sem informação (achados 4 e 5). |
| ~~E~~ | ~~Pesquisa profissional igual dentro de cada disputa.~~ **Retirada:** ela já é igual em todas as disputas (achado 6). Fica só como regra para o futuro: quando um candidato novo entrar numa disputa já pesquisada, ele também deve ser pesquisado. | — |
| **F** | Dar peso a vice-governador e vice-prefeito. | Achado 7. |

### Efeito simulado (cópia em memória, nada gravado)

| Cenário | Recomendados que mudam (de 702) | Deputados recomendados com mandato real | Superior completo | Advogado e finanças | Saúde e educação |
|---|---|---|---|---|---|
| Atual | — | 80% | 98% | 27% | 0,8% |
| A | 301 | 89% | 98% | 26% | 11,2% |
| A+B | 294 | 93% | 99% | 18% | 17,6% |
| A+B+C | 320 | **95%** | 93% | 17% | 16,4% |

Com A+B, o ex-deputado federal tem nota 7,1 qualquer que seja a ocupação declarada, o vereador declarado cai para 5,9,
o advogado sem mandato vai a 4,2 e o médico sem mandato sobe para 2,6.

### Decisão que cabe ao usuário
A proposta corrige as incoerências, mas **aumenta a vantagem de quem já tem mandato** (de 80% para 95% dos
deputados recomendados), porque experiência real passa a ser o que mais pesa e a idoneidade não diferencia os
deputados. Se a intenção é dar chance a quem nunca teve mandato, há duas saídas:
1. **Teto para a experiência:** o mandato soma no máximo um bônus fixo (por exemplo, até +2 sobre a nota da ocupação),
   em vez de substituir a nota.
2. **Competência só desempata:** para deputado, a recomendação é por idoneidade e a competência entra só entre quem
   empatar na idoneidade.

Qualquer opção muda cerca de 300 dos 702 recomendados.

## Proposta 2: competências transferíveis por hierarquia de experiência (sem escolaridade)

Princípio do usuário: experiência pública no mesmo poder do cargo pretendido vale mais, ponderada pela esfera; depois
vem a experiência no outro poder; sem experiência pública, vale a matriz de competências por profissão.

Para cada uma das 4 frentes do cargo: **nota = maior entre (1) mesmo poder, (2) outro poder × transferência da frente,
(3) profissão**. A nota no cargo é a média das 4 frentes.

1. **Mesmo poder** (vale igual nas 4 frentes). Esferas: federal (Presidente, Senador, Dep. Federal), estadual
   (Governador, Dep. Estadual/Distrital), municipal (Prefeito, Vereador). Mesma esfera ou acima = **10**; uma abaixo =
   **8**; duas abaixo = **6**. Vice = 2 a menos que o titular.
2. **Outro poder**: a mesma tabela, multiplicada pela transferência de cada frente, com teto de 8.
   - Executivo → Legislativo: processo legislativo 0,7 · fiscalização 0,8 · representação 1,0 · orçamento/emendas 1,0.
   - Legislativo → Governador: administração 0,5 · finanças 0,6 · processo legislativo 1,0 · articulação 1,0.
   - Legislativo → Presidente: administração 0,5 · macroeconomia 0,6 · articulação 1,0 · relações internacionais 0,4.
3. **Profissão**: biografia pesquisada × 0,7 (teto 7) ou, sem pesquisa, matriz da ocupação × 0,6 (teto 6). Título
   político declarado (Vereador, Deputado…) não é profissão: conta como mandato daquele cargo se nenhum for achado.

Simulação (cópia em memória, comparando sem escolaridade dos dois lados): 311 dos 702 recomendados mudam; deputados
recomendados com mandato passam de 87% para 95%; saúde e educação de 0,2% para 14,9%. Exemplos (Dep. Federal): ex-dep.
federal 6,4 → 10; ex-dep. estadual 6,0 → 8; só ex-vereador 5,3 → 6; só ex-prefeito 4,0 → 5,3; advogado sem mandato
5,5 → 3,3; médico sem mandato 1,5 → 0,9. Governador: ex-governador 7,8 → 10; ex-prefeito 6,0 → 8; legislador federal
6,5 → 6,8. Senador: ex-governador 5,5 → 7,0.

## Implementado (04/10/2026)
- Proposta 2 aplicada: pesos em `pipeline/pesos_competencia.py`; `mapear_competencias.py` (matriz × 0,6, título
  político não pontua), `enriquecer_experiencia.py` (mesmo poder / outro poder por esfera; título sem mandato achado
  conta como o cargo), `enriquecer_competencia_transferivel.py` (pesquisa × 0,7). Escolaridade continua com 50% na
  competência geral.
- Achados 4 e 5 corrigidos em `competencia_dimensoes.py` (339 candidatos reclassificados): "ATOR E DIRETOR" no lugar de
  "ATOR "; laboratório → saúde; lanterneiro e pintor de veículos → manual; agenciador de propaganda → comunicação;
  operador de produção industrial → manual; fiscal → servidor público; despachante, corretor de imóveis, supervisor de
  compras e agente de viagem → gestão; desenhista → arte; biólogo, químico, físico, astrônomo, estatístico → novo
  arquétipo `ciencias_naturais_exatas`; aposentado e dona de casa valem o mesmo que "outros".
- Efeito no site (com a escolaridade em 50%): 317 dos 702 recomendados mudam (Dep. Federal 135/243, Dep. Estadual
  131/231, Dep. Distrital 8/9, Senador 26/145, Governador 17/71, Presidente 0/3). Idoneidade inalterada.
- Achados 3 (escolaridade) e 7 (tempo de mandato) seguem pendentes.
