/* Kit de cenas do estilo Motion. Lê window.REEL (identidade e enquadramento) e window.CENAS (o mapa de cenas)
   e monta tudo numa linha do tempo GSAP pausada, determinada só pelo tempo (o render pula para cada quadro).
   Cada tipo de cena é uma função abaixo. Leia o SKILL.md e references/cenas.md antes de mudar. */
(function () {
  "use strict";
  var R = window.REEL || {}, C = window.CENAS || { cenas: [] };
  var A = /^#[0-9a-fA-F]{6}$/.test(R.acento || "") ? R.acento : "#ffffff";
  var rgb = [1, 3, 5].map(function (i) { return parseInt(A.substr(i, 2), 16); }).join(",");
  var root = document.documentElement;
  root.style.setProperty("--acento", A);
  root.style.setProperty("--acento-rgb", rgb);
  var tl = gsap.timeline({ paused: true });
  var palco = document.getElementById("cenas");
  var B = "blur(26px)", N = "blur(0px)";
  var CAP = R.capY || 1490, FAIXA = [CAP - 75, CAP + 75];

  function el(tag, cls, css, html, pai) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (css) e.setAttribute("style", css);
    if (html) e.innerHTML = html;
    (pai || palco).appendChild(e);
    return e;
  }
  function svg(css, inner, pai) {
    var w = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    w.setAttribute("width", 1080); w.setAttribute("height", 1920); w.setAttribute("viewBox", "0 0 1080 1920");
    w.setAttribute("style", "position:absolute;left:0;top:0;" + (css || ""));
    w.innerHTML = inner; (pai || palco).appendChild(w); return w;
  }
  // *palavra* vira destaque na cor de acento
  function marca(s) { return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\*([^*]+)\*/g, '<span class="ac">$1</span>'); }
  function letras(s) { return String(s || "").split("").map(function (c) { return c === " " ? " " : "<i>" + c + "</i>"; }).join(""); }
  function bat(c, i, padrao) { return c.batidas && c.batidas[i] != null ? c.batidas[i] : padrao; }

  // ---------- peças reutilizáveis ----------
  function arquivoHTML(rotulo, w, h) {
    return '<div class="arq" style="width:' + w + "px;height:" + h + 'px"><div class="play" style="border-left-width:' + Math.round(w * .3) + "px;border-top-width:" + Math.round(w * .18) + "px;border-bottom-width:" + Math.round(w * .18) + 'px"></div><b style="font-size:' + Math.round(w * .17) + 'px">' + marca(rotulo) + "</b></div>";
  }
  function mascote(px, extra) { return '<div class="masc" style="width:' + px + "px;height:" + px + "px;" + (extra || "") + '"><i></i><i></i></div>'; }
  function grade(pai, y0) {
    var s = "", y;
    for (var i = 0; i < 9; i++) { y = y0 + Math.pow(i / 8, 1.8) * (1900 - y0); s += '<line x1="0" y1="' + y + '" x2="1080" y2="' + y + '"/>'; }
    for (var j = -6; j <= 6; j++) s += '<line x1="' + (540 + j * 40) + '" y1="' + y0 + '" x2="' + (540 + j * 260) + '" y2="1920"/>';
    return svg("opacity:.32", '<g stroke="var(--acento)" stroke-width="2" fill="none">' + s + "</g>", pai);
  }
  function titulo(pai, txt, y, tam) { return el("div", "tit", "top:" + y + "px;font-size:" + (tam || 104) + "px", letras(txt), pai); }
  function entraTitulo(t, at) {
    tl.fromTo(t.querySelectorAll("i"), { autoAlpha: 0, y: 60, filter: B }, { autoAlpha: 1, y: 0, filter: N, duration: .35, stagger: .035, ease: "power3.out" }, at);
  }

  // ---------- a cena: caixa, fundo preto do takeover, entrada e saída ----------
  var TAKE_PADRAO = { abertura: false, timeline: false, rede: false, cartao: false };
  function ehTake(c) { return c.takeover != null ? c.takeover : TAKE_PADRAO[c.tipo] !== false; }
  function cena(c, takeoverPadrao) {
    var take = c.takeover != null ? c.takeover : takeoverPadrao;
    var g = el("div", "cena", "z-index:" + (take ? 20 : 30)); // cena sobre o rosto fica acima do fundo preto: pode entrar no fim de um takeover e seguir no rosto
    if (take) {
      var bk = el("div", "bk", "", "", g);
      tl.set(bk, { autoAlpha: 1 }, c.de);
      // encadeada: outro takeover começa no fim desta, o preto continua sem piscar o rosto
      var segue = (C.cenas || []).some(function (o) { return o !== c && ehTake(o) && Math.abs(o.de - c.ate) < .06; });
      if (!segue) tl.to(bk, { autoAlpha: 0, duration: .14, ease: "none" }, c.ate - .14);
    }
    tl.set(g, { autoAlpha: 1 }, c.de);
    tl.set(g, { autoAlpha: 0 }, c.ate);
    return g;
  }
  function sai(alvos, c, d) { tl.to(alvos, { autoAlpha: 0, filter: B, y: "-=60", duration: d || .3, ease: "power2.in" }, c.ate - (d || .3)); }

  var T = {};

  // ABERTURA: painel desenhado em cima, headline no meio, rosto embaixo (a câmera é reposicionada pelo index).
  T.abertura = function (c) {
    var g = cena(c, false);
    var top = c.painelAltura || 700, faixa = c.faixaAltura || 286;
    var p = el("div", "painel", "height:" + top + "px", "", g);
    var tela = el("div", "monitor", "", "", p);
    var prev = el("div", "prev", "", '<div class="play" style="border-left-width:70px;border-top-width:42px;border-bottom-width:42px"></div>', tela);
    for (var i = 0; i < 3; i++) el("div", "thumb", "top:" + (40 + i * 92) + "px", "", tela);
    var faixas = [[0, 230, 1], [250, 210, 0], [480, 260, 1], [760, 120, 0]];
    var trk = el("div", "trilha", "top:330px", "", tela);
    faixas.forEach(function (f) { el("div", "clip " + (f[2] ? "cw" : "cg"), "left:" + f[0] + "px;width:" + f[1] + "px", "", trk); });
    var leg = el("div", "trilha", "top:420px;height:44px", "", tela);
    [[40, 200], [320, 200], [640, 220]].forEach(function (f) { el("div", "clip cg", "left:" + f[0] + "px;width:" + f[1] + "px;height:30px;top:7px", "", leg); });
    var onda = "", x;
    for (x = 0; x < 900; x += 9) { var h = 6 + Math.abs(Math.sin(x * .071) * Math.cos(x * .023)) * 34; onda += '<rect x="' + x + '" y="' + (40 - h / 2) + '" width="5" height="' + h + '" rx="2"/>'; }
    el("div", "onda", "", '<svg width="900" height="80" viewBox="0 0 900 80"><g fill="var(--acento)" opacity=".75">' + onda + "</g></svg>", tela);
    var cab = el("div", "cabeca", "", "", tela);
    var hl = el("div", "headline", "top:" + top + "px;height:" + faixa + "px", (c.linhas || []).map(function (l) { return "<div>" + marca(l) + "</div>"; }).join(""), g);
    tl.fromTo(cab, { x: 0 }, { x: 860, duration: Math.max(.5, c.ate - c.de), ease: "none" }, c.de);
    tl.fromTo(trk.children, { y: -40, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: .3, stagger: .25, ease: "back.out(1.4)" }, c.de + .1);
    tl.fromTo(prev, { scale: .96 }, { scale: 1, duration: Math.max(.5, c.ate - c.de), ease: "none" }, c.de);
    window.__abertura = { de: c.de, ate: c.ate, camTop: top + faixa, hl: hl };
  };

  // ARQUIVO: o arquivo de vídeo nasce, gira, e dá lugar a um segundo cartão (ex.: o pedido, o roteiro).
  T.arquivo = function (c) {
    var g = cena(c, true);
    var f = el("div", "a", "left:300px;top:260px", arquivoHTML(c.rotulo || "VÍDEO", 480, 620), g);
    tl.fromTo(f, { autoAlpha: 0, scale: .3, rotationY: -70, filter: B }, { autoAlpha: 1, scale: 1, rotationY: 0, filter: N, duration: .6, ease: "power3.out" }, c.de);
    var t2 = bat(c, 0, c.de + .6);
    if (c.segundo) {
      var br = el("div", "a vidro", "left:330px;top:320px;width:440px;height:560px;padding:40px", '<b class="ac" style="font-size:54px;display:block;margin-bottom:40px">' + marca(c.segundo) + '</b><i class="ln"></i><i class="ln"></i><i class="ln"></i><i class="ln"></i><i class="ln" style="width:60%"></i>', g);
      tl.to(f, { x: -200, rotation: -8, scale: .75, duration: .5, ease: "power2.inOut" }, t2);
      tl.fromTo(br, { autoAlpha: 0, x: 0, rotationY: 60, filter: B }, { autoAlpha: 1, x: 170, rotationY: 0, filter: N, duration: .6, ease: "back.out(1.4)" }, t2 + .15);
      tl.fromTo(br.querySelectorAll(".ln"), { scaleX: 0 }, { scaleX: 1, duration: .25, stagger: .1 }, t2 + .5);
      sai([f, br], c);
    } else sai(f, c);
  };

  // LINHA DO TEMPO: os pedaços caem numa trilha de edição e a agulha corre (no peito, ou dentro de um takeover).
  T.timeline = function (c) {
    var g = cena(c, false);
    var y = c.y != null ? c.y : CAP - 370;
    var t = el("div", "a trilha-grande", "left:90px;top:" + y + "px", '<div class="c cw" style="left:30px;width:250px"></div><div class="c cg" style="left:300px;width:320px"></div><div class="c cw" style="left:640px;width:220px"></div><div class="agulha"></div>', g);
    if (c.rotulo) el("div", "a rot", "left:120px;top:" + (y - 70) + "px", marca(c.rotulo), g);
    tl.fromTo(t, { autoAlpha: 0, y: 200, filter: B }, { autoAlpha: 1, y: 0, filter: N, duration: .45, ease: "power3.out" }, c.de);
    tl.fromTo(t.querySelectorAll(".c"), { y: -700, x: 120, rotation: 15, autoAlpha: 0 }, { y: 0, x: 0, rotation: 0, autoAlpha: 1, duration: .5, stagger: .15, ease: "back.out(1.2)" }, c.de + .15);
    tl.fromTo(t.querySelector(".agulha"), { x: 0 }, { x: 860, duration: Math.max(.6, c.ate - c.de - .9), ease: "none" }, c.de + .6);
    sai(g.querySelectorAll(".a"), c);
  };

  // REDE: um objeto no peito liga caminhos até mascotes em volta do rosto (sem cobrir rosto nem legenda).
  T.rede = function (c) {
    var g = cena(c, false);
    var r = R.rosto || { x: 250, y: 180, w: 570, h: 860 };
    var y0 = c.y != null ? c.y : CAP - 460;
    var clip = "M0 0H1080V1920H0Z M" + r.x + " " + r.y + "V" + (r.y + r.h) + "H" + (r.x + r.w) + "V" + r.y + "Z M0 " + FAIXA[0] + "V" + FAIXA[1] + "H1080V" + FAIXA[0] + "Z";
    var ys = Math.max(r.y + 300, 520), yb = Math.min(1880, FAIXA[1] + 150);
    var cam = ["M330 " + (y0 + 120) + "C150 " + (y0 + 70) + " 150 " + (ys + 200) + " 170 " + (ys + 75),
      "M750 " + (y0 + 120) + "C930 " + (y0 + 70) + " 930 " + (ys + 200) + " 910 " + (ys + 75),
      "M400 " + (y0 + 310) + "C350 " + (yb - 90) + " 300 " + (yb - 40) + " 275 " + (yb - 10),
      "M680 " + (y0 + 310) + "C730 " + (yb - 90) + " 780 " + (yb - 40) + " 805 " + (yb - 10)];
    var s = svg("", '<defs><clipPath id="rede-' + c.de + '"><path clip-rule="evenodd" d="' + clip + '"/></clipPath></defs><g clip-path="url(#rede-' + c.de + ')" fill="none" stroke="var(--acento)" stroke-width="14" stroke-linecap="round">' +
      cam.map(function (d) { return '<path class="p" d="' + d + '"/>'; }).join("") + "</g>", g);
    var pc = el("div", "a", "left:300px;top:" + y0 + "px;width:480px", '<div class="tela-pc">' + marca(c.centro || "") + '</div><div class="pe"></div>', g);
    var ags = [[95, ys], [835, ys], [200, yb - 70], [730, yb - 70]].map(function (p) { return el("div", "a", "left:" + p[0] + "px;top:" + p[1] + "px", mascote(150, "border:8px solid #000"), g); });
    var rot = c.rotulo ? el("div", "a rot", "left:0;width:1080px;text-align:center;top:" + Math.min(1850, yb + 40) + "px", marca(c.rotulo), g) : null;
    var paths = s.querySelectorAll(".p");
    paths.forEach(function (p) { var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; });
    tl.fromTo(pc, { autoAlpha: 0, y: 300, rotationX: 60, filter: B }, { autoAlpha: 1, y: 0, rotationX: 0, filter: N, duration: .6, ease: "power3.out" }, c.de);
    tl.to(paths, { strokeDashoffset: 0, duration: .8, stagger: .15, ease: "power2.inOut" }, c.de + .5);
    tl.fromTo(ags, { autoAlpha: 0, scale: 0 }, { autoAlpha: 1, scale: 1, duration: .45, stagger: .12, ease: "back.out(2)" }, c.de + 1);
    tl.to(ags, { scale: 1.1, duration: .35, yoyo: true, repeat: 3, stagger: .1 }, c.de + 1.6);
    if (rot) tl.fromTo(rot, { autoAlpha: 0, y: 40, filter: B }, { autoAlpha: 1, y: 0, filter: N, duration: .45 }, bat(c, 0, c.de + 1.4));
    sai([s, pc].concat(ags, rot ? [rot] : []), c);
  };

  // DESTINO: o arquivo viaja por um caminho tracejado até um destino (pasta, nuvem, sistema).
  T.destino = function (c) {
    var g = cena(c, true);
    var s = svg("", '<path class="q" d="M260 1000C260 600 560 900 780 580" fill="none" stroke="var(--acento)" stroke-width="12" stroke-dasharray="30 26"/>', g);
    var dv = el("div", "a pilula", "left:580px;top:290px;width:420px;height:280px", '<div>' + marca(c.rotulo || "") + "</div>", g);
    var f = el("div", "a", "left:100px;top:880px", arquivoHTML(c.arquivo || "VÍDEO", 320, 420), g);
    var dur = c.ate - c.de;
    tl.fromTo(s.querySelector(".q"), { strokeDashoffset: 600 }, { strokeDashoffset: 0, duration: dur * .8, ease: "none" }, c.de);
    tl.fromTo(dv, { autoAlpha: 0, scale: .4, filter: B }, { autoAlpha: 1, scale: 1, filter: N, duration: .5, ease: "back.out(1.6)" }, c.de + .1);
    tl.fromTo(f, { autoAlpha: 0, scale: 1.4, rotationY: -50, filter: B }, { autoAlpha: 1, scale: 1, rotationY: 0, filter: N, duration: .5 }, c.de + .1);
    var t2 = bat(c, 0, c.de + Math.min(.9, dur * .35));
    tl.to(f, { keyframes: [{ x: 200, y: -300, rotation: 12, duration: .5 }, { x: 560, y: -520, scale: .3, rotation: 0, autoAlpha: 0, duration: .5 }], ease: "power2.in" }, t2);
    tl.to(dv, { scale: 1.15, yoyo: true, repeat: 1, duration: .15 }, t2 + 1);
    sai([s, dv], c);
  };

  // CARTÃO: um cartão de vidro no peito, com ícone e a palavra falada (abaixo do queixo, acima da legenda).
  T.cartao = function (c) {
    var g = cena(c, false);
    var y = c.y != null ? c.y : CAP - 400, w = c.largura || 920, x = c.x != null ? c.x : Math.round((1080 - w) / 2);
    var ic = c.icone === "agente" ? mascote(110) : c.icone === "doc" ? '<div class="doc"><i></i><i></i><i></i></div>' : c.icone === "nenhum" ? "" : arquivoHTML("", 100, 124);
    var k = el("div", "a vidro cartao", "left:" + x + "px;top:" + y + "px;width:" + w + "px", '<div class="ic">' + ic + '</div><div class="tx">' + (c.sub ? '<small>' + marca(c.sub) + "</small>" : "") + "<b>" + letras(c.texto || "") + '</b><div class="barras"><i></i><i></i><i></i><i></i></div></div>', g);
    tl.fromTo(k, { autoAlpha: 0, y: 120, scale: .85, filter: B }, { autoAlpha: 1, y: 0, scale: 1, filter: N, duration: .45, ease: "back.out(1.5)" }, c.de);
    tl.fromTo(k.querySelectorAll("b i"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: .25, stagger: .04 }, c.de + .2);
    tl.fromTo(k.querySelectorAll(".barras i"), { scaleX: 0 }, { scaleX: 1, duration: .3, stagger: .12, ease: "power2.out" }, c.de + .35);
    sai(k, c);
  };

  // TELA: uma página desenhada se monta bloco a bloco (ilustração, nunca print fingido).
  T.tela = function (c) {
    var g = cena(c, true);
    var t = titulo(g, c.titulo || "", 169, c.tam || 108);
    var p = el("div", "a vidro", "left:130px;top:330px;width:820px;height:880px;padding:50px",
      '<div class="pt"><i></i><i></i><i></i></div><div class="blk hero"><i class="l1"></i><i class="l2"></i><div class="bola"></div></div><div class="row"><div class="blk"><i></i><i></i></div><div class="blk"><i></i><i></i></div><div class="blk"><i></i><i></i></div></div><i class="l3"></i><div class="btn"></div>', g);
    entraTitulo(t, c.de);
    tl.fromTo(p, { autoAlpha: 0, y: 160, rotationX: 35, filter: B }, { autoAlpha: 1, y: 0, rotationX: 0, filter: N, duration: .55, ease: "power3.out" }, c.de + .1);
    tl.fromTo(p.querySelectorAll(".hero,.row .blk,.l3,.btn"), { autoAlpha: 0, y: 50 }, { autoAlpha: 1, y: 0, duration: .3, stagger: .12, ease: "back.out(1.4)" }, c.de + .45);
    tl.to(p.querySelector(".btn"), { scale: 1.06, boxShadow: "0 0 50px rgba(var(--acento-rgb),.8)", yoyo: true, repeat: 1, duration: .2 }, c.de + 1.3);
    sai([t, p], c);
  };

  // CONVERSA: uma janela de mensagens enche com balões alternados (atendimento, suporte, venda).
  T.chat = function (c) {
    var g = cena(c, true);
    var t = titulo(g, c.titulo || "", 170, c.tam || 92);
    var bal = [[0, 70], [1, 60], [0, 85], [1, 55], [0, 65]].map(function (b) { return '<div class="bal ' + (b[0] ? "eu" : "ele") + '" style="width:' + b[1] + '%"><i></i><i></i></div>'; }).join("");
    var w = el("div", "a vidro", "left:120px;top:340px;width:840px;height:900px;padding:40px", '<div class="topo">' + mascote(54) + "<i></i></div>" + bal + '<div class="entrada"><i></i><b></b></div>', g);
    entraTitulo(t, c.de);
    tl.fromTo(w, { autoAlpha: 0, scale: .8, filter: B }, { autoAlpha: 1, scale: 1, filter: N, duration: .45, ease: "power3.out" }, c.de + .1);
    tl.fromTo(w.querySelectorAll(".bal"), { autoAlpha: 0, y: 40, scale: .9 }, { autoAlpha: 1, y: 0, scale: 1, duration: .28, stagger: Math.min(.4, (c.ate - c.de - 1) / 5), ease: "back.out(1.6)" }, c.de + .4);
    sai([t, w], c);
  };

  // CELULAR: mensagens chegam de fora e entram num celular (leads, pedidos, contatos).
  T.celular = function (c) {
    var g = cena(c, true);
    var t = titulo(g, c.titulo || "", 120, c.tam || 92);
    var t2 = c.sub ? el("div", "tit ac", "top:230px;font-size:" + Math.round((c.tam || 92) * .8) + "px", letras(c.sub), g) : null;
    var s = svg("", '<g fill="none" stroke="var(--acento)" stroke-width="4" stroke-dasharray="14 12" opacity=".8"><path class="lc" d="M0 700C150 690 240 760 330 760"/><path class="lc" d="M0 1060C150 1080 240 1000 330 980"/><path class="lc" d="M1080 640C930 650 840 720 750 760"/><path class="lc" d="M1080 1080C930 1060 840 1000 750 980"/></g>', g);
    var bal = [[0, 70], [1, 60], [0, 80], [1, 50], [0, 66]].map(function (b) { return '<div class="bal ' + (b[0] ? "eu" : "ele") + '" style="width:' + b[1] + '%"><i></i><i></i></div>'; }).join("");
    var ph = el("div", "a fone", "left:290px;top:370px;width:500px;height:920px", '<div class="topo">' + mascote(44) + "<i></i></div>" + bal, g);
    entraTitulo(t, c.de);
    if (t2) tl.fromTo(t2.querySelectorAll("i"), { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: .3, stagger: .035 }, bat(c, 0, c.de + .5));
    tl.fromTo(ph, { autoAlpha: 0, y: 200, rotationY: -30, filter: B }, { autoAlpha: 1, y: 0, rotationY: 0, filter: N, duration: .5, ease: "power3.out" }, c.de + .1);
    tl.fromTo(s.querySelectorAll(".lc"), { strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: 1.2, ease: "none" }, c.de + .3);
    tl.fromTo(ph.querySelectorAll(".bal"), { autoAlpha: 0, x: function (i) { return i % 2 ? 120 : -120; } }, { autoAlpha: 1, x: 0, duration: .3, stagger: .22, ease: "power2.out" }, c.de + .5);
    sai([t, s, ph].concat(t2 ? [t2] : []), c);
  };

  // ANEL: um anel de luz em perspectiva liga ideias em volta (imaginação, visão, plano).
  T.anel = function (c) {
    var g = cena(c, true);
    var s = svg("", '<g fill="none" stroke="var(--acento)" stroke-width="5"><path class="ln" d="M540 700L250 360"/><path class="ln" d="M540 700L860 380"/><path class="ln" d="M540 760L330 980"/><path class="ln" d="M540 760L780 960"/></g>', g);
    var an = el("div", "a anel", "left:240px;top:540px;width:600px;height:300px", "<div></div><div></div><div></div>", g);
    var sol = el("div", "a sol", "left:180px;top:280px", "", g);
    var doc = el("div", "a", "left:800px;top:290px", '<div class="doc grande"><i></i><i></i><i></i></div>', g);
    var mini = el("div", "a vidro", "left:230px;top:950px;width:200px;height:120px;padding:24px", '<div class="row2"><i></i><i class="ac-bg"></i><i></i></div>', g);
    var m = el("div", "a", "left:720px;top:900px", mascote(140), g);
    var t = titulo(g, c.titulo || "", 1100, c.tam || 84);
    tl.fromTo(an, { autoAlpha: 0, scale: .2, rotationX: 70, filter: B }, { autoAlpha: 1, scale: 1, rotationX: 0, filter: N, duration: .6, ease: "power3.out" }, c.de);
    tl.to(an.children[1], { rotation: 360, duration: c.ate - c.de, ease: "none" }, c.de);
    var ls = s.querySelectorAll(".ln"); ls.forEach(function (p) { var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; });
    tl.to(ls, { strokeDashoffset: 0, duration: .5, stagger: .12 }, c.de + .4);
    tl.fromTo([sol, doc, mini, m], { autoAlpha: 0, scale: 0 }, { autoAlpha: 1, scale: 1, duration: .4, stagger: .15, ease: "back.out(1.8)" }, c.de + .6);
    tl.to(sol, { rotation: 180, duration: c.ate - c.de, ease: "none" }, c.de);
    entraTitulo(t, bat(c, 0, c.de + .5));
    tl.to(an, { boxShadow: "0 0 120px rgba(var(--acento-rgb),.9)", yoyo: true, repeat: 3, duration: .4 }, c.de + .8);
    sai([s, an, sol, doc, mini, m, t], c);
  };

  // MENTE: uma cabeça se desenha, ganha conexões, e dela saem os ramos (construir, cérebro do negócio, processos).
  T.mente = function (c) {
    var g = cena(c, true);
    grade(g, 1180);
    var t = titulo(g, c.titulo || "", 98, c.tam || 130);
    var mk = c.marca ? el("div", "a ac", "left:850px;top:610px;font-size:56px;letter-spacing:3px", letras(c.marca), g) : null;
    var cab = svg("", '<g fill="none" stroke="var(--acento)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"><path class="cb" d="M400 1140C400 1060 330 1010 320 930C300 820 300 700 350 620C410 520 520 470 630 480C760 495 840 590 845 700C848 760 835 790 850 830L905 900C915 915 905 930 885 930L850 935C850 975 845 1010 820 1030C790 1050 740 1040 720 1050C700 1080 700 1110 700 1140"/></g><g class="cst" stroke="#fff" stroke-width="5" fill="#fff"><line x1="450" y1="700" x2="560" y2="610"/><line x1="560" y1="610" x2="700" y2="660"/><line x1="560" y1="610" x2="580" y2="790"/><line x1="580" y1="790" x2="700" y2="660"/><line x1="450" y1="700" x2="580" y2="790"/><line x1="580" y1="790" x2="480" y2="880"/><line x1="700" y1="660" x2="760" y2="800"/><circle cx="450" cy="700" r="17"/><circle cx="560" cy="610" r="17"/><circle cx="700" cy="660" r="17"/><circle cx="580" cy="790" r="17"/><circle cx="480" cy="880" r="14"/><circle cx="760" cy="800" r="14"/></g>', g);
    var sub = c.sub || c.destaque ? el("div", "a vidro", "left:170px;top:1150px;width:740px;padding:26px 40px", (c.sub ? '<small class="mono ac">' + marca(c.sub) + "</small>" : "") + (c.destaque ? '<b style="display:block;font-size:64px;margin-top:8px">' + marca(c.destaque) + "</b>" : ""), g) : null;
    var rm = c.ramos ? el("div", "a", "left:0;top:" + (FAIXA[1] + 30) + "px;width:1080px;text-align:center;font-size:70px;color:var(--acento)", letras(c.ramos), g) : null;
    var pills = el("div", "a", "left:150px;top:1300px;width:780px;height:70px", '<div class="pil" style="left:0"></div><div class="pil ac-bg" style="left:280px"></div><div class="pil" style="left:560px"></div>', g);
    var cb = cab.querySelector(".cb"), L = cb.getTotalLength(); cb.style.strokeDasharray = L; cb.style.strokeDashoffset = L;
    entraTitulo(t, c.de);
    tl.to(cb, { strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }, c.de + .2);
    tl.fromTo(cab.querySelectorAll(".cst > *"), { autoAlpha: 0, scale: 0, transformOrigin: "50% 50%" }, { autoAlpha: 1, scale: 1, duration: .25, stagger: .07 }, c.de + .9);
    var t2 = bat(c, 0, c.de + 1.6), t3 = bat(c, 1, t2 + .9);
    if (mk) tl.fromTo(mk.querySelectorAll("i"), { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: .25, stagger: .04 }, bat(c, 2, c.de + 1.2));
    if (sub) tl.fromTo(sub, { autoAlpha: 0, y: 80, filter: B }, { autoAlpha: 1, y: 0, filter: N, duration: .45, ease: "power3.out" }, t2);
    tl.fromTo(pills.children, { autoAlpha: 0, y: -60, scale: .6 }, { autoAlpha: 1, y: 0, scale: 1, duration: .3, stagger: .12, ease: "back.out(1.7)" }, t3);
    if (rm) tl.fromTo(rm.querySelectorAll("i"), { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: .25, stagger: .04 }, t3 + .1);
    sai([t, cab, pills].concat(sub ? [sub] : [], rm ? [rm] : [], mk ? [mk] : []), c);
  };

  // AGENTE: o mascote nasce grande, ganha órbita, e uma lista de tarefas se marca (o agente pronto, a tarefa feita).
  T.agente = function (c) {
    var g = cena(c, true);
    grade(g, 1100);
    var t = titulo(g, c.titulo || "", 72, c.tam || 130);
    var t2 = c.sub ? el("div", "tit ac", "top:212px;font-size:80px;letter-spacing:8px", letras(c.sub), g) : null;
    var m = el("div", "a", "left:390px;top:440px", '<div class="antena"></div>' + mascote(300, "border-width:0;box-shadow:0 0 140px rgba(var(--acento-rgb),.75)"), g);
    var orb = el("div", "a orbita", "left:190px;top:640px;width:700px;height:260px", "", g);
    var lista = el("div", "a vidro", "left:190px;top:920px;width:700px;padding:30px 40px", (c.tarefa ? '<small class="mono">' + marca(c.rotuloTarefa || "") + '</small><b style="display:block;font-size:52px;margin:6px 0 20px">' + marca(c.tarefa) + "</b>" : "") + '<div class="chk"><i></i><b></b></div><div class="chk"><i></i><b></b></div><div class="chk"><i></i><b></b></div>', g);
    entraTitulo(t, c.de);
    if (t2) tl.fromTo(t2.querySelectorAll("i"), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: .25, stagger: .04 }, c.de + .35);
    tl.fromTo(m, { autoAlpha: 0, scale: 0, y: 120 }, { autoAlpha: 1, scale: 1, y: 0, duration: .6, ease: "back.out(1.7)" }, c.de + .15);
    tl.fromTo(orb, { autoAlpha: 0, scale: .3 }, { autoAlpha: 1, scale: 1, duration: .5 }, c.de + .4);
    tl.to(orb, { rotation: 8, yoyo: true, repeat: 3, duration: .5, ease: "sine.inOut" }, c.de + .9);
    var t3 = bat(c, 0, c.de + 1.2);
    tl.fromTo(lista, { autoAlpha: 0, y: 120, filter: B }, { autoAlpha: 1, y: 0, filter: N, duration: .45, ease: "power3.out" }, t3);
    tl.fromTo(lista.querySelectorAll(".chk i"), { backgroundColor: "rgba(255,255,255,0)" }, { backgroundColor: A, duration: .15, stagger: .35 }, t3 + .4);
    tl.fromTo(lista.querySelectorAll(".chk b"), { scaleX: 0 }, { scaleX: 1, duration: .3, stagger: .35 }, t3 + .3);
    sai([t, m, orb, lista].concat(t2 ? [t2] : []), c);
  };

  // NÍVEIS: degraus 1, 2, 3 sobem e o mascote pula para o nível de destino.
  T.niveis = function (c) {
    var g = cena(c, true);
    grade(g, 1150);
    var t = titulo(g, c.titulo || "", 170, c.tam || 110);
    var n = c.niveis || 3, alvo = c.alvo || n, base = 1380, wd = Math.min(300, Math.floor(960 / n) - 20), x0 = Math.round((1080 - n * (wd + 20) + 20) / 2), passo = Math.round(600 / Math.max(1, n - 1));
    var degs = [];
    for (var i = 1; i <= n; i++) {
      var h = 190 + (i - 1) * passo;
      degs.push(el("div", "a degrau" + (i === alvo ? " alvo" : ""), "left:" + (x0 + (i - 1) * (wd + 20)) + "px;top:" + (base - h) + "px;width:" + wd + "px;height:" + h + "px", "<b>" + i + "</b>", g));
    }
    var m = el("div", "a", "left:" + (x0 + Math.round(wd / 2) - 55) + "px;top:" + (base - 190 - 110) + "px", mascote(110), g);
    entraTitulo(t, bat(c, 1, c.de));
    tl.fromTo(degs, { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: .45, stagger: Math.min(.4, (c.ate - c.de) / 8), ease: "back.out(1.3)" }, c.de + .2);
    tl.fromTo(m, { autoAlpha: 0, y: -80 }, { autoAlpha: 1, y: 0, duration: .3 }, c.de + .6);
    var t2 = bat(c, 0, c.de + 1.4), dx = (alvo - 1) * (wd + 20), dy = -passo * (alvo - 1);
    tl.to(m, { keyframes: [{ x: dx / 2, y: dy - 140, duration: .3, ease: "power2.out" }, { x: dx, y: dy, duration: .3, ease: "power2.in" }] }, t2);
    tl.to(degs[alvo - 1], { boxShadow: "0 0 90px rgba(var(--acento-rgb),.9)", duration: .3 }, t2 + .6);
    sai([t, m].concat(degs), c);
  };

  // PALAVRA: uma palavra ou frase curta grande na tela inteira, letra por letra.
  T.palavra = function (c) {
    var g = cena(c, true);
    var t = titulo(g, c.texto || "", c.y || 760, c.tam || 140);
    if (c.acento) t.classList.add("ac");
    entraTitulo(t, c.de);
    sai(t, c);
  };

  // ---------- montagem ----------
  (C.cenas || []).slice().sort(function (a, b) { return a.de - b.de; }).forEach(function (c) {
    if (!T[c.tipo]) throw new Error("tipo de cena desconhecido: " + c.tipo);
    if (!(c.ate > c.de)) throw new Error("cena " + c.tipo + " com ate <= de");
    T[c.tipo](c);
  });

  // câmera: zoom do corpo e, na abertura, o rosto na caixa de baixo
  var wrap = document.getElementById("camwrap"), cam = document.getElementById("cam");
  var z = R.camZoom || 1, oy = R.camOrigemY != null ? R.camOrigemY : 960;
  gsap.set(cam, { transformOrigin: "540px " + oy + "px", scale: z });
  var ab = window.__abertura;
  if (ab) {
    tl.set(wrap, { top: ab.camTop, height: 1920 - ab.camTop }, 0);
    tl.set(cam, { top: -(R.aberturaCamY != null ? R.aberturaCamY : 490), scale: 1.02, transformOrigin: "540px 960px" }, 0); // 2% de margem: a borda direita da câmera nunca aparece
    tl.set(wrap, { top: 0, height: 1920 }, ab.ate);
    tl.set(cam, { top: 0, scale: z, transformOrigin: "540px " + oy + "px" }, ab.ate);
  }

  // legenda: grupo inteiro aparece, a palavra falada ganha o acento
  var grupos = document.querySelectorAll("#cap .grp");
  grupos.forEach(function (gp) {
    var de = +gp.dataset.de, ate = +gp.dataset.ate;
    tl.set(gp, { autoAlpha: 1 }, de);
    tl.set(gp, { autoAlpha: 0 }, ate);
    var ws = gp.querySelectorAll("span");
    ws.forEach(function (w, i) {
      tl.set(w, { color: A }, +w.dataset.t);
      if (ws[i + 1]) tl.set(w, { color: "#ffffff" }, +ws[i + 1].dataset.t);
    });
  });

  // chamada final
  if (C.cta && C.cta.texto) {
    var k = document.getElementById("cta");
    k.innerHTML = marca(C.cta.texto);
    tl.fromTo(k, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: .25 }, C.cta.de);
  }

  tl.to({}, { duration: +document.getElementById("reel").dataset.duration }, 0);
  window.__timelines = window.__timelines || {};
  window.__timelines["reel"] = tl;
})();
