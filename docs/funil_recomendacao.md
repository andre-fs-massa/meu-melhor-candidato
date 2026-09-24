# Funil de recomendação: do eleitor ao "melhor candidato"

Código: `pipeline/recomendar.py`. Rodar: `python -m pipeline.recomendar --cargo GOVERNADOR --uf SP`
(`--corte 6`, `--nao-avaliados manter_sinalizado`, `--csv` para gerar `data/processed/recomendacoes_2026.csv`).

## Protótipo ponta a ponta

Página: `site/index.html` (funciona por duplo clique, sem servidor; o protótipo antigo `prototipo/` foi aposentado em 2026-09-24). Os dados vêm de
`site/dados.js` (só o índice) e de um arquivo por cargo/UF em `site/dados/`, baixado sob demanda, gerados por `python -m pipeline.exportar_prototipo` a partir do próprio funil (corte 6,0; só recomenda
quem tem idoneidade geral verificada). Sempre que o pipeline rodar de novo, regerar o `dados.js`.
Hoje há 4 combinações liberadas (Presidente, Governador de MG, RJ e SP); as outras 105 mostram "ainda sem verificação".
A página tem: seleção de cargo/estado, lista com o motivo de cada saída, diagrama de Nolan interativo (com versão em
tabela), cartões por quadrante com "por que este candidato?" e as fontes. Testada em claro/escuro e em largura de celular.

## Modo rápido: descobrir o quadrante em 2 perguntas

Para o eleitor que não sabe seu quadrante, o passo 4 tem "Descubra em 1 minuto": 2 perguntas gerais, uma por eixo, cada uma
com dois polos que trazem custo (A/B, com a ordem sorteada a cada carga para evitar viés de posição) e uma escala de 5 posições
(0, 2,5, 5, 7,5, 10) mais "prefiro não responder".
* **Economia:** "Para o país melhorar, o que deve pesar mais?" (Estado mais presente x Estado menor).
* **Costumes:** "Em escolhas pessoais sobre as quais a sociedade se divide, o que a lei deve priorizar?" (valores morais e tradicionais x liberdade individual).
* **Leitura da resposta:** ponta (0 ou 10) = lado firme; leve (2,5 ou 7,5) = lado provável, mas o vizinho também é mostrado; meio-termo (5) ou eixo pulado = os dois lados.
  Os cartões do quadrante do eleitor ganham "Seu quadrante" e vão para o início; os vizinhos ganham "Vizinho do seu".
* **Ponto "Você"** no diagrama do passo 3 (losango vazado; uma linha quando só um eixo é conhecido) e **deslizadores** para ajustar a posição.
* **Plano B por distância:** se nenhum candidato dos quadrantes do eleitor continuou na disputa (por exemplo, o quadrante
  estatista-autoritário, sempre vazio), mostra os 3 mais próximos no diagrama e avisa quando o mais próximo está a mais de 5 pontos.
* **Privacidade:** as respostas ficam só na memória da página; o código não usa armazenamento nem rede (verificado).
* **Limites:** as perguntas não foram calibradas nem testadas com eleitores; uma pergunta por eixo é ruído alto perto do centro;
  o eixo de costumes mistura moral e rigor penal, e a pergunta 2 cobre só a moral. O modo completo (6 perguntas) é o próximo passo.

## Passo a passo para o eleitor

1. **Escolher o cargo e o estado** (Presidente usa `BR`).
2. **Etapa 0 -- quem está fora da disputa.** Saem candidatos com registro indeferido ou inelegibilidade vigente
   (derivado dos `achados` de `idoneidade.json`). O eleitor vê quem saiu e por quê.
3. **Etapa 1 -- filtro de idoneidade.** Sai quem tem `nota_idoneidade_geral` (média da idoneidade pessoal com a do
   círculo político) abaixo do corte (padrão 6,0, definido pelo usuário). O eleitor vê quem saiu, a nota e os apoiadores que pesaram.
4. **Etapa 2 -- posição no diagrama de Nolan.** Cada candidato cai em um de quatro quadrantes (limiar 5,0 nos dois
   eixos): Libertário, Direita conservadora, Esquerda progressista, Estatista-autoritário. A posição vem da pesquisa
   individual; sem ela, do baseline do partido (sempre marcado). Quem está a menos de 0,5 do centro leva a marca FRONTEIRA.
5. **Etapa 3 -- melhor por quadrante, por qualificação geral (`nota_qualificacao_geral`, decisão do usuário em
   2026-09-22).** É a média simples entre `nota_idoneidade_geral` e `nota_competencia_geral` -- antes disso, a etapa 3
   usava só `nota_competencia_geral`, com a idoneidade entrando apenas como critério de desempate. Presidente,
   Governador e Senador: 1 candidato por quadrante. Deputados federal, estadual e distrital: 3 por quadrante, e o
   eleitor escolhe entre eles.
