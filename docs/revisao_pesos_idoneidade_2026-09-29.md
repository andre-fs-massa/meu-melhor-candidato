# Revisão de justiça dos pesos de idoneidade (2026-09-29)

Pedido do usuário: revisar se o peso de cada tipo de achado de idoneidade é justo e implementar as correções, em
ordem de gravidade. A tabela fica em `pipeline/pesos.py` (`PESOS_ACHADO`); os achados de cada candidato ficam em
`data/reference/idoneidade.json` (a nota gravada é recalculada e conferida pelo pipeline). A tabela de caciques
(`PESOS_CACIQUE`) e a verificação estrutural dos deputados (TCU, CEIS/CNEP, Ibama) **não mudaram**.

## O que mudou, em ordem de gravidade

| # | Injustiça encontrada | Correção | Achados reclassificados |
|---|---|---|---|
| 1 | Condenação de 1ª instância (−2) pesava menos que ser só réu em ação penal (−3) | `condenacao_1a_instancia_recorrivel` −2 → **−3**; não somar com `reu_acao_penal` no mesmo processo (os 4 registros com as duas categorias são de processos diferentes) | 27 (só o peso) |
| 2 | Condenação revertida pesava igual a condenação de pé | `condenacao_revertida` **mantida em −2** (regra do usuário de 26/09); com o item 1 a condenação de pé passa a pesar mais | — |
| 3 | Condenação criminal **anulada** com pena cumprida (−5) pesava mais que condenação criminal **de pé** (−4); crime e improbidade dividiam a mesma categoria | Nova `condenacao_criminal_confirmada` **−5**; `condenacao_confirmada_sem_reversao` (−4) fica para improbidade e abuso de poder eleitoral | 14 casos criminais |
| 4 | Registro indeferido (−3) ou contestado (−2) punia a pessoa pela papelada do partido (DRAP, convenção, certidão) e, quando a causa era conduta, contava a mesma coisa duas vezes | `registro_indeferido` e `registro_contestado_sub_judice` → **0** (continuam como marcadores: fora da disputa / aviso "sub judice"); quando a causa é conduta pessoal, a **causa** vira achado próprio | 10 AIJEs/pedidos de cassação pendentes viraram `investigacao_ou_acao_civil_em_curso` (−2, mesma régua de "AIJE pendente" da auditoria de 24/09); Waguinho ganhou `contas_rejeitadas` |
| 5 | Contas aprovadas com ressalva (rotina) e contas rejeitadas (base de inelegibilidade) pesavam igual (−1) | Novas `contas_rejeitadas` **−2** (gestão rejeitada ou campanha desaprovada) e `contas_aprovadas_com_ressalva` **−0,5**; a categoria antiga (−1) fica só para **multa** (conduta vedada, doação acima do limite, tribunal de contas) | 7 → rejeitadas; 2 → ressalva |
| 6 | Absolvido no mérito pesava igual a citado (−1) | Nova `absolvido_no_merito` **−0,5**: absolvição, denúncia/queixa rejeitada, ação eleitoral ou impugnação improcedente, **arquivamento por falta de provas/crime ou a pedido do MP**. Segue −1 (`acusacao_anulada_ou_absolvida`) o que caiu sem exame do fato: provas anuladas, incompetência, prescrição, excesso de prazo, extinção ou arquivamento sem motivo conhecido | 54 de `acusacao_anulada_ou_absolvida` e 22 de `citado_ou_apuracao_preliminar` (investigações arquivadas por falta de provas, para uma investigação arquivada não pesar mais que uma denúncia rejeitada) |
| 7 | "Citado ou apuração preliminar" sem teto: quem tem décadas de cargo acumulava menções | Soma limitada a **−2** (`TETOS_POR_CATEGORIA`) | — |
| 8 | Acordo de não persecução (exige confissão, no penal) tratado como citado (−1) | Nova `acordo_de_nao_persecucao` **−2** (abaixo da condenação de 1ª instância: só cabe para crime sem violência com pena mínima abaixo de 4 anos e não há sentença) | 3 (Lahesio Bonfim/MA, Silas Câmara/AM, Professor Euler/PR — ANPC) |
| 9 | Cassação de mandato (−2) baixa para perda de mandato decretada e mantida | `cassacao_de_mandato` −2 → **−3**; suspensão temporária de mandato vira `sancao_institucional_confirmada` (−2) | Glauber Braga (suspensão de 6 meses) |

