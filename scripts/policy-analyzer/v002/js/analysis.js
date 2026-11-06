// Analysis core of the policy analyzer: coding units, label checks, the
// combination of model labels, the harm trees and the agreement statistics.
// Pure functions only, so that tests/analysis.test.js can run them in Node.
// The rules follow the methodology chapter (Sections "Coding and Assessment"
// and "Instrument Freeze and Validation") and reference model v2.
(function (root) {
  'use strict';

  var PRESENT = 'present', ABSENT = 'absent', UNCERTAIN = 'uncertain';

  // Routine labels are kept when every model returns them; high-stakes labels
  // are the union of all models and go to a person (Table "How the labels of
  // the two models are combined").
  var ROUTINE = { 'L-CMP': 1, 'L-CAP': 1, 'P-BRC': 1, 'P-INC': 1, 'P-NOT': 1,
    'T-3RD': 1, 'T-INF': 1, 'T-DEV': 1, 'T-ENC': 1, 'T-ANO': 1, 'T-SEC': 1, 'T-OTH': 1, 'N-COM': 1 };
  var HIGH_STAKES = { 'L-HRM': 1, 'L-GEN': 1, 'S-GRS': 1, 'C-REA': 1,
    'S-ACK': 1, 'S-QUA': 1, 'S-MIN': 1, 'S-RSP': 1, 'S-DEN': 1 };
  var PEOPLE_ONLY = { 'S-MIN': 1 };

  // Label families for the agreement statistics.
  var FAMILIES = [
    { id: 'components', name: 'Components (L-CMP)', match: function (l) { return l.code === 'L-CMP'; } },
    { id: 'capabilities', name: 'Capabilities (L-CAP)', match: function (l) { return l.code === 'L-CAP'; } },
    { id: 'harms', name: 'Named harms (L-HRM)', match: function (l) { return l.code === 'L-HRM'; } },
    { id: 'generic', name: 'Generic risk and responsibility (L-GEN, S-GRS)', match: function (l) { return l.code === 'L-GEN' || l.code === 'S-GRS'; } },
    { id: 'incident', name: 'Incident details (P-BRC, P-INC, P-NOT)', match: function (l) { return /^P-/.test(l.code); } },
    { id: 'stance', name: 'Stance (Stage 2)', match: function (l) { return l.stage === 2; } },
    { id: 'protection', name: 'Protection claims (Stage 3)', match: function (l) { return l.stage === 3; } }
  ];

  // ---------- Coding units ----------

  function normalise(s) {
    return String(s || '').replace(/ /g, ' ').replace(/[​-‍﻿]/g, '')
      .replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
      .replace(/\s+/g, ' ').trim();
  }

  function htmlToText(html) {
    // Block elements end a paragraph; tags are dropped; entities are decoded.
    var s = String(html).replace(/<(script|style|noscript)[\s\S]*?<\/\1>/gi, ' ')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/(p|div|li|h[1-6]|tr|section|article|header|footer|ul|ol|table|blockquote)>/gi, '\n\n')
      .replace(/<li[^>]*>/gi, '\n- ')
      .replace(/<[^>]+>/g, ' ');
    var entities = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };
    s = s.replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, function (m, e) {
      if (e[0] === '#') {
        var n = e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        return isNaN(n) ? m : String.fromCodePoint(n);
      }
      return entities.hasOwnProperty(e.toLowerCase()) ? entities[e.toLowerCase()] : m;
    });
    return s.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n');
  }

  function isHeading(block) {
    var t = block.trim();
    return t.length <= 80 && !/[.:;!?]$/.test(t) && t.split(/\s+/).length <= 10 && !/^- /.test(t);
  }

  // A unit is one paragraph of the policy or one block of interface text
  // (Section "Coding Units and Axes"). A short line without end punctuation is
  // taken as the heading of the units that follow it.
  function unitize(text, surface, prefix) {
    var blocks = String(text || '').replace(/\r\n?/g, '\n').split(/\n\s*\n/);
    var units = [], heading = '', n = 0;
    prefix = prefix || (surface === 'interface' ? 'I' : 'P');
    blocks.forEach(function (b) {
      var t = normalise(b);
      if (!t) return;
      // Interface blocks are units even when short (button and toggle labels).
      if (surface === 'policy' && isHeading(b)) { heading = t; return; }
      n += 1;
      units.push({ id: prefix + String(n).padStart(3, '0'), surface: surface, heading: heading, text: t });
    });
    return units;
  }

  function chunk(list, size) {
    var out = [];
    for (var i = 0; i < list.length; i += size) out.push(list.slice(i, i + size));
    return out;
  }

  // ---------- Model output ----------

  function parseJSON(raw) {
    if (raw && typeof raw === 'object') return raw;
    var s = String(raw || '').trim();
    var fence = s.match(/```(?:json)?\s*([\s\S]*?)```/i);
    if (fence) s = fence[1].trim();
    try { return JSON.parse(s); } catch (e) { /* fall through */ }
    var a = s.indexOf('{'), b = s.lastIndexOf('}');
    if (a >= 0 && b > a) return JSON.parse(s.slice(a, b + 1));
    throw new Error('no JSON object in the model output');
  }

  // Every label must quote a span of its unit; a label whose span is not in
  // the unit is dropped and counted as a model failure (Section "LLM Coding").
  function spanOk(span, unitText) {
    var s = normalise(span).toLowerCase();
    return s.length > 0 && normalise(unitText).toLowerCase().indexOf(s) >= 0;
  }

  function labelKey(l) {
    if (l.stage === 1) return l.unit + '|' + l.code + (l.node || l.harm ? '|' + (l.node || l.harm) : '');
    if (l.stage === 2) return l.unit + '|' + l.harm + '|' + l.code;
    return l.unit + '|' + l.code;
  }

  function valueKey(l) {
    // The coded value without the unit, for per-code tables.
    return labelKey(l).split('|').slice(1).join('|');
  }

  function readStage1(obj, unitsById, model, run) {
    var labels = [], failures = [], flags = {};
    (obj.units || []).forEach(function (u) {
      var unit = unitsById[u.unit];
      if (!unit) { failures.push({ model: model, stage: 1, unit: u.unit, reason: 'unknown unit id' }); return; }
      flags[u.unit] = { harm: !!(u.flags && u.flags.harm), protection: !!(u.flags && u.flags.protection) };
      (u.codes || []).forEach(function (c) {
        var l = { model: model, run: run || 1, stage: 1, unit: u.unit, surface: unit.surface, code: c.code,
          node: c.node || null, harm: c.harm || null, status: c.status || 'asserted', tag: c.tag || null,
          span: c.span || '', reason: c.reason || '', unsure: !!c.unsure };
        if (!l.code) { failures.push({ model: model, stage: 1, unit: u.unit, reason: 'label without a code' }); return; }
        if (!spanOk(l.span, unit.text)) { failures.push({ model: model, stage: 1, unit: u.unit, code: l.code, reason: 'span not found in the unit', span: l.span }); return; }
        if (l.code === 'L-HRM') flags[u.unit].harm = true;
        labels.push(l);
      });
    });
    return { labels: labels, failures: failures, flags: flags };
  }

  function readStage2(obj, unitsById, model, run) {
    var labels = [], failures = [], rejected = [];
    (obj.harms || []).forEach(function (h) {
      var unit = unitsById[h.unit];
      if (!unit) { failures.push({ model: model, stage: 2, unit: h.unit, reason: 'unknown unit id' }); return; }
      if (h.reject) rejected.push({ model: model, unit: h.unit, harm: h.harm });
      (h.stances || []).forEach(function (s) {
        var l = { model: model, run: run || 1, stage: 2, unit: h.unit, surface: unit.surface, harm: h.harm,
          code: s.code, target: s.target || null, span: s.span || '', reason: s.reason || '', unsure: !!s.unsure };
        if (!spanOk(l.span, unit.text)) { failures.push({ model: model, stage: 2, unit: h.unit, code: l.code, reason: 'span not found in the unit', span: l.span }); return; }
        labels.push(l);
      });
    });
    return { labels: labels, failures: failures, rejected: rejected };
  }

  function readStage3(obj, unitsById, model, run) {
    var labels = [], failures = [];
    (obj.claims || []).forEach(function (c) {
      var unit = unitsById[c.unit];
      if (!unit) { failures.push({ model: model, stage: 3, unit: c.unit, reason: 'unknown unit id' }); return; }
      (c.claims || []).forEach(function (m) {
        var l = { model: model, run: run || 1, stage: 3, unit: c.unit, surface: unit.surface, code: m.code,
          actor: m.actor || null, data: m.data || null, outcome: m.outcome || null, conditions: m.conditions || null,
          framing: m.framing || null, strength: m.strength || null,
          span: m.span || '', reason: m.reason || '', unsure: !!m.unsure };
        if (!spanOk(l.span, unit.text)) { failures.push({ model: model, stage: 3, unit: c.unit, code: l.code, reason: 'span not found in the unit', span: l.span }); return; }
        labels.push(l);
      });
    });
    return { labels: labels, failures: failures };
  }

  // ---------- Combining the models ----------

  // One combined record per label key. Routine: "agreed" when every model
  // returned it and none marked it unsure, otherwise "uncertain". High-stakes:
  // the union, "to check" by a person. Minimisation is only a proposal.
  function combine(labels, models) {
    var byKey = {};
    labels.forEach(function (l) {
      var k = labelKey(l);
      if (!byKey[k]) byKey[k] = { key: k, unit: l.unit, surface: l.surface, stage: l.stage, code: l.code,
        node: l.node || null, harm: l.harm || null, by: {}, statuses: {}, unsure: false, examples: [] };
      var r = byKey[k];
      if (!r.by[l.model]) r.by[l.model] = l;
      if (l.status) r.statuses[l.model] = l.status;
      if (l.unsure) r.unsure = true;
    });
    return Object.keys(byKey).map(function (k) {
      var r = byKey[k], n = Object.keys(r.by).length;
      r.count = n;
      var first = r.by[Object.keys(r.by)[0]];
      r.span = first.span;
      if (PEOPLE_ONLY[r.code]) r.decision = 'proposal';
      else if (HIGH_STAKES[r.code] || r.stage === 2) r.decision = 'check';
      else r.decision = (n === models.length && !r.unsure) ? 'agreed' : 'uncertain';
      var sts = Object.keys(r.statuses).map(function (m) { return r.statuses[m]; });
      r.status = sts.length && sts.every(function (s) { return s === sts[0]; }) ? sts[0] : (sts.length ? 'mixed' : null);
      if (r.stage === 3) {
        r.framing = majority(Object.keys(r.by).map(function (m) { return r.by[m].framing; }));
        r.strength = majority(Object.keys(r.by).map(function (m) { return r.by[m].strength; }));
      }
      return r;
    }).sort(function (a, b) { return a.key < b.key ? -1 : 1; });
  }

  function majority(values) {
    var c = {};
    values.filter(Boolean).forEach(function (v) { c[v] = (c[v] || 0) + 1; });
    var keys = Object.keys(c);
    if (!keys.length) return null;
    keys.sort(function (a, b) { return c[b] - c[a]; });
    return keys.length > 1 && c[keys[0]] === c[keys[1]] ? 'mixed' : keys[0];
  }

  // ---------- Harm trees (three-valued, as scripts/instrument-test/v002/evaluate.py) ----------

  function evaluate(expr, states) {
    if (typeof expr === 'string') return states[expr] || UNCERTAIN;
    var op = Object.keys(expr)[0], children = expr[op];
    if (op === 'orplus') throw new Error('OR+ must be rewritten as an OR of sufficient AND-combinations');
    var v = children.map(function (c) { return evaluate(c, states); });
    if (op === 'and') {
      if (v.indexOf(ABSENT) >= 0) return ABSENT;
      return v.every(function (x) { return x === PRESENT; }) ? PRESENT : UNCERTAIN;
    }
    if (op === 'or') {
      if (v.indexOf(PRESENT) >= 0) return PRESENT;
      return v.every(function (x) { return x === ABSENT; }) ? ABSENT : UNCERTAIN;
    }
    throw new Error('unknown operator ' + op);
  }

  function leaves(expr) {
    if (typeof expr === 'string') return [expr];
    var op = Object.keys(expr)[0];
    return expr[op].reduce(function (acc, c) { return acc.concat(leaves(c)); }, [])
      .filter(function (x, i, a) { return a.indexOf(x) === i; });
  }

  function pathways(model) {
    var out = [];
    Object.keys(model.harms).forEach(function (h) {
      model.harms[h].pathways.forEach(function (p) {
        out.push({ id: p.id, harm: h, harmLabel: model.harms[h].label, capability: p.capability,
          consequence: p.consequence, basis: p.basis, sources: p.sources, tag: p.tag || null,
          components: leaves(model.capabilities[p.capability].needs) });
      });
    });
    return out;
  }

  function evaluateModel(model, states) {
    var caps = {};
    Object.keys(model.capabilities).forEach(function (k) { caps[k] = evaluate(model.capabilities[k].needs, states); });
    var paths = {};
    pathways(model).forEach(function (p) { paths[p.id] = caps[p.capability]; });
    var harms = {};
    Object.keys(model.harms).forEach(function (h) {
      var v = model.harms[h].pathways.map(function (p) { return paths[p.id]; });
      harms[h] = v.every(function (x) { return x === ABSENT; }) ? ABSENT : (v.indexOf(PRESENT) >= 0 ? PRESENT : UNCERTAIN);
    });
    return { capabilities: caps, pathways: paths, harms: harms };
  }

  // A pathway rests on an assumption when it needs an external event (EX1-EX3).
  function assumptionDependent(model, p) {
    return p.components.some(function (c) { return model.components[c].origin === 'external'; });
  }

  // ---------- Step 1: applicability proposal ----------

  // Evidence from the coded text only; people confirm or change every state.
  // Stored data are assumed accessible to an attacker; authority and insurer
  // use stay uncertain; a non-finding leaves a component uncertain.
  function proposeApplicability(model, combined, opts) {
    opts = opts || {};
    var countPossible = opts.countPossible !== false, includeUncertain = !!opts.includeUncertain;
    var out = {};
    Object.keys(model.components).forEach(function (id) {
      out[id] = { state: UNCERTAIN, basis: 'not mentioned in the coded text', evidence: [] };
    });
    combined.filter(function (r) { return r.code === 'L-CMP' && r.node && out[r.node]; }).forEach(function (r) {
      out[r.node].evidence.push(r);
    });
    Object.keys(out).forEach(function (id) {
      var rec = out[id], ev = rec.evidence;
      var usable = ev.filter(function (r) { return r.decision === 'agreed' || includeUncertain; });
      var pos = usable.filter(function (r) { return r.status === 'asserted' || (countPossible && r.status === 'possible'); });
      var neg = usable.filter(function (r) { return r.status === 'denied'; });
      if (pos.length && !neg.length) { rec.state = PRESENT; rec.basis = 'stated in the text (' + pos.map(function (r) { return r.unit; }).join(', ') + ')'; }
      else if (neg.length && !pos.length) { rec.state = ABSENT; rec.basis = 'denied in the text (' + neg.map(function (r) { return r.unit; }).join(', ') + ')'; }
      else if (pos.length && neg.length) { rec.basis = 'stated and denied in different units'; }
      else if (ev.length) { rec.basis = 'mentioned by one model only, unsure, hedged or mixed: check'; }
    });
    // Rules of Step 1 that do not come from the text.
    out.CO1 = { state: PRESENT, basis: 'assumed: every sampled app records health data (eligibility E1)', evidence: out.CO1.evidence };
    out.EX1 = { state: PRESENT, basis: 'assumed: stored data are accessible to a potential attacker', evidence: out.EX1.evidence };
    ['EX2', 'EX3'].forEach(function (id) {
      if (out[id].state !== PRESENT) out[id] = { state: UNCERTAIN, basis: 'uncertain unless supported by evidence', evidence: out[id].evidence };
    });
    return out;
  }

  // ---------- Step 2: coverage levels ----------

  // Level of one pathway on one surface: 0 silent, 1 a component of its
  // capability mentioned (any polarity), 2 the capability mentioned, 3 a
  // harm of its category named. A harm mention lifts a pathway to level 3
  // only if the text also reaches the pathway itself (level 1 or 2);
  // otherwise it stays a category-level mention. Level 3 is a candidate until
  // a person checks that consequence, data, actor and access match.
  function coverage(model, combined, surface, mode) {
    var use = combined.filter(function (r) {
      if (r.surface !== surface || r.stage !== 1) return false;
      if (r.decision === 'uncertain') return mode === 'with-uncertain';
      return true;
    });
    var cmp = {}, cap = {}, hrm = {};
    use.forEach(function (r) {
      if (r.code === 'L-CMP' && r.node) (cmp[r.node] = cmp[r.node] || []).push(r);
      if (r.code === 'L-CAP' && r.node) (cap[r.node] = cap[r.node] || []).push(r);
      if (r.code === 'L-HRM' && r.harm) (hrm[r.harm] = hrm[r.harm] || []).push(r);
    });
    var out = {};
    pathways(model).forEach(function (p) {
      var level = 0, ev = [];
      var c1 = [];
      p.components.forEach(function (c) { if (cmp[c]) c1 = c1.concat(cmp[c]); });
      if (c1.length) { level = 1; ev = c1; }
      if (cap[p.capability]) { level = 2; ev = cap[p.capability]; }
      var categoryOnly = false;
      if (hrm[p.harm] && level >= 1) { level = 3; ev = hrm[p.harm].concat(ev); }
      else if (hrm[p.harm]) categoryOnly = true;
      var lower = ev.filter(function (r) { return r.code !== 'L-HRM'; });
      out[p.id] = { level: level, categoryOnly: categoryOnly, evidence: ev.map(function (r) { return r.unit; })
        .filter(function (x, i, a) { return a.indexOf(x) === i; }),
        denied: lower.length > 0 && lower.every(function (r) { return r.status === 'denied'; }) };
    });
    return out;
  }

  // RQ1 shares: per app, the share of applicable pathways at each level.
  // Scenario A: applicable pathways; scenario B: applicable and uncertain.
  function levelShares(pathStates, cov, scenario) {
    var ids = Object.keys(pathStates).filter(function (id) {
      return pathStates[id] === PRESENT || (scenario === 'B' && pathStates[id] === UNCERTAIN);
    });
    var counts = [0, 0, 0, 0];
    ids.forEach(function (id) { counts[cov[id].level] += 1; });
    return { n: ids.length, counts: counts, shares: counts.map(function (c) { return ids.length ? c / ids.length : null; }) };
  }

  // ---------- Step 3: protection ----------

  // Pathways that stay open if a measure removed the chosen components.
  function afterMeasure(model, states, removed) {
    var changed = {};
    Object.keys(states).forEach(function (k) { changed[k] = states[k]; });
    removed.forEach(function (c) { changed[c] = ABSENT; });
    return evaluateModel(model, changed).pathways;
  }

  // ---------- Agreement between models ----------

  // Binary indicators per (unit, value) for every value that any model used in
  // this family, over all coded units of the stages concerned.
  function indicatorTable(labels, models, family, units) {
    var fam = labels.filter(family.match);
    var values = {};
    fam.forEach(function (l) { values[valueKey(l)] = 1; });
    var has = {};
    fam.forEach(function (l) { has[l.model + '#' + labelKey(l)] = 1; });
    var rows = [];
    units.forEach(function (u) {
      Object.keys(values).forEach(function (v) {
        rows.push(models.map(function (m) { return has[m + '#' + u + '|' + v] ? 1 : 0; }));
      });
    });
    return { rows: rows, values: Object.keys(values).sort() };
  }

  // Krippendorff's alpha for nominal data, any number of coders, no missing values.
  function krippendorffAlpha(rows) {
    var o = {}, nTotal = 0;
    rows.forEach(function (r) {
      var m = r.length;
      if (m < 2) return;
      var c = {};
      r.forEach(function (v) { c[v] = (c[v] || 0) + 1; });
      Object.keys(c).forEach(function (a) {
        Object.keys(c).forEach(function (b) {
          var pairs = a === b ? c[a] * (c[a] - 1) : c[a] * c[b];
          o[a + '|' + b] = (o[a + '|' + b] || 0) + pairs / (m - 1);
        });
      });
      nTotal += m;
    });
    var nc = {};
    Object.keys(o).forEach(function (k) { var a = k.split('|')[0]; nc[a] = (nc[a] || 0) + o[k]; });
    var n = Object.keys(nc).reduce(function (s, k) { return s + nc[k]; }, 0);
    if (n <= 1) return null;
    var Do = 0, De = 0;
    Object.keys(o).forEach(function (k) { var p = k.split('|'); if (p[0] !== p[1]) Do += o[k]; });
    Object.keys(nc).forEach(function (a) { Object.keys(nc).forEach(function (b) { if (a !== b) De += nc[a] * nc[b]; }); });
    Do = Do / n; De = De / (n * (n - 1));
    if (De === 0) return null; // no variation: alpha is undefined
    return 1 - Do / De;
  }

  function pairStats(rows, i, j) {
    var a = 0, b = 0, c = 0, d = 0;
    rows.forEach(function (r) {
      if (r[i] && r[j]) a++; else if (r[i]) b++; else if (r[j]) c++; else d++;
    });
    var n = a + b + c + d;
    var po = n ? (a + d) / n : null;
    var pe = n ? ((a + b) * (a + c) + (c + d) * (b + d)) / (n * n) : null;
    var kappa = n && pe !== 1 ? (po - pe) / (1 - pe) : null;
    var dice = (2 * a + b + c) ? 2 * a / (2 * a + b + c) : null;
    var alpha = krippendorffAlpha(rows.map(function (r) { return [r[i], r[j]]; }));
    return { both: a, onlyA: b, onlyB: c, neither: d, n: n, agreement: po, kappa: kappa,
      pabak: po === null ? null : 2 * po - 1, positiveAgreement: dice, alpha: alpha,
      prevalence: n ? (2 * a + b + c) / (2 * n) : null };
  }

  function tokenJaccard(x, y) {
    var A = normalise(x).toLowerCase().split(' '), B = normalise(y).toLowerCase().split(' ');
    var sa = {}, sb = {}, inter = 0;
    A.forEach(function (t) { sa[t] = 1; }); B.forEach(function (t) { sb[t] = 1; });
    Object.keys(sa).forEach(function (t) { if (sb[t]) inter++; });
    var uni = Object.keys(sa).length + Object.keys(sb).length - inter;
    return uni ? inter / uni : 1;
  }

  // Deviation between models: per family, pairwise and across all models; on
  // labels both models found, agreement on status, span and attributes.
  function agreement(labels, models, units) {
    var unitIds = units.map(function (u) { return u.id; });
    var families = FAMILIES.map(function (f) {
      var t = indicatorTable(labels, models, f, unitIds);
      var pairs = [];
      for (var i = 0; i < models.length; i++) for (var j = i + 1; j < models.length; j++) {
        var s = pairStats(t.rows, i, j); s.a = models[i]; s.b = models[j]; pairs.push(s);
      }
      return { id: f.id, name: f.name, values: t.values.length, units: unitIds.length,
        alphaAll: models.length > 1 ? krippendorffAlpha(t.rows) : null, pairs: pairs };
    });
    // Per coded value (for example L-CMP|IM3): who found it how often.
    var perValue = {};
    labels.forEach(function (l) {
      var v = valueKey(l);
      if (!perValue[v]) { perValue[v] = { value: v, stage: l.stage, by: {}, keys: {} }; }
      perValue[v].by[l.model] = (perValue[v].by[l.model] || 0) + 1;
      (perValue[v].keys[labelKey(l)] = perValue[v].keys[labelKey(l)] || {})[l.model] = 1;
    });
    var values = Object.keys(perValue).sort().map(function (v) {
      var r = perValue[v], keys = Object.keys(r.keys);
      var all = keys.filter(function (k) { return Object.keys(r.keys[k]).length === models.length; }).length;
      return { value: v, stage: r.stage, by: r.by, union: keys.length, allModels: all,
        positiveAgreement: keys.length ? all / keys.length : null };
    });
    // Labels found by every model: do they agree on the rest?
    var byKey = {};
    labels.forEach(function (l) { (byKey[labelKey(l)] = byKey[labelKey(l)] || {})[l.model] = l; });
    var shared = 0, statusSame = 0, statusN = 0, jac = 0, framingSame = 0, framingN = 0, strengthSame = 0, strengthN = 0;
    Object.keys(byKey).forEach(function (k) {
      var g = byKey[k], ls = models.map(function (m) { return g[m]; });
      if (ls.some(function (x) { return !x; })) return;
      shared++;
      if (ls[0].stage === 1) { statusN++; if (ls.every(function (x) { return x.status === ls[0].status; })) statusSame++; }
      if (ls[0].stage === 3) {
        framingN++; if (ls.every(function (x) { return x.framing === ls[0].framing; })) framingSame++;
        strengthN++; if (ls.every(function (x) { return x.strength === ls[0].strength; })) strengthSame++;
      }
      var s = 0, pairs = 0;
      for (var i = 0; i < ls.length; i++) for (var j = i + 1; j < ls.length; j++) { s += tokenJaccard(ls[i].span, ls[j].span); pairs++; }
      jac += pairs ? s / pairs : 1;
    });
    // What each model adds: share of the union that only it found.
    var keysAll = Object.keys(byKey);
    var adds = {};
    models.forEach(function (m) {
      var only = keysAll.filter(function (k) { return byKey[k][m] && Object.keys(byKey[k]).length === 1; }).length;
      adds[m] = { only: only, total: keysAll.filter(function (k) { return byKey[k][m]; }).length,
        shareOfUnion: keysAll.length ? only / keysAll.length : null };
    });
    return { families: families, values: values, adds: adds, union: keysAll.length,
      shared: { n: shared, statusAgreement: statusN ? statusSame / statusN : null,
        framingAgreement: framingN ? framingSame / framingN : null,
        strengthAgreement: strengthN ? strengthSame / strengthN : null,
        meanSpanJaccard: shared ? jac / shared : null } };
  }

  // Run-to-run stability of one model (validation runs, Section "LLM Coding").
  function stability(labels, model, runs, units) {
    if (runs < 2) return null;
    var rowsModel = labels.filter(function (l) { return l.model === model; }).map(function (l) {
      var c = {}; for (var k in l) c[k] = l[k]; c.model = 'run' + l.run; return c;
    });
    var runIds = []; for (var r = 1; r <= runs; r++) runIds.push('run' + r);
    var all = { id: 'all', name: 'all', match: function () { return true; } };
    var t = indicatorTable(rowsModel, runIds, all, units.map(function (u) { return u.id; }));
    return { alpha: krippendorffAlpha(t.rows), pairs: runIds.length === 2 ? pairStats(t.rows, 0, 1) : null };
  }

  // Coverage computed from one model's labels alone, to show how far the
  // RQ1 result depends on the model.
  function singleModelCombined(labels, m) {
    return combine(labels.filter(function (l) { return l.model === m; }), [m]);
  }

  // ---------- Term view of a capability (as ADTool's attack-defense terms) ----------

  // {and: [A, {or: [B, C]}]} <-> "A AND (B OR C)". Mixing AND and OR needs brackets.
  function termToString(expr, nested) {
    if (typeof expr === 'string') return expr;
    var op = Object.keys(expr)[0];
    var s = expr[op].map(function (c) { return termToString(c, true); }).join(' ' + op.toUpperCase() + ' ');
    return nested && expr[op].length > 1 ? '(' + s + ')' : s;
  }

  function parseTerm(text, componentIds) {
    var tokens = String(text || '').toUpperCase().match(/\(|\)|[A-Z][A-Z0-9_-]*/g) || [];
    var rest = String(text || '').toUpperCase().replace(/\(|\)|[A-Z][A-Z0-9_-]*|\s+/g, '');
    if (rest) throw new Error('unexpected characters: ' + rest);
    var i = 0;
    function peek() { return tokens[i]; }
    function group() {
      var items = [primary()], op = null;
      while (peek() === 'AND' || peek() === 'OR') {
        var o = tokens[i++].toLowerCase();
        if (op && o !== op) throw new Error('mixing AND and OR needs brackets');
        op = o;
        items.push(primary());
      }
      if (!op) return items[0];
      var e = {}; e[op] = items; return e;
    }
    function primary() {
      var t = tokens[i++];
      if (t === undefined) throw new Error('the term ends too early');
      if (t === '(') {
        var g = group();
        if (tokens[i++] !== ')') throw new Error('a bracket is not closed');
        return g;
      }
      if (t === ')' || t === 'AND' || t === 'OR') throw new Error('unexpected ' + t);
      if (componentIds && componentIds.indexOf(t) < 0) throw new Error('unknown component ' + t);
      return t;
    }
    if (!tokens.length) throw new Error('the term is empty');
    var e = group();
    if (i < tokens.length) throw new Error('unexpected ' + tokens[i]);
    return e;
  }

  // The checks of scripts/instrument-test/v002/evaluate.py (check_model), as a list of problems.
  function checkModel(model) {
    var problems = [], used = {}, comps = model.components || {};
    Object.keys(model.capabilities || {}).forEach(function (k) {
      var cap = model.capabilities[k];
      try { termToString(cap.needs); } catch (e) { problems.push(k + ': invalid term'); return; }
      if (JSON.stringify(cap.needs).indexOf('orplus') >= 0) problems.push(k + ' still uses OR+');
      leaves(cap.needs).forEach(function (c) {
        if (!comps[c]) problems.push(k + ' uses unknown component ' + c);
        used[c] = 1;
      });
    });
    Object.keys(comps).forEach(function (c) { if (!used[c]) problems.push('component ' + c + ' is in no capability'); });
    var seen = {};
    Object.keys(model.harms || {}).forEach(function (h) {
      (model.harms[h].pathways || []).forEach(function (p) {
        if (!model.capabilities[p.capability]) problems.push(p.id + ' uses unknown capability ' + p.capability);
        if (seen[p.id]) problems.push('duplicate pathway ' + p.id);
        seen[p.id] = 1;
        if (!p.sources || !p.sources.length) problems.push(p.id + ' has no source');
      });
    });
    return problems;
  }

  function nextId(existing, prefix) {
    var n = 1;
    existing.forEach(function (id) {
      var m = new RegExp('^' + prefix + '(\\d+)$').exec(id);
      if (m) n = Math.max(n, +m[1] + 1);
    });
    return prefix + (prefix === 'P' && n < 10 ? '0' : '') + n;
  }

  // Character range of a span in its unit (units are already normalised).
  function spanRange(span, unitText) {
    var s = normalise(span).toLowerCase();
    if (!s) return null;
    var i = unitText.toLowerCase().indexOf(s);
    return i < 0 ? null : [i, i + s.length];
  }

  var api = { PRESENT: PRESENT, ABSENT: ABSENT, UNCERTAIN: UNCERTAIN, ROUTINE: ROUTINE, HIGH_STAKES: HIGH_STAKES,
    FAMILIES: FAMILIES, normalise: normalise, htmlToText: htmlToText, unitize: unitize, chunk: chunk,
    parseJSON: parseJSON, spanOk: spanOk, labelKey: labelKey, valueKey: valueKey,
    readStage1: readStage1, readStage2: readStage2, readStage3: readStage3, combine: combine,
    evaluate: evaluate, leaves: leaves, pathways: pathways, evaluateModel: evaluateModel,
    assumptionDependent: assumptionDependent, proposeApplicability: proposeApplicability,
    coverage: coverage, levelShares: levelShares, afterMeasure: afterMeasure,
    krippendorffAlpha: krippendorffAlpha, pairStats: pairStats, tokenJaccard: tokenJaccard,
    agreement: agreement, stability: stability, singleModelCombined: singleModelCombined,
    termToString: termToString, parseTerm: parseTerm, checkModel: checkModel, nextId: nextId, spanRange: spanRange };

  root.PA = root.PA || {};
  root.PA.analysis = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
