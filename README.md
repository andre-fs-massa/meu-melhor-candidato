# Meu melhor candidato

Projeto independente e open source para ajudar eleitores brasileiros a avaliar candidatos nas eleições de 2026,
cruzando três coisas: **idoneidade** (processos, Ficha Limpa, círculo político), **competência** (formação e
experiência) e **alinhamento ideológico** (diagrama de Nolan). 1º turno em 4 de outubro de 2026.

🔗 **Site:** https://meu-melhor-candidato.afsm.me

> **Este projeto usa inteligência artificial** para buscar informações e gerar boa parte do conteúdo (notas,
> descrições de achados, textos). Por isso pode haver erros ou imprecisões. As notas são uma avaliação própria do
> projeto a partir de fontes públicas, listadas em cada candidato — não são um índice oficial e não substituem a
> leitura do plano de governo de cada um. Encontrou um erro ou quer criticar construtivamente? Escreva para
> **contact@afsm.me**.

## Estrutura do repositório

| Pasta | O que tem |
|---|---|
| `pipeline/` | Scripts Python que baixam/normalizam os dados oficiais do TSE e calculam as notas (competência, idoneidade, círculo político, posicionamento ideológico, qualificação geral, recomendação por quadrante). |
| `data/reference/` | **A fonte de verdade da pesquisa manual**: achados, apoiadores/círculo político, ideologia partidária, experiência política/profissional — cada um com as fontes usadas. |
| `data/raw/`, `data/processed/` | Dados baixados do TSE e o resultado processado do pipeline. Não versionados (grandes e regeráveis) — ver `.gitignore`. |
| `site/` | O site publicado: HTML/CSS/JS estático, sem build, consumindo `site/dados.js` (gerado pelo pipeline). |
| `docs/` | Metodologia do funil de recomendação, auditoria de padronização das notas e relatório da busca dos deputados finalistas, estado a estado. |
| `ferramentas/` | Utilitários da pesquisa: `busca_finalistas/` (listar deputados finalistas ainda não pesquisados, gravar resultados, rodar o pipeline, gerar a seção do relatório) e `datajud/` (consulta à API pública do CNJ para confirmar o andamento de processos). |

## Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

1. Baixe o dataset `consulta_cand_2026` do [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/) e
   extraia em `data/raw/` (o download automático é bloqueado pelo CDN do TSE — baixe manualmente pelo navegador).
2. Rode o pipeline, na ordem (na raiz do projeto):

   ```bash
   python -m pipeline.parse_candidatos          # só se o zip do TSE mudou
   python -m pipeline.mapear_competencias       # idem
   python -m pipeline.gerar_estrutural_deputados  # círculo e experiência política de Deputado Federal, sem busca na web (usa consulta_cand_2014..2024 em data/raw/)
   python -m pipeline.enriquecer_experiencia
   python -m pipeline.enriquecer_competencia_transferivel
   python -m pipeline.cruzar_bases_oficiais     # confere CPFs em TCU, TSE 2022, CEIS, CNEP, CEAF e Ibama (data/raw/); precisa do parquet enriquecido
   python -m pipeline.gerar_idoneidade_estrutural # idoneidade pessoal de Deputado Federal a partir das bases acima, sem busca na web
   python -m pipeline.enriquecer_idoneidade
   python -m pipeline.enriquecer_circulo_politico
   python -m pipeline.calcular_idoneidade_geral
   python -m pipeline.enriquecer_posicionamento_ideologico
   python -m pipeline.mapear_escolaridade
   python -m pipeline.calcular_competencia_geral
   python -m pipeline.calcular_cobertura
   python -m pipeline.exportar_prototipo        # gera site/dados.js (índice) e site/dados/<cargo>_<uf>.js (um por grupo)
   ```

   Qualquer linha `Aviso:` no stderr indica uma nota que diverge das tabelas de peso em `pipeline/pesos.py` —
   resolva antes de seguir.
3. Abra `site/index.html` direto no navegador (funciona por duplo clique, sem servidor).

Metodologia completa do funil de recomendação: [`docs/funil_recomendacao.md`](docs/funil_recomendacao.md).
Os descontos de idoneidade seguem categorias fechadas com pesos em [`pipeline/pesos.py`](pipeline/pesos.py); as regras
de classificação usadas na busca dos deputados estão em
[`docs/busca_deputados_finalistas_2026-09-25.md`](docs/busca_deputados_finalistas_2026-09-25.md).

## Cobertura atual

| Cargo | Como foi avaliado |
|---|---|
| Presidente, Governador (27 UFs) e Senador (27 UFs) | Pesquisa individual na internet de todos os candidatos: processos e achados, círculo político (vice, suplentes, coligação, caciques do partido), experiência e posicionamento ideológico. |
| Deputado Federal, Estadual e Distrital | Verificação estrutural de todos os ~19,5 mil candidatos, sem busca na web: círculo político (presidente do partido), cargos eletivos de 2014 a 2024 no TSE e cruzamento com bases oficiais (TCU, TSE 2022, CEIS, CNEP, CEAF, Ibama). Em seguida, busca rápida na internet dos finalistas de cada quadrante e de todos os empatados com eles; concluída nos 27 estados. |

O site mostra, em cada candidato, a profundidade da pesquisa (aprofundada, padrão, rápida ou estrutural) e as fontes
usadas.

## Como contribuir

Veja [`CONTRIBUTING.md`](CONTRIBUTING.md) — formas de ajudar incluem pesquisar candidatos ainda não cobertos
(sobretudo aprofundar a busca dos deputados, hoje rápida ou só estrutural), corrigir ou atualizar achados
existentes, e melhorar código/site.

## Limitações conhecidas

- Profundidade desigual: Presidente, Governador e Senador têm pesquisa individual na web; Deputados têm verificação
  estrutural (bases oficiais, sem processos judiciais nem notícias) e só os finalistas passaram por uma busca rápida.
- Nota 10 de idoneidade significa "nada encontrado na busca", não "nada aconteceu" — a profundidade da apuração
  varia, sobretudo para partidos menores.
- "Competência" mede formação e experiência declaradas, favorecendo quem tem carreira eletiva ou diploma superior
  — não mede a qualidade do plano de governo.
- O questionário de 2 perguntas para descobrir o posicionamento ideológico do eleitor ainda não foi calibrado nem
  testado com eleitores reais.

## Licença

[CC BY-NC-SA 4.0](LICENSE.md) — uso e modificação livres, inclusive para criar seu próprio site a partir disso,
desde que não seja para fins comerciais, com atribuição e mantendo a mesma licença nas derivações.

## Autor

André Felipe Suzano Massa
