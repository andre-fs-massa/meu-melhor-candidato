// Gerado por pipeline/exportar_prototipo.py -- não editar à mão. Índice: cada cargo/UF tem o seu arquivo em dados/.
const DADOS = {
 "meta": {
  "gerado_em": "2026-09-26",
  "corte": 6.0,
  "corte_deputados": 8.5,
  "limiar": 5.0,
  "margem_fronteira": 0.5,
  "politica_nao_avaliados": "excluir",
  "data_eleicao": "2026-10-04",
  "total_candidatos": 20042
 },
 "profundidade": {
  "aprofundada": {
   "rotulo": "Pesquisa aprofundada",
   "descricao": "Várias buscas por candidato, reconferência dos achados e dos vices, e revisão das notas mais baixas."
  },
  "padrao": {
   "rotulo": "Pesquisa padrão",
   "descricao": "Várias buscas por candidato na internet, com reconferência dos achados mais graves."
  },
  "rapida": {
   "rotulo": "Pesquisa rápida",
   "descricao": "1 a 2 buscas na internet por candidato. Nota 10 significa apenas \"nada encontrado\"; não é atestado de que não haja pendência."
  },
  "estrutural": {
   "rotulo": "Verificação estrutural",
   "descricao": "Sem busca individual na internet: círculo político (só o presidente do partido), experiência política (cargos eletivos de 2014 a 2024 no TSE) e conferência em bases oficiais. Nota 10 quer dizer apenas que nada consta nessas bases; não inclui processos judiciais, inquéritos nem notícias."
  }
 },
 "bases_oficiais": [
  {
   "id": "tcu_eleitoral",
   "rotulo": "TCU: contas julgadas irregulares (implicação eleitoral)",
   "data": "2026-09-24"
  },
  {
   "id": "tse_2022",
   "rotulo": "TSE: motivos de indeferimento/cassação em 2022",
   "data": "2026-09-24"
  },
  {
   "id": "ceis",
   "rotulo": "CEIS: empresas e pessoas sancionadas (Portal da Transparência)",
   "data": "2026-09-23"
  },
  {
   "id": "cnep",
   "rotulo": "CNEP: punições da Lei Anticorrupção (Portal da Transparência)",
   "data": "2026-09-23"
  },
  {
   "id": "ceaf",
   "rotulo": "CEAF: servidores expulsos do serviço público federal",
   "data": "2026-09-23"
  },
  {
   "id": "ibama",
   "rotulo": "Ibama: autos de infração ambiental",
   "data": "2026-09-24"
  }
 ],
 "quadrantes": [
  {
   "chave": "LIBERTARIO",
   "nome": "Libertário (economia livre, costumes liberais)",
   "curto": "Libertário"
  },
  {
   "chave": "DIREITA",
   "nome": "Direita conservadora (economia livre, costumes conservadores)",
   "curto": "Direita conservadora"
  },
  {
   "chave": "ESQUERDA",
   "nome": "Esquerda progressista (mais Estado na economia, costumes liberais)",
   "curto": "Esquerda progressista"
  },
  {
   "chave": "AUTORITARIO",
   "nome": "Estatista-autoritário (mais Estado na economia, costumes conservadores)",
   "curto": "Estatista-autoritário"
  }
 ],
 "cargos": [
  {
   "codigo": "PRESIDENTE",
   "rotulo": "Presidente",
   "vagas": 1
  },
  {
   "codigo": "GOVERNADOR",
   "rotulo": "Governador",
   "vagas": 1
  },
  {
   "codigo": "SENADOR",
   "rotulo": "Senador",
   "vagas": 1
  },
  {
   "codigo": "DEPUTADO FEDERAL",
   "rotulo": "Deputado federal",
   "vagas": 3
  },
  {
   "codigo": "DEPUTADO ESTADUAL",
   "rotulo": "Deputado estadual",
   "vagas": 3
  },
  {
   "codigo": "DEPUTADO DISTRITAL",
   "rotulo": "Deputado distrital",
   "vagas": 3
  }
 ],
 "grupos": {
  "DEPUTADO DISTRITAL|DF": {
   "cargo": "DEPUTADO DISTRITAL",
   "uf": "DF",
   "n_total": 433,
   "n_avaliados": 433,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_distrital_df.js"
  },
  "DEPUTADO ESTADUAL|AC": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "AC",
   "n_total": 247,
   "n_avaliados": 247,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ac.js"
  },
  "DEPUTADO ESTADUAL|AL": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "AL",
   "n_total": 144,
   "n_avaliados": 144,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_al.js"
  },
  "DEPUTADO ESTADUAL|AM": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "AM",
   "n_total": 294,
   "n_avaliados": 294,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_am.js"
  },
  "DEPUTADO ESTADUAL|AP": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "AP",
   "n_total": 194,
   "n_avaliados": 194,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ap.js"
  },
  "DEPUTADO ESTADUAL|BA": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "BA",
   "n_total": 640,
   "n_avaliados": 640,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ba.js"
  },
  "DEPUTADO ESTADUAL|CE": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "CE",
   "n_total": 376,
   "n_avaliados": 376,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ce.js"
  },
  "DEPUTADO ESTADUAL|ES": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "ES",
   "n_total": 410,
   "n_avaliados": 410,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_es.js"
  },
  "DEPUTADO ESTADUAL|GO": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "GO",
   "n_total": 594,
   "n_avaliados": 594,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_go.js"
  },
  "DEPUTADO ESTADUAL|MA": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "MA",
   "n_total": 285,
   "n_avaliados": 285,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ma.js"
  },
  "DEPUTADO ESTADUAL|MG": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "MG",
   "n_total": 998,
   "n_avaliados": 998,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_mg.js"
  },
  "DEPUTADO ESTADUAL|MS": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "MS",
   "n_total": 253,
   "n_avaliados": 253,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ms.js"
  },
  "DEPUTADO ESTADUAL|MT": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "MT",
   "n_total": 268,
   "n_avaliados": 268,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_mt.js"
  },
  "DEPUTADO ESTADUAL|PA": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "PA",
   "n_total": 417,
   "n_avaliados": 417,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_pa.js"
  },
  "DEPUTADO ESTADUAL|PB": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "PB",
   "n_total": 213,
   "n_avaliados": 213,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_pb.js"
  },
  "DEPUTADO ESTADUAL|PE": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "PE",
   "n_total": 517,
   "n_avaliados": 517,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_pe.js"
  },
  "DEPUTADO ESTADUAL|PI": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "PI",
   "n_total": 153,
   "n_avaliados": 153,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_pi.js"
  },
  "DEPUTADO ESTADUAL|PR": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "PR",
   "n_total": 617,
   "n_avaliados": 617,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_pr.js"
  },
  "DEPUTADO ESTADUAL|RJ": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "RJ",
   "n_total": 1188,
   "n_avaliados": 1188,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_rj.js"
  },
  "DEPUTADO ESTADUAL|RN": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "RN",
   "n_total": 154,
   "n_avaliados": 154,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_rn.js"
  },
  "DEPUTADO ESTADUAL|RO": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "RO",
   "n_total": 260,
   "n_avaliados": 260,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_ro.js"
  },
  "DEPUTADO ESTADUAL|RR": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "RR",
   "n_total": 250,
   "n_avaliados": 250,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_rr.js"
  },
  "DEPUTADO ESTADUAL|RS": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "RS",
   "n_total": 542,
   "n_avaliados": 542,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_rs.js"
  },
  "DEPUTADO ESTADUAL|SC": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "SC",
   "n_total": 414,
   "n_avaliados": 414,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_sc.js"
  },
  "DEPUTADO ESTADUAL|SE": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "SE",
   "n_total": 222,
   "n_avaliados": 222,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_se.js"
  },
  "DEPUTADO ESTADUAL|SP": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "SP",
   "n_total": 1430,
   "n_avaliados": 1430,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_sp.js"
  },
  "DEPUTADO ESTADUAL|TO": {
   "cargo": "DEPUTADO ESTADUAL",
   "uf": "TO",
   "n_total": 209,
   "n_avaliados": 209,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_estadual_to.js"
  },
  "DEPUTADO FEDERAL|AC": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "AC",
   "n_total": 102,
   "n_avaliados": 102,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ac.js"
  },
  "DEPUTADO FEDERAL|AL": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "AL",
   "n_total": 110,
   "n_avaliados": 110,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_al.js"
  },
  "DEPUTADO FEDERAL|AM": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "AM",
   "n_total": 139,
   "n_avaliados": 139,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_am.js"
  },
  "DEPUTADO FEDERAL|AP": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "AP",
   "n_total": 91,
   "n_avaliados": 91,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ap.js"
  },
  "DEPUTADO FEDERAL|BA": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "BA",
   "n_total": 532,
   "n_avaliados": 532,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ba.js"
  },
  "DEPUTADO FEDERAL|CE": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "CE",
   "n_total": 295,
   "n_avaliados": 295,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ce.js"
  },
  "DEPUTADO FEDERAL|DF": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "DF",
   "n_total": 172,
   "n_avaliados": 172,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_df.js"
  },
  "DEPUTADO FEDERAL|ES": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "ES",
   "n_total": 137,
   "n_avaliados": 137,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_es.js"
  },
  "DEPUTADO FEDERAL|GO": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "GO",
   "n_total": 265,
   "n_avaliados": 265,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_go.js"
  },
  "DEPUTADO FEDERAL|MA": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "MA",
   "n_total": 282,
   "n_avaliados": 282,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ma.js"
  },
  "DEPUTADO FEDERAL|MG": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "MG",
   "n_total": 756,
   "n_avaliados": 756,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_mg.js"
  },
  "DEPUTADO FEDERAL|MS": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "MS",
   "n_total": 124,
   "n_avaliados": 124,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ms.js"
  },
  "DEPUTADO FEDERAL|MT": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "MT",
   "n_total": 138,
   "n_avaliados": 138,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_mt.js"
  },
  "DEPUTADO FEDERAL|PA": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "PA",
   "n_total": 268,
   "n_avaliados": 268,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_pa.js"
  },
  "DEPUTADO FEDERAL|PB": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "PB",
   "n_total": 190,
   "n_avaliados": 190,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_pb.js"
  },
  "DEPUTADO FEDERAL|PE": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "PE",
   "n_total": 392,
   "n_avaliados": 392,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_pe.js"
  },
  "DEPUTADO FEDERAL|PI": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "PI",
   "n_total": 162,
   "n_avaliados": 162,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_pi.js"
  },
  "DEPUTADO FEDERAL|PR": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "PR",
   "n_total": 428,
   "n_avaliados": 428,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_pr.js"
  },
  "DEPUTADO FEDERAL|RJ": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "RJ",
   "n_total": 793,
   "n_avaliados": 793,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_rj.js"
  },
  "DEPUTADO FEDERAL|RN": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "RN",
   "n_total": 111,
   "n_avaliados": 111,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_rn.js"
  },
  "DEPUTADO FEDERAL|RO": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "RO",
   "n_total": 134,
   "n_avaliados": 134,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_ro.js"
  },
  "DEPUTADO FEDERAL|RR": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "RR",
   "n_total": 108,
   "n_avaliados": 108,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_rr.js"
  },
  "DEPUTADO FEDERAL|RS": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "RS",
   "n_total": 458,
   "n_avaliados": 458,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_rs.js"
  },
  "DEPUTADO FEDERAL|SC": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "SC",
   "n_total": 231,
   "n_avaliados": 231,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_sc.js"
  },
  "DEPUTADO FEDERAL|SE": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "SE",
   "n_total": 141,
   "n_avaliados": 141,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_se.js"
  },
  "DEPUTADO FEDERAL|SP": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "SP",
   "n_total": 1131,
   "n_avaliados": 1131,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_sp.js"
  },
  "DEPUTADO FEDERAL|TO": {
   "cargo": "DEPUTADO FEDERAL",
   "uf": "TO",
   "n_total": 98,
   "n_avaliados": 98,
   "corte": 8.5,
   "status": "completo",
   "arquivo": "dados/deputado_federal_to.js"
  },
  "GOVERNADOR|AC": {
   "cargo": "GOVERNADOR",
   "uf": "AC",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_ac.js"
  },
  "GOVERNADOR|AL": {
   "cargo": "GOVERNADOR",
   "uf": "AL",
   "n_total": 4,
   "n_avaliados": 4,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_al.js"
  },
  "GOVERNADOR|AM": {
   "cargo": "GOVERNADOR",
   "uf": "AM",
   "n_total": 7,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_am.js"
  },
  "GOVERNADOR|AP": {
   "cargo": "GOVERNADOR",
   "uf": "AP",
   "n_total": 5,
   "n_avaliados": 5,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_ap.js"
  },
  "GOVERNADOR|BA": {
   "cargo": "GOVERNADOR",
   "uf": "BA",
   "n_total": 7,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_ba.js"
  },
  "GOVERNADOR|CE": {
   "cargo": "GOVERNADOR",
   "uf": "CE",
   "n_total": 9,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_ce.js"
  },
  "GOVERNADOR|DF": {
   "cargo": "GOVERNADOR",
   "uf": "DF",
   "n_total": 11,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_df.js"
  },
  "GOVERNADOR|ES": {
   "cargo": "GOVERNADOR",
   "uf": "ES",
   "n_total": 5,
   "n_avaliados": 5,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_es.js"
  },
  "GOVERNADOR|GO": {
   "cargo": "GOVERNADOR",
   "uf": "GO",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_go.js"
  },
  "GOVERNADOR|MA": {
   "cargo": "GOVERNADOR",
   "uf": "MA",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_ma.js"
  },
  "GOVERNADOR|MG": {
   "cargo": "GOVERNADOR",
   "uf": "MG",
   "n_total": 11,
   "n_avaliados": 11,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_mg.js"
  },
  "GOVERNADOR|MS": {
   "cargo": "GOVERNADOR",
   "uf": "MS",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_ms.js"
  },
  "GOVERNADOR|MT": {
   "cargo": "GOVERNADOR",
   "uf": "MT",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_mt.js"
  },
  "GOVERNADOR|PA": {
   "cargo": "GOVERNADOR",
   "uf": "PA",
   "n_total": 8,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_pa.js"
  },
  "GOVERNADOR|PB": {
   "cargo": "GOVERNADOR",
   "uf": "PB",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_pb.js"
  },
  "GOVERNADOR|PE": {
   "cargo": "GOVERNADOR",
   "uf": "PE",
   "n_total": 8,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_pe.js"
  },
  "GOVERNADOR|PI": {
   "cargo": "GOVERNADOR",
   "uf": "PI",
   "n_total": 11,
   "n_avaliados": 11,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_pi.js"
  },
  "GOVERNADOR|PR": {
   "cargo": "GOVERNADOR",
   "uf": "PR",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_pr.js"
  },
  "GOVERNADOR|RJ": {
   "cargo": "GOVERNADOR",
   "uf": "RJ",
   "n_total": 9,
   "n_avaliados": 9,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_rj.js"
  },
  "GOVERNADOR|RN": {
   "cargo": "GOVERNADOR",
   "uf": "RN",
   "n_total": 10,
   "n_avaliados": 9,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_rn.js"
  },
  "GOVERNADOR|RO": {
   "cargo": "GOVERNADOR",
   "uf": "RO",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_ro.js"
  },
  "GOVERNADOR|RR": {
   "cargo": "GOVERNADOR",
   "uf": "RR",
   "n_total": 5,
   "n_avaliados": 4,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_rr.js"
  },
  "GOVERNADOR|RS": {
   "cargo": "GOVERNADOR",
   "uf": "RS",
   "n_total": 7,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_rs.js"
  },
  "GOVERNADOR|SC": {
   "cargo": "GOVERNADOR",
   "uf": "SC",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_sc.js"
  },
  "GOVERNADOR|SE": {
   "cargo": "GOVERNADOR",
   "uf": "SE",
   "n_total": 6,
   "n_avaliados": 6,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_se.js"
  },
  "GOVERNADOR|SP": {
   "cargo": "GOVERNADOR",
   "uf": "SP",
   "n_total": 7,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/governador_sp.js"
  },
  "GOVERNADOR|TO": {
   "cargo": "GOVERNADOR",
   "uf": "TO",
   "n_total": 8,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/governador_to.js"
  },
  "PRESIDENTE|BR": {
   "cargo": "PRESIDENTE",
   "uf": "BR",
   "n_total": 14,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/presidente_br.js"
  },
  "SENADOR|AC": {
   "cargo": "SENADOR",
   "uf": "AC",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ac.js"
  },
  "SENADOR|AL": {
   "cargo": "SENADOR",
   "uf": "AL",
   "n_total": 7,
   "n_avaliados": 7,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_al.js"
  },
  "SENADOR|AM": {
   "cargo": "SENADOR",
   "uf": "AM",
   "n_total": 9,
   "n_avaliados": 9,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_am.js"
  },
  "SENADOR|AP": {
   "cargo": "SENADOR",
   "uf": "AP",
   "n_total": 9,
   "n_avaliados": 9,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ap.js"
  },
  "SENADOR|BA": {
   "cargo": "SENADOR",
   "uf": "BA",
   "n_total": 10,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ba.js"
  },
  "SENADOR|CE": {
   "cargo": "SENADOR",
   "uf": "CE",
   "n_total": 8,
   "n_avaliados": 8,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ce.js"
  },
  "SENADOR|DF": {
   "cargo": "SENADOR",
   "uf": "DF",
   "n_total": 13,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_df.js"
  },
  "SENADOR|ES": {
   "cargo": "SENADOR",
   "uf": "ES",
   "n_total": 11,
   "n_avaliados": 11,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_es.js"
  },
  "SENADOR|GO": {
   "cargo": "SENADOR",
   "uf": "GO",
   "n_total": 11,
   "n_avaliados": 11,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_go.js"
  },
  "SENADOR|MA": {
   "cargo": "SENADOR",
   "uf": "MA",
   "n_total": 11,
   "n_avaliados": 11,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ma.js"
  },
  "SENADOR|MG": {
   "cargo": "SENADOR",
   "uf": "MG",
   "n_total": 18,
   "n_avaliados": 16,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/senador_mg.js"
  },
  "SENADOR|MS": {
   "cargo": "SENADOR",
   "uf": "MS",
   "n_total": 10,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ms.js"
  },
  "SENADOR|MT": {
   "cargo": "SENADOR",
   "uf": "MT",
   "n_total": 10,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_mt.js"
  },
  "SENADOR|PA": {
   "cargo": "SENADOR",
   "uf": "PA",
   "n_total": 13,
   "n_avaliados": 12,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/senador_pa.js"
  },
  "SENADOR|PB": {
   "cargo": "SENADOR",
   "uf": "PB",
   "n_total": 10,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_pb.js"
  },
  "SENADOR|PE": {
   "cargo": "SENADOR",
   "uf": "PE",
   "n_total": 12,
   "n_avaliados": 12,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_pe.js"
  },
  "SENADOR|PI": {
   "cargo": "SENADOR",
   "uf": "PI",
   "n_total": 20,
   "n_avaliados": 20,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_pi.js"
  },
  "SENADOR|PR": {
   "cargo": "SENADOR",
   "uf": "PR",
   "n_total": 9,
   "n_avaliados": 9,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_pr.js"
  },
  "SENADOR|RJ": {
   "cargo": "SENADOR",
   "uf": "RJ",
   "n_total": 17,
   "n_avaliados": 15,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/senador_rj.js"
  },
  "SENADOR|RN": {
   "cargo": "SENADOR",
   "uf": "RN",
   "n_total": 14,
   "n_avaliados": 14,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_rn.js"
  },
  "SENADOR|RO": {
   "cargo": "SENADOR",
   "uf": "RO",
   "n_total": 10,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_ro.js"
  },
  "SENADOR|RR": {
   "cargo": "SENADOR",
   "uf": "RR",
   "n_total": 13,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_rr.js"
  },
  "SENADOR|RS": {
   "cargo": "SENADOR",
   "uf": "RS",
   "n_total": 13,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_rs.js"
  },
  "SENADOR|SC": {
   "cargo": "SENADOR",
   "uf": "SC",
   "n_total": 13,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_sc.js"
  },
  "SENADOR|SE": {
   "cargo": "SENADOR",
   "uf": "SE",
   "n_total": 11,
   "n_avaliados": 10,
   "corte": 6.0,
   "status": "parcial",
   "arquivo": "dados/senador_se.js"
  },
  "SENADOR|SP": {
   "cargo": "SENADOR",
   "uf": "SP",
   "n_total": 15,
   "n_avaliados": 15,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_sp.js"
  },
  "SENADOR|TO": {
   "cargo": "SENADOR",
   "uf": "TO",
   "n_total": 13,
   "n_avaliados": 13,
   "corte": 6.0,
   "status": "completo",
   "arquivo": "dados/senador_to.js"
  }
 },
 "tabelas": {
  "apoiadores": [
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso por corrupção e lavagem de dinheiro no escândalo do Mensalão (2012); recebeu indulto do STF em 2016. Sem pendência penal ativa encontrada hoje, mas histórico grave."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em investigação sobre fraudes em contratos da prefeitura de Ribeirão Preto e na delação da JBS; o MP-SP repassou as suspeitas à PGR e elas correm em inquérito sob sigilo no STF desde 2018 (relator Nunes Marques). Nega irregularidades. RESSALVA: a fonte é de 2021 -- o status atual NÃO foi confirmado."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do REPUBLICANOS, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Marcos Pereira",
     "partido": "REPUBLICANOS",
     "pendencia": "Nenhuma pendência encontrada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do NOVO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma pendência encontrada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre irregularidades nas contas de campanha do Podemos em 2018 (contratos de publicidade e comunicação): o MPE ofereceu a ela um acordo de não persecução penal; não foi possível confirmar se aceitou. Parte da investigação (outras pessoas e uma empresa) foi arquivada por falta de justa causa. Sem denúncia."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PDT, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Carlos Lupi",
     "partido": "PDT",
     "pendencia": "Deixou o Ministério da Previdência em 05/2025 após a fraude dos descontos ilegais no INSS; foi delatado por ex-dirigentes do INSS (relatos de fev/2026) por demorar cerca de um ano para agir enquanto os descontos subiram de R$ 80,6 mi para R$ 248,1 mi. Sem denúncia formal encontrada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do PSD, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Gilberto Kassab",
     "partido": "PSD",
     "pendencia": "Réu desde 2021 por corrupção passiva, lavagem de dinheiro, caixa 2 eleitoral e associação criminosa (recebimento de R$16,5 milhões do grupo JBS via contratos simulados, 2014-2016). Também condenado por improbidade administrativa como ex-prefeito de São Paulo (não pagamento de precatórios judiciais)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PSDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Aécio Neves",
     "partido": "PSDB",
     "pendencia": "Nenhuma pendência ATIVA encontrada nesta busca geral (não exaustiva): a 2ª Turma do STF arquivou em fev/2024 o inquérito INQ 4830. Histórico de múltiplas investigações da era Lava Jato/JBS não reexaminado aqui."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato aberto em 2015 (delação de Ricardo Pessoa/UTC: suspeita de R$ 7,5 mi em propina para a campanha de Dilma 2014, quando era tesoureiro) foi TRANCADO pelo TRE-DF por excesso de prazo (8 anos), sem denúncia e sem julgamento de mérito."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do AVANTE, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Luis Tibé",
     "partido": "AVANTE",
     "pendencia": "Condenado em 2015 por improbidade civil (uso irregular de verba indenizatória da Câmara de BH, 2009-2011); a dívida foi quitada e o MPMG pediu a extinção do processo. Inquérito da PF (2022) sobre gráficas de divulgação não viu crime. Citado em relatório da PF sobre lavagem de dinheiro apenas por contatos (NÃO contado). Sem pendência penal ativa encontrada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "João Campos",
     "partido": "PSB",
     "pendencia": "Nenhuma pendência encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do UNIÃO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Antonio Rueda",
     "partido": "UNIÃO",
     "pendencia": "Investigado pela PF na Operação Carbono Oculto (esquema do PCC no setor de combustíveis): suspeita de ser dono oculto de jatos, em nome de terceiros e fundos, usados para transportar integrantes do crime organizado. Colocou seus sigilos bancário e fiscal à disposição da PGR e diz ter provas de que pagou pelos voos. Sem denúncia formal encontrada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSOL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paula Coradi",
     "partido": "PSOL",
     "pendencia": "Nenhuma pendência encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do DC, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "João Caldas",
     "partido": "DC",
     "pendencia": "CORRIGIDO 2026-09-22 (pesquisando o filho dele, JHC, candidato ao governo de Alagoas): ex-deputado federal (AL), CONDENADO por improbidade administrativa no esquema 'Máfia das Ambulâncias' (Operação Taturana/Sanguessugas -- fraude em licitações de ambulâncias com emendas parlamentares, 2006). A condenação (1ª Vara Federal de Alagoas) foi CONFIRMADA pelo Plenário do TRF5 em grau de recurso, com pena de devolução de recursos públicos e PERDA DE DIREITOS POLÍTICOS -- avaliação de 2026-09-21 (que classificou como '1ª instância ainda recorrível', por uma manchete ambígua sobre o TRF5) estava desatualizada/cautelosa demais; corrigido para condenação confirmada sem reversão. Há também um processo distinto da Máfia das Sanguessugas propriamente dita, julgado em 2018 pela Justiça Federal de Cuiabá/MT -- mesma família de esquemas, tratado como o mesmo achado (não somado em dobro)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PP, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Ciro Nogueira",
     "partido": "PP",
     "pendencia": "Alvo da Polícia Federal na Operação Compliance Zero (caso Banco Master), com supervisão do STF (relator André Mendonça): suspeita de receber R$ 300-500 mil por mês de Daniel Vorcaro, além de imóveis, empresa comprada abaixo do mercado e viagens, em troca de atuar no Congresso pelo Master -- a Emenda 11 à PEC 65/2023, que ampliava a cobertura do FGC, teria sido redigida pela assessoria do banco. Sem denúncia formal até a pesquisa."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do MOBILIZA, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Antonio Carlos Massarollo",
     "partido": "MOBILIZA",
     "pendencia": "Nenhuma pendência encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do SOLIDARIEDADE, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paulinho da Força",
     "partido": "SOLIDARIEDADE",
     "pendencia": "Investigado em inquérito no STF (relator André Mendonça, destravado em dez/2025 após 2 anos parado) por suposto esquema de captação de clientes para ações trabalhistas com listas de demitidos obtidas em sindicatos -- o MP-SP aponta R$ 100 mil mensais. Sem denúncia até a pesquisa."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MISSÃO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Renan Santos",
     "partido": "MISSÃO",
     "pendencia": "Ação civil pública do MPF em curso (discurso de ódio contra indígenas) e condenação cível anterior (danos morais a um deputado). Nenhuma questão penal ou de Ficha Limpa."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PRD, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Marcus Vinícius Neskau",
     "partido": "PRD",
     "pendencia": "NÃO VERIFICADO: os resultados da busca são ambíguos (menção a afastamento determinado por Alexandre de Moraes no inquérito das fake news e a influência em nomeações no Detran-RJ segundo o MPF); não consegui confirmar nenhum fato em fonte primária, então nada foi contado."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do AGIR, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Daniel Tourinho",
     "partido": "AGIR",
     "pendencia": "Nenhuma pendência encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do DEMOCRATA, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Suêd Haidar",
     "partido": "DEMOCRATA",
     "pendencia": "NÃO VERIFICADO: a busca mostra processos de 2026 envolvendo ela, o partido e o Procurador Geral Eleitoral, mas sem detalhes claros sobre a natureza ou o objeto -- não confirmado em fonte primária, nada contado."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do REDE, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paulo Lamac",
     "partido": "REDE",
     "pendencia": "Firmou em 2026 acordo com o Ministério Público de Minas Gerais para encerrar ação sobre uso irregular de verba pública, comprometendo-se a pagar cerca de R$ 171 mil -- reconhecimento implícito de irregularidade, sem condenação criminal. Também há disputa interna sobre a legitimidade do congresso partidário de 2025 (anulado pela Justiça do RJ em jan/2026), sem relação com esta pendência."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do CIDADANIA, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Roberto Freire",
     "partido": "CIDADANIA",
     "pendencia": "Sem achado individual verificado. O grupo rival (Roberto Freire) anunciou representação criminal ao MPF sobre a gestão de Comte em 2023-2025; é acusação interna de disputa partidária, NÃO contada."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "NÃO VERIFICADO: uma fonte partidária (Brasil Sem Medo) afirma que Luciana Santos tem condenação por improbidade em licitação de iluminação pública; não confirmei em fonte independente e ela já não preside o partido. Nada pesquisado sobre a atual presidente."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do UP, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Leonardo Péricles",
     "partido": "UP",
     "pendencia": "Nenhuma pendência pessoal encontrada nesta busca geral (não exaustiva). Há um processo interno de aprovação de estatuto do partido (parcialmente aprovado em 2026), sem relação com conduta pessoal dele."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PCO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Rui Costa Pimenta",
     "partido": "PCO",
     "pendencia": "Contas partidárias com histórico recorrente de rejeição/falhas técnicas no TSE (contas não prestadas, divergências não justificadas, repasse indevido à fundação partidária). Rui Costa Pimenta pessoalmente investigado pela PF por suposto desvio de verba eleitoral."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSTU, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "José Maria Almeida",
     "partido": "PSTU",
     "pendencia": "Nenhuma pendência pessoal encontrada nesta busca geral (não exaustiva). O PSTU teve candidaturas de 2026 indeferidas em vários estados por pendências de contas partidárias (DRAP) -- problema do partido, não achado de conduta pessoal dele."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSOL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paula Coradi",
     "partido": "PSOL",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do REDE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Paulo Lamac",
     "partido": "REDE",
     "pendencia": "Acordo com o MPMG (2026) para encerrar ação por uso irregular de verba pública, pagando cerca de R$ 171 mil"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o PSTU, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "José Maria Almeida",
     "partido": "PSTU",
     "pendencia": "Nenhuma pendência pessoal encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside a Unidade Popular, partido da candidata",
     "ligacao": "presidente do partido do candidato",
     "nome": "Leonardo Péricles Vieira Roque",
     "partido": "UP",
     "pendencia": "Nenhuma pendência pessoal encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside a Unidade Popular, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Leonardo Péricles Vieira Roque",
     "partido": "UP",
     "pendencia": "Nenhuma pendência pessoal encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "preside o PCO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Rui Costa Pimenta",
     "partido": "PCO",
     "pendencia": "Investigado pela PF por suposto desvio de verba eleitoral; sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o PSTU, partido da candidata",
     "ligacao": "presidente do partido do candidato",
     "nome": "José Maria Almeida",
     "partido": "PSTU",
     "pendencia": "Nenhuma pendência pessoal encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "preside o DC, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "João Caldas da Silva",
     "partido": "DC",
     "pendencia": "Condenado por improbidade administrativa na 'Máfia das Ambulâncias', confirmada pelo TRF5 em recurso, com perda de direitos políticos"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o Novo, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma pendência encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Edmilson Costa",
     "partido": "PCB",
     "pendencia": "Nenhuma pendência pessoal encontrada nesta busca geral (não exaustiva)."
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "preside o DC, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "João Caldas da Silva",
     "partido": "DC",
     "pendencia": "Ex-deputado federal (AL), condenado por improbidade na Máfia das Ambulâncias (TRF5 confirmou, com perda de direitos políticos)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o Agir, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Daniel Sampaio Tourinho",
     "partido": "AGIR",
     "pendencia": "Nenhuma pendência encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside a Unidade Popular, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Leonardo Péricles Vieira Roque",
     "partido": "UP",
     "pendencia": "Nenhuma pendência pessoal encontrada nesta busca geral (não exaustiva)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o Mobiliza, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Antonio Carlos Bosco Massarollo",
     "partido": "MOBILIZA",
     "pendencia": "Nenhuma pendência encontrada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "preside o Avante, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Luis Tibé",
     "partido": "AVANTE",
     "pendencia": "Condenado por improbidade civil em 2015 (verba indenizatória da Câmara de BH); dívida quitada, extinção pedida pelo MPMG"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MISSÃO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Renan Santos",
     "partido": "MISSÃO",
     "pendencia": "Ação civil pública do MPF em curso (discurso de ódio contra indígenas); condenação cível anterior por danos morais (não é improbidade); sem questão penal"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o Democrata, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Suéd Haidar Nogueira",
     "partido": "DEMOCRATA",
     "pendencia": "Há registros de processos de 2026 envolvendo ela, mas sem detalhes confirmados em fonte primária; nada contado"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "preside o PCO, partido do candidato (também candidato a Presidente em 2026)",
     "ligacao": "presidente do partido do candidato",
     "nome": "Rui Costa Pimenta",
     "partido": "PCO",
     "pendencia": "Investigado pela PF por suposto desvio de verba eleitoral; sem denúncia até a pesquisa"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do REDE, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paulo Lamac",
     "partido": "REDE",
     "pendencia": "Acordo com o MPMG (2026) para encerrar ação por uso irregular de verba pública, pagando cerca de R$ 171 mil"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSOL, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Paula Coradi",
     "partido": "PSOL",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do NOVO, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PSDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Aécio Neves",
     "partido": "PSDB",
     "pendencia": "Inquérito INQ 4830 arquivado pelo STF (fev/2024); absolvido da acusação de propina de R$ 2 mi da J&F (1ª instância 2022, confirmada por unanimidade no TRF-3); sem pendência ativa"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do CIDADANIA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Roberto Freire",
     "partido": "CIDADANIA",
     "pendencia": "Presidência restituída a Roberto Freire por decisão judicial mantida pelo STF (2026), após disputa com Comte Bittencourt; pendências pessoais não pesquisadas"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "preside o MDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em investigação sobre fraudes em contratos e na delação da JBS; inquérito sob sigilo desde 2018. Ressalva: status atual não confirmado"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em inquérito sigiloso no STF desde 2018 (fraudes em Ribeirão Preto e delação da JBS), sem denúncia; o caso Alba Branca foi arquivado"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do AGIR, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Daniel Tourinho",
     "partido": "AGIR",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do AVANTE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Luis Tibé",
     "partido": "AVANTE",
     "pendencia": "Condenado por improbidade civil (2015, verba indenizatória da Câmara de BH); dívida quitada"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "João Campos",
     "partido": "PSB",
     "pendencia": "Nenhuma pendência pessoal como dirigente encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do PSD, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Gilberto Kassab",
     "partido": "PSD",
     "pendencia": "Réu desde 2021 no caso JBS (corrupção, lavagem, caixa 2, associação criminosa), sem sentença. Condenado por improbidade em 1ª instância em 2014 (precatórios de 2006), desfecho do recurso não localizado; a ação dos precatórios de 2007 terminou em absolvição mantida pelo TJSP (2019). Sem condenação confirmada localizada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "preside o PSD, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Gilberto Kassab",
     "partido": "PSD",
     "pendencia": "Réu desde 2021 por corrupção/lavagem/caixa 2 (JBS) + condenação civil por improbidade"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    },
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do DC, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "João Caldas",
     "partido": "DC",
     "pendencia": "Condenado por improbidade na Máfia das Ambulâncias (Operação Taturana), confirmada pelo Plenário do TRF-5, com perda de direitos políticos"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do DEMOCRATA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Suêd Haidar",
     "partido": "DEMOCRATA",
     "pendencia": "Processos de 2026 com a Procuradoria-Geral Eleitoral sem objeto identificado; não contado"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MDB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em inquérito sigiloso no STF desde 2018 (fraudes em Ribeirão Preto e delação da JBS), sem denúncia; o caso Alba Branca foi arquivado"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do MOBILIZA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Antonio Carlos Massarollo",
     "partido": "MOBILIZA",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PP, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Ciro Nogueira",
     "partido": "PP",
     "pendencia": "Alvo da PF na Operação Compliance Zero (caso Banco Master), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PRD, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Marcus Vinícius Neskau",
     "partido": "PRD",
     "pendencia": "Afastado da presidência do PTB por Alexandre de Moraes (2022, INQ 4874, milícias digitais) por atuar como fachada de Roberto Jefferson; mandado ouvir pela PF; sem denúncia localizada"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do REPUBLICANOS, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Marcos Pereira",
     "partido": "REPUBLICANOS",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do SOLIDARIEDADE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Paulinho da Força",
     "partido": "SOLIDARIEDADE",
     "pendencia": "Investigado em inquérito no STF (captação de clientes para ações trabalhistas), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do UNIÃO, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Antonio Rueda",
     "partido": "UNIÃO",
     "pendencia": "Investigado pela PF na Operação Carbono Oculto, sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSOL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Paula Coradi",
     "partido": "PSOL",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PDT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Carlos Lupi",
     "partido": "PDT",
     "pendencia": "Delatado por ex-dirigentes do INSS (fraude dos descontos), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "João Campos",
     "partido": "PSB",
     "pendencia": "Nenhuma pendência pessoal como dirigente encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do REDE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Paulo Lamac",
     "partido": "REDE",
     "pendencia": "Acordo com o MPMG (2026) para encerrar ação por uso irregular de verba pública, pagando cerca de R$ 171 mil"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PRD, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Marcus Vinícius Neskau",
     "partido": "PRD",
     "pendencia": "Afastado da presidência do PTB por Alexandre de Moraes (2022, INQ 4874, milícias digitais) por atuar como fachada de Roberto Jefferson; mandado ouvir pela PF; sem denúncia localizada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do SOLIDARIEDADE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Paulinho da Força",
     "partido": "SOLIDARIEDADE",
     "pendencia": "Investigado em inquérito no STF (captação de clientes para ações trabalhistas), sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do AVANTE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Luis Tibé",
     "partido": "AVANTE",
     "pendencia": "Condenado por improbidade civil (2015, verba indenizatória da Câmara de BH); dívida quitada"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do CIDADANIA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Roberto Freire",
     "partido": "CIDADANIA",
     "pendencia": "Presidência restituída a Roberto Freire por decisão judicial mantida pelo STF (2026), após disputa com Comte Bittencourt; pendências pessoais não pesquisadas"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MDB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em inquérito sigiloso no STF desde 2018 (fraudes em Ribeirão Preto e delação da JBS), sem denúncia; o caso Alba Branca foi arquivado"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PP, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Ciro Nogueira",
     "partido": "PP",
     "pendencia": "Alvo da PF na Operação Compliance Zero (caso Banco Master), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do PSD, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Gilberto Kassab",
     "partido": "PSD",
     "pendencia": "Réu desde 2021 no caso JBS (corrupção, lavagem, caixa 2, associação criminosa), sem sentença. Condenado por improbidade em 1ª instância em 2014 (precatórios de 2006), desfecho do recurso não localizado; a ação dos precatórios de 2007 terminou em absolvição mantida pelo TJSP (2019). Sem condenação confirmada localizada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PSDB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Aécio Neves",
     "partido": "PSDB",
     "pendencia": "Inquérito INQ 4830 arquivado pelo STF (fev/2024); absolvido da acusação de propina de R$ 2 mi da J&F (1ª instância 2022, confirmada por unanimidade no TRF-3); sem pendência ativa"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do REPUBLICANOS, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Marcos Pereira",
     "partido": "REPUBLICANOS",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do UNIÃO, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Antonio Rueda",
     "partido": "UNIÃO",
     "pendencia": "Investigado pela PF na Operação Carbono Oculto, sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PDT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Carlos Lupi",
     "partido": "PDT",
     "pendencia": "Delatado por ex-dirigentes do INSS (fraude dos descontos), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PSB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "João Campos",
     "partido": "PSB",
     "pendencia": "Nenhuma pendência pessoal como dirigente encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do MDB, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Baleia Rossi",
     "partido": "MDB",
     "pendencia": "Citado em inquérito sigiloso no STF desde 2018 (fraudes em Ribeirão Preto e delação da JBS), sem denúncia; o caso Alba Branca foi arquivado"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do CIDADANIA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Roberto Freire",
     "partido": "CIDADANIA",
     "pendencia": "Presidência restituída a Roberto Freire por decisão judicial mantida pelo STF (2026), após disputa com Comte Bittencourt; pendências pessoais não pesquisadas"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do DEMOCRATA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Suêd Haidar",
     "partido": "DEMOCRATA",
     "pendencia": "Processos de 2026 com a Procuradoria-Geral Eleitoral sem objeto identificado; não contado"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PDT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Carlos Lupi",
     "partido": "PDT",
     "pendencia": "Delatado por ex-dirigentes do INSS (fraude dos descontos), sem denúncia"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do PSD, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Gilberto Kassab",
     "partido": "PSD",
     "pendencia": "Réu desde 2021 no caso JBS (corrupção, lavagem, caixa 2, associação criminosa), sem sentença. Condenado por improbidade em 1ª instância em 2014 (precatórios de 2006), desfecho do recurso não localizado; a ação dos precatórios de 2007 terminou em absolvição mantida pelo TJSP (2019). Sem condenação confirmada localizada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PSDB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Aécio Neves",
     "partido": "PSDB",
     "pendencia": "Inquérito INQ 4830 arquivado pelo STF (fev/2024); absolvido da acusação de propina de R$ 2 mi da J&F (1ª instância 2022, confirmada por unanimidade no TRF-3); sem pendência ativa"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "fundadora e presidente do Democrata, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Suêd Haidar Nogueira",
     "partido": "DEMOCRATA",
     "pendencia": "Há processos de 2026 envolvendo ela e o partido, mas sem detalhes confirmados em fonte primária -- não contado"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PV, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "José Luiz de França Penna",
     "partido": "PV",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do PCDOB, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Nádia Campeão",
     "partido": "PCDOB",
     "pendencia": "Presidente em exercício; nenhuma pendência encontrada (busca geral). A presidente licenciada, Luciana Santos (ministra), tem condenação por improbidade em 1ª instância (2019, iluminação pública de Olinda, em recurso) -- não contada por estar licenciada"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PT, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Edinho Silva",
     "partido": "PT",
     "pendencia": "Inquérito da Lava Jato (campanha Dilma 2014) trancado por excesso de prazo, sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    },
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do DC, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "João Caldas",
     "partido": "DC",
     "pendencia": "Condenado por improbidade na Máfia das Ambulâncias (Operação Taturana), confirmada pelo Plenário do TRF-5, com perda de direitos políticos"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do MOBILIZA, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Antonio Carlos Massarollo",
     "partido": "MOBILIZA",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do NOVO, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o NOVO, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma encontrada nesta busca (não exaustiva)"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do REPUBLICANOS, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Marcos Pereira",
     "partido": "REPUBLICANOS",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 2,
     "detalhe": "presidente nacional do AVANTE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Luis Tibé",
     "partido": "AVANTE",
     "pendencia": "Condenado por improbidade civil (2015, verba indenizatória da Câmara de BH); dívida quitada"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 4,
     "detalhe": "presidente nacional do PL, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Valdemar Costa Neto",
     "partido": "PL",
     "pendencia": "Condenado e preso no Mensalão (2012); indultado em 2016"
    },
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "presidente nacional do NOVO, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Eduardo Ribeiro",
     "partido": "NOVO",
     "pendencia": "Nenhuma pendência encontrada (busca geral)"
    },
    {
     "contado": true,
     "desconto": 1,
     "detalhe": "presidente nacional do PODE, que integra a coligação/federação no TSE",
     "ligacao": "presidente de partido aliado (coligação)",
     "nome": "Renata Abreu",
     "partido": "PODE",
     "pendencia": "Inquérito eleitoral sobre contas de campanha do Podemos em 2018 (ANPP oferecido), sem denúncia"
    }
   ],
   [
    {
     "contado": true,
     "desconto": 0,
     "detalhe": "preside o DEMOCRATA, partido do candidato",
     "ligacao": "presidente do partido do candidato",
     "nome": "Suêd Haidar Nogueira",
     "partido": "DEMOCRATA",
     "pendencia": "Não verificado: processos de 2026 sem detalhe em fonte primária; nada contado"
    }
   ]
  ],
  "fontes": [
   [
    "https://en.wikipedia.org/wiki/Valdemar_Costa_Neto"
   ],
   [
    "https://www.poder360.com.br/congresso/baleia-rossi-e-citado-em-investigacoes-contra-fraudes-e-em-delacao-da-jbs/",
    "https://baleiarossi.com.br/noticias/baleia-rossi-e-reconduzido-como-presidente-nacional-do-mdb/"
   ],
   [
    "https://www.metropoles.com/colunas/mirelle-pinheiro/mp-propoe-acordo-para-evitar-denuncia-contra-renata-abreu"
   ],
   [
    "https://www.metropoles.com/colunas/andreza-matais/dirigentes-do-inss-delataram-carlos-lupi-ex-ministro-da-previdencia-de-lula",
    "https://www.portaldacapital.com/2026/05/14/presidente-nacional-do-pdt-carlos-lupi-participa-de-posse-de-diretoria-do-partido-nesta-quinta/"
   ],
   [
    "https://www.correiobraziliense.com.br/politica/2021/03/4911463-kassab-vira-reu-por-corrupcao-caixa-2-e-lavagem-de-rs-165-milhoes-da-jbs.html",
    "https://www.tjsp.jus.br/Noticias/noticia?codigoNoticia=23053&Id=23053",
    "https://conjur.com.br/2014-jun-04/kassab-condenado-improbidade-direitos-politicos-suspensos/",
    "https://www.conjur.com.br/2019-ago-23/tj-mantem-absolvicao-kassab-nao-pagar-precatorios-alimentares/"
   ],
   [
    "https://en.wikipedia.org/wiki/A%C3%A9cio_Neves",
    "https://portaldeprefeitura.com.br/bastidores-da-politica/aecio-neves-desiste-candidatura-psdb-lancara-nome-planalto/626505/",
    "https://www.cnnbrasil.com.br/politica/justica-absolve-aecio-neves-de-acusacao-de-propina-de-r-2-milhoes-da-jf/",
    "https://www.metropoles.com/brasil/aecio-neves-e-absolvido-de-forma-unanime-em-caso-de-corrupcao-passiva"
   ],
   [
    "https://www.folhape.com.br/politica/tre-tranca-inquerito-da-lava-jato-que-espreitava-edinho-silva-desde/340254/",
    "https://www.terra.com.br/noticias/brasil/politica/cotado-para-presidir-o-pt-edinho-se-livra-de-inquerito-da-lava-jato,76ee9924f0b981722d076c1c6b1c71aasodqtqtx.html"
   ],
   [
    "https://ofator.com.br/informacao/luis-tibe-quita-divida-de-improbidade-por-mau-uso-de-verba-da-camara-de-bh/",
    "https://www.cnnbrasil.com.br/blogs/luisa-martins/politica/pf-afirma-nao-ver-crime-por-parte-do-presidente-do-avante-investigado-no-stf/"
   ],
   [
    "https://en.wikipedia.org/wiki/Jo%C3%A3o_Henrique_Campos"
   ],
   [
    "https://www.cnnbrasil.com.br/politica/pf-inclui-presidente-do-uniao-brasil-em-investigacao-sobre-esquemas-do-pcc/",
    "https://www.poder360.com.br/poder-justica/pf-inclui-presidente-do-uniao-brasil-em-operacao-que-mira-pcc/"
   ],
   [
    "https://reporternordeste.com.br/condenado-por-receber-propina-joao-caldas-volta-ao-banco-dos-reus-nesta-4a/",
    "https://www.urbanitarios-al.com.br/2014/12/joao-caldas-e-condenado-no-trf-na-mafia-das-ambulancias/",
    "https://www.tribunadosertao.com.br/politica/2026/09/11/977133-jhc-aciona-a-justica-para-esconder-condenacao-do-pai-por-desvios-na-saude"
   ],
   [
    "https://psol50.org.br/com-67-dos-votos-paula-coradi-e-eleita-a-nova-presidenta-do-psol/"
   ],
   [
    "https://www.jota.info/stf/do-supremo/caso-master-ciro-nogueira-e-alvo-da-pf-por-suspeita-de-corrupcao-em-emenda-que-ampliava-fgc",
    "https://www.metropoles.com/colunas/andreza-matais/leia-a-integra-da-decisao-do-stf-contra-ciro-nogueira-no-caso-master",
    "https://www.cartacapital.com.br/cartaexpressa/ciro-nogueira-entre-os-alvos-sela-permanencia-do-caso-master-no-stf/"
   ],
   [
    "https://pt.wikipedia.org/wiki/Mobiliza%C3%A7%C3%A3o_Nacional"
   ],
   [
    "https://www.poder360.com.br/poder-justica/stf-destrava-investigacao-contra-paulinho-da-forca-apos-2-anos/",
    "https://www.cnnbrasil.com.br/politica/mendonca-movimenta-inquerito-contra-paulinho-da-forca-apos-dois-anos-parado/"
   ],
   [
    "https://www.mpf.mp.br/o-mpf/unidades/pr-pa/noticias/mpf-processa-candidato-a-presidencia-e-o-mbl-por-discurso-de-odio-contra-indigenas-do-para"
   ],
   [
    "https://pt.wikipedia.org/wiki/Marcus_Vin%C3%ADcius_de_Vasconcelos_Ferreira",
    "https://noticias.stf.jus.br/postsnoticias/ministro-alexandre-de-moraes-afasta-presidente-do-ptb-e-determina-que-pf-ouca-roberto-jefferson/"
   ],
   [
    "https://pt.wikipedia.org/wiki/Daniel_Tourinho"
   ],
   [
    "https://www.escavador.com/nomes/sued-haidar-nogueira-2203134fb6"
   ],
   [
    "https://pt.wikipedia.org/wiki/Rede_Sustentabilidade"
   ],
   [
    "https://pv.org.br/presidente-nacional-do-pv-jose-luiz-penna/"
   ],
   [
    "https://www.band.com.br/noticias/comte-bittencourt-entrega-chave-do-tse-e-cidadania-tera-novo-presidente-202603021859",
    "https://www.band.com.br/noticias/destituido-da-presidencia-do-cidadania-pelo-stf-comte-bittencourt-ainda-detem-a-chave-do-partido-usada-no-tse-202601071637"
   ],
   [
    "https://brasilsemmedo.com/ministra-da-ciencia-e-tecnologia-de-lula-tem-condenacao-por-improbidade-administrativa/",
    "https://pcdob.org.br/noticias/pcdob-inicia-transicao-na-presidencia-com-nadia-campeao-a-frente/",
    "https://www.leiaja.com/politica/2019/11/02/luciana-santos-e-condenada-por-improbidade-administrativa/"
   ],
   [
    "https://sbtnews.sbt.com.br/noticia/politica/unidade-popular-quer-presidencia-e-mira-17-governos"
   ],
   [
    "https://www.cnnbrasil.com.br/eleicoes/pf-mira-candidato-do-pco-a-presidente-por-suposto-desvio-de-verba-eleitoral/"
   ],
   [
    "https://www.tse.jus.br/partidos/partidos-registrados-no-tse/partido-socialista-dos-trabalhadores-unificado"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://en.wikipedia.org/wiki/Valdemar_Costa_Neto"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.poder360.com.br/congresso/baleia-rossi-e-citado-em-investigacoes-contra-fraudes-e-em-delacao-da-jbs/",
    "https://baleiarossi.com.br/noticias/baleia-rossi-e-reconduzido-como-presidente-nacional-do-mdb/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.metropoles.com/colunas/mirelle-pinheiro/mp-propoe-acordo-para-evitar-denuncia-contra-renata-abreu"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://en.wikipedia.org/wiki/A%C3%A9cio_Neves",
    "https://portaldeprefeitura.com.br/bastidores-da-politica/aecio-neves-desiste-candidatura-psdb-lancara-nome-planalto/626505/",
    "https://www.cnnbrasil.com.br/politica/justica-absolve-aecio-neves-de-acusacao-de-propina-de-r-2-milhoes-da-jf/",
    "https://www.metropoles.com/brasil/aecio-neves-e-absolvido-de-forma-unanime-em-caso-de-corrupcao-passiva"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.correiobraziliense.com.br/politica/2021/03/4911463-kassab-vira-reu-por-corrupcao-caixa-2-e-lavagem-de-rs-165-milhoes-da-jbs.html",
    "https://www.tjsp.jus.br/Noticias/noticia?codigoNoticia=23053&Id=23053",
    "https://conjur.com.br/2014-jun-04/kassab-condenado-improbidade-direitos-politicos-suspensos/",
    "https://www.conjur.com.br/2019-ago-23/tj-mantem-absolvicao-kassab-nao-pagar-precatorios-alimentares/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.jota.info/stf/do-supremo/caso-master-ciro-nogueira-e-alvo-da-pf-por-suspeita-de-corrupcao-em-emenda-que-ampliava-fgc",
    "https://www.metropoles.com/colunas/andreza-matais/leia-a-integra-da-decisao-do-stf-contra-ciro-nogueira-no-caso-master",
    "https://www.cartacapital.com.br/cartaexpressa/ciro-nogueira-entre-os-alvos-sela-permanencia-do-caso-master-no-stf/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.cnnbrasil.com.br/politica/pf-inclui-presidente-do-uniao-brasil-em-investigacao-sobre-esquemas-do-pcc/",
    "https://www.poder360.com.br/poder-justica/pf-inclui-presidente-do-uniao-brasil-em-operacao-que-mira-pcc/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://pt.wikipedia.org/wiki/Marcus_Vin%C3%ADcius_de_Vasconcelos_Ferreira",
    "https://noticias.stf.jus.br/postsnoticias/ministro-alexandre-de-moraes-afasta-presidente-do-ptb-e-determina-que-pf-ouca-roberto-jefferson/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.escavador.com/nomes/sued-haidar-nogueira-2203134fb6"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://reporternordeste.com.br/condenado-por-receber-propina-joao-caldas-volta-ao-banco-dos-reus-nesta-4a/",
    "https://www.urbanitarios-al.com.br/2014/12/joao-caldas-e-condenado-no-trf-na-mafia-das-ambulancias/",
    "https://www.tribunadosertao.com.br/politica/2026/09/11/977133-jhc-aciona-a-justica-para-esconder-condenacao-do-pai-por-desvios-na-saude"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.metropoles.com/colunas/andreza-matais/dirigentes-do-inss-delataram-carlos-lupi-ex-ministro-da-previdencia-de-lula",
    "https://www.portaldacapital.com/2026/05/14/presidente-nacional-do-pdt-carlos-lupi-participa-de-posse-de-diretoria-do-partido-nesta-quinta/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://pt.wikipedia.org/wiki/Daniel_Tourinho"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://ofator.com.br/informacao/luis-tibe-quita-divida-de-improbidade-por-mau-uso-de-verba-da-camara-de-bh/",
    "https://www.cnnbrasil.com.br/blogs/luisa-martins/politica/pf-afirma-nao-ver-crime-por-parte-do-presidente-do-avante-investigado-no-stf/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://en.wikipedia.org/wiki/Jo%C3%A3o_Henrique_Campos"
   ],
   [
    "https://portaldatransparencia.gov.br/sancoes/consulta",
    "https://www.folhape.com.br/politica/tre-tranca-inquerito-da-lava-jato-que-espreitava-edinho-silva-desde/340254/",
    "https://www.terra.com.br/noticias/brasil/politica/cotado-para-presidir-o-pt-edinho-se-livra-de-inquerito-da-lava-jato,76ee9924f0b981722d076c1c6b1c71aasodqtqtx.html"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.folhape.com.br/politica/tre-tranca-inquerito-da-lava-jato-que-espreitava-edinho-silva-desde/340254/",
    "https://www.terra.com.br/noticias/brasil/politica/cotado-para-presidir-o-pt-edinho-se-livra-de-inquerito-da-lava-jato,76ee9924f0b981722d076c1c6b1c71aasodqtqtx.html"
   ],
   [
    "https://portaldatransparencia.gov.br/sancoes/consulta",
    "https://www.correiobraziliense.com.br/politica/2021/03/4911463-kassab-vira-reu-por-corrupcao-caixa-2-e-lavagem-de-rs-165-milhoes-da-jbs.html",
    "https://www.tjsp.jus.br/Noticias/noticia?codigoNoticia=23053&Id=23053",
    "https://conjur.com.br/2014-jun-04/kassab-condenado-improbidade-direitos-politicos-suspensos/",
    "https://www.conjur.com.br/2019-ago-23/tj-mantem-absolvicao-kassab-nao-pagar-precatorios-alimentares/"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://pt.wikipedia.org/wiki/Mobiliza%C3%A7%C3%A3o_Nacional"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://pv.org.br/presidente-nacional-do-pv-jose-luiz-penna/"
   ],
   [
    "https://cn7.com.br/ex-prefeito-de-granja-e-condenado-8-meses-de-detencao-por-crime-de-calunia/",
    "https://blogdoedisonsilva.com.br/2024/11/25/elmano-quer-romeu-aldigueri-na-presidencia-da-al-ele-e-acusado-de-falsidade-ideologica-atropelamento-seguido-de-homicidio-agressao-a-ex-primeira-mulher-e-estupro-em-granja/",
    "https://www.al.ce.gov.br/deputados/romeu-aldigueri",
    "https://en.wikipedia.org/wiki/Jo%C3%A3o_Henrique_Campos"
   ],
   [
    "https://portaldatransparencia.gov.br/sancoes/consulta",
    "https://www.poder360.com.br/congresso/baleia-rossi-e-citado-em-investigacoes-contra-fraudes-e-em-delacao-da-jbs/",
    "https://baleiarossi.com.br/noticias/baleia-rossi-e-reconduzido-como-presidente-nacional-do-mdb/"
   ],
   [
    "https://portaldatransparencia.gov.br/sancoes/consulta",
    "https://en.wikipedia.org/wiki/Jo%C3%A3o_Henrique_Campos"
   ],
   [
    "https://portaldatransparencia.gov.br/sancoes/consulta",
    "https://www.metropoles.com/colunas/mirelle-pinheiro/mp-propoe-acordo-para-evitar-denuncia-contra-renata-abreu"
   ],
   [
    "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
    "https://www.poder360.com.br/poder-justica/stf-destrava-investigacao-contra-paulinho-da-forca-apos-2-anos/",
    "https://www.cnnbrasil.com.br/politica/mendonca-movimenta-inquerito-contra-paulinho-da-forca-apos-dois-anos-parado/"
   ],
   [
    "https://www.gazetadopovo.com.br/eleicoes/2026/minas-gerais/quem-sao-candidatos-governador-minas-gerais-2026/",
    "https://portalg37.com.br/minas-gerais/minas-gerais-tem-11-candidatos-ao-governo-em-2026-veja-nomes-vices-e-perfis/"
   ],
   [
    "https://www.infomoney.com.br/politica/candidatos-governador-rs-2026/"
   ],
   [
    "https://ndmais.com.br/politica/com-aval-da-justica-democrata-substitui-candidato-ao-governo-do-tocantins-a-20-dias-das-eleicoes/"
   ]
  ],
  "verificacao": [
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nao_se_aplica"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nada_consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nada_consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "rapida"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nao_se_aplica"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "rapida"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nada_consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "padrao"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nao_se_aplica"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "padrao"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "itens": [
       "Fundamento citado no julgamento do registro: Abuso de poder político"
      ],
      "n": 1,
      "ref": "https://dadosabertos.tse.jus.br/dataset/candidatos-2022",
      "resultado": "consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "itens": [
       "Fundamento citado no julgamento do registro: Ficha limpa (LC 64/90)"
      ],
      "n": 1,
      "ref": "https://dadosabertos.tse.jus.br/dataset/candidatos-2022",
      "resultado": "consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nao_se_aplica"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "aprofundada"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nada_consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "aprofundada"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "resultado": "nada_consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "itens": [
       "Auto de infração de R$ 21.500,00 em 19/03/2025 (PA)"
      ],
      "n": 1,
      "ref": "https://dadosabertos.ibama.gov.br/dataset/fiscalizacao-auto-de-infracao",
      "resultado": "consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "itens": [
       "Fundamento citado no julgamento do registro: Abuso de poder (LC 64/90)"
      ],
      "n": 1,
      "ref": "https://dadosabertos.tse.jus.br/dataset/candidatos-2022",
      "resultado": "consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "estrutural"
   },
   {
    "bases": [
     {
      "id": "tcu_eleitoral",
      "resultado": "nada_consta"
     },
     {
      "id": "tse_2022",
      "itens": [
       "Fundamento citado no julgamento do registro: Ficha limpa (LC 64/90)"
      ],
      "n": 1,
      "ref": "https://dadosabertos.tse.jus.br/dataset/candidatos-2022",
      "resultado": "consta"
     },
     {
      "id": "ceis",
      "resultado": "nada_consta"
     },
     {
      "id": "cnep",
      "resultado": "nada_consta"
     },
     {
      "id": "ceaf",
      "resultado": "nada_consta"
     },
     {
      "id": "ibama",
      "resultado": "nada_consta"
     }
    ],
    "nivel": "rapida"
   }
  ],
  "cobertura": [
   "idoneidade; círculo político; experiência política",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal c)",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal c); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal c); experiência política",
   "idoneidade; círculo político; posicionamento (econômico a, pessoal c); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal c); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico a, pessoal a); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico a, pessoal b); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal b); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal b); experiência política",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal b); experiência política; competência profissional",
   "nenhuma (só proxy de ocupação + escolaridade)",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal b)",
   "idoneidade; círculo político; posicionamento (econômico a, pessoal a); competência profissional",
   "idoneidade; círculo político; posicionamento (econômico a, pessoal a); experiência política",
   "idoneidade; experiência política",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal a); experiência política; competência profissional",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal a); experiência política",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal b); experiência política",
   "idoneidade; círculo político; posicionamento (econômico b, pessoal c)",
   "idoneidade; círculo político; posicionamento (econômico c, pessoal a); experiência política"
  ],
  "posicao_fonte": [
   "baseline do partido",
   "pesquisa individual"
  ]
 },
 "versao": "da1f19fa81"
};
