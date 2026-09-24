(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  if (typeof DADOS === "undefined") {
    $("cobertura").textContent = "Não foi possível carregar os dados (dados.js). Recarregue a página.";
    return;
  }

  // dados.js guarda uma vez só os valores repetidos (DADOS.tabelas) e deixa em cada candidato o índice;
  // aqui cada índice volta a ser o valor original, então o resto do código não muda (valores compartilhados, só leitura).
  (function expandirTabelas() {
    const T = DADOS.tabelas || {};
    Object.values(DADOS.grupos).forEach(g => (g.candidatos || []).forEach(c => {
      Object.keys(T).forEach(campo => { if (typeof c[campo] === "number") c[campo] = T[campo][c[campo]]; });
    }));
  })();

  // ---------- tema (só conveniência local, nunca enviado) ----------
  (function tema() {
    const btn = $("btnTema");
    let salvo = null;
    try { salvo = localStorage.getItem("mmc_tema"); } catch (e) { /* navegação privada: ignora */ }
    if (salvo === "dark" || salvo === "light") document.documentElement.setAttribute("data-theme", salvo);
    const atualizar = () => {
      const escuro = document.documentElement.getAttribute("data-theme") === "dark" ||
        (!document.documentElement.hasAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      btn.textContent = escuro ? "Modo claro" : "Modo escuro";
      btn.setAttribute("aria-pressed", String(escuro));
    };
    btn.addEventListener("click", () => {
      const agoraEscuro = document.documentElement.getAttribute("data-theme") !== "dark" &&
        !(!document.documentElement.hasAttribute("data-theme") && !matchMedia("(prefers-color-scheme: dark)").matches);
      const novo = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", novo);
      try { localStorage.setItem("mmc_tema", novo); } catch (e) { /* ignora */ }
      atualizar();
    });
    atualizar();
  })();

  const UF_NOME = {BR:"Brasil",AC:"Acre",AL:"Alagoas",AM:"Amazonas",AP:"Amapá",BA:"Bahia",CE:"Ceará",DF:"Distrito Federal",ES:"Espírito Santo",GO:"Goiás",MA:"Maranhão",MG:"Minas Gerais",MS:"Mato Grosso do Sul",MT:"Mato Grosso",PA:"Pará",PB:"Paraíba",PE:"Pernambuco",PI:"Piauí",PR:"Paraná",RJ:"Rio de Janeiro",RN:"Rio Grande do Norte",RO:"Rondônia",RR:"Roraima",RS:"Rio Grande do Sul",SC:"Santa Catarina",SE:"Sergipe",SP:"São Paulo",TO:"Tocantins"};
  const fmt = (x, d = 1) => x == null ? "n/d" : x.toLocaleString("pt-BR", {minimumFractionDigits: d, maximumFractionDigits: d});
  const MIN = new Set(["da","de","do","das","dos","e"]);
  const tc = (s) => s.toLowerCase().split(" ").map((w, i) => (i && MIN.has(w)) ? w : w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
  const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  const NS = "http://www.w3.org/2000/svg";
  const sv = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };
  const META = DADOS.meta, GRUPOS = DADOS.grupos;
  const QUAD = Object.fromEntries(DADOS.quadrantes.map(q => [q.chave, q]));
  const CARGO = Object.fromEntries(DADOS.cargos.map(c => [c.codigo, c]));
  const SITUACAO = {
    recomendado: ["★", "Recomendado"], segue: ["✓", "Continua"], abaixo_do_corte: ["▼", "Abaixo do corte"],
    fora_da_disputa: ["✕", "Fora da disputa"], nao_avaliado: ["?", "Sem verificação"],
  };
  const subJudice = (c) => c.achados.find(a => a.categoria === "registro_contestado_sub_judice");
  const QCLASSE = {ESQUERDA: "q-esquerda", LIBERTARIO: "q-libertario", AUTORITARIO: "q-autoritario", DIREITA: "q-direita"};
  const qcor = (chave) => `var(--${QCLASSE[chave]})`;
  const qcorWash = (chave) => `var(--${QCLASSE[chave]}-wash)`;
  let atual = null;
  let ultimoGrupo = null;  // "cargo|uf" do último evento enviado ao GA (evita duplicar)
  let acaoAtual = "carga"; // o que disparou o render: "carga" | "cargo" | "uf" (trocar o cargo preenche um UF padrão sozinho)

  // Evento de uso agregado para o Google Analytics. Nunca envia respostas do quiz nem a posição do usuário.
  function rastrear(nome, params) {
    try { if (typeof gtag === "function") gtag("event", nome, params); } catch (e) { /* GA bloqueado: ignora */ }
  }

  // ---------- "Você": quiz de 2 perguntas. Nada disto é enviado ou guardado além do próprio navegador ----------
  const QUIZ = [
    {id: "eco", pergunta: "Para o país melhorar, o que deve pesar mais?",
     baixo: "Um Estado mais presente na economia: regula as empresas, cobra mais impostos e usa o dinheiro para reduzir desigualdades e garantir serviços, mesmo que isso possa desestimular investimentos.",
     alto: "Um Estado menor: menos regras e impostos mais baixos, para que empresas e pessoas invistam e gerem riqueza, mesmo que isso deixe os mais pobres com menos proteção do governo."},
    {id: "pes", pergunta: "Em escolhas pessoais sobre as quais a sociedade se divide, o que a lei deve priorizar?",
     baixo: "Preservar os valores morais e tradicionais da sociedade, mesmo que isso limite algumas escolhas individuais.",
     alto: "Proteger a liberdade de cada um decidir sobre a própria vida, desde que não prejudique outras pessoas, mesmo que a sociedade em geral desaprove essas escolhas."},
  ];
  const ROT_ESCALA = ["Só A", "Mais A", "Meio-termo", "Mais B", "Só B"];
  const invertido = QUIZ.map(() => Math.random() < 0.5);  // true: o polo "alto" aparece como A (evita viés de posição)
  const respostas = {};  // id -> 0-10 | undefined (não respondeu ainda)
  let voce = null;       // {eco, pes} em 0-10 (null = desconhecido) ou null

  const LADOS = (v) => v == null ? {main: null, alts: ["low", "high"]}
    : v <= 1 ? {main: "low", alts: []} : v < 4.5 ? {main: "low", alts: ["high"]}
    : v <= 5.5 ? {main: null, alts: ["low", "high"]} : v < 9 ? {main: "high", alts: ["low"]} : {main: "high", alts: []};
  const QDE = (e, p) => e === "high" ? (p === "high" ? "LIBERTARIO" : "DIREITA") : (p === "high" ? "ESQUERDA" : "AUTORITARIO");
  function classificarVoce() {
    if (!voce) return null;
    const E = LADOS(voce.eco), P = LADOS(voce.pes);
    const proprios = (L) => L.main ? [L.main] : ["low", "high"], amplos = (L) => L.main ? [L.main, ...L.alts] : ["low", "high"];
    const seu = new Set(), amplo = new Set();
    proprios(E).forEach(e => proprios(P).forEach(p => seu.add(QDE(e, p))));
    amplos(E).forEach(e => amplos(P).forEach(p => amplo.add(QDE(e, p))));
    return {seu, viz: new Set([...amplo].filter(q => !seu.has(q)))};
  }
  function montarQuiz() {
    const corpo = $("quizCorpo"); corpo.textContent = "";
    QUIZ.forEach((q, qi) => {
      const fs = el("fieldset", "pergunta"); fs.append(el("legend", null, `${qi + 1}. ${q.pergunta}`));
      const A = invertido[qi] ? q.alto : q.baixo, B = invertido[qi] ? q.baixo : q.alto;
      const polos = el("div", "polos");
      [["A", A], ["B", B]].forEach(([r, t]) => { const d = el("div", "polo"); d.append(el("b", null, r + ") "), document.createTextNode(t)); polos.append(d); });
      fs.append(polos);
      const esc = el("div", "escala");
      ROT_ESCALA.forEach((rot, i) => {
        const l = el("label", "op"), inp = document.createElement("input");
        inp.type = "radio"; inp.name = "q_" + q.id; inp.dataset.valor = String(invertido[qi] ? 10 - 2.5 * i : 2.5 * i);
        inp.addEventListener("change", () => { respostas[q.id] = Number(inp.dataset.valor); atualizarVoce(true); });
        l.append(inp, el("span", null, rot)); esc.append(l);
      });
      fs.append(esc);
      corpo.append(fs);
    });
  }
  function atualizarVoce(dosRadios) {
    if (dosRadios) {
      const r = QUIZ.map(q => respostas[q.id]);
      voce = r.every(v => v == null) ? null : {eco: r[0] == null ? null : r[0], pes: r[1] == null ? null : r[1]};
    }
    renderVoce();
    if (atual) { renderNolan(atual); renderSeuCandidato(atual); }
  }
  function renderVoce() {
    const box = $("resultadoQuiz");
    if (!voce) { box.hidden = true; return; }
    box.hidden = false;
    const cl = classificarVoce(), nomes = (s) => [...s].map(k => QUAD[k].curto).join(" ou ");
    $("resTexto").textContent = `economia ${voce.eco == null ? "não informada" : fmt(voce.eco)} · costumes ${voce.pes == null ? "não informados" : fmt(voce.pes)}.`;
    $("resQuad").textContent = nomes(cl.seu) + ".";
    // usa a cor do quadrante (mesma paleta do diagrama de Nolan) quando o quadrante é único e sem ambiguidade
    const chaves = [...cl.seu];
    if (chaves.length === 1) {
      box.style.borderColor = qcor(chaves[0]);
      box.style.background = qcorWash(chaves[0]);
      $("resQuad").style.color = qcor(chaves[0]);
    } else {
      box.style.borderColor = "";
      box.style.background = "";
      $("resQuad").style.color = "";
    }
  }

  // ---------- seletores de cargo/estado ----------
  const ufsReais = (cargo) => Object.keys(GRUPOS).filter(k => k.startsWith(cargo + "|")).map(k => k.split("|")[1]).filter(u => u !== "BR").sort((a, b) => UF_NOME[a].localeCompare(UF_NOME[b], "pt-BR"));
  function preencherCargos() {
    const s = $("cargo"); s.textContent = "";
    DADOS.cargos.forEach(c => { const o = el("option", null, c.rotulo); o.value = c.codigo; s.append(o); });
  }
  function preencherUfs(cargo, escolhida) {
    const campo = $("campoUf");
    if (cargo === "PRESIDENTE") { campo.hidden = true; return; }
    campo.hidden = false;
    const s = $("uf"); s.textContent = "";
    const ufs = ufsReais(cargo);
    ufs.forEach(u => { const o = el("option", null, UF_NOME[u] + (GRUPOS[cargo + "|" + u].status === "sem_verificacao" ? "" : "  ✓")); o.value = u; s.append(o); });
    s.value = escolhida && ufs.includes(escolhida) ? escolhida : ufs[0];
  }
  function ufAtual(cargo) { return cargo === "PRESIDENTE" ? "BR" : $("uf").value; }

  // ---------- profundidade da pesquisa e conferência em bases oficiais ----------
  const BASE_INFO = Object.fromEntries((DADOS.bases_oficiais || []).map(b => [b.id, b]));
  const dataBr = iso => iso.split("-").reverse().join("/");
  function verif(c) {
    const v = c.verificacao || { nivel: "rapida", bases: [] };
    const niv = DADOS.profundidade[v.nivel];
    const consultadas = v.bases.filter(b => b.resultado !== "nao_se_aplica");
    return { v, niv, nivel: v.nivel, curto: niv.rotulo.replace("Pesquisa ", "").toLowerCase(), consultadas: consultadas.length,
             comRegistro: consultadas.filter(b => b.resultado === "consta" || b.resultado === "a_confirmar").length };
  }
  function blocoVerificacao(c) {
    const { v, niv, consultadas, comRegistro } = verif(c);
    const box = el("div", "verif");
    box.append(el("h4", null, "Profundidade da pesquisa"));
    const p = el("p"); p.append(el("strong", null, niv.rotulo + ". "), document.createTextNode(niv.descricao + " "));
    const fontes = c.fontes.filter(f => /^https?:\/\//.test(f)).length;
    p.append(document.createTextNode(fontes ? `${fontes} ${fontes === 1 ? "fonte citada" : "fontes citadas"} para esta nota.` : "Nenhuma fonte citada: nada foi encontrado na busca."));
    box.append(p);
    if (!v.bases.length) return box;
    box.append(el("h4", null, "Conferência em bases oficiais"));
    box.append(el("p", "nota", comRegistro ? `${consultadas} bases consultadas por CPF; ${comRegistro} com registro (detalhado abaixo).` : `${consultadas} bases consultadas por CPF, nenhum registro encontrado.`));
    const ul = el("ul", "bases");
    v.bases.forEach(b => {
      const info = BASE_INFO[b.id]; const li = el("li", "base " + b.resultado);
      const icone = { nada_consta: "✓", consta: "●", a_confirmar: "?", nao_se_aplica: "–" }[b.resultado];
      const txt = { nada_consta: "nada consta", consta: "há registro", a_confirmar: "possível correspondência, a confirmar", nao_se_aplica: b.id === "tse_2022" ? "não se aplica (sem candidatura em 2022)" : "não se aplica" }[b.resultado];
      li.append(el("span", "ico", icone), document.createTextNode(` ${info.rotulo} — ${txt} `), el("span", "data", `(arquivo de ${dataBr(info.data)})`));
      if (b.itens && b.itens.length) {
        const sub = el("ul", "itens");
        b.itens.forEach(t => sub.append(el("li", null, t)));
        if (b.n > b.itens.length) sub.append(el("li", null, `… e mais ${b.n - b.itens.length}.`));
        if (b.ref && /^https?:\/\//.test(b.ref)) { const li2 = el("li"), a = el("a", null, "ver fonte"); a.href = b.ref; a.target = "_blank"; a.rel = "noopener noreferrer"; li2.append(a); sub.append(li2); }
        li.append(sub);
      }
      ul.append(li);
    });
    box.append(ul);
    box.append(el("p", "nota", "Conferência automática por CPF e nome. \"Nada consta\" vale só para o que cada base cobre e não é atestado; um registro aqui não altera a nota por si só, a nota usa os achados verificados na pesquisa."));
    return box;
  }

  // ---------- explicação/fontes de um candidato ----------
  function detalhe(c) {
    const d = el("div", "detalhe");
    d.append(el("p", null, `Idoneidade pessoal ${fmt(c.idoneidade_pessoal, 0)} · círculo político ${fmt(c.circulo, 0)} · idoneidade geral ${fmt(c.idoneidade_geral)}. Competência ${fmt(c.competencia)} e escolaridade ${fmt(c.escolaridade)} → competência geral ${fmt(c.competencia_geral)}. Qualificação geral (média das duas gerais) ${fmt(c.qualificacao_geral)}.`));
    d.append(el("h4", null, "Achados sobre o candidato"));
    if (c.achados.length) {
      const ul = el("ul");
      c.achados.forEach(a => { const li = el("li"); li.append(el("span", "peso", "−" + a.peso + " "), document.createTextNode(a.rotulo + ": " + a.descricao)); ul.append(li); });
      d.append(ul);
    } else {
      const { v, niv, consultadas, comRegistro } = verif(c);
      d.append(el("p", null, `Nenhum achado verificado na ${niv.rotulo.toLowerCase()}` + (consultadas && !comRegistro ? ` nem nas ${consultadas} bases oficiais conferidas.` : ".") + " A nota 10 reflete só o que se encontrou, não garante que não haja pendência."));
    }
    d.append(el("h4", null, "Apoiadores e o tipo de ligação"));
    if (c.apoiadores.length) {
      const ul = el("ul");
      c.apoiadores.forEach(a => {
        const li = el("li");
        const quem = a.nome ? a.nome + (a.partido ? " (" + a.partido + ")" : "") + " — " : "";
        li.append(el("span", "peso", (a.desconto ? "−" + a.desconto : "0") + " "), document.createTextNode(quem + a.ligacao + (a.detalhe ? ": " + a.detalhe : "") + ". " + a.pendencia + (a.contado ? "" : " (não contado na nota)")));
        ul.append(li);
      });
      d.append(ul);
    } else d.append(el("p", null, "Vice ainda não pesquisado."));
    if (c.apoiadores.some(a => a.desconto)) d.append(el("p", "nota", "Os descontos dos presidentes de partidos aliados somam no máximo −4 por chapa."));
    d.append(blocoVerificacao(c));
    d.append(el("h4", null, "Cobertura da pesquisa"));
    d.append(el("p", null, `${c.camadas} de 5 camadas: ${c.cobertura}.`));
    if (c.fontes.length) {
      d.append(el("h4", null, "Fontes"));
      const ul = el("ul", "fontes");
      c.fontes.filter(f => /^https?:\/\//.test(f)).forEach(f => { const li = el("li"), a = el("a", null, f); a.href = f; a.target = "_blank"; a.rel = "noopener noreferrer"; li.append(a); ul.append(li); });
      d.append(ul);
    }
    return d;
  }

  // ---------- cartão de candidato reaproveitado (quadrantes, seu candidato) ----------
  function blocoCandidato(c, origem) {
    const b = el("div", "cand");
    b.append(el("div", "nomegrande", tc(c.nome_urna)), el("div", "nota", `${c.partido} · número ${c.numero}`));
    const sj = subJudice(c);
    if (sj) b.append(el("div", "aviso-sub", `⚠ Candidatura contestada, aguardando decisão da Justiça Eleitoral: ${sj.descricao}`));
    const st = el("div", "stats");
    [[fmt(c.qualificacao_geral), "qualificação geral"], [fmt(c.idoneidade_geral), "idoneidade geral"], [fmt(c.competencia_geral), "competência geral"]].forEach(([v, l]) => { const d = el("div"); d.append(el("b", null, v), el("span", null, l)); st.append(d); });
    b.append(st);
    const vf = verif(c);
    b.append(el("p", "selo " + vf.nivel, `${vf.niv.rotulo}` + (vf.consultadas ? ` · ${vf.consultadas} bases oficiais conferidas` + (vf.comRegistro ? `, ${vf.comRegistro} com registro` : "") : "")));
    b.append(el("p", "nota", `Posição: economia ${fmt(c.eco)} · costumes ${fmt(c.pes)} (${c.posicao_fonte}). ${c.camadas} de 5 camadas pesquisadas.`));
    if (c.fronteira) b.append(el("p", "nota", "Está perto do centro do diagrama: pode se identificar também com a posição vizinha."));
    if (c.empate > 1) b.append(el("p", "nota", `Empatou com outros ${c.empate - 1} candidatos na última vaga; o desempate foi por sorteio.`));
    const btn = el("button", "btn", "Notas, achados e fontes"); btn.type = "button"; btn.setAttribute("aria-expanded", "false");
    const det = detalhe(c); det.hidden = true;
    btn.addEventListener("click", () => {
      const abre = det.hidden; det.hidden = !abre; btn.setAttribute("aria-expanded", String(abre));
      if (abre) rastrear("abrir_notas_candidato", { cargo: $("cargo").value, uf: ufAtual($("cargo").value), candidato: c.nome_urna, partido: c.partido, origem: origem });
    });
    b.append(btn, det);
    return b;
  }

  // ---------- diagrama de Nolan ----------
  const dica = $("dica");
  function mostrarDica(c, x, y) {
    dica.textContent = "";
    dica.append(el("strong", null, tc(c.nome_urna)));
    dica.append(document.createTextNode(`${c.partido} ${c.numero} · ${QUAD[c.quadrante].curto}`));
    dica.append(document.createElement("br"));
    dica.append(document.createTextNode(`Economia ${fmt(c.eco)} · costumes ${fmt(c.pes)} (${c.posicao_fonte})`));
    dica.append(document.createElement("br"));
    dica.append(document.createTextNode(`${SITUACAO[c.situacao][1]}${c.fronteira ? " · perto do centro" : ""}`));
    if (subJudice(c)) { dica.append(document.createElement("br")); dica.append(el("strong", null, "⚠ Candidatura contestada, sub judice")); }
    dica.hidden = false;
    const w = dica.offsetWidth, h = dica.offsetHeight;
    dica.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x + 14)) + "px";
    dica.style.top = Math.max(8, Math.min(window.innerHeight - h - 8, y + 14)) + "px";
  }
  function renderNolan(g) {
    const W = 440, H = 470, ml = 44, mr = 16, mt = 30, mb = 62, pw = W - ml - mr, ph = H - mt - mb;
    const X = (v) => ml + v / 10 * pw, Y = (v) => mt + (1 - v / 10) * ph;
    const svg = $("nolan"); svg.textContent = "";
    const sup = "var(--surface)";
    svg.append(sv("rect", {x: ml, y: mt, width: pw, height: ph, fill: sup, stroke: "var(--axis)", "stroke-width": 1}));
    // fundo colorido de cada quadrante, para identificar de relance a posição ideológica
    svg.append(sv("rect", {x: ml, y: mt, width: X(5) - ml, height: Y(5) - mt, fill: qcorWash("ESQUERDA")}));
    svg.append(sv("rect", {x: X(5), y: mt, width: ml + pw - X(5), height: Y(5) - mt, fill: qcorWash("LIBERTARIO")}));
    svg.append(sv("rect", {x: ml, y: Y(5), width: X(5) - ml, height: mt + ph - Y(5), fill: qcorWash("AUTORITARIO")}));
    svg.append(sv("rect", {x: X(5), y: Y(5), width: ml + pw - X(5), height: mt + ph - Y(5), fill: qcorWash("DIREITA")}));
    const m = META.margem_fronteira;
    svg.append(sv("rect", {x: X(5 - m), y: mt, width: X(5 + m) - X(5 - m), height: ph, fill: sup, opacity: .55}));
    svg.append(sv("rect", {x: ml, y: Y(5 + m), width: pw, height: Y(5 - m) - Y(5 + m), fill: sup, opacity: .55}));
    svg.append(sv("line", {x1: X(5), y1: mt, x2: X(5), y2: mt + ph, stroke: "var(--axis)", "stroke-width": 1}));
    svg.append(sv("line", {x1: ml, y1: Y(5), x2: ml + pw, y2: Y(5), stroke: "var(--axis)", "stroke-width": 1}));
    [0, 5, 10].forEach(v => {
      const tx = sv("text", {x: X(v), y: mt + ph + 15, "text-anchor": "middle", class: "tick"}); tx.textContent = v; svg.append(tx);
      const ty = sv("text", {x: ml - 8, y: Y(v) + 4, "text-anchor": "end", class: "tick"}); ty.textContent = v; svg.append(ty);
    });
    const rot = (t, x, y, anchor, cor) => { const e = sv("text", {x, y, "text-anchor": anchor, class: "rot", fill: cor}); e.textContent = t; svg.append(e); };
    rot(QUAD.ESQUERDA.curto, ml + pw * .25, mt - 10, "middle", qcor("ESQUERDA")); rot(QUAD.LIBERTARIO.curto, ml + pw * .75, mt - 10, "middle", qcor("LIBERTARIO"));
    rot(QUAD.AUTORITARIO.curto, ml + pw * .25, mt + ph + 32, "middle", qcor("AUTORITARIO")); rot(QUAD.DIREITA.curto, ml + pw * .75, mt + ph + 32, "middle", qcor("DIREITA"));
    const ex = sv("text", {x: ml + pw / 2, y: H - 8, "text-anchor": "middle", class: "eixo"}); ex.textContent = "Economia: mais Estado (0)  →  mais livre mercado (10)"; svg.append(ex);
    const ey = sv("text", {x: 13, y: mt + ph / 2, "text-anchor": "middle", class: "eixo", transform: `rotate(-90 13 ${mt + ph / 2})`}); ey.textContent = "Costumes: conservador (0)  →  liberal (10)"; svg.append(ey);

    const ordem = {fora_da_disputa: 0, abaixo_do_corte: 0, nao_avaliado: 1, segue: 2, recomendado: 3};
    const pts = g.candidatos.filter(c => c.eco != null).sort((a, b) => ordem[a.situacao] - ordem[b.situacao]);
    const camada = sv("g", {}); svg.append(camada);
    const posicoes = [];
    pts.forEach(c => {
      const x = X(c.eco), y = Y(c.pes), rec = c.situacao === "recomendado", fora = c.situacao === "fora_da_disputa" || c.situacao === "abaixo_do_corte";
      posicoes.push({c, x, y});
      const gp = sv("g", {class: "ponto", tabindex: 0, role: "img", "aria-label": `${tc(c.nome_urna)}, ${c.partido}. ${QUAD[c.quadrante].curto}. Economia ${fmt(c.eco)}, costumes ${fmt(c.pes)}. ${SITUACAO[c.situacao][1]}.`});
      gp.append(sv("circle", {class: "anel", cx: x, cy: y, r: rec ? 12 : 10, fill: "none", stroke: "var(--ink)", "stroke-width": 0, opacity: 0}));
      const r = rec ? 8 : 6;
      gp.append(sv("circle", {cx: x, cy: y, r: r + 2, fill: sup}));
      gp.append(sv("circle", fora ? {cx: x, cy: y, r, fill: sup, stroke: "var(--muted)", "stroke-width": 2}
                                 : {cx: x, cy: y, r, fill: rec ? "var(--accent)" : "var(--neutral)"}));
      gp.append(sv("circle", {cx: x, cy: y, r: 16, fill: "transparent"}));
      gp.addEventListener("focus", () => { const b = gp.getBoundingClientRect(); mostrarDica(c, b.right, b.top); });
      gp.addEventListener("blur", () => { dica.hidden = true; });
      c._g = gp; camada.append(gp);
    });
    const alvos = posicoes.slice();
    let pv = null;
    if (voce && (voce.eco != null || voce.pes != null)) {
      const gv = sv("g", {role: "img", "aria-label": `Sua posição: economia ${voce.eco == null ? "não informada" : fmt(voce.eco)}, costumes ${voce.pes == null ? "não informados" : fmt(voce.pes)}`});
      const st = {fill: "none", stroke: "var(--ink)", "stroke-width": 3, "stroke-linejoin": "round", "stroke-linecap": "round"};
      if (voce.eco != null && voce.pes != null) {
        const x = X(voce.eco), y = Y(voce.pes);
        gv.append(sv("path", Object.assign({d: `M${x} ${y - 10} L${x + 10} ${y} L${x} ${y + 10} L${x - 10} ${y} Z`}, st)));
        pv = {c: {situacao: "voce"}, x, y};
      } else if (voce.eco != null) {
        const x = X(voce.eco);
        gv.append(sv("line", Object.assign({x1: x, y1: mt, x2: x, y2: mt + ph, opacity: .8}, st)));
        pv = {c: {situacao: "voce"}, x, y: mt + 16};
      } else {
        const y = Y(voce.pes);
        gv.append(sv("line", Object.assign({x1: ml, y1: y, x2: ml + pw, y2: y, opacity: .8}, st)));
        pv = {c: {situacao: "voce"}, x: ml + pw - 36, y};
      }
      camada.append(gv); posicoes.push(pv);
    }
    const rotular = (o, texto) => {
      const {x, y} = o, larg = texto.length * 7.4 + 6;
      const opcoes = [
        {tx: x + 13, ty: y + 4, anchor: "start", box: [x + 11, y - 10, larg, 20]},
        {tx: x - 13, ty: y + 4, anchor: "end", box: [x - 11 - larg, y - 10, larg, 20]},
        {tx: x, ty: y - 15, anchor: "middle", box: [x - larg / 2, y - 30, larg, 20]},
        {tx: x, ty: y + 27, anchor: "middle", box: [x - larg / 2, y + 12, larg, 20]},
      ];
      const livre = (b) => b[0] >= ml && b[0] + b[2] <= ml + pw && b[1] >= mt && b[1] + b[3] <= mt + ph &&
        !posicoes.some(q => q !== o && q.x > b[0] - 8 && q.x < b[0] + b[2] + 8 && q.y > b[1] - 8 && q.y < b[1] + b[3] + 8);
      const e = opcoes.find(op => livre(op.box)) || opcoes[0];
      const t = sv("text", {x: e.tx, y: e.ty, "text-anchor": e.anchor, class: "rot", stroke: "var(--surface)", "stroke-width": 3, "paint-order": "stroke"});
      t.textContent = texto; camada.append(t);
    };
    posicoes.filter(o => o.c.situacao === "recomendado").forEach(o => rotular(o, tc(o.c.nome_urna)));
    if (pv) rotular(pv, "Você");
    let ativo = null;
    const limpar = () => { if (ativo) ativo.classList.remove("ativo"); ativo = null; dica.hidden = true; };
    svg.onpointermove = (ev) => {
      const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
      const p = pt.matrixTransform(svg.getScreenCTM().inverse());
      let melhor = null, dmin = 26;
      alvos.forEach(o => { const d = Math.hypot(o.x - p.x, o.y - p.y); if (d < dmin) { dmin = d; melhor = o; } });
      if (melhor && melhor.c._g !== ativo) { if (ativo) ativo.classList.remove("ativo"); ativo = melhor.c._g; ativo.classList.add("ativo"); }
      if (!melhor) return limpar();
      mostrarDica(melhor.c, ev.clientX, ev.clientY);
    };
    svg.onpointerleave = limpar;

    const lg = $("legenda"); lg.textContent = "";
    const item = (svgHtml, t) => { const s = el("span"); const v = sv("svg", {viewBox: "0 0 16 16"}); svgHtml(v); s.append(v, document.createTextNode(t)); lg.append(s); };
    item(v => v.append(sv("circle", {cx: 8, cy: 8, r: 6, fill: "var(--accent)"})), "Recomendado");
    item(v => v.append(sv("circle", {cx: 8, cy: 8, r: 4.5, fill: "var(--neutral)"})), "Continua na disputa");
    item(v => v.append(sv("circle", {cx: 8, cy: 8, r: 4.5, fill: "var(--surface)", stroke: "var(--muted)", "stroke-width": 2})), "Fora da disputa ou abaixo do corte");
    item(v => v.append(sv("rect", {x: 1, y: 4, width: 14, height: 8, fill: "var(--wash)", stroke: "var(--axis)"})), "Perto do centro");
    if (pv) item(v => v.append(sv("path", {d: "M8 1 L15 8 L8 15 L1 8 Z", fill: "none", stroke: "var(--ink)", "stroke-width": 2, "stroke-linejoin": "round"})), "Você");
    const indiv = g.candidatos.filter(c => c.posicao_fonte === "pesquisa individual").length;
    $("nolanNota").textContent = `Posição por pesquisa individual: ${indiv} de ${g.candidatos.length} candidatos. Os demais usam a posição do partido.`;
  }

  // ---------- cartões por quadrante (sem depender do quiz) ----------
  function montarQuadrantes(g) {
    const ordemVisual = ["ESQUERDA", "LIBERTARIO", "AUTORITARIO", "DIREITA"];
    const box = $("cardsQuadrantes"); box.textContent = "";
    ordemVisual.forEach(chave => {
      const q = QUAD[chave];
      const recs = g.recomendados.map(sq => g.candidatos.find(c => c.sq === sq)).filter(c => c.quadrante === chave);
      const card = el("article", "qcard " + QCLASSE[chave]);
      card.append(el("div", "qtitulo", q.nome));
      if (!recs.length) {
        const fora = g.candidatos.filter(c => c.quadrante === chave);
        card.append(el("p", "vazio-quad", fora.length ? "Nenhum candidato desta posição continuou na disputa." : "Nenhum candidato registrado nesta posição."));
        if (fora.length) card.append(el("p", "nota", "Ficaram de fora: " + fora.map(c => `${tc(c.nome_urna)} (${c.situacao === "fora_da_disputa" ? "fora da disputa" : c.situacao === "abaixo_do_corte" ? "idoneidade " + fmt(c.idoneidade_geral) : "sem verificação"})`).join("; ") + "."));
      } else recs.forEach(c => card.append(blocoCandidato(c, "quadrante")));
      box.append(card);
    });
  }

  // ---------- o melhor candidato para você ----------
  function melhorParaVoce(g, cl) {
    const recPorQuadrante = (chaves) => {
      const cands = [];
      chaves.forEach(ch => g.recomendados.forEach(sq => { const c = g.candidatos.find(x => x.sq === sq); if (c && c.quadrante === ch) cands.push(c); }));
      return cands.sort((a, b) => b.qualificacao_geral - a.qualificacao_geral)[0] || null;
    };
    let c = recPorQuadrante([...cl.seu]);
    if (c) return {candidato: c, origem: "É o melhor avaliado no seu quadrante político."};
    c = recPorQuadrante([...cl.viz]);
    if (c) return {candidato: c, origem: "Seu posicionamento está perto do centro; este é o melhor avaliado no quadrante vizinho ao seu."};
    // plano B: ninguém recomendado nos quadrantes possíveis do eleitor -- pega o mais próximo por distância, entre quem segue na disputa
    const vivos = g.candidatos.filter(x => x.situacao === "segue" || x.situacao === "recomendado");
    if (!vivos.length) return null;
    const dist = (x) => { let s = 0, n = 0; if (voce.eco != null) { s += (x.eco - voce.eco) ** 2; n++; } if (voce.pes != null) { s += (x.pes - voce.pes) ** 2; n++; } return n ? Math.sqrt(s) : Infinity; };
    const [prox, d] = vivos.map(x => [x, dist(x)]).sort((a, b) => a[1] - b[1] || b[0].qualificacao_geral - a[0].qualificacao_geral)[0];
    return {candidato: prox, origem: `Nenhum candidato bem avaliado do seu quadrante (ou do vizinho) continua na disputa. Este é o mais próximo da sua posição entre os que seguem na disputa (a ${fmt(d)} pontos de distância no diagrama)${d > 5 ? " — uma distância grande; vale ler o plano de governo com atenção" : ""}.`};
  }
  function renderSeuCandidato(g) {
    const sec = $("secSeuCandidato"), box = $("blocoSeuCandidato");
    const cl = classificarVoce();
    if (!cl) { sec.hidden = true; return; }
    const achado = melhorParaVoce(g, cl);
    box.textContent = "";
    if (!achado) {
      sec.style.borderColor = ""; sec.style.background = "";
      box.append(el("p", "semvoce", "Nenhum candidato deste cargo continua na disputa para comparar com a sua posição."));
      sec.hidden = false; return;
    }
    // usa a cor do quadrante do candidato (mesma paleta do diagrama de Nolan) para destacar a seção
    const k = achado.candidato.quadrante;
    sec.style.borderColor = qcor(k);
    sec.style.background = qcorWash(k);
    const origem = el("p", "origem", achado.origem);
    origem.style.background = qcorWash(k);
    origem.style.color = qcor(k);
    box.append(origem);
    box.append(blocoCandidato(achado.candidato, "seu_candidato"));
    sec.hidden = false;
  }

  // ---------- lista com todos os candidatos do cargo/estado ----------
  function renderTodos(g) {
    const onde = CARGO[g.cargo].rotulo + (g.uf === "BR" ? "" : " · " + UF_NOME[g.uf]);
    $("todosSub").textContent = `${onde}. Ordenados pela qualificação geral (média entre idoneidade geral e competência geral). Quem tem registro indeferido ou idoneidade abaixo de ${fmt(g.corte)} não é recomendado, mas segue listado para transparência.`;
    const rec = g.candidatos.filter(c => c.situacao === "recomendado" || c.situacao === "segue").length;
    const fora = g.candidatos.filter(c => c.situacao === "fora_da_disputa").length;
    const abaixo = g.candidatos.filter(c => c.situacao === "abaixo_do_corte").length;
    const r = $("resumo"); r.textContent = "";
    [[g.candidatos.length, "candidatos"], [fora, "fora da disputa"], [abaixo, "abaixo do corte"], [rec, "continuam na disputa"]].forEach(([n, t]) => { const s = el("span"); s.append(el("b", null, String(n)), document.createTextNode(" " + t)); r.append(s); });
    $("detalheTodos").open = false;
    $("resumoToggle").textContent = `Ver a lista completa dos ${g.candidatos.length} candidatos`;

    const ordenados = g.candidatos.slice().sort((a, b) => (b.qualificacao_geral ?? -1) - (a.qualificacao_geral ?? -1) || a.nome_urna.localeCompare(b.nome_urna, "pt-BR"));
    const ol = $("listaTodos"); ol.textContent = "";
    const criarLinha = (c, i) => {
      const li = el("li", "linha" + (c.situacao === "fora_da_disputa" || c.situacao === "abaixo_do_corte" ? " fora" : ""));
      const b = el("button"); b.type = "button"; b.setAttribute("aria-expanded", "false");
      const quem = el("span", "quem"); const nm = el("span", "nomelista", tc(c.nome_urna)); quem.append(nm, el("small", null, `${c.partido} ${c.numero} · pesquisa ${verif(c).curto}`));
      const med = el("span");
      const n3 = el("span", "notas3");
      [["Qualificação", c.qualificacao_geral], ["Idoneidade", c.idoneidade_geral], ["Competência", c.competencia_geral]].forEach(([lab, v]) => {
        const s = el("span"); s.append(document.createTextNode(lab + " "), el("b", null, fmt(v))); n3.append(s);
      });
      med.append(n3);
      const tr = el("span", "trilho"); const fill = document.createElement("i"); fill.style.width = ((c.qualificacao_geral || 0) * 10) + "%"; tr.append(fill); med.append(tr);
      const [ico, rot] = SITUACAO[c.situacao];
      const pill = el("span", "pill" + (c.situacao === "recomendado" ? " rec" : ""), `${ico} ${rot}`);
      const pillwrap = el("span", "pillwrap"); pillwrap.append(pill);
      if (subJudice(c)) pillwrap.append(el("span", "pill warn", "⚠ Sub judice"));
      b.append(quem, med, pillwrap);
      // o painel de detalhes só é montado na primeira abertura (com ~1.000 candidatos por lista, montar todos trava a página)
      const det = el("div"); det.hidden = true; det.id = "det-" + i; b.setAttribute("aria-controls", det.id);
      let montado = false;
      const montarDetalhe = () => {
        const d = detalhe(c);
        if (c.motivo_saida && c.situacao !== "abaixo_do_corte") d.prepend(el("p", null, "Por que saiu: " + c.motivo_saida.replace(/^[a-z_]+: /, "")));
        if (c.situacao === "abaixo_do_corte") d.prepend(el("p", null, `Por que saiu: idoneidade geral ${c.motivo_saida.replace(/\./g, ",")} (corte ${fmt(g.corte)}).`));
        det.className = d.className; det.append(...d.childNodes);
      };
      b.addEventListener("click", () => {
        if (!montado) { montado = true; montarDetalhe(); }
        const abre = det.hidden; det.hidden = !abre; b.setAttribute("aria-expanded", String(abre));
      });
      li.append(b, det); return li;
    };

    // paginação: só as linhas da página atual existem no DOM (listas de deputados passam de mil candidatos)
    const porPagina = 25, paginas = Math.max(1, Math.ceil(ordenados.length / porPagina));
    const nav = $("paginacao"); nav.textContent = ""; nav.hidden = paginas <= 1;
    const ant = el("button", "btn", "‹ Anterior"), prox = el("button", "btn", "Próxima ›");
    ant.type = prox.type = "button";
    const seletor = document.createElement("select"); seletor.setAttribute("aria-label", "Ir para a página");
    const faixa = el("span", "faixa"); faixa.setAttribute("aria-live", "polite");
    if (paginas > 1) {
      for (let p = 1; p <= paginas; p++) { const o = el("option", null, `Página ${p} de ${paginas}`); o.value = String(p); seletor.append(o); }
      ant.addEventListener("click", () => mostrarPagina(pagina - 1, true));
      prox.addEventListener("click", () => mostrarPagina(pagina + 1, true));
      seletor.addEventListener("change", () => mostrarPagina(Number(seletor.value), true));
      nav.append(ant, seletor, prox, faixa);
    }
    let pagina = 1;
    const mostrarPagina = (n, rolar) => {
      pagina = Math.min(paginas, Math.max(1, n));
      const ini = (pagina - 1) * porPagina;
      ol.textContent = "";
      ordenados.slice(ini, ini + porPagina).forEach((c, k) => ol.append(criarLinha(c, ini + k)));
      ant.disabled = pagina === 1; prox.disabled = pagina === paginas; seletor.value = String(pagina);
      faixa.textContent = `Mostrando ${ini + 1} a ${Math.min(ini + porPagina, ordenados.length)} de ${ordenados.length.toLocaleString("pt-BR")}`;
      if (rolar) $("detalheTodos").scrollIntoView({block: "start"});
    };
    mostrarPagina(1, false);
  }

  // ---------- metodologia ----------
  function renderMetodologia() {
    const m = $("metodo"); m.textContent = "";
    [`Reunimos os candidatos oficiais do TSE para o cargo e o estado escolhidos.`,
     `Etapa 0: saem candidatos com registro indeferido ou inelegíveis, mesmo que ainda apareçam no arquivo do TSE.`,
     `Etapa 1: sai quem tem idoneidade geral abaixo de ${fmt(META.corte)} (de 0 a 10; para deputados o corte é ${fmt(META.corte_deputados)}, porque a nota deles vem só de bases oficiais e do partido). Idoneidade geral é a média entre a idoneidade pessoal do candidato (processos, Ficha Limpa, contas) e a do círculo político dele (vice, presidentes de partido, padrinhos). Quem não teve a idoneidade pesquisada não é recomendado, para não punir quem foi mais escrutinado.`,
     `Etapa 2: cada candidato restante é posicionado num de quatro quadrantes do diagrama de Nolan (limite em ${fmt(META.limiar)} nos dois eixos: economia e costumes).`,
     `Etapa 3: em cada quadrante, o recomendado é quem tem maior qualificação geral — a média entre idoneidade geral e competência geral (que por sua vez é a média da competência declarada e da escolaridade).`,
     `Empates na última vaga de um quadrante são resolvidos por sorteio, nunca por ordem alfabética.`,
     `Cada candidato mostra a profundidade da pesquisa (verificação estrutural, rápida, padrão ou aprofundada) e o resultado da conferência automática, por CPF, em bases oficiais: contas julgadas irregulares pelo TCU, motivos de indeferimento no TSE em 2022, sanções do CEIS, CNEP e CEAF e autos de infração do Ibama.`,
     `Se você não sabe seu quadrante, 2 perguntas simples indicam uma posição provável, que não é armazenada. Se nenhum candidato do seu quadrante (ou do vizinho) continuar na disputa, mostramos o mais próximo da sua posição entre os demais.`].forEach(t => m.append(el("li", null, t)));
    const lim = $("limites"); lim.textContent = "";
    [`Cobertura desigual: Presidente, Governador e Senador têm pesquisa individual na internet em todos os estados. Deputado federal tem só verificação estrutural: círculo político (presidente do partido), cargos eletivos de 2014 a 2024 e conferência em bases oficiais; ali, nota 10 quer dizer apenas que nada consta nessas bases, sem incluir processos judiciais, inquéritos nem notícias. Deputados estadual e distrital ainda não entraram. A pesquisa de Senador foi feita com busca mais rápida (1 a 2 buscas por candidato), então nota 10 vale como "nada encontrado", não como atestado.`,
     `A posição de quem não teve pesquisa individual é a do partido (indicado ao passar o mouse ou focar o ponto no diagrama). Quem está perto do centro pode pertencer ao quadrante vizinho.`,
     `"Competência" mede formação e experiência declaradas, e favorece quem tem carreira eletiva ou diploma superior — não mede a qualidade do plano de governo.`,
     `O questionário de 2 perguntas ainda não foi calibrado nem testado com eleitores; uma pergunta por eixo é pouco, e respostas de meio-termo ficam "perto do centro". Ajuste sua posição manualmente se o resultado não parecer com você.`,
     `Nota 10 de idoneidade significa "nada encontrado na busca", não "nada aconteceu" — a profundidade da apuração varia, sobretudo para partidos menores.`,
     `Nenhuma nota substitui ler o plano de governo e as fontes citadas em cada candidato.`].forEach(t => lim.append(el("li", null, t)));
    $("rodape").textContent = `Dados de ${META.gerado_em}. ${META.total_candidatos.toLocaleString("pt-BR")} candidatos no arquivo do TSE; ${Object.values(GRUPOS).filter(x => x.status !== "sem_verificacao").length} combinações de cargo e estado já com verificação.`;
  }

  // ---------- render principal ----------
  function render() {
    const cargo = $("cargo").value, uf = ufAtual(cargo), g = GRUPOS[cargo + "|" + uf];
    const chave = cargo + "|" + uf;
    if (chave !== ultimoGrupo) {
      rastrear("selecionar_grupo", { cargo: cargo, uf: uf, acao: acaoAtual });
      ultimoGrupo = chave;
    }
    acaoAtual = "carga";
    history.replaceState(null, "", "#" + cargo + "|" + uf);
    const onde = CARGO[cargo].rotulo + (uf === "BR" ? "" : " · " + UF_NOME[uf]);
    if (!g || g.status === "sem_verificacao") {
      $("cobertura").innerHTML = "";
      $("cobertura").className = "status alerta";
      $("cobertura").textContent = `${onde}: ${g ? g.n_total : 0} candidatos registrados, nenhum com idoneidade verificada ainda. Este cargo e estado serão liberados quando a pesquisa cobrir os candidatos.`;
      $("fluxo").hidden = true; atual = null; return;
    }
    $("cobertura").className = "status";
    $("cobertura").textContent = `${onde}: ${g.n_avaliados} de ${g.n_total} candidatos com idoneidade verificada.` + (g.status === "parcial" ? " Quem não foi verificado não entra nas recomendações." : "");
    $("fluxo").hidden = false; atual = g;
    renderNolan(g); montarQuadrantes(g); renderSeuCandidato(g); renderTodos(g);
  }

  function iniciar() {
    preencherCargos();
    const h = decodeURIComponent(location.hash.slice(1)).split("|");
    const cargo = CARGO[h[0]] ? h[0] : "PRESIDENTE";
    $("cargo").value = cargo; preencherUfs(cargo, h[1]);
    $("cargo").addEventListener("change", () => { preencherUfs($("cargo").value); acaoAtual = "cargo"; render(); });
    $("uf").addEventListener("change", () => { acaoAtual = "uf"; render(); });
    montarQuiz();
    renderMetodologia();
    $("btnRefazer").addEventListener("click", () => {
      Object.keys(respostas).forEach(k => delete respostas[k]);
      document.querySelectorAll("#quizCorpo input[type=radio]").forEach(r => { r.checked = false; });
      voce = null; atualizarVoce(false); $("secDescubra").scrollIntoView({block: "start"});
    });
    render();
  }
  iniciar();
})();