Regras de classificação usadas caso a caso:

- **Criminal x não criminal (item 3):** entrou como criminal a condenação por crime confirmada por tribunal (2ª
  instância, STF/STJ, TRE em crime eleitoral) ou transitada. Improbidade, AIJE e cassação eleitoral seguem −4.
  André Moura e Regina Tio Ivo continuam condenados (o acordo posterior extinguiu a pena, não a condenação);
  Roberto Góes (pena prescrita) também.
- **Mérito x processual (item 6):** na dúvida (arquivamento sem motivo informado), −1.
- **Registro (item 4):** registro barrado por condenação já contada (Dr João Neto, Dra Rosangella, Antônia Lúcia,
  Lucas Cardoso) não soma nada; o de Elizeu Aguiar tem a causa (contas no TCU) já contada.

## Impacto

Comparação do site antes e depois (idoneidade pessoal ou geral alterada; inclui 2 casos que mudaram só pelo
círculo político: Caiado, pelo vice, e Mateus Simões, pelo padrinho Zema).

### Candidatos com nota alterada, por UF e cargo

| UF | Presidente | Governador | Senador | Dep. federal | Dep. estadual | Dep. distrital | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| AC | · | · | 1 | 1 | 2 | · | 4 |
| AL | · | · | 1 | 4 | · | · | 5 |
| AM | · | 1 | · | 4 | 3 | · | 8 |
| AP | · | · | 1 | 2 | 2 | · | 5 |
| BA | · | 1 | 1 | 3 | 1 | · | 6 |
| BR | 2 | · | · | · | · | · | 2 |
| CE | · | · | · | 1 | · | · | 1 |
| DF | · | · | · | 2 | · | 2 | 4 |
| ES | · | 1 | 1 | · | 1 | · | 3 |
| GO | · | 1 | · | 4 | · | · | 5 |
| MA | · | 2 | 3 | 1 | 1 | · | 7 |
| MG | · | 2 | 1 | 2 | · | · | 5 |
| MS | · | 1 | · | 3 | · | · | 4 |
| MT | · | 1 | · | 2 | 2 | · | 5 |
| PA | · | 1 | 1 | 3 | 3 | · | 8 |
| PB | · | · | 1 | 2 | 2 | · | 5 |
| PE | · | 1 | 2 | 2 | 3 | · | 8 |
| PI | · | 6 | · | 2 | · | · | 8 |
| PR | · | · | · | 5 | 2 | · | 7 |
| RJ | · | · | 3 | 1 | 1 | · | 5 |
| RN | · | 2 | · | 3 | 2 | · | 7 |
| RO | · | · | · | 1 | · | · | 1 |
| RR | · | 2 | 3 | 1 | 2 | · | 8 |
| RS | · | 1 | · | · | 1 | · | 2 |
| SC | · | · | · | 3 | 3 | · | 6 |
| SE | · | · | 1 | 2 | · | · | 3 |
| SP | · | 3 | · | 6 | 2 | · | 11 |
| TO | · | 1 | 1 | 1 | 3 | · | 6 |
| **Total** | **2** | **27** | **21** | **61** | **36** | **2** | **149** |

### Por cargo

| Cargo | Candidatos com nota alterada | Sobem | Descem | Mudaram de situação no funil |
|---|---:|---:|---:|---:|
| Presidente | 2 | 1 | 1 | 0 |
| Governador | 27 | 23 | 4 | 4 |
| Senador | 21 | 15 | 6 | 5 |
| Dep. federal | 61 | 37 | 24 | 26 |
| Dep. estadual | 36 | 17 | 19 | 9 |
| Dep. distrital | 2 | 2 | 0 | 0 |
| **Total** | **149** | **95** | **54** | **44** |

### Quem mudou de situação no funil

