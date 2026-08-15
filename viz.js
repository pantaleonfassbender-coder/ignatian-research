/* viz.js — leichte Visualisierungen ohne externe Bibliothek */

export const TEILFARBE = {
  "0": "#8b95a5", "I": "#d3a24a", "II": "#8fb8c9", "III": "#b98a7a",
  "IV": "#6fbf9a", "V": "#9d8fc9", "VI": "#c98fae", "VII": "#7fa9d9",
  "VIII": "#d98b5f", "IX": "#a3b86c",
};
export function teilfarbe(t) { return TEILFARBE[t || "0"] || "#8b95a5"; }

function dpi(cv, w, h) {
  const r = window.devicePixelRatio || 1;
  cv.width = w * r; cv.height = h * r;
  cv.style.width = w + "px"; cv.style.height = h + "px";
  const c = cv.getContext("2d"); c.setTransform(r, 0, 0, r, 0, 0);
  return c;
}

/** Sparkline über 38 Kapitel */
export function sparkline(el, values, opts = {}) {
  const w = el.clientWidth || 320, h = opts.h || 34;
  const c = dpi(el, w, h);
  const max = Math.max(1, ...values);
  const bw = w / values.length;
  values.forEach((v, i) => {
    const bh = Math.max(v > 0 ? 1.5 : 0, (v / max) * (h - 4));
    c.fillStyle = opts.colors ? opts.colors[i] : (v > 0 ? "#c9a227" : "#332c22");
    c.globalAlpha = v > 0 ? 0.9 : 0.5;
    c.fillRect(i * bw + .5, h - bh, Math.max(1, bw - 1.2), bh);
  });
  c.globalAlpha = 1;
}

/** Horizontale Balken mit Label */
export function bars(el, rows, opts = {}) {
  const rowH = opts.rowH || 22, padL = opts.padL || 150;
  const w = el.clientWidth || 600, h = rows.length * rowH + 8;
  const c = dpi(el, w, h);
  const max = Math.max(1, ...rows.map(r => r.v));
  c.font = "12px -apple-system,Segoe UI,Roboto,sans-serif";
  c.textBaseline = "middle";
  rows.forEach((r, i) => {
    const y = i * rowH + rowH / 2 + 4;
    c.fillStyle = "#bcae99"; c.textAlign = "right";
    c.fillText(clip(c, r.label, padL - 10), padL - 8, y);
    const bw = (r.v / max) * (w - padL - 52);
    c.fillStyle = r.color || "#c9a227"; c.globalAlpha = .85;
    c.fillRect(padL, y - 7, Math.max(1.5, bw), 14);
    c.globalAlpha = 1;
    c.fillStyle = "#8a7d6a"; c.textAlign = "left";
    c.fillText(r.disp != null ? r.disp : r.v, padL + bw + 7, y);
  });
}
function clip(c, s, max) {
  if (c.measureText(s).width <= max) return s;
  while (s.length > 3 && c.measureText(s + "…").width > max) s = s.slice(0, -1);
  return s + "…";
}

