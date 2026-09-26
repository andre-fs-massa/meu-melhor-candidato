"""Grava a 2ª rodada de busca (pelo nome completo) dos deputados finalistas, SOMANDO aos achados da 1ª rodada.

Uso: python aplicar_rodada2.py resultados_2a_SP.json
O JSON de entrada é {sq: {"achados": [...novos...], "motivo": "...", "fontes": [...]}}.
- Sem achados novos: o motivo da 1ª rodada é mantido e ganha o sufixo "2ª rodada (...): <motivo>".
- Com achados novos: o motivo informado substitui o texto da busca (deve resumir as duas rodadas); o trecho
  "Bases oficiais: ..." do estrutural é mantido.
O registro ganha "rodada2": DATA. Candidato ainda sem 1ª rodada é recusado (rodar aplicar_busca.py antes).
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]  # raiz do repositório
sys.path.insert(0, str(RAIZ))
from pipeline.pesos import calcular_nota  # noqa: E402

IDON = RAIZ / "data/reference/idoneidade.json"
ESTR = RAIZ / "data/processed/estrutural_idoneidade.json"
DATA = "2026-09-26"

entrada = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
idon = json.loads(IDON.read_text(encoding="utf-8"))
estr = json.loads(ESTR.read_text(encoding="utf-8"))["candidatos"]

for sq, r in entrada.items():
    reg = idon["candidatos"].get(sq)
    if not reg or reg.get("origem") != "busca_finalistas":
        sys.exit(f"{sq} sem 1ª rodada gravada (origem busca_finalistas); rodar aplicar_busca.py antes")
    base = estr[sq].get("achados", [])
    busca_ant = reg["achados"][len(base):]
    motivo_ant, _, bases_txt = reg["motivo"].partition(" Bases oficiais: ")
    bases_txt = (" Bases oficiais: " + bases_txt) if bases_txt else ""
    if r["achados"]:
        motivo = r["motivo"]
    else:
        motivo = motivo_ant.rstrip(". ") + ". 2ª rodada (busca pelo nome completo, 26/09): " + r["motivo"]
    nota_ant = reg["nota"]
    reg["achados"] = list(base) + busca_ant + r["achados"]
    reg["nota"] = calcular_nota(reg["achados"])
    reg["motivo"] = motivo + bases_txt
    reg["fontes"] = list(dict.fromkeys(reg["fontes"] + r["fontes"]))
    reg["rodada2"] = DATA
    print(f"{reg['nome_urna']:<35} {nota_ant:>4} -> {reg['nota']}")

IDON.write_text(json.dumps(idon, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
