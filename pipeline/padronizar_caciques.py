"""Padroniza os caciques do círculo político (Presidente, Governador, Senador) -- 2026-09-24.

Uso: python -m pipeline.padronizar_caciques [--aplicar] [--sem-federacao]
Sem --aplicar só mostra o que mudaria. --sem-federacao não conta os membros das federações.
Depois de aplicar, rodar o pipeline a partir de enriquecer_circulo_politico.

Regra única:
  * caciques = presidente NACIONAL de cada partido que compõe a coligação segundo o TSE
    (DS_COMPOSICAO_COLIGACAO), incluindo os membros das federações listadas nela e da federação
    do próprio candidato (federação age como um partido só na eleição);
  * a pendência de cada presidente vem de UMA linha canônica por partido
    (liderancas_partidarias.json -> campo "cacique"), igual em todos os registros;
  * partido citado no registro mas fora da composição oficial fica com contado=false;
  * presidente que já está na chapa (vice/suplente/padrinho) não é contado de novo;
  * quando o próprio candidato preside o partido, conta o mesmo desconto de cacique que qualquer
    candidato daquele partido recebe (substitui os "descontos_adicionais" ad hoc).
"""
import json, re, sys
import pandas as pd

from . import config
from .pesos import PESOS_CACIQUE
from .enriquecer_circulo_politico import calcular_nota, TIPOS_CACIQUE

R = str(config.RAW_DIR.parent / "reference") + "/"
HOJE = "2026-09-24"