6. **Resultado:** até 3 recomendações (o quadrante Estatista-autoritário fica vazio, ver limites), cada uma com idoneidade,
   competência, posição, quantas das 5 camadas foram pesquisadas e a marca de qualquer ressalva.

## Regras de desenho (parametrizáveis)

| Decisão | Padrão | Por quê |
|---|---|---|
| Corte de idoneidade geral | 6,0 | Definido pelo usuário em 2026-09-21. **Muito sensível**: com 5,0 ou 7,0 mudam recomendações. |
| Corte de idoneidade geral dos **deputados** | 8,5 | Definido pelo usuário em 2026-09-24 (8,0 e depois 8,5; `CORTE_POR_CARGO` em `recomendar.py`). A nota deles vem de bases oficiais e do presidente do partido, sem busca individual. **Efeito:** com círculo 6 (PL, DC) a idoneidade geral máxima é 8,0, então os 891 federais desses dois partidos ficam de fora (mais 6 de outros partidos); com 8,0 só caíam 14. |
| Idoneidade pessoal **estrutural** (Deputado Federal) | 10 menos: TCU -2; CEIS/CNEP vigente -2; Ibama com auto >= R$ 1 mi -2, abaixo disso -1 | `gerar_idoneidade_estrutural.py`. TSE 2022 e CEAF só aparecem no painel. **Não pega processo judicial, inquérito nem notícia**: nota 10 = "nada consta nestas bases". O site rotula como "Verificação estrutural". |
| Candidato sem idoneidade geral pesquisada | **excluído** da recomendação (fica numa lista à parte) | Se passasse direto, ser pesquisado viraria desvantagem: só os pesquisados poderiam ser reprovados. |
| Critério de escolha por quadrante | qualificação geral (média de idoneidade geral e competência geral) | Decisão do usuário em 2026-09-22; antes era só competência geral. |
| Desempate na última vaga | competência geral, idoneidade geral, competência bruta, escolaridade; depois sorteio com semente fixa | Nunca ordem alfabética. O tamanho do empate é informado. |
| Pessoa registrada duas vezes no TSE | mantém o registro mais pesquisado e o mais recente | 17 casos em 2026 (34 linhas). |

## Cobertura atual (o que o funil consegue recomendar hoje)

| Cargo | Candidatos | Com idoneidade geral | Recomendável hoje |
|---|---|---|---|
| Presidente | 14 | 13 | Sim (Marçal está fora da disputa) |
| Governador | 201 | 92 (RJ, SP, MG, PI, RN, AL, MS, BA, PR, RS, PE, CE) | Nesses 12 estados |
| Senador | 319 | 0 | Não |
| Deputados (federal, estadual, distrital) | 19.526 | 0 | Não |

Com `--nao-avaliados manter_sinalizado` o funil roda para todos, mas as recomendações saem marcadas SEM IDONEIDADE
e a etapa 1 não protege o eleitor de ninguém.

## Limites conhecidos

* **Deputados: a competência geral empata.** Ela vem da ocupação declarada e da escolaridade, que têm poucos valores.
  Em 49 dos 81 grupos (UF x quadrante) de Deputado Federal há mais de 3 candidatos com a nota máxima; em SP, o topo de um
  quadrante tem 51 empatados. Os "3 melhores" viram um sorteio entre eles.
* **Quadrante Estatista-autoritário vazio.** Nenhum baseline partidário combina economia estatista com costumes
  conservadores, e só 1 governador cai ali.
* **Senador e Deputados só têm posição pelo partido.** O quadrante deles é o do partido, não o da pessoa.
* **Fronteira.** Partidos de centro mudam de quadrante por 0,3 ponto (PSD 6,0/5,5 é Libertário; MDB 5,5/4,8 é Direita).
* **Competência é comparável só entre candidatos com experiência política pesquisada** (ver coluna `cobertura_pesquisa`).
* **A qualificação geral (média) favorece quem tem idoneidade 10 por falta de achado, não por ser mais limpo de fato.**
  Como a nota 10 de idoneidade muitas vezes reflete busca mais rasa (partido pequeno, menos cobertura de imprensa) e não
  ausência real de pendência, candidatos de partidos pequenos com idoneidade 10 mas competência mediana passaram a vencer
  quadrantes contra candidatos mais competentes e mais escrutinados (com idoneidade 6-9 por achados reais, ainda que
  leves). Ex.: Sergio Moro (PR, idoneidade 6,5 após achado) perdeu o quadrante Direita para o Dr. Alexandre Salomão
  (Mobiliza, idoneidade 10, menos competência) só depois da mudança de critério em 2026-09-22.
* **O funil escolhe o melhor por quadrante, não o melhor candidato.** A nota de competência premia escolaridade e
  carreira eletiva; candidatos de partidos pequenos com nota alta de competência aparecem (Edmilson Costa/PCB para
  Presidente, Cyro Garcia/PSTU no RJ).
