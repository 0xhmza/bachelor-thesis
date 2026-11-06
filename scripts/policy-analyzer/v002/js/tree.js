// Harm trees as SVG, in the notation of the thesis (after Knabenhans et al.,
// Fig. 4): the harm on top, the capabilities that lead to it below, and the
// components each capability needs at the leaves, joined by AND and OR.
// Component borders follow the paper's origin colours.
(function (root) {
  'use strict';
  var A = root.PA.analysis;
  var NS = 'http://www.w3.org/2000/svg';

  // Colours of 03_Thesis/config/preamble.tex (origincore, originctx, originimp,
  // originext, primary, muted, stateunsure, stateclosed).
  var THEMES = {
    paper: { bg: '#ffffff', grid: '#eef0f3', core: '#1A1A1A', context: '#496D91', implementation: '#A33B3B', external: '#535B63',
      harm: '#233F5B', harmText: '#ffffff', cap: '#f3f4f5', capLine: '#535B63', text: '#1A1A1A', muted: '#535B63',
      leaf: '#ffffff', edge: '#8a9097', unsure: '#F0C987', closed: '#e6e6e6', closedText: '#9aa0a6', gate: '#ffffff', accent: '#37665D', sel: '#2f6fd6' },
    dark: { bg: '#0f1318', grid: '#161b22', core: '#e6e9ee', context: '#7fa6cf', implementation: '#e07a7a', external: '#9aa3ad',
      harm: '#2e5279', harmText: '#ffffff', cap: '#1a2029', capLine: '#6e7787', text: '#e6e9ee', muted: '#9aa3ad',
      leaf: '#141920', edge: '#4a5361', unsure: '#6b5420', closed: '#1b1f25', closedText: '#5d6570', gate: '#0f1318', accent: '#5fb59e', sel: '#6ea8fe' }
  };

  var SIZE = { harm: [250, 46], cap: [214, 66], comp: [150, 50], gate: [40, 18] };
  var GAP_X = 18, GAP_Y = 44;

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { if (attrs[k] !== null && attrs[k] !== undefined) e.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(e);
    return e;
  }

  function wrap(text, maxChars, maxLines) {
    var words = String(text || '').split(/\s+/), lines = [], cur = '';
    words.forEach(function (w) {
      if ((cur + ' ' + w).trim().length > maxChars && cur) { lines.push(cur); cur = w; } else cur = (cur + ' ' + w).trim();
    });
    if (cur) lines.push(cur);
    if (lines.length > maxLines) { lines = lines.slice(0, maxLines); lines[maxLines - 1] = lines[maxLines - 1].replace(/.{0,2}$/, '') + '…'; }
    return lines;
  }

  // ---------- Tree structure ----------

  function exprNode(expr, path) {
    if (typeof expr === 'string') return { type: 'comp', id: expr, key: path + '/' + expr, children: [] };
    var op = Object.keys(expr)[0];
    return { type: 'gate', op: op, key: path + '/' + op, children: expr[op].map(function (c, i) { return exprNode(c, path + '/' + op + i); }) };
  }

  function harmTree(model, h, collapsed) {
    var harm = model.harms[h];
    var caps = harm.pathways.map(function (p) {
      var key = h + '/' + p.id;
      var node = { type: 'cap', id: p.capability, pathway: p, harm: h, key: key, children: [], hidden: 0 };
      var needs = model.capabilities[p.capability] && model.capabilities[p.capability].needs;
      if (needs) {
        var sub = exprNode(needs, key);
        if (collapsed[key]) node.hidden = A.leaves(needs).length; else node.children = [sub];
      }
      return node;
    });
    var root = { type: 'harm', id: h, label: harm.label, key: h, children: caps };
    if (caps.length > 1) root.children = [{ type: 'gate', op: 'or', key: h + '/or', children: caps }];
    return root;
  }

  // Tidy layout along the breadth axis (left to right in the paper's top-down
  // trees, top to bottom when the tree grows to the right): leaves in order,
  // parents centred on their children. b is the centre on that axis.
  function layout(node, depth, b0, lr) {
    var sz = SIZE[node.type];
    node.w = sz[0]; node.h = sz[1]; node.depth = depth;
    var size = lr ? node.h : node.w, gap = lr ? 10 : GAP_X;
    if (!node.children.length) { node.b = b0 + size / 2; node.span = size; return node.span; }
    var b = b0, total = 0;
    node.children.forEach(function (c, i) {
      var s = layout(c, depth + 1, b, lr);
      b += s + gap; total += s + (i ? gap : 0);
    });
    node.span = Math.max(total, size);
    var first = node.children[0], last = node.children[node.children.length - 1];
    node.b = (first.b + last.b) / 2;
    if (total < size) { var shift = (size - total) / 2; node.children.forEach(function (c) { shiftB(c, shift); }); node.b = b0 + size / 2; }
    return node.span;
  }
  function shiftB(n, d) { n.b += d; n.children.forEach(function (c) { shiftB(c, d); }); }

  function place(node, levels, lr) {
    if (lr) { node.left = levels[node.depth]; node.top = node.b - node.h / 2; }
    else { node.left = node.b - node.w / 2; node.top = levels[node.depth]; }
    node.x = node.left + node.w / 2; node.y = node.top;
    node.children.forEach(function (c) { place(c, levels, lr); });
  }

  function levelSizes(node, acc, lr) {
    acc[node.depth] = Math.max(acc[node.depth] || 0, lr ? node.w : node.h);
    node.children.forEach(function (c) { levelSizes(c, acc, lr); });
    return acc;
  }

  // ---------- Rendering ----------

  function stateOf(node, ctx) {
    if (!ctx.ev) return null;
    if (node.type === 'comp') return ctx.states[node.id];
    if (node.type === 'cap') return ctx.ev.pathways[node.pathway.id];
    if (node.type === 'harm') return ctx.ev.harms[node.id];
    return null;
  }

  function fills(node, st, T, base) {
    if (st === 'uncertain') return { fill: T.unsure, text: T.text, opacity: 1 };
    if (st === 'absent') return { fill: T.closed, text: T.closedText, opacity: 0.85 };
    return { fill: base, text: node.type === 'harm' ? T.harmText : T.text, opacity: 1 };
  }

  function drawNode(g, node, ctx) {
    var T = ctx.T, model = ctx.model, x = node.left, y = node.top;
    var st = stateOf(node, ctx);
    var grp = el('g', { class: 'tn tn-' + node.type, 'data-key': node.key, transform: 'translate(' + x + ',' + y + ')', tabindex: node.type === 'gate' ? null : 0 }, g);
    if (node.type === 'gate') {
      el('rect', { width: node.w, height: node.h, rx: 9, fill: T.gate, stroke: T.edge }, grp);
      var t = el('text', { x: node.w / 2, y: 12.5, 'text-anchor': 'middle', class: 'tg', fill: T.text }, grp);
      t.textContent = node.op.toUpperCase();
      return;
    }
    var selected = ctx.selected && ctx.selected === node.key;
    if (node.type === 'harm') {
      var f = fills(node, st, T, T.harm);
      el('rect', { width: node.w, height: node.h, rx: 4, fill: f.fill, stroke: selected ? T.sel : f.fill, 'stroke-width': selected ? 2.5 : 1 }, grp);
      var l1 = el('text', { x: node.w / 2, y: 19, 'text-anchor': 'middle', class: 'th', fill: f.text }, grp);
      l1.textContent = 'Harm: ' + node.label;
      var l2 = el('text', { x: node.w / 2, y: 35, 'text-anchor': 'middle', class: 'ts', fill: f.text, opacity: 0.8 }, grp);
      l2.textContent = node.id + (st ? ' · ' + st : '');
      return;
    }
    if (node.type === 'cap') {
      var cap = model.capabilities[node.id] || { label: '(missing capability)', actor: '' };
      var fc = fills(node, st, T, T.cap);
      el('rect', { width: node.w, height: node.h, rx: 4, fill: fc.fill, stroke: selected ? T.sel : T.capLine, 'stroke-width': selected ? 2.5 : 1, opacity: fc.opacity }, grp);
      var p = node.pathway;
      var head = el('text', { x: 8, y: 14, class: 'ts', fill: T.muted }, grp);
      head.textContent = wrap(p.id + ' · ' + p.consequence, 36, 1)[0];
      wrap(node.id + '  ' + cap.label, 33, 2).forEach(function (line, i) {
        var t = el('text', { x: 8, y: 31 + i * 13, class: i ? 'tl' : 'tb', fill: fc.text }, grp);
        t.textContent = line;
      });
      var act = el('text', { x: 8, y: node.h - 6, class: 'ts', fill: T.muted }, grp);
      act.textContent = wrap(cap.actor, 38, 1)[0];
      if (p.basis === 'argued') { var b = el('text', { x: node.w - 6, y: 14, 'text-anchor': 'end', class: 'ts', fill: T.muted }, grp); b.textContent = 'argued'; }
      if (ctx.levels && ctx.levels[p.id] !== undefined && st === 'present') {
        var lv = ctx.levels[p.id].level;
        el('rect', { x: node.w - 26, y: node.h - 17, width: 20, height: 13, rx: 3, fill: ['#c9ced6', '#bcd0f2', '#7da2e6', '#233F5B'][lv] }, grp);
        var lt = el('text', { x: node.w - 16, y: node.h - 7, 'text-anchor': 'middle', class: 'tg', fill: lv === 3 ? '#fff' : '#1A1A1A' }, grp);
        lt.textContent = 'L' + lv;
      }
      if (node.hidden) {
        var h2 = el('text', { x: node.w / 2, y: node.h + 14, 'text-anchor': 'middle', class: 'ts', fill: T.muted }, grp);
        h2.textContent = '+' + node.hidden + ' components';
      }
      if (ctx.edited && ctx.edited[p.id]) el('circle', { cx: node.w - 4, cy: 4, r: 4, fill: T.accent }, grp);
      return;
    }
    // Component
    var c = model.components[node.id] || { label: '(unknown component)', origin: 'external' };
    var color = T[c.origin] || T.external;
    var fl = fills(node, st, T, T.leaf);
    el('rect', { width: node.w, height: node.h, rx: 4, fill: fl.fill, stroke: selected ? T.sel : color, 'stroke-width': selected ? 2.6 : 1.6,
      'stroke-dasharray': c.origin === 'external' ? '5 3' : null, opacity: fl.opacity }, grp);
    var idt = el('text', { x: 8, y: 15, class: 'tb', fill: color }, grp);
    idt.textContent = node.id;
    if (st) { var stt = el('text', { x: node.w - 6, y: 15, 'text-anchor': 'end', class: 'ts', fill: fl.text }, grp); stt.textContent = st; }
    wrap(c.label, 26, 2).forEach(function (line, i) {
      var t = el('text', { x: 8, y: 29 + i * 12, class: 'tl', fill: fl.text }, grp);
      t.textContent = line;
    });
    if (ctx.edited && ctx.edited[node.id]) el('circle', { cx: node.w - 4, cy: node.h - 4, r: 3.5, fill: T.accent }, grp);
  }

  function drawEdges(g, node, ctx) {
    node.children.forEach(function (c) {
      var d;
      if (ctx.lr) {
        var ax = node.left + node.w, ay = node.top + node.h / 2, bx = c.left, by = c.top + c.h / 2, mx = (ax + bx) / 2;
        d = 'M' + ax + ',' + ay + ' C' + mx + ',' + ay + ' ' + mx + ',' + by + ' ' + bx + ',' + by;
      } else {
        var x1 = node.left + node.w / 2, y1 = node.top + node.h, x2 = c.left + c.w / 2, y2 = c.top, my = (y1 + y2) / 2;
        d = 'M' + x1 + ',' + y1 + ' C' + x1 + ',' + my + ' ' + x2 + ',' + my + ' ' + x2 + ',' + y2;
      }
      el('path', { d: d, fill: 'none', stroke: ctx.T.edge, 'stroke-width': 1.2 }, g);
      drawEdges(g, c, ctx);
    });
  }

  function drawAll(g, node, ctx) { drawNode(g, node, ctx); node.children.forEach(function (c) { drawAll(g, c, ctx); }); }

  function find(node, key) {
    if (node.key === key) return node;
    for (var i = 0; i < node.children.length; i++) { var f = find(node.children[i], key); if (f) return f; }
    return null;
  }

  // ---------- View with pan and zoom ----------

  function TreeView(host, opts) {
    this.host = host; this.opts = opts || {};
    this.collapsed = {}; this.zoom = 1; this.pan = { x: 0, y: 0 };
    this.svg = el('svg', { class: 'tree-svg', role: 'img' }, host);
    this.g = el('g', {}, this.svg);
    this.bind();
  }

  TreeView.prototype.render = function (ctx) {
    var self = this;
    this.ctx = ctx;
    var T = THEMES[ctx.theme || 'paper'];
    ctx.T = T;
    this.svg.style.background = T.bg;
    while (this.g.firstChild) this.g.removeChild(this.g.firstChild);
    var harms = ctx.harm === '*' ? Object.keys(ctx.model.harms) : [ctx.harm];
    var collapsed = this.collapsed;
    if (ctx.harm === '*') {
      collapsed = {};
      harms.forEach(function (h) { ctx.model.harms[h].pathways.forEach(function (p) { if (!self.collapsed['open:' + h + '/' + p.id]) collapsed[h + '/' + p.id] = 1; }); });
    }
    var lr = ctx.lr = ctx.orient === 'lr';
    var b = 0, roots = [], between = lr ? 40 : 70, gapDepth = lr ? 56 : GAP_Y;
    harms.forEach(function (h) {
      var r = harmTree(ctx.model, h, collapsed);
      layout(r, 0, b, lr);
      b += r.span + between;
      roots.push(r);
    });
    var sizes = {};
    roots.forEach(function (r) { levelSizes(r, sizes, lr); });
    var levels = {}, d0 = 0;
    Object.keys(sizes).map(Number).sort(function (a, c) { return a - c; }).forEach(function (d) { levels[d] = d0; d0 += sizes[d] + gapDepth; });
    roots.forEach(function (r) { place(r, levels, lr); });
    var breadth = Math.max(b - between, 10), depth = d0 - gapDepth + 20;
    this.bounds = lr ? { w: depth, h: breadth } : { w: breadth, h: depth };
    this.roots = roots;
    roots.forEach(function (r) { drawEdges(self.g, r, ctx); });
    roots.forEach(function (r) { drawAll(self.g, r, ctx); });
    if (!this.fitted || ctx.refit) { this.fit(); this.fitted = true; } else this.apply();
  };

  TreeView.prototype.apply = function () {
    this.g.setAttribute('transform', 'translate(' + this.pan.x + ',' + this.pan.y + ') scale(' + this.zoom + ')');
  };

  TreeView.prototype.fit = function () {
    var r = this.host.getBoundingClientRect();
    var w = r.width || 900, h = r.height || 600, pad = 32;
    var z = Math.min(1.25, Math.min((w - 2 * pad) / this.bounds.w, (h - 2 * pad) / this.bounds.h));
    var single = this.roots && this.roots.length === 1;
    if (single && z < 0.5) {
      // Too small to read: keep a readable zoom and centre the harm; drag to pan.
      z = 0.5;
      var root0 = this.roots[0];
      this.pan = this.ctx.lr ? { x: pad, y: h / 2 - (root0.top + root0.h / 2) * z } : { x: w / 2 - root0.x * z, y: pad };
    } else {
      z = Math.max(0.12, z);
      this.pan = { x: (w - this.bounds.w * z) / 2, y: this.ctx.lr ? (h - this.bounds.h * z) / 2 : pad };
    }
    this.zoom = z;
    this.apply();
  };

  TreeView.prototype.zoomBy = function (f, cx, cy) {
    var r = this.host.getBoundingClientRect();
    cx = cx === undefined ? r.width / 2 : cx; cy = cy === undefined ? r.height / 2 : cy;
    var z = Math.min(3, Math.max(0.1, this.zoom * f));
    this.pan.x = cx - (cx - this.pan.x) * (z / this.zoom);
    this.pan.y = cy - (cy - this.pan.y) * (z / this.zoom);
    this.zoom = z; this.apply();
  };

  TreeView.prototype.bind = function () {
    var self = this, drag = null;
    this.svg.addEventListener('wheel', function (e) {
      e.preventDefault();
      var r = self.svg.getBoundingClientRect();
      self.zoomBy(Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top);
    }, { passive: false });
    this.svg.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.tn')) return;
      drag = { x: e.clientX, y: e.clientY, px: self.pan.x, py: self.pan.y };
      self.svg.setPointerCapture(e.pointerId); self.svg.classList.add('grabbing');
    });
    this.svg.addEventListener('pointermove', function (e) {
      if (!drag) return;
      self.pan.x = drag.px + e.clientX - drag.x; self.pan.y = drag.py + e.clientY - drag.y; self.apply();
    });
    this.svg.addEventListener('pointerup', function () { drag = null; self.svg.classList.remove('grabbing'); });
    function pick(e) {
      var n = e.target.closest('.tn'); if (!n) return null;
      var key = n.getAttribute('data-key'), node = null;
      (self.roots || []).some(function (r) { node = find(r, key); return node; });
      return node;
    }
    this.svg.addEventListener('click', function (e) { var n = pick(e); if (n && self.opts.onSelect) self.opts.onSelect(n); });
    this.svg.addEventListener('dblclick', function (e) {
      var n = pick(e); if (!n || n.type !== 'cap') return;
      if (self.ctx.harm === '*') { var k = 'open:' + n.key; if (self.collapsed[k]) delete self.collapsed[k]; else self.collapsed[k] = 1; }
      else if (self.collapsed[n.key]) delete self.collapsed[n.key]; else self.collapsed[n.key] = 1;
      self.render(self.ctx);
    });
    this.svg.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { var n = pick(e); if (n && self.opts.onSelect) { e.preventDefault(); self.opts.onSelect(n); } }
    });
  };

  TreeView.prototype.collapseAll = function (on) {
    var self = this;
    this.collapsed = {};
    if (on && this.ctx.harm !== '*') this.ctx.model.harms[this.ctx.harm].pathways.forEach(function (p) { self.collapsed[self.ctx.harm + '/' + p.id] = 1; });
    this.render(Object.assign({}, this.ctx, { refit: true }));
  };

  // Standalone SVG of the current tree, for the thesis or a report.
  TreeView.prototype.exportSVG = function () {
    var clone = this.svg.cloneNode(true);
    var g = clone.querySelector('g');
    g.setAttribute('transform', 'translate(20,20)');
    clone.setAttribute('xmlns', NS);
    clone.setAttribute('width', Math.ceil(this.bounds.w + 40));
    clone.setAttribute('height', Math.ceil(this.bounds.h + 40));
    clone.setAttribute('viewBox', '0 0 ' + Math.ceil(this.bounds.w + 40) + ' ' + Math.ceil(this.bounds.h + 40));
    clone.removeAttribute('class');
    var style = el('style', {});
    style.textContent = 'text{font-family:"Segoe UI",Inter,Arial,sans-serif}.th{font-size:12px;font-weight:600}.tb{font-size:11px;font-weight:700}.tl{font-size:10.5px}.ts{font-size:9.5px}.tg{font-size:9px;font-weight:700;letter-spacing:.04em}';
    clone.insertBefore(style, clone.firstChild);
    var bg = el('rect', { width: '100%', height: '100%', fill: this.ctx.T.bg });
    clone.insertBefore(bg, style.nextSibling);
    return new XMLSerializer().serializeToString(clone);
  };

  TreeView.prototype.exportPNG = function (cb) {
    var svg = this.exportSVG(), img = new Image(), scale = 2, self = this;
    img.onload = function () {
      var c = document.createElement('canvas');
      c.width = (self.bounds.w + 40) * scale; c.height = (self.bounds.h + 40) * scale;
      var x = c.getContext('2d'); x.scale(scale, scale); x.drawImage(img, 0, 0);
      c.toBlob(cb, 'image/png');
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  };

  root.PA = root.PA || {};
  root.PA.tree = { TreeView: TreeView, THEMES: THEMES };
})(window);