CANON = {  # partido: (presidente, tipo_pendencia, pendência curta, fontes novas)
    "PSD": ("Gilberto Kassab", "reu_acao_penal",
            "Réu desde 2021 no caso JBS (corrupção, lavagem, caixa 2, associação criminosa), sem sentença. Condenado por improbidade em 1ª instância em 2014 (precatórios de 2006), desfecho do recurso não localizado; a ação dos precatórios de 2007 terminou em absolvição mantida pelo TJSP (2019). Sem condenação confirmada localizada",
            ["https://conjur.com.br/2014-jun-04/kassab-condenado-improbidade-direitos-politicos-suspensos/",
             "https://www.conjur.com.br/2019-ago-23/tj-mantem-absolvicao-kassab-nao-pagar-precatorios-alimentares/"]),
    "PL": ("Valdemar Costa Neto", "condenacao_criminal_confirmada", "Condenado e preso no Mensalão (2012); indultado em 2016", []),
    "REPUBLICANOS": ("Marcos Pereira", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "NOVO": ("Eduardo Ribeiro", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "PCO": ("Rui Costa Pimenta", "investigado_sem_denuncia", "Alvo de operação da PF por suposto desvio de verba eleitoral, sem denúncia", []),
    "MISSÃO": ("Renan Santos", "acao_civil_em_curso",
               "Ação civil pública do MPF em curso (discurso de ódio contra indígenas); condenação cível anterior por danos morais (não é improbidade); sem questão penal", []),
    "PT": ("Edinho Silva", "investigacao_arquivada_sem_denuncia", "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia", []),
    "PDT": ("Carlos Lupi", "delatado_sem_denuncia", "Delatado por ex-dirigentes do INSS (fraude dos descontos), sem denúncia", []),
    "PSDB": ("Aécio Neves", "investigacao_arquivada_sem_denuncia",
             "Inquérito INQ 4830 arquivado pelo STF (fev/2024); absolvido da acusação de propina de R$ 2 mi da J&F (1ª instância 2022, confirmada por unanimidade no TRF-3); sem pendência ativa",
             ["https://www.cnnbrasil.com.br/politica/justica-absolve-aecio-neves-de-acusacao-de-propina-de-r-2-milhoes-da-jf/",
              "https://www.metropoles.com/brasil/aecio-neves-e-absolvido-de-forma-unanime-em-caso-de-corrupcao-passiva"]),
    "PP": ("Ciro Nogueira", "investigado_sem_denuncia", "Alvo da PF na Operação Compliance Zero (caso Banco Master), sem denúncia", []),
    "UNIÃO": ("Antonio Rueda", "investigado_sem_denuncia", "Investigado pela PF na Operação Carbono Oculto, sem denúncia", []),
    "MDB": ("Baleia Rossi", "investigado_sem_denuncia",
            "Citado em inquérito sigiloso no STF desde 2018 (fraudes em Ribeirão Preto e delação da JBS), sem denúncia; o caso Alba Branca foi arquivado",
            ["https://www.poder360.com.br/congresso/baleia-rossi-e-citado-em-investigacoes-contra-fraudes-e-em-delacao-da-jbs/"]),
    "PSB": ("João Campos", "nenhuma_encontrada", "Nenhuma pendência pessoal como dirigente encontrada (busca geral)", []),
    "PSOL": ("Paula Coradi", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "SOLIDARIEDADE": ("Paulinho da Força", "investigado_sem_denuncia", "Investigado em inquérito no STF (captação de clientes para ações trabalhistas), sem denúncia", []),
    "AVANTE": ("Luis Tibé", "condenacao_civil", "Condenado por improbidade civil (2015, verba indenizatória da Câmara de BH); dívida quitada", []),
    "PCDOB": ("Nádia Campeão", "nenhuma_encontrada",
              "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada",
              ["https://pcdob.org.br/noticias/pcdob-inicia-transicao-na-presidencia-com-nadia-campeao-a-frente/",
               "https://www.leiaja.com/politica/2019/11/02/luciana-santos-e-condenada-por-improbidade-administrativa/"]),
    "PRD": ("Marcus Vinícius Neskau", "investigado_sem_denuncia",
            "Afastado da presidência do PTB por Alexandre de Moraes (2022, INQ 4874, milícias digitais) por atuar como fachada de Roberto Jefferson; mandado ouvir pela PF; sem denúncia localizada",
            ["https://noticias.stf.jus.br/postsnoticias/ministro-alexandre-de-moraes-afasta-presidente-do-ptb-e-determina-que-pf-ouca-roberto-jefferson/"]),
    "CIDADANIA": ("Roberto Freire", "nao_verificado",
                  "Presidência restituída a Roberto Freire por decisão judicial mantida pelo STF (2026), após disputa com Comte Bittencourt; pendências pessoais não pesquisadas",
                  ["https://www.band.com.br/noticias/destituido-da-presidencia-do-cidadania-pelo-stf-comte-bittencourt-ainda-detem-a-chave-do-partido-usada-no-tse-202601071637"]),
    "PV": ("José Luiz de França Penna", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "UP": ("Leonardo Péricles", "nenhuma_encontrada", "Nenhuma pendência pessoal encontrada (busca geral)", []),
    "PSTU": ("José Maria Almeida", "nenhuma_encontrada", "Nenhuma pendência pessoal encontrada (busca geral)", []),
    "REDE": ("Paulo Lamac", "condenacao_civil", "Acordo com o MPMG (2026) para encerrar ação por uso irregular de verba pública, pagando cerca de R$ 171 mil", []),
    "DEMOCRATA": ("Suêd Haidar", "nao_verificado", "Processos de 2026 com a Procuradoria-Geral Eleitoral sem objeto identificado; não contado", []),
    "DC": ("João Caldas", "condenacao_confirmada_sem_reversao", "Condenado por improbidade na Máfia das Ambulâncias (Operação Taturana), confirmada pelo Plenário do TRF-5, com perda de direitos políticos", []),
    "AGIR": ("Daniel Tourinho", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "MOBILIZA": ("Antonio Carlos Massarollo", "nenhuma_encontrada", "Nenhuma pendência encontrada (busca geral)", []),
    "PRTB": ("Leonardo Avalanche", "reu_acao_penal", "Réu desde mar/2026 por associação criminosa, violência política de gênero e inserção de dados falsos; investigado por desvio do fundo eleitoral", []),
    "PCB": ("Edmilson Costa", "nenhuma_encontrada", "Nenhuma pendência pessoal encontrada (busca geral)", []),
    "PODE": ("Renata Abreu", "investigado_sem_denuncia", "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia", []),
}
# entrada de cacique estadual mantida de propósito (irmão da vice, presidente do MDB-RJ)
MANTER = {"Washington Reis"}
ADIC_REMOVER = re.compile(r"PCO|preside o próprio partido|próprio preside", re.I)


def sig(x):
    x = x.strip().upper().replace(" ", "")
    return {"PCDOB": "PCDOB", "PODEMOS": "PODE", "UNIAO": "UNIÃO", "MISSAO": "MISSÃO"}.get(x, x)


def primeiro_nome(n):
    return re.sub(r"[^a-z]", "", n.lower().split()[0]) if n else ""


def mesmo(a, b):
    a, b = a.lower(), b.lower()
    return a in b or b in a or (primeiro_nome(a) == primeiro_nome(b) and a.split()[-1] == b.split()[-1])


def composicao(row, com_federacao=True):
    comp = row.DS_COMPOSICAO_COLIGACAO or ""
    ps = {sig(row.SG_PARTIDO)}
    if com_federacao:
        for m in re.finditer(r"\(([^)]*)\)", comp):
            ps |= {sig(p.split("-", 1)[1]) for p in m.group(1).split("/")}
    for p in re.sub(r"FEDERA[ÇC][ÃA]O[^(]*\([^)]*\)", "", comp).split("/"):
        if p.strip() and "ISOLADO" not in p.upper():
            ps.add(sig(p))
    if com_federacao and row.DS_COMPOSICAO_FEDERACAO and row.DS_COMPOSICAO_FEDERACAO != "#NULO":
        ps |= {sig(p.split("-", 1)[1]) for p in row.DS_COMPOSICAO_FEDERACAO.split("/")}
    return ps


def main(aplicar, com_federacao=True):
    cir_all = json.load(open(R + "circulo_politico.json", encoding="utf-8"))
    cir = cir_all["candidatos"]
    t = pd.read_csv(config.EXTRACT_DIR / "consulta_cand_2026_BRASIL.csv", sep=";", encoding="latin-1", dtype=str)
    t = t[t.DS_CARGO.isin(["PRESIDENTE", "GOVERNADOR", "SENADOR"])].set_index("SQ_CANDIDATO")
    mud = []
    for sq, r in cir.items():
        if sq not in t.index:
            continue
        row = t.loc[sq]
        partido = sig(row.SG_PARTIDO)
        comp = composicao(row, com_federacao)
        falta = sorted(p for p in comp if p not in CANON)
        if falta:
            print("SEM CANON:", r["nome_urna"], falta)
        antes = r["nota"]
        aps = r.get("apoiadores", [])
        chapa = [a for a in aps if a["tipo_ligacao"] not in TIPOS_CACIQUE]
        velhos = [a for a in aps if a["tipo_ligacao"] in TIPOS_CACIQUE]
        novos = []
        for p in sorted(comp, key=lambda p: (p != partido, p)):
            if p not in CANON:
                continue
            nome, tp, pend, _ = CANON[p]
            ap = {"nome": nome, "partido": p,
                  "tipo_ligacao": "presidente_do_partido_do_candidato" if p == partido else "presidente_de_partido_aliado",
                  "ligacao_detalhe": (f"presidente nacional do {p}, partido do candidato" if p == partido
                                      else f"presidente nacional do {p}, que integra a coligação/federação no TSE"),
                  "tipo_pendencia": tp, "pendencia": pend, "desconto": PESOS_CACIQUE[tp], "contado": True}
            if mesmo(nome, r["nome_urna"]) or (p == partido and mesmo(nome, row.NM_CANDIDATO)):
                ap["ligacao_detalhe"] = f"o próprio candidato preside o {p}; conta o mesmo desconto de cacique que qualquer candidato do partido"
            dup = next((a for a in chapa if mesmo(nome, a["nome"])), None)
            if dup:
                ap["contado"] = False
                ap["pendencia"] += f" -- já contado como {dup['tipo_ligacao']}"
            novos.append(ap)
        for a in velhos:
            p = sig(a.get("partido") or "")
            if a["nome"] in MANTER:
                novos.append(a)
            elif p not in comp and p in CANON and a.get("contado", True):
                b = dict(a)
                b["contado"] = False
                b["pendencia"] = CANON[p][2] + " -- NÃO contado: partido fora da composição oficial da coligação no TSE"
                b["tipo_pendencia"], b["desconto"] = CANON[p][1], PESOS_CACIQUE[CANON[p][1]]
                novos.append(b)
        adic = [d for d in r.get("descontos_adicionais", []) if not ADIC_REMOVER.search(d["motivo"])]
        rem = [d for d in r.get("descontos_adicionais", []) if ADIC_REMOVER.search(d["motivo"])]
        novo = dict(r)
        novo["apoiadores"] = chapa + novos
        novo["descontos_adicionais"] = adic
        depois = calcular_nota(novo)
        nomes_antes = sorted((sig(a.get("partido") or ""), a["tipo_pendencia"], a["desconto"], a.get("contado", True)) for a in velhos)
        nomes_dep = sorted((a["partido"], a["tipo_pendencia"], a["desconto"], a.get("contado", True)) for a in novos)
        if nomes_antes != nomes_dep or rem or depois != antes:
            mud.append((r["cargo_pretendido"], row.SG_UF, r["nome_urna"], antes, depois, rem))
            if depois != antes:
                novo["motivo"] = (f"PADRONIZADO em {HOJE} (caciques = presidentes nacionais de todos os partidos da coligação oficial no TSE, "
                                  f"com a mesma pendência por partido em todo o projeto): nota {antes} -> {depois}. || " + r["motivo"])
            if aplicar:
                novo["padronizado_em"] = HOJE
                cir[sq] = novo
    for m in mud:
        flag = "  <<< NOTA MUDA" if m[3] != m[4] else ""
        print(f"{m[0][:3]} {m[1]} {m[2]}: {m[3]} -> {m[4]}{flag}" + (f"  (removido adicional: {[d['desconto'] for d in m[5]]})" if m[5] else ""))
    print(len(mud), "registros alterados;", sum(1 for m in mud if m[3] != m[4]), "com nota diferente")
    if aplicar:
        for sq, r in cir.items():
            if sq in t.index and r.get("padronizado_em") == HOJE:
                r["nota"] = calcular_nota(r)
        json.dump(cir_all, open(R + "circulo_politico.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
        lid_all = json.load(open(R + "liderancas_partidarias.json", encoding="utf-8"))
        for p, (nome, tp, pend, fontes) in CANON.items():
            e = lid_all["partidos"].setdefault(p, {"presidente_nacional": nome, "pendencias": pend, "fontes": [], "pesquisado_em": HOJE})
            e["cacique"] = {"nome": nome, "tipo_pendencia": tp, "desconto": PESOS_CACIQUE[tp], "pendencia": pend, "definido_em": HOJE}
            for f in fontes:
                if f not in e.setdefault("fontes", []):
                    e["fontes"].append(f)
        json.dump(lid_all, open(R + "liderancas_partidarias.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
        print("gravado")


if __name__ == "__main__":
    main("--aplicar" in sys.argv, "--sem-federacao" not in sys.argv)