/** Zeitreihe (z.B. Publikationsjahre der Referenzen) */
export function timeline(el, pairs, opts = {}) {
  const w = el.clientWidth || 700, h = opts.h || 180;
  const c = dpi(el, w, h);
  const from = opts.from ?? Math.min(...pairs.map(p => p[0]));
  const to = opts.to ?? Math.max(...pairs.map(p => p[0]));
  const max = Math.max(1, ...pairs.map(p => p[1]));
  const m = { l: 34, r: 8, t: 10, b: 24 };
  const iw = w - m.l - m.r, ih = h - m.t - m.b;
  c.strokeStyle = "#332c22"; c.lineWidth = 1;
  c.beginPath(); c.moveTo(m.l, m.t + ih + .5); c.lineTo(m.l + iw, m.t + ih + .5); c.stroke();
  const bw = Math.max(1.2, iw / (to - from + 1));
  for (const [y, v] of pairs) {
    if (y < from || y > to) continue;
    const x = m.l + ((y - from) / (to - from + 1)) * iw;
    const bh = (v / max) * ih;
    c.fillStyle = "#9db8a4"; c.globalAlpha = .85;
    c.fillRect(x, m.t + ih - bh, Math.max(1, bw - .6), bh);
  }
  c.globalAlpha = 1;
  c.fillStyle = "#8a7d6a"; c.font = "11px ui-monospace,monospace"; c.textAlign = "center";
  const step = (to - from) > 120 ? 40 : (to - from) > 60 ? 20 : 10;
  for (let y = Math.ceil(from / step) * step; y <= to; y += step) {
    const x = m.l + ((y - from) / (to - from + 1)) * iw;
    c.fillText(y, x, h - 8);
  }
  c.textAlign = "right"; c.fillText(max, m.l - 5, m.t + 6);
}

