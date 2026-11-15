// Page controller: the inputs, the coding run with every model, the human
// decisions (applicability and the components a measure would remove) and
// the report.
(function (root) {
  'use strict';
  var A = root.PA.analysis, L = root.PA.llm, P = root.PA.providers, Rp = root.PA.report;
  var DATA = root.PA_DATA;
  var $ = function (id) { return document.getElementById(id); };
  var esc = Rp.esc;

  var S = { models: [], run: null, overrides: {}, removes: {}, abort: null };
  var STORE = 'pa.v001.models';

  // ---------- Models ----------

  function defaultModels() {
    return [
      { provider: 'anthropic', model: P.anthropic.model, key: '', label: 'Claude', effort: 'high' },
      { provider: 'compatible', model: '', key: '', label: 'Open-weight', baseUrl: P.compatible.baseUrl }
    ];
  }

  function loadModels() {
    try {
      var saved = JSON.parse(localStorage.getItem(STORE) || 'null');
      if (saved && saved.length) { $('remember').checked = true; return saved; }
    } catch (e) { /* storage unavailable */ }
    return defaultModels();
  }

  function saveModels() {
    try {
      if ($('remember').checked) localStorage.setItem(STORE, JSON.stringify(S.models));
      else localStorage.removeItem(STORE);
    } catch (e) { /* storage unavailable */ }
  }

  function renderModels() {
    $('models').innerHTML = S.models.map(function (m, i) {
      var p = P[m.provider];
      return '<div class="model" data-i="' + i + '">' +
        '<div class="row"><label>Name <input data-f="label" value="' + esc(m.label || '') + '" placeholder="Model ' + (i + 1) + '"></label>' +
        '<label>Provider <select data-f="provider">' + Object.keys(P).map(function (k) {
          return '<option value="' + k + '"' + (k === m.provider ? ' selected' : '') + '>' + esc(P[k].name) + '</option>';
        }).join('') + '</select></label>' +
        '<label>Model id <input data-f="model" value="' + esc(m.model || '') + '" placeholder="model id"></label>' +
        (m.provider === 'demo' ? '' : '<label>API key <input data-f="key" type="password" autocomplete="off" value="' + esc(m.key || '') + '" placeholder="' + (p.needsKey ? 'required' : 'optional') + '"></label>') +
        (m.provider === 'compatible' ? '<label>Base URL <input data-f="baseUrl" value="' + esc(m.baseUrl || p.baseUrl) + '"></label>' : '') +
        (m.provider === 'anthropic' ? '<label>Effort <select data-f="effort">' + ['low', 'medium', 'high', 'xhigh', 'max'].map(function (e) {
          return '<option' + (e === (m.effort || 'high') ? ' selected' : '') + '>' + e + '</option>'; }).join('') + '</select></label>' : '') +
        (m.provider === 'openai' || m.provider === 'gemini' || m.provider === 'compatible' ? '<label>Temperature <input data-f="temperature" value="' + esc(m.temperature === undefined ? '' : m.temperature) + '" placeholder="model default" size="6"></label>' : '') +
        '<button class="ghost" data-del="' + i + '" title="Remove">✕</button></div>' +
        '<div class="hint">' + esc(p.hint) + '</div></div>';
    }).join('');
  }

  function bindModels() {
    $('models').addEventListener('input', function (e) {
      var box = e.target.closest('.model'); if (!box) return;
      var m = S.models[+box.dataset.i], f = e.target.dataset.f; if (!f) return;
      m[f] = e.target.value;
      if (f === 'provider') { m.model = P[m.provider].model; if (m.provider === 'compatible') m.baseUrl = P.compatible.baseUrl; renderModels(); }
      saveModels();
    });
    $('models').addEventListener('click', function (e) {
      if (e.target.dataset.del === undefined) return;
      S.models.splice(+e.target.dataset.del, 1); renderModels(); saveModels();
    });
    $('add-model').onclick = function () { S.models.push({ provider: 'openai', model: '', key: '', label: '' }); renderModels(); saveModels(); };
    $('demo-models').onclick = function () {
      S.models = [{ provider: 'demo', model: 'demo-a', label: 'Demo A' }, { provider: 'demo', model: 'demo-b', label: 'Demo B' }];
      renderModels(); saveModels();
    };
    $('remember').onchange = saveModels;
  }

  function modelNames() {
    var seen = {};
    return S.models.map(function (m, i) {
      var n = (m.label || '').trim() || (m.provider + ':' + (m.model || i + 1));
      if (seen[n]) n += ' (' + (i + 1) + ')';
      seen[n] = 1; return n;
    });
  }

  // ---------- Input ----------

  function currentUnits() {
    var policy = A.unitize($('policy').value, 'policy');
    var iface = A.unitize($('interface').value, 'interface');
    return policy.concat(iface);
  }

  function showUnits() {
    var u = currentUnits();
    var p = u.filter(function (x) { return x.surface === 'policy'; }).length;
    $('unit-count').textContent = p + ' policy units, ' + (u.length - p) + ' interface units';
  }

  function readFile(input, target) {
    var f = input.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      var t = String(r.result);
      $(target).value = /\.html?$/i.test(f.name) || /^\s*</.test(t) ? A.htmlToText(t) : t;
      showUnits();
    };
    r.readAsText(f);
  }

  // ---------- Run ----------

  function log(msg, cls) {
    var li = document.createElement('li');
    li.textContent = new Date().toLocaleTimeString() + '  ' + msg;
    if (cls) li.className = cls;
    $('log').appendChild(li); li.scrollIntoView({ block: 'nearest' });
  }

  function jsonl(objs) { return objs.map(function (o) { return JSON.stringify(o); }).join('\n'); }

  async function callWithRetry(cfg, system, user, signal, what) {
    for (var attempt = 1; ; attempt++) {
      try { return await L.call(cfg, system, user, signal); } catch (e) {
        var retry = attempt < 3 && !signal.aborted && (!e.status || e.status === 429 || e.status >= 500);
        log(what + ': ' + e.message + (retry ? ' – retrying' : ''), 'err');
        if (!retry) throw e;
        await new Promise(function (r) { setTimeout(r, 2000 * attempt * attempt); });
      }
    }
  }

  function context(units, i) {
    return { before: i > 0 ? units[i - 1].text : '', after: i < units.length - 1 ? units[i + 1].text : '' };
  }

  async function runModel(cfg, name, units, opts, signal, progress) {
    var byId = {}; units.forEach(function (u) { byId[u.id] = u; });
    var out = { name: name, labels: [], failures: [], raw: [], errors: 0, calls: 0, ms: 0, tokensIn: 0, tokensOut: 0, servedBy: '', flags: {}, wording: [] };
    function account(r) { out.calls++; out.ms += r.ms; if (r.usage) { out.tokensIn += r.usage.input || 0; out.tokensOut += r.usage.output || 0; } out.servedBy = r.servedBy; }
    var stage1Units = units.map(function (u) { return { unit: u.id, heading: u.heading, text: u.text }; });
    var chunks = A.chunk(stage1Units, opts.chunk);
    var runs = opts.runs + (opts.paraphrase ? 1 : 0);
    for (var run = 1; run <= runs; run++) {
      var para = opts.paraphrase && run === runs;
      for (var c = 0; c < chunks.length; c++) {
        if (signal.aborted) throw new Error('stopped');
        var what = name + ' stage 1' + (para ? ' (paraphrase)' : ' run ' + run) + ', part ' + (c + 1) + '/' + chunks.length;
        try {
          var r = await callWithRetry(cfg, para ? DATA.prompts.stage1p : DATA.prompts.stage1, jsonl(chunks[c]), signal, what);
          account(r); out.raw.push({ stage: 1, run: para ? 'paraphrase' : run, part: c + 1, text: r.text });
          var parsed = A.readStage1(A.parseJSON(r.text), byId, name, para ? 2 : run);
          if (para) out.wording = out.wording.concat(parsed.labels);
          else {
            out.labels = out.labels.concat(parsed.labels);
            if (run === 1) { out.failures = out.failures.concat(parsed.failures); Object.assign(out.flags, parsed.flags); }
          }
        } catch (e) {
          if (signal.aborted) throw e;
          out.errors++; out.failures.push({ model: name, stage: 1, reason: 'call or JSON failed: ' + e.message });
        }
        progress();
      }
    }
    return out;
  }

  async function runStage(stage, cfg, name, items, units, signal, out, progress) {
    var byId = {}; units.forEach(function (u) { byId[u.id] = u; });
    var chunks = A.chunk(items, 20);
    for (var c = 0; c < chunks.length; c++) {
      if (signal.aborted) throw new Error('stopped');
      var what = name + ' stage ' + stage + ', part ' + (c + 1) + '/' + chunks.length;
      try {
        var r = await callWithRetry(cfg, stage === 2 ? DATA.prompts.stage2 : DATA.prompts.stage3, jsonl(chunks[c]), signal, what);
        out.calls++; out.ms += r.ms; if (r.usage) { out.tokensIn += r.usage.input || 0; out.tokensOut += r.usage.output || 0; }
        out.raw.push({ stage: stage, run: 1, part: c + 1, text: r.text });
        var parsed = (stage === 2 ? A.readStage2 : A.readStage3)(A.parseJSON(r.text), byId, name, 1);
        out.labels = out.labels.concat(parsed.labels); out.failures = out.failures.concat(parsed.failures);
      } catch (e) {
        if (signal.aborted) throw e;
        out.errors++; out.failures.push({ model: name, stage: stage, reason: 'call or JSON failed: ' + e.message });
      }
      progress();
    }
  }

  async function run() {
    var units = currentUnits();
    if (!units.length) { alert('Paste a privacy policy first.'); return; }
    if (S.models.length < 2) { alert('The method codes with at least two models of different families. Add a second model.'); return; }
    var names = modelNames();
    for (var i = 0; i < S.models.length; i++) {
      var m = S.models[i];
      if (!m.model) { alert(names[i] + ': enter a model id.'); return; }
      if (P[m.provider].needsKey && !m.key) { alert(names[i] + ': enter an API key.'); return; }
    }
    var opts = { chunk: Math.max(1, +$('chunk').value || 15), runs: Math.max(1, Math.min(3, +$('runs').value || 1)), paraphrase: $('paraphrase').checked };
    S.abort = new AbortController();
    var signal = S.abort.signal;
    $('run').disabled = true; $('stop').disabled = false; $('log').innerHTML = '';
    var total = S.models.length * Math.ceil(units.length / opts.chunk) * (opts.runs + (opts.paraphrase ? 1 : 0));
    var done = 0, bar = $('progress');
    bar.max = total; bar.value = 0;
    var progress = function () { done++; bar.value = Math.min(done, bar.max); };
    log('Coding ' + units.length + ' units with ' + names.join(', ') + '.');
    try {
      var results = await Promise.all(S.models.map(function (cfg, i) { return runModel(cfg, names[i], units, opts, signal, progress); }));
      // Stages 2 and 3 take the union of both models' stage 1 results.
      var run1 = [].concat.apply([], results.map(function (r) { return r.labels.filter(function (l) { return l.run === 1; }); }));
      var harmItems = {}, protUnits = {};
      run1.forEach(function (l) { if (l.code === 'L-HRM') harmItems[l.unit + '|' + l.harm] = harmItems[l.unit + '|' + l.harm] || l; });
      results.forEach(function (r) { Object.keys(r.flags).forEach(function (u) { if (r.flags[u].protection) protUnits[u] = 1; }); });
      var idx = {}; units.forEach(function (u, k) { idx[u.id] = k; });
      var s2 = Object.keys(harmItems).map(function (k) {
        var l = harmItems[k], c = context(units, idx[l.unit]);
        return { unit: l.unit, harm: l.harm, span: l.span, text: units[idx[l.unit]].text, before: c.before, after: c.after };
      });
      var s3 = Object.keys(protUnits).map(function (u) {
        var c = context(units, idx[u]);
        return { unit: u, text: units[idx[u]].text, before: c.before, after: c.after };
      });
      bar.max += S.models.length * (Math.ceil(s2.length / 20) + Math.ceil(s3.length / 20));
      log('Stage 2: ' + s2.length + ' named harms; stage 3: ' + s3.length + ' units with protection claims.');
      await Promise.all(S.models.map(async function (cfg, i) {
        if (s2.length) await runStage(2, cfg, names[i], s2, units, signal, results[i], progress);
        if (s3.length) await runStage(3, cfg, names[i], s3, units, signal, results[i], progress);
      }));
      S.run = { date: new Date().toISOString().slice(0, 16).replace('T', ' '), app: $('app-name').value.trim(), units: units,
        names: names, results: results, opts: opts,
        configs: S.models.map(function (m, i) { return { name: names[i], provider: m.provider, model: m.model, effort: m.effort || null, temperature: m.temperature || null, baseUrl: m.provider === 'compatible' ? m.baseUrl : null }; }) };
      S.overrides = {}; S.removes = {};
      log('Done.', 'ok');
      renderAll();
      $('report-wrap').scrollIntoView({ behavior: 'smooth' });
    } catch (e) {
      log('Stopped: ' + e.message, 'err');
    } finally {
      $('run').disabled = false; $('stop').disabled = true;
    }
  }

  // ---------- Build the report data ----------

  function build() {
    var run = S.run, model = DATA.model, names = run.names;
    var labels = [].concat.apply([], run.results.map(function (r) { return r.labels.filter(function (l) { return l.run === 1 || l.stage > 1; }); }));
    var combined = A.combine(labels, names);
    var proposal = A.proposeApplicability(model, combined, { countPossible: $('count-possible').checked });
    var states = {};
    Object.keys(proposal).forEach(function (k) { states[k] = S.overrides[k] || proposal[k].state; });
    var ev = A.evaluateModel(model, states);
    var hasInterface = run.units.some(function (u) { return u.surface === 'interface'; });
    var covPolicyA = A.coverage(model, combined, 'policy', 'agreed'), covPolicyB = A.coverage(model, combined, 'policy', 'with-uncertain');
    var covIfA = A.coverage(model, combined, 'interface', 'agreed'), covIfB = A.coverage(model, combined, 'interface', 'with-uncertain');
    var pc = { total: 0, present: 0, absent: 0, uncertain: 0 };
    Object.keys(ev.pathways).forEach(function (k) { pc.total++; pc[ev.pathways[k]]++; });

    // RQ2: named harms with the stances of each model.
    var harmRecords = combined.filter(function (r) { return r.code === 'L-HRM'; }).map(function (r) {
      var st = {}, union = {};
      labels.filter(function (l) { return l.stage === 2 && l.unit === r.unit && l.harm === r.harm; }).forEach(function (l) {
        (st[l.model] = st[l.model] || []).push(l.code); union[l.code] = 1;
      });
      return { unit: r.unit, harm: r.harm, span: r.span, foundBy: Object.keys(r.by), stances: st, union: Object.keys(union).sort() };
    });
    var stanceCounts = {};
    harmRecords.forEach(function (h) { h.union.forEach(function (c) { stanceCounts[c] = (stanceCounts[c] || 0) + 1; }); });
    var count = function (code) { return combined.filter(function (r) { return r.code === code; }).length; };

    // RQ3: claims, with the human choice of the component a measure removes.
    var claimRecords = combined.filter(function (r) { return r.stage === 3 && r.code !== 'C-REA'; }).map(function (r) {
      var removes = S.removes[r.key] || '';
      var rec = { key: r.key, unit: r.unit, code: r.code, span: r.span, framing: r.framing, strength: r.strength,
        foundBy: Object.keys(r.by), decision: r.decision, removes: removes, closes: [], leftOpen: [] };
      if (removes) {
        // Within the claim's scope: applicable pathways whose tree contains the
        // removed component. Those that stay open are candidate mismatches.
        var after = A.afterMeasure(model, states, [removes]);
        A.pathways(model).forEach(function (p) {
          if (ev.pathways[p.id] !== 'present' || p.components.indexOf(removes) < 0) return;
          (after[p.id] === 'absent' ? rec.closes : rec.leftOpen).push(p.id);
        });
      }
      return rec;
    });

    // Deviation: coverage and applicability from each model alone.
    var levelDeviation = [], applicabilityDeviation = [];
    var single = {};
    names.forEach(function (m) {
      var c = A.singleModelCombined(labels, m);
      single[m] = { cov: A.coverage(model, c, 'policy', 'agreed'), appl: A.proposeApplicability(model, c, { countPossible: $('count-possible').checked }) };
    });
    A.pathways(model).forEach(function (p) {
      var lv = {}; names.forEach(function (m) { lv[m] = single[m].cov[p.id].level; });
      if (names.some(function (m) { return lv[m] !== lv[names[0]]; })) levelDeviation.push({ id: p.id, harm: p.harm, levels: lv });
    });
    Object.keys(model.components).forEach(function (id) {
      var st = {}; names.forEach(function (m) { st[m] = single[m].appl[id].state; });
      if (names.some(function (m) { return st[m] !== st[names[0]]; })) applicabilityDeviation.push({ id: id, states: st });
    });

    var agreement = A.agreement(labels, names, run.units);
    var perModel = {};
    run.results.forEach(function (r) {
      var stab = A.stability(r.labels.filter(function (l) { return l.stage === 1; }), r.name, run.opts.runs, run.units);
      var word = null;
      if (r.wording.length || run.opts.paraphrase) {
        var both = r.labels.filter(function (l) { return l.stage === 1 && l.run === 1; }).concat(r.wording);
        word = A.stability(both, r.name, 2, run.units);
      }
      perModel[r.name] = { servedBy: r.servedBy, labels: r.labels.filter(function (l) { return l.run === 1 || l.stage > 1; }).length,
        failures: r.failures.filter(function (f) { return /span/.test(f.reason); }).length, errors: r.errors, calls: r.calls, ms: r.ms,
        tokensIn: r.tokensIn, tokensOut: r.tokensOut, stability: stab ? stab.alpha : null, wording: word ? word.alpha : null };
    });
    var compFam = agreement.families.filter(function (f) { return f.id === 'components'; })[0];

    return { app: run.app, date: run.date, model: model, models: names, combined: combined, proposal: proposal, states: states, ev: ev,
      units: { policy: run.units.filter(function (u) { return u.surface === 'policy'; }).length, interface: run.units.filter(function (u) { return u.surface === 'interface'; }).length },
      sources: { model: DATA.sources.model.sha256.slice(0, 12), modelVersion: model.version,
        prompts: ['stage1', 'stage2', 'stage3'].map(function (k) { return DATA.sources[k].path.split('/').pop(); }).join(', ') },
      hasInterface: hasInterface, covPolicyA: covPolicyA, covPolicyB: covPolicyB, covIfA: covIfA, covIfB: covIfB, pathCounts: pc,
      shares: { policyA: A.levelShares(ev.pathways, covPolicyA, 'A'), policyB: A.levelShares(ev.pathways, covPolicyB, 'B'),
        ifA: A.levelShares(ev.pathways, covIfA, 'A'), ifB: A.levelShares(ev.pathways, covIfB, 'B') },
      harmRecords: harmRecords, stanceCounts: stanceCounts, harmMentions: harmRecords.length,
      toCheck: combined.filter(function (r) { return r.decision === 'check' || r.decision === 'proposal'; }).length,
      secondary: { gen: count('L-GEN'), grs: count('S-GRS'), rea: count('C-REA') },
      claimRecords: claimRecords, claims: claimRecords.length, reassurance: count('C-REA'),
      agreement: agreement, alphaComponents: compFam && compFam.pairs.length ? (names.length > 2 ? compFam.alphaAll : compFam.pairs[0].alpha) : null,
      perModel: perModel, levelDeviation: levelDeviation, applicabilityDeviation: applicabilityDeviation,
      failures: [].concat.apply([], run.results.map(function (r) { return r.failures; })) };
  }

  // ---------- Rendering ----------

  function renderApplicability(R) {
    var model = R.model;
    var rows = Object.keys(model.components).map(function (id) {
      var c = model.components[id], p = R.proposal[id], cur = S.overrides[id] || p.state;
      return '<tr' + (S.overrides[id] ? ' class="changed"' : '') + '><td><span class="cmp o-' + esc(c.origin) + '">' + esc(id) + '</span></td><td>' + esc(c.label) +
        '<div class="muted small">' + esc(c.feature) + '</div></td><td>' + Rp.badge(p.state) + '<div class="muted small">' + esc(p.basis) + '</div></td>' +
        '<td><select data-comp="' + id + '">' + ['present', 'absent', 'uncertain'].map(function (s) {
          return '<option' + (s === cur ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select></td></tr>';
    }).join('');
    $('applicability').innerHTML = '<div class="tw"><table class="small"><thead><tr><th>ID</th><th>Component</th><th>Proposal from the text</th><th>Your decision</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  function renderAll() {
    if (!S.run) return;
    var R = build();
    S.lastReport = R;
    renderApplicability(R);
    $('report').innerHTML = Rp.render(R);
    $('report-wrap').hidden = false;
    $('appl-wrap').hidden = false;
  }

  function renderTreesOnly() {
    $('trees').innerHTML = Rp.legend() + Rp.trees(DATA.model, null, null, null, null);
  }

  // ---------- Export ----------

  function download(name, type, text) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: type }));
    a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  function slug() { return (S.run.app || 'app').replace(/[^\w-]+/g, '_').slice(0, 40) + '_' + S.run.date.replace(/[ :]/g, '-'); }

  function exportJSON() {
    var R = S.lastReport;
    download('policy-analysis_' + slug() + '.json', 'application/json', JSON.stringify({
      tool: 'policy-analyzer v001', date: S.run.date, app: S.run.app, instruments: DATA.sources,
      models: S.run.configs, settings: S.run.opts, units: S.run.units,
      decisions: { applicability: R.states, overridden: S.overrides, measureRemoves: S.removes },
      raw: S.run.results.map(function (r) { return { model: r.name, servedBy: r.servedBy, outputs: r.raw }; }),
      labels: [].concat.apply([], S.run.results.map(function (r) { return r.labels.concat(r.wording); })),
      failures: R.failures, combined: R.combined, pathways: R.ev.pathways,
      coverage: { policyA: R.covPolicyA, policyB: R.covPolicyB, interfaceA: R.covIfA, interfaceB: R.covIfB },
      agreement: R.agreement
    }, null, 1));
  }

  function exportCSV() {
    var rows = [['model', 'run', 'stage', 'unit', 'surface', 'code', 'node', 'harm', 'status', 'framing', 'strength', 'unsure', 'span']];
    S.run.results.forEach(function (r) {
      r.labels.concat(r.wording.map(function (l) { var c = Object.assign({}, l); c.run = 'paraphrase'; return c; })).forEach(function (l) {
        rows.push([l.model, l.run, l.stage, l.unit, l.surface, l.code, l.node || '', l.harm || '', l.status || '', l.framing || '', l.strength || '', l.unsure ? 1 : 0, l.span]);
      });
    });
    download('labels_' + slug() + '.csv', 'text/csv', rows.map(function (r) {
      return r.map(function (c) { c = String(c); return /[",\n]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c; }).join(',');
    }).join('\n'));
  }

  function exportHTML() {
    var css = Array.prototype.map.call(document.styleSheets, function (s) {
      try { return Array.prototype.map.call(s.cssRules, function (r) { return r.cssText; }).join('\n'); } catch (e) { return ''; }
    }).join('\n');
    var html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Policy analysis – ' + esc(S.run.app || 'app') + '</title><style>' + css +
      '</style></head><body><main class="report">' + $('report').innerHTML.replace(/<select[\s\S]*?<\/select>/g, function (s) {
        var m = s.match(/<option[^>]*selected[^>]*>([^<]*)</); return m ? esc(m[1]) : '–';
      }) + '<h2>Applicability decisions</h2>' + $('applicability').innerHTML.replace(/<select[\s\S]*?<\/select>/g, function (s) {
        var m = s.match(/<option[^>]*selected[^>]*>([^<]*)</); return m ? esc(m[1]) : '–';
      }) + '</main></body></html>';
    download('report_' + slug() + '.html', 'text/html', html);
  }

  // ---------- Start ----------

  function init() {
    if (!DATA) { document.body.innerHTML = '<p style="padding:2em">output/data.js is missing. Run <code>python build_data.py</code> in this folder first.</p>'; return; }
    S.models = loadModels();
    renderModels(); bindModels(); renderTreesOnly();
    $('instr').textContent = 'Reference model v' + DATA.model.version + ' (' + DATA.model.date + '), ' + Object.keys(DATA.model.components).length +
      ' components, ' + Object.keys(DATA.model.capabilities).length + ' capabilities, ' + A.pathways(DATA.model).length + ' pathways; prompts ' +
      ['stage1', 'stage2', 'stage3'].map(function (k) { return DATA.sources[k].path.split('/').pop(); }).join(', ') + '.';
    $('policy').addEventListener('input', showUnits); $('interface').addEventListener('input', showUnits);
    $('policy-file').onchange = function () { readFile(this, 'policy'); };
    $('interface-file').onchange = function () { readFile(this, 'interface'); };
    $('load-example').onclick = function () {
      $('app-name').value = root.PA_EXAMPLE.app; $('policy').value = root.PA_EXAMPLE.policy; $('interface').value = root.PA_EXAMPLE.interface; showUnits();
    };
    $('run').onclick = run;
    $('stop').onclick = function () { if (S.abort) S.abort.abort(); };
    $('applicability').addEventListener('change', function (e) {
      var id = e.target.dataset.comp; if (!id) return;
      if (e.target.value === S.lastReport.proposal[id].state) delete S.overrides[id]; else S.overrides[id] = e.target.value;
      renderAll();
    });
    $('reset-appl').onclick = function () { S.overrides = {}; renderAll(); };
    $('count-possible').onchange = renderAll;
    $('report').addEventListener('change', function (e) {
      var i = e.target.dataset.claim; if (i === undefined) return;
      var key = S.lastReport.claimRecords[+i].key;
      if (e.target.value) S.removes[key] = e.target.value; else delete S.removes[key];
      renderAll();
    });
    $('export-json').onclick = exportJSON; $('export-csv').onclick = exportCSV; $('export-html').onclick = exportHTML;
    $('print').onclick = function () { window.print(); };
    showUnits();
  }

  document.addEventListener('DOMContentLoaded', init);
})(window);
