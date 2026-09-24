# Meu melhor candidato

Projeto independente e open source para ajudar eleitores brasileiros a avaliar candidatos nas eleições de 2026,
cruzando três coisas: **idoneidade** (processos, Ficha Limpa, círculo político), **competência** (formação e
experiência) e **alinhamento ideológico** (diagrama de Nolan). 1º turno em 4 de outubro de 2026.

🔗 **Site:** _em breve (publicação pendente)_

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
| `docs/` | Metodologia detalhada do funil de recomendação. |

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
   python -m pipeline.exportar_prototipo        # gera site/dados.js
   ```

   Qualquer linha `Aviso:` no stderr indica uma nota que diverge das tabelas de peso em `pipeline/pesos.py` —
   resolva antes de seguir.
3. Abra `site/index.html` direto no navegador (funciona por duplo clique, sem servidor).

Metodologia completa do funil de recomendação: [`docs/funil_recomendacao.md`](docs/funil_recomendacao.md).

## Como contribuir

Veja [`CONTRIBUTING.md`](CONTRIBUTING.md) — formas de ajudar incluem pesquisar candidatos ainda não cobertos
(Senador e Deputados estão 100% pendentes), corrigir ou atualizar achados existentes, e melhorar código/site.

## Limitações conhecidas

- Cobertura desigual: hoje só há verificação completa para Presidente e para Governador em vários estados. Senador
  e Deputados (Estadual/Distrital/Federal) ainda não têm nenhuma pesquisa.
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