| Cargo | UF | Candidato | Idoneidade pessoal | Idoneidade geral | Situação |
|---|---|---|---|---|---|
| Governador | ES | BRENO BARCELOS | 10 → 10 | 9,5 → 9,5 | recomendado → **continua** |
| Governador | ES | RICARDO FERRAÇO | 9 → 9,5 | 7,5 → 7,75 | continua → **recomendado** |
| Governador | PI | GERALDO CARVALHO | 8 → 10 | 9 → 10 | continua → **recomendado** |
| Governador | PI | RAFAEL FONTELES | 10 → 10 | 8 → 8 | recomendado → **continua** |
| Senador | BA | JAQUES WAGNER | 9 → 9,5 | 7,5 → 7,75 | continua → **recomendado** |
| Senador | BA | RUI COSTA | 8 → 8 | 7 → 7 | recomendado → **continua** |
| Senador | MG | AÉCIO NEVES | 9 → 9,5 | 8,5 → 8,75 | continua → **recomendado** |
| Senador | MG | MARCO ANTÔNIO SUPERMAN | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Senador | RR | TERESA SURITA | 4 → 3 | 6 → 5,5 | continua → **abaixo do corte** |
| Dep. federal | AM | JOANA DARC | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | AM | SILAS CÂMARA | 7 → 6 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | BA | DUDA DE ALAN SANCHES | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. federal | BA | PROF. LEANDRO SANSON | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | MS | CAMILA JARA | 8 → 8,5 | 8,5 → 8,75 | continua → **recomendado** |
| Dep. federal | MS | JEFFERSOM MARECCO | 10 → 10 | 9,5 → 9,5 | recomendado → **continua** |
| Dep. federal | MS | MAURICIO PICARELLI | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | MT | CAIO CORDEIRO | 8 → 8,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. federal | MT | DOUTORA DÉBORA | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | MT | DR. LEONARDO | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | MT | MAGALY | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. federal | PA | OZORIO JUVENIL | 9 → 9,5 | 9,5 → 9,75 | continua → **recomendado** |
| Dep. federal | PA | RENILCE NICODEMOS | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. federal | PA | RODRIGO SANTARÉM | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | PA | VALÉRIA PRADO | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | PI | FLORENTINO NETO | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | RN | MARLEIDE CUNHA | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. federal | RN | RAPOSINHA | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | RR | ADJALMA | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | SP | ERIKA HILTON | 9 → 9,5 | 9,5 → 9,75 | continua → **recomendado** |
| Dep. federal | SP | KEIKO OTA | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | SP | NABIL BONDUKI | 10 → 10 | 9,5 → 9,5 | recomendado → **continua** |
| Dep. federal | SP | ORLANDO SILVA | 9 → 9,5 | 9,5 → 9,75 | continua → **recomendado** |
| Dep. federal | SP | PAULO TEIXEIRA | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. federal | TO | FABIO VAZ | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. federal | TO | RICARDO AYRES | 5 → 7,5 | 7,5 → 8,75 | abaixo do corte → **recomendado** |
| Dep. estadual | MT | DR.. FLAVIANE RAMALHO | 10 → 10 | 10 → 10 | recomendado → **continua** |
| Dep. estadual | MT | VALDENIRIA DUTRA | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. estadual | PB | FELIPE LEITÃO | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. estadual | RJ | MAICON CRUZ | 7 → 6,5 | 8,5 → 8,25 | continua → **abaixo do corte** |
| Dep. estadual | RN | ERIKO JÁCOME | 10 → 10 | 9,5 → 9,5 | recomendado → **continua** |
| Dep. estadual | RN | EZEQUIEL | 9 → 9,5 | 9 → 9,25 | continua → **recomendado** |
| Dep. estadual | RN | TAVEIRA JÚNIOR | 8 → 7 | 8,5 → 8 | continua → **abaixo do corte** |
| Dep. estadual | RR | GENILSON COSTA | 7 → 6,5 | 8,5 → 8,25 | continua → **abaixo do corte** |
| Dep. estadual | SC | JEAN KUHLMANN | 7 → 6 | 8,5 → 8 | continua → **abaixo do corte** |

Observações:

- Quem **sobe** são sobretudo candidatos com registro barrado por papelada do partido (Piauí: 5 candidatos a
  governador de 8 para 10) e absolvidos ou com investigação arquivada por falta de provas (−1 → −0,5).
- Quem **desce** são condenados em 1ª instância (−2 → −3), condenados criminalmente em 2ª instância (−4 → −5),
  cassados (−2 → −3), contas desaprovadas (−1 → −2) e acordos de não persecução (−1 → −2).
- Troca de recomendado mesmo quando o recomendado anterior tinha 10 acontece porque a etapa 3 do funil escolhe pela
  qualificação geral (média entre idoneidade geral e competência geral): meio ponto de idoneidade a mais para um
  candidato mais experiente basta para ele passar à frente (ex.: Aécio x Marco Antônio Superman em MG).
