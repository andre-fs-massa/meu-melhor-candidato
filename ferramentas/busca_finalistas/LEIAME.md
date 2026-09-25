# Ferramentas da busca na web dos deputados finalistas

Apoio à fase 2 dos deputados (método e regras em `docs/busca_deputados_finalistas_2026-09-25.md`). Rodar da raiz do
repositório, com `PYTHONUTF8=1` no Windows.

1. `python ferramentas/busca_finalistas/pendentes.py BA` — lista quem falta pesquisar no bloco do topo de cada
   quadrante da UF (estado fechado = `TOTAL pendentes BA: 0`).
2. Pesquisar cada um (1 busca, modelo fixo) e gravar um JSON `{sq: {"achados": [...], "motivo": "...", "fontes": [...]}}`
   com categorias de `pipeline/pesos.py`.
3. `python ferramentas/busca_finalistas/aplicar_busca.py resultados_BA.json` — grava em `data/reference/idoneidade.json`
   (somando os achados das bases oficiais) e marca a profundidade "rapida".
4. `sh ferramentas/busca_finalistas/rodar_pipeline.sh` — recalcula do passo da idoneidade até o funil; deve terminar
   com "sem avisos". Voltar ao passo 1 até não haver pendentes.
5. `python ferramentas/busca_finalistas/secao_uf.py BA` — gera a seção da UF para colar no relatório.

Não exporta o site: publicar exige `python -m pipeline.exportar_prototipo` e aprovação.
