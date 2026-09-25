"""Grava em data/reference/idoneidade.json o resultado da busca na web dos deputados finalistas de uma UF.

Uso: python aplicar_busca.py resultados_SP.json
O JSON de entrada é {sq: {"achados": [...], "motivo": "...", "fontes": [...]}}.
Os achados estruturais (TCU, CEIS/CNEP, Ibama) já existentes são mantidos, porque o registro manual substitui
o estrutural inteiro. A profundidade do candidato vira 'rapida' (exceção em profundidade_pesquisa.json).
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]  # raiz do repositório
sys.path.insert(0, str(RAIZ))
from pipeline.pesos import calcular_nota  # noqa: E402

IDON = RAIZ / "data/reference/idoneidade.json"
PROF = RAIZ / "data/reference/profundidade_pesquisa.json"
ESTR = RAIZ / "data/processed/estrutural_idoneidade.json"
DATA = "2026-09-25"

entrada = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
idon = json.loads(IDON.read_text(encoding="utf-8"))
prof = json.loads(PROF.read_text(encoding="utf-8"))
estr = json.loads(ESTR.read_text(encoding="utf-8"))["candidatos"]
prof.setdefault("excecoes", {})

for sq, r in entrada.items():
    base = estr[sq]
    if sq in idon["candidatos"] and idon["candidatos"][sq].get("origem") != "busca_finalistas":
        sys.exit(f"{sq} já tem registro manual de outra origem; revisar à mão")
    achados = list(base.get("achados", [])) + r["achados"]
    nota = calcular_nota(achados)
    estrutural_txt = ""
    if base.get("achados"):
        estrutural_txt = " Bases oficiais: " + "; ".join(a["descricao"] for a in base["achados"])
    busca_txt = r["motivo"] if r["achados"] else "Busca rápida na internet (1 busca): " + r["motivo"]
    idon["candidatos"][sq] = {
        "nome_urna": base["nome_urna"],
        "cargo_pretendido": base["cargo_pretendido"],
        "nota": nota,
        "motivo": busca_txt + estrutural_txt,
        "fontes": list(dict.fromkeys(r["fontes"] + base.get("fontes", []))),
        "pesquisado_em": DATA,
        "achados": achados,
        "origem": "busca_finalistas",
    }
    prof["excecoes"][sq] = "rapida"
    print(f"{base['nome_urna']:<35} {base['nota']:>4} -> {nota}")

IDON.write_text(json.dumps(idon, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
PROF.write_text(json.dumps(prof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
