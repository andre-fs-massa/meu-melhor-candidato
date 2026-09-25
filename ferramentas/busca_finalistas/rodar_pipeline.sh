#!/bin/sh
# Roda o pipeline a partir da idoneidade (sem exportar o site) e mostra só avisos novos e erros.
cd "$(dirname "$0")/../.." || exit 1
LOG="${TMPDIR:-/tmp}/busca_finalistas_pipeline.log"
: > "$LOG"
for passo in enriquecer_idoneidade enriquecer_circulo_politico calcular_idoneidade_geral enriquecer_posicionamento_ideologico mapear_escolaridade calcular_competencia_geral calcular_cobertura; do
  echo "== $passo" >> "$LOG"
  PYTHONUTF8=1 python -m pipeline.$passo >> "$LOG" 2>&1 || { echo "FALHOU: $passo"; tail -20 "$LOG"; exit 1; }
done
PYTHONUTF8=1 python -m pipeline.recomendar --csv >> "$LOG" 2>&1 || { echo "FALHOU: recomendar"; exit 1; }
grep -n "Aviso\|Traceback\|Error" "$LOG" | grep -v "NÃO DIVULGÁVEL" || echo "sem avisos"
