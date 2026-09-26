# Como contribuir

Obrigado pelo interesse! Este é um projeto de pesquisa cívica feito por voluntários — toda contribuição, grande ou
pequena, ajuda.

## Formas de contribuir

1. **Aprofundar a pesquisa dos deputados.** Presidente, Governador e Senador já têm pesquisa individual na web. Os
   ~19,5 mil candidatos a Deputado Federal/Estadual/Distrital têm só verificação estrutural (bases oficiais), e os
   finalistas de cada quadrante passaram por uma busca rápida (1 a 2 buscas). Casos marcados "a confirmar" no
   relatório [`docs/busca_deputados_finalistas_2026-09-25.md`](docs/busca_deputados_finalistas_2026-09-25.md) e
   posicionamento ideológico individual (hoje quase todos usam a posição do partido) são boas frentes.
2. **Corrigir ou atualizar um achado existente.** Processos mudam de status (recursos, reversões, prescrições).
   Se você encontrar uma informação desatualizada ou errada, abra uma issue ou um PR com a fonte.
3. **Melhorar o código** — pipeline (`pipeline/`), site (`site/`) ou documentação.

## Regra de ouro para dados de pesquisa

A nota de cada candidato **não é digitada à mão** — ela é calculada por tabelas fechadas de peso em
`pipeline/pesos.py` (`PESOS_ACHADO`, `PESOS_CACIQUE`) a partir de categorias e achados estruturados nos JSONs de
`data/reference/`. Isso existe para manter a análise padronizada e justa entre candidatos.

Ao contribuir com pesquisa:

- **Toda entrada precisa de fontes.** Preencha o campo `fontes` com links verificáveis (notícia, decisão judicial,
  portal de transparência). Nunca deixe vazio.
- **Use as categorias existentes** em `PESOS_ACHADO`/`PESOS_CACIQUE` sempre que uma delas descrever o achado.
  Proponha uma categoria nova só quando nenhuma existente couber, explicando o porquê no PR.
- **Distinga status jurídico.** Investigado, réu e condenado (com ou sem trânsito em julgado) são coisas
  diferentes e têm pesos diferentes — não trate um como o outro.
- **Explicite o tipo de ligação de cada apoiador** (vice, presidente de partido, padrinho político) em
  `circulo_politico.json` — não some um desconto sem dizer de quem e por quê.
- **Sem sinal individual de posicionamento ideológico**, use o baseline do partido em `ideologia_partidaria.json`
  (nunca a nota central por padrão) e marque a origem como `fallback de partido`.
- **Depois de editar os JSONs, rode o pipeline até o fim** (ver ordem no `README.md`) e confira que não aparece
  nenhum `Aviso:` no stderr — isso indica que uma nota gravada diverge do que as tabelas calculariam.

## Homônimos e armadilhas conhecidas

Antes de atribuir um achado, confira o **nome completo**, não só o sobrenome ou o cargo — já houve confusão entre
políticos de mesma família ou mesmo nome em estados diferentes. Desconfie de frases idênticas retornadas por
ferramentas de busca para pessoas diferentes: confirme em fonte primária antes de registrar.

## Enviando o PR

1. Faça um fork e uma branch com um nome descritivo (`pesquisa/senador-sp`, `fix/idoneidade-kalil`, ...).
2. Se mexeu em `data/reference/`, rode o pipeline completo e inclua o `Aviso:` zero como evidência na descrição do PR.
3. Descreva as fontes usadas e, se aplicável, o que mudou e por quê.