/** Streudiagramm Kapitel: x/y frei wählbar */
export function scatter(el, pts, opts = {}) {
  const w = el.clientWidth || 700, h = opts.h || 380;
  const c = dpi(el, w, h);
  const m = { l: 48, r: 14, t: 14, b: 40 };
  const iw = w - m.l - m.r, ih = h - m.t - m.b;
  const xs = pts.map(p => p.x), ys = pts.map(p => p.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  const X = v => m.l + ((v - x0) / (x1 - x0 || 1)) * iw;
  const Y = v => m.t + ih - ((v - y0) / (y1 - y0 || 1)) * ih;
  c.strokeStyle = "#2a241c";
  for (let i = 0; i <= 4; i++) {
    const y = m.t + (ih / 4) * i;
    c.beginPath(); c.moveTo(m.l, y + .5); c.lineTo(m.l + iw, y + .5); c.stroke();
  }
  c.font = "10.5px ui-monospace,monospace"; c.fillStyle = "#8a7d6a";
  c.textAlign = "right";
  for (let i = 0; i <= 4; i++) {
    const v = y1 - ((y1 - y0) / 4) * i;
    c.fillText(v.toFixed(opts.yDec ?? 0), m.l - 6, m.t + (ih / 4) * i + 3.5);
  }
  c.textAlign = "center";
  for (let i = 0; i <= 4; i++) {
    const v = x0 + ((x1 - x0) / 4) * i;
    c.fillText(v.toFixed(opts.xDec ?? 0), m.l + (iw / 4) * i, h - 22);
  }
  c.fillStyle = "#bcae99"; c.font = "11px sans-serif";
  c.fillText(opts.xLabel || "", m.l + iw / 2, h - 6);
  c.save(); c.translate(12, m.t + ih / 2); c.rotate(-Math.PI / 2);
  c.fillText(opts.yLabel || "", 0, 0); c.restore();
  const hit = [];
  for (const p of pts) {
    const x = X(p.x), y = Y(p.y), r = p.r || 5;
    c.beginPath(); c.arc(x, y, r, 0, 7);
    c.fillStyle = p.color || "#c9a227"; c.globalAlpha = .82; c.fill();
    c.globalAlpha = 1; c.strokeStyle = "rgba(0,0,0,.4)"; c.stroke();
    hit.push({ x, y, r: r + 4, d: p });
  }
  return hit;
}

/* ------------------------------------------------ Kraftgerichtetes Netz */
export function network(cv, data, opts = {}) {
  const PAL = opts.palette || null;
  const col = t => (PAL ? (PAL[t] || "#8a7d6a") : teilfarbe(t));
  const w = cv.clientWidth || 900, h = opts.h || 560;
  const c = dpi(cv, w, h);
  const nodes = data.nodes.map(n => ({
    ...n, x: w / 2 + (Math.random() - .5) * w * .6, y: h / 2 + (Math.random() - .5) * h * .6,
    vx: 0, vy: 0,
  }));
  const byId = new Map(nodes.map(n => [n.id, n]));
  const edges = data.edges.filter(e => byId.has(e.s) && byId.has(e.t))
    .map(e => ({ ...e, a: byId.get(e.s), b: byId.get(e.t) }));
  const deg = new Map();
  for (const e of edges) { deg.set(e.s, (deg.get(e.s) || 0) + 1); deg.set(e.t, (deg.get(e.t) || 0) + 1); }
  const maxF = Math.max(...nodes.map(n => n.f));
  for (const n of nodes) {
    n.r = 3.2 + 9 * Math.sqrt(n.f / maxF);
    n.deg = deg.get(n.id) || 0;
  }
  const maxE = Math.max(...edges.map(e => e.f));

  let alpha = 1, hover = null, sel = opts.selected || null, run = true;
  const state = { transform: { k: 1, x: 0, y: 0 } };

  // Fruchterman–Reingold mit Abkühlung
  const K = 0.74 * Math.sqrt((w * h) / Math.max(1, nodes.length));
  let temp = Math.min(w, h) / 7;

  function step() {
    for (const n of nodes) { n.dx = 0; n.dy = 0; }
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        let dx = a.x - b.x, dy = a.y - b.y;
        let d = Math.hypot(dx, dy);
        if (d < 0.6) { dx = Math.random() - .5; dy = Math.random() - .5; d = 0.6; }
        const rep = (K * K) / d * (1 + (a.r + b.r) / 26);
        a.dx += (dx / d) * rep; a.dy += (dy / d) * rep;
        b.dx -= (dx / d) * rep; b.dy -= (dy / d) * rep;
      }
    }
    for (const e of edges) {
      let dx = e.a.x - e.b.x, dy = e.a.y - e.b.y;
      const d = Math.hypot(dx, dy) || 0.6;
      const att = (d * d) / K * (0.35 + 0.9 * (e.f / maxE));
      e.a.dx -= (dx / d) * att; e.a.dy -= (dy / d) * att;
      e.b.dx += (dx / d) * att; e.b.dy += (dy / d) * att;
    }
    for (const n of nodes) {
      // schwache Zentrierung, damit nichts wegdriftet
      n.dx += (w / 2 - n.x) * 0.012 * K * 0.03;
      n.dy += (h / 2 - n.y) * 0.012 * K * 0.03;
      const d = Math.hypot(n.dx, n.dy) || 1;
      const lim = Math.min(d, temp);
      n.x += (n.dx / d) * lim;
      n.y += (n.dy / d) * lim;
      n.x = Math.max(n.r + 10, Math.min(w - n.r - 10, n.x));
      n.y = Math.max(n.r + 16, Math.min(h - n.r - 10, n.y));
    }
    temp *= 0.975;
    alpha *= 0.982;
  }

  function draw() {
    c.clearRect(0, 0, w, h);
    const t = state.transform;
    c.save(); c.translate(t.x, t.y); c.scale(t.k, t.k);
    const focus = hover || sel;
    const near = focus ? new Set(edges.filter(e => e.s === focus || e.t === focus)
      .flatMap(e => [e.s, e.t])) : null;
    for (const e of edges) {
      const on = focus && (e.s === focus || e.t === focus);
      c.globalAlpha = focus ? (on ? .8 : .04) : Math.min(.5, .14 + (e.f / maxE) * .8);
      c.strokeStyle = on ? "#c9a227" : "#5d5241";
      c.lineWidth = on ? 1.5 : Math.max(.5, (e.f / maxE) * 2.4);
      c.beginPath(); c.moveTo(e.a.x, e.a.y); c.lineTo(e.b.x, e.b.y); c.stroke();
    }
    c.globalAlpha = 1;
    for (const n of nodes) {
      const dim = focus && !near.has(n.id) && n.id !== focus;
      c.globalAlpha = dim ? .16 : 1;
      c.beginPath(); c.arc(n.x, n.y, n.r, 0, 7);
      c.fillStyle = col(n.teil); c.fill();
      if (n.id === focus) { c.strokeStyle = "#fff"; c.lineWidth = 1.6; c.stroke(); }
    }
    c.font = "11.5px -apple-system,Segoe UI,Roboto,sans-serif";
    c.textAlign = "center"; c.textBaseline = "bottom";
    const labelled = focus
      ? nodes.filter(n => near.has(n.id) || n.id === focus).sort((a, b) => b.f - a.f)
      : nodes.slice().sort((a, b) => b.f - a.f);
    const placed = [];
    let shown = 0;
    const cap = focus ? 40 : (opts.labelCap || 40);
    for (const n of labelled) {
      if (shown >= cap) break;
      const tw = c.measureText(n.id).width;
      const box = { x0: n.x - tw / 2 - 3, x1: n.x + tw / 2 + 3, y0: n.y - n.r - 15, y1: n.y - n.r - 1 };
      if (placed.some(p => !(box.x1 < p.x0 || box.x0 > p.x1 || box.y1 < p.y0 || box.y0 > p.y1))) continue;
      placed.push(box); shown++;
      c.globalAlpha = 1;
      c.fillStyle = "rgba(16,14,12,.80)";
      c.fillRect(box.x0, box.y0, box.x1 - box.x0, box.y1 - box.y0);
      c.fillStyle = n.id === focus ? "#fff" : "#ded3c2";
      c.fillText(n.id, n.x, n.y - n.r - 3);
    }
    c.globalAlpha = 1; c.restore();
  }

  function loop() { if (!run) return; if (alpha > 0.012) step(); draw(); requestAnimationFrame(loop); }
  loop();

  function pick(ev) {
    const rect = cv.getBoundingClientRect();
    const t = state.transform;
    const mx = (ev.clientX - rect.left - t.x) / t.k, my = (ev.clientY - rect.top - t.y) / t.k;
    let best = null, bd = 1e9;
    for (const n of nodes) {
      const d = (n.x - mx) ** 2 + (n.y - my) ** 2;
      if (d < bd && d < (n.r + 7) ** 2) { bd = d; best = n; }
    }
    return best;
  }
  cv.onmousemove = ev => { const n = pick(ev); const id = n ? n.id : null; if (id !== hover) { hover = id; cv.style.cursor = id ? "pointer" : "default"; if (alpha <= .012) draw(); } };
  cv.onmouseleave = () => { hover = null; if (alpha <= .012) draw(); };
  cv.onclick = ev => { const n = pick(ev); sel = n ? (sel === n.id ? null : n.id) : null; if (opts.onSelect) opts.onSelect(sel, n); if (alpha <= .012) draw(); };
  cv.onwheel = ev => {
    ev.preventDefault();
    const rect = cv.getBoundingClientRect();
    const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
    const t = state.transform, f = ev.deltaY < 0 ? 1.12 : 1 / 1.12;
    const k = Math.max(.4, Math.min(4, t.k * f));
    t.x = mx - (mx - t.x) * (k / t.k); t.y = my - (my - t.y) * (k / t.k); t.k = k;
    if (alpha <= .012) draw();
  };
  let drag = null;
  cv.onmousedown = ev => { drag = { x: ev.clientX, y: ev.clientY, tx: state.transform.x, ty: state.transform.y }; };
  window.addEventListener("mouseup", () => drag = null);
  window.addEventListener("mousemove", ev => {
    if (!drag) return;
    state.transform.x = drag.tx + ev.clientX - drag.x;
    state.transform.y = drag.ty + ev.clientY - drag.y;
    if (alpha <= .012) draw();
  });

  return {
    select(id) { sel = id; if (alpha <= .012) draw(); },
    stop() { run = false; },
    reheat() { alpha = 1; temp = Math.min(w, h) / 9; },
  };
}
