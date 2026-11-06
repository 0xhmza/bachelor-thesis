// Controller of the Privacy Policy Analyser: the workspace state (saved in this
// browser), navigation between the views, the coding run, the human
// decisions, and the YAML record of everything.
(function (root) {
  'use strict';
  var A = root.PA.analysis, L = root.PA.llm, P = root.PA.providers, Y = root.PA.yaml;
  var DATA = root.PA_DATA;
  var VERSION = 'v002';
  var STORE = 'pa.v002.workspace', KEYSTORE = 'pa.v002.keys';
  var $ = function (id) { return document.getElementById(id); };

  function clone(x) { return JSON.parse(JSON.stringify(x)); }
  function now() { return new Date().toISOString(); }
  function localTime() {
    var d = new Date(), off = -d.getTimezoneOffset(), s = off >= 0 ? '+' : '-', a = Math.abs(off);
    var p = function (n) { return String(n).padStart(2, '0'); };
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + 'T' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds()) + s + p(Math.floor(a / 60)) + ':' + p(a % 60);
  }

  // ---------- Workspace ----------

  function defaults() {
    return {
      project: { app: '', analyst: '', notes: '', created: localTime() },
      text: { policy: '', interface: '', policySource: '', interfaceSource: '' },
      models: [
        { provider: 'anthropic', model: P.anthropic.model, key: '', label: 'Claude', effort: 'high' },
        { provider: 'compatible', model: '', key: '', label: 'Open-weight', baseUrl: P.compatible.baseUrl }
      ],
      remember: false,
      settings: { chunk: 15, runs: 1, paraphrase: false, countPossible: true },
      model: clone(DATA.model), modelEdits: [],
      run: null, review: {}, overrides: {}, removes: {},
      ui: { tab: 'project', harm: 'H-PSY', theme: 'paper', textFilter: { surface: 'all', family: 'all', decision: 'all' }, reviewFilter: 'pending', reviewSel: null, selected: null }
    };
  }

  var S = defaults(), rev = 0, cache = null, saveTimer = null, running = null;
  S.progress = {};

  function load() {
    try {
      var w = JSON.parse(localStorage.getItem(STORE) || 'null');
      if (w) {
        var d = defaults();
        Object.keys(d).forEach(function (k) { if (w[k] !== undefined) S[k] = w[k]; else S[k] = d[k]; });
        S.ui = Object.assign(d.ui, w.ui || {});
        var keys = JSON.parse(localStorage.getItem(KEYSTORE) || 'null');
        if (keys && S.remember) S.models.forEach(function (m, i) { if (keys[i]) m.key = keys[i]; });
      }
    } catch (e) { toast('The saved workspace could not be read; starting fresh.', 'bad'); }
    S.progress = {};
  }

  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      try {
        var w = {};
        Object.keys(S).forEach(function (k) { if (k !== 'progress') w[k] = S[k]; });
        w.models = S.models.map(function (m) { var c = Object.assign({}, m); delete c.key; return c; });
        localStorage.setItem(STORE, JSON.stringify(w));
        if (S.remember) localStorage.setItem(KEYSTORE, JSON.stringify(S.models.map(function (m) { return m.key || ''; })));
        else localStorage.removeItem(KEYSTORE);
        S.saveError = null;
      } catch (e) { S.saveError = 'Autosave failed (' + e.name + '): export the record to keep this work.'; }
      renderFoot();
    }, 350);
  }

  function changed(affectsResults) { if (affectsResults !== false) { rev++; cache = null; } save(); }

  // ---------- Units, model names ----------

  function units() { return A.unitize(S.text.policy, 'policy').concat(A.unitize(S.text.interface, 'interface')); }

  function modelNames(models) {
    var seen = {};
    return (models || S.models).map(function (m, i) {
      var n = (m.label || '').trim() || (m.provider + ':' + (m.model || i + 1));
      if (seen[n]) n += ' (' + (i + 1) + ')';
      seen[n] = 1; return n;
    });
  }

  // ---------- Reference model edits ----------

  function editedIds() {
    var f = DATA.model, w = S.model, out = {};
    Object.keys(w.components).forEach(function (k) { if (JSON.stringify(w.components[k]) !== JSON.stringify(f.components[k])) out[k] = 1; });
    Object.keys(w.capabilities).forEach(function (k) { if (JSON.stringify(w.capabilities[k]) !== JSON.stringify(f.capabilities[k])) out[k] = 1; });
    var fp = {};
    Object.keys(f.harms).forEach(function (h) { f.harms[h].pathways.forEach(function (p) { fp[p.id] = JSON.stringify(p) + h; }); });
    Object.keys(w.harms).forEach(function (h) { w.harms[h].pathways.forEach(function (p) { if (fp[p.id] !== JSON.stringify(p) + h) out[p.id] = 1; }); });
    return out;
  }
  function modelEdited() { return JSON.stringify(S.model) !== JSON.stringify(DATA.model); }
  function logEdit(op, target, detail) {
    S.modelEdits.push({ at: localTime(), op: op, target: target, detail: detail || null });
    changed();
  }

  // ---------- Run ----------

  function jsonl(objs) { return objs.map(function (o) { return JSON.stringify(o); }).join('\n'); }

  function log(msg, cls) {
    if (!S.runLog) S.runLog = [];
    S.runLog.push({ t: new Date().toLocaleTimeString(), msg: msg, cls: cls || '' });
    if (S.ui.tab === 'run') renderView();
  }

  async function callLogged(cfg, name, stage, run, part, system, user, signal, out) {
    var started = localTime();
    for (var attempt = 1; ; attempt++) {
      try {
        var r = await L.call(cfg, system, user, signal);
        out.calls.push({ model: name, stage: stage, run: run, part: part, started: started, attempt: attempt, ms: r.ms,
          tokens_in: r.usage ? r.usage.input : null, tokens_out: r.usage ? r.usage.output : null, served_by: r.servedBy, ok: true });
        out.ms += r.ms; out.servedBy = r.servedBy;
        if (r.usage) { out.tokensIn += r.usage.input || 0; out.tokensOut += r.usage.output || 0; }
        return r;
      } catch (e) {
        var retry = attempt < 3 && !signal.aborted && (!e.status || e.status === 429 || e.status >= 500);
        out.calls.push({ model: name, stage: stage, run: run, part: part, started: started, attempt: attempt, ok: false, error: e.message });
        log(name + ' stage ' + stage + ' part ' + part + ': ' + e.message + (retry ? ' (retrying)' : ''), 'err');
        if (!retry) throw e;
        await new Promise(function (res) { setTimeout(res, 2000 * attempt * attempt); });
      }
    }
  }

  function tick(name) { var p = S.progress[name]; if (p) { p.done++; if (S.ui.tab === 'run') renderView(); } }

  async function runModel(cfg, name, us, opts, signal) {
    var byId = {}; us.forEach(function (u) { byId[u.id] = u; });
    var out = { name: name, labels: [], wording: [], failures: [], raw: [], calls: [], errors: 0, ms: 0, tokensIn: 0, tokensOut: 0, servedBy: '', flags: {} };
    var chunks = A.chunk(us.map(function (u) { return { unit: u.id, heading: u.heading, text: u.text }; }), opts.chunk);
    var runs = opts.runs + (opts.paraphrase ? 1 : 0);
    for (var run = 1; run <= runs; run++) {
      var para = opts.paraphrase && run === runs;
      for (var c = 0; c < chunks.length; c++) {
        if (signal.aborted) throw new Error('stopped');
        try {
          var r = await callLogged(cfg, name, 1, para ? 'paraphrase' : run, c + 1, para ? DATA.prompts.stage1p : DATA.prompts.stage1, jsonl(chunks[c]), signal, out);
          out.raw.push({ stage: 1, run: para ? 'paraphrase' : run, part: c + 1, text: r.text });
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
        tick(name);
      }
    }
    return out;
  }

  async function runStage(stage, cfg, name, items, us, signal, out) {
    var byId = {}; us.forEach(function (u) { byId[u.id] = u; });
    var chunks = A.chunk(items, 20);
    for (var c = 0; c < chunks.length; c++) {
      if (signal.aborted) throw new Error('stopped');
      try {
        var r = await callLogged(cfg, name, stage, 1, c + 1, stage === 2 ? DATA.prompts.stage2 : DATA.prompts.stage3, jsonl(chunks[c]), signal, out);
        out.raw.push({ stage: stage, run: 1, part: c + 1, text: r.text });
        var parsed = (stage === 2 ? A.readStage2 : A.readStage3)(A.parseJSON(r.text), byId, name, 1);
        out.labels = out.labels.concat(parsed.labels); out.failures = out.failures.concat(parsed.failures);
      } catch (e) {
        if (signal.aborted) throw e;
        out.errors++; out.failures.push({ model: name, stage: stage, reason: 'call or JSON failed: ' + e.message });
      }
      tick(name);
    }
  }

  function validateRun() {
    var us = units(), names = modelNames();
    if (!us.length) return 'Add the privacy policy text first (Text).';
    if (S.models.length < 2) return 'The method codes with at least two models of different families. Add a second model (Models).';
    for (var i = 0; i < S.models.length; i++) {
      var m = S.models[i];
      if (!m.model) return names[i] + ': enter a model id (Models).';
      if (P[m.provider].needsKey && !m.key) return names[i] + ': enter an API key (Models).';
    }
    var problems = A.checkModel(S.model);
    if (problems.length) return 'The reference model has problems (Harm trees): ' + problems[0];
    return null;
  }

  async function startRun() {
    var err = validateRun();
    if (err) { toast(err, 'bad'); return; }
    if (S.run && !confirm('Start a new run? The current results and review decisions are replaced (export the record first to keep them).')) return;
    var us = units(), names = modelNames(), opts = Object.assign({}, S.settings);
    opts.chunk = Math.max(1, Math.min(60, +opts.chunk || 15)); opts.runs = Math.max(1, Math.min(3, +opts.runs || 1));
    var ctrl = new AbortController(); running = ctrl;
    S.runLog = []; S.progress = {};
    var perModel = Math.ceil(us.length / opts.chunk) * (opts.runs + (opts.paraphrase ? 1 : 0));
    names.forEach(function (n) { S.progress[n] = { done: 0, total: perModel }; });
    var started = localTime(), t0 = Date.now();
    log('Coding ' + us.length + ' units with ' + names.join(', ') + '.');
    try {
      var results = await Promise.all(S.models.map(function (cfg, i) { return runModel(cfg, names[i], us, opts, ctrl.signal); }));
      var run1 = [].concat.apply([], results.map(function (r) { return r.labels.filter(function (l) { return l.run === 1; }); }));
      var harmItems = {}, protUnits = {}, idx = {};
      us.forEach(function (u, k) { idx[u.id] = k; });
      run1.forEach(function (l) { if (l.code === 'L-HRM' && !harmItems[l.unit + '|' + l.harm]) harmItems[l.unit + '|' + l.harm] = l; });
      results.forEach(function (r) { Object.keys(r.flags).forEach(function (u) { if (r.flags[u].protection) protUnits[u] = 1; }); });
      var ctxOf = function (u) { var k = idx[u]; return { before: k > 0 ? us[k - 1].text : '', after: k < us.length - 1 ? us[k + 1].text : '' }; };
      var s2 = Object.keys(harmItems).map(function (k) { var l = harmItems[k], c = ctxOf(l.unit); return { unit: l.unit, harm: l.harm, span: l.span, text: us[idx[l.unit]].text, before: c.before, after: c.after }; });
      var s3 = Object.keys(protUnits).map(function (u) { var c = ctxOf(u); return { unit: u, text: us[idx[u]].text, before: c.before, after: c.after }; });
      names.forEach(function (n) { S.progress[n].total += Math.ceil(s2.length / 20) + Math.ceil(s3.length / 20); });
      log('Stage 2: ' + s2.length + ' named harms. Stage 3: ' + s3.length + ' units with protection claims.');
      await Promise.all(S.models.map(async function (cfg, i) {
        if (s2.length) await runStage(2, cfg, names[i], s2, us, ctrl.signal, results[i]);
        if (s3.length) await runStage(3, cfg, names[i], s3, us, ctrl.signal, results[i]);
      }));
      S.run = {
        id: 'run-' + Date.now().toString(36), started: started, finished: localTime(), seconds: Math.round((Date.now() - t0) / 100) / 10,
        units: us, names: names, opts: opts, modelEdited: modelEdited(), model: clone(S.model),
        configs: S.models.map(function (m, i) {
          return { name: names[i], provider: m.provider, provider_name: P[m.provider].name, model: m.model, endpoint: endpointOf(m),
            effort: m.provider === 'anthropic' ? (m.effort || 'high') : null, temperature: m.temperature === undefined || m.temperature === '' ? null : Number(m.temperature),
            json_mode: m.provider === 'openai' || m.provider === 'compatible' || m.provider === 'gemini' };
        }),
        results: results
      };
      S.review = {}; S.overrides = {}; S.removes = {};
      log('Done in ' + S.run.seconds + ' s.', 'ok');
      toast('Coding finished. Review the high-stakes labels next.', 'ok');
      changed();
      go('review');
    } catch (e) {
      log('Stopped: ' + e.message, 'err');
    } finally { running = null; renderView(); renderNav(); }
  }

  function endpointOf(m) {
    if (m.provider === 'anthropic') return 'https://api.anthropic.com/v1/messages';
    if (m.provider === 'openai') return 'https://api.openai.com/v1/chat/completions';
    if (m.provider === 'gemini') return 'https://generativelanguage.googleapis.com/v1beta/models/' + m.model + ':generateContent';
    if (m.provider === 'compatible') return String(m.baseUrl || P.compatible.baseUrl).replace(/\/+$/, '') + '/chat/completions';
    return 'local demo coder';
  }

  async function testModel(i) {
    var m = S.models[i], name = modelNames()[i];
    try {
      var r = await L.call(m, 'Reply with the JSON object {"ok": true} and nothing else.', '{"ping": 1}', new AbortController().signal);
      toast(name + ': reachable (' + (r.servedBy || m.model) + ', ' + r.ms + ' ms).', 'ok');
    } catch (e) { toast(name + ': ' + e.message, 'bad'); }
  }

  // ---------- Results ----------

  function reviewItems(combined) {
    return combined.filter(function (r) { return r.decision === 'check' || r.decision === 'proposal' || (r.stage === 3); });
  }

  function build() {
    if (cache) return cache;
    if (!S.run) return null;
    var run = S.run, model = S.model, names = run.names;
    var labels = [].concat.apply([], run.results.map(function (r) { return r.labels.filter(function (l) { return l.run === 1 || l.stage > 1; }); }));
    var all = A.combine(labels, names);
    var rejected = {};
    Object.keys(S.review).forEach(function (k) { if (S.review[k].verdict === 'rejected') rejected[k] = 1; });
    var rejectedHarms = {};
    all.forEach(function (r) { if (r.code === 'L-HRM' && rejected[r.key]) rejectedHarms[r.unit + '|' + r.harm] = 1; });
    var combined = all.filter(function (r) { return !rejected[r.key] && !(r.stage === 2 && rejectedHarms[r.unit + '|' + r.harm]); });
    var items = reviewItems(all);
    var reviewStats = { total: items.length, accepted: 0, rejected: 0 };
    items.forEach(function (r) { var v = S.review[r.key]; if (v) reviewStats[v.verdict]++; });
    reviewStats.pending = reviewStats.total - reviewStats.accepted - reviewStats.rejected;

    var proposal = A.proposeApplicability(model, combined, { countPossible: S.settings.countPossible });
    var states = {};
    Object.keys(proposal).forEach(function (k) { states[k] = S.overrides[k] ? S.overrides[k].state : proposal[k].state; });
    var ev = A.evaluateModel(model, states);
    var hasInterface = run.units.some(function (u) { return u.surface === 'interface'; });
    var cov = {
      policyA: A.coverage(model, combined, 'policy', 'agreed'), policyB: A.coverage(model, combined, 'policy', 'with-uncertain'),
      ifA: A.coverage(model, combined, 'interface', 'agreed'), ifB: A.coverage(model, combined, 'interface', 'with-uncertain')
    };
    var pc = { total: 0, present: 0, absent: 0, uncertain: 0 };
    Object.keys(ev.pathways).forEach(function (k) { pc.total++; pc[ev.pathways[k]]++; });

    var harmRecords = combined.filter(function (r) { return r.code === 'L-HRM'; }).map(function (r) {
      var st = {}, union = {};
      combined.filter(function (x) { return x.stage === 2 && x.unit === r.unit && x.harm === r.harm; }).forEach(function (x) {
        Object.keys(x.by).forEach(function (m) { (st[m] = st[m] || []).push(x.code); }); union[x.code] = 1;
      });
      return { key: r.key, unit: r.unit, harm: r.harm, span: r.span, foundBy: Object.keys(r.by), stances: st, union: Object.keys(union).sort(), verdict: S.review[r.key] && S.review[r.key].verdict };
    });
    var stanceCounts = {};
    harmRecords.forEach(function (h) { h.union.forEach(function (c) { stanceCounts[c] = (stanceCounts[c] || 0) + 1; }); });
    var count = function (code) { return combined.filter(function (r) { return r.code === code; }).length; };

    var paths = A.pathways(model);
    var claimRecords = combined.filter(function (r) { return r.stage === 3 && r.code !== 'C-REA'; }).map(function (r) {
      var removes = S.removes[r.key] || '';
      var rec = { key: r.key, unit: r.unit, code: r.code, span: r.span, framing: r.framing, strength: r.strength,
        foundBy: Object.keys(r.by), decision: r.decision, removes: removes, closes: [], leftOpen: [], verdict: S.review[r.key] && S.review[r.key].verdict };
      if (removes && model.components[removes]) {
        var after = A.afterMeasure(model, states, [removes]);
        paths.forEach(function (p) {
          if (ev.pathways[p.id] !== 'present' || p.components.indexOf(removes) < 0) return;
          (after[p.id] === 'absent' ? rec.closes : rec.leftOpen).push(p.id);
        });
      }
      return rec;
    });

    var levelDeviation = [], applicabilityDeviation = [], single = {};
    names.forEach(function (m) {
      var c = A.singleModelCombined(labels, m);
      single[m] = { cov: A.coverage(model, c, 'policy', 'agreed'), appl: A.proposeApplicability(model, c, { countPossible: S.settings.countPossible }) };
    });
    paths.forEach(function (p) {
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
      if (run.opts.paraphrase) word = A.stability(r.labels.filter(function (l) { return l.stage === 1 && l.run === 1; }).concat(r.wording || []), r.name, 2, run.units);
      perModel[r.name] = { servedBy: r.servedBy, labels: r.labels.filter(function (l) { return l.run === 1 || l.stage > 1; }).length,
        invalidSpans: r.failures.filter(function (f) { return /span/.test(f.reason); }).length, errors: r.errors,
        calls: (r.calls || []).filter(function (c) { return c.ok; }).length, ms: r.ms, tokensIn: r.tokensIn, tokensOut: r.tokensOut,
        stability: stab ? stab.alpha : null, wording: word ? word.alpha : null };
    });
    var compFam = agreement.families.filter(function (f) { return f.id === 'components'; })[0];

    cache = {
      run: run, model: model, models: names, labels: labels, all: all, combined: combined, rejected: rejected, reviewItems: items, reviewStats: reviewStats,
      proposal: proposal, states: states, ev: ev, cov: cov, hasInterface: hasInterface, pathCounts: pc, paths: paths,
      units: { policy: run.units.filter(function (u) { return u.surface === 'policy'; }).length, interface: run.units.filter(function (u) { return u.surface === 'interface'; }).length },
      shares: { policyA: A.levelShares(ev.pathways, cov.policyA, 'A'), policyB: A.levelShares(ev.pathways, cov.policyB, 'B'),
        ifA: A.levelShares(ev.pathways, cov.ifA, 'A'), ifB: A.levelShares(ev.pathways, cov.ifB, 'B') },
      harmRecords: harmRecords, stanceCounts: stanceCounts,
      secondary: { gen: count('L-GEN'), grs: count('S-GRS'), rea: count('C-REA') },
      claimRecords: claimRecords, levelDeviation: levelDeviation, applicabilityDeviation: applicabilityDeviation,
      agreement: agreement, perModel: perModel,
      alphaComponents: compFam && compFam.pairs.length ? (names.length > 2 ? compFam.alphaAll : compFam.pairs[0].alpha) : null,
      failures: [].concat.apply([], run.results.map(function (r) { return r.failures; }))
    };
    return cache;
  }

  // ---------- The YAML record ----------

  async function sha256(text) {
    try {
      var buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text || ''));
      return Array.prototype.map.call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, '0'); }).join('');
    } catch (e) { return null; }
  }

  async function record() {
    var R = build(), run = S.run;
    var model = S.model; // the trees the results use; edits after the run apply to them
    var modelAtRun = run && JSON.stringify(run.model) !== JSON.stringify(S.model) ? run.model : undefined;
    var prompts = {};
    ['stage1', 'stage1p', 'stage2', 'stage3'].forEach(function (k) {
      prompts[k] = { file: DATA.sources[k].path, version: DATA.sources[k].version, file_sha256: DATA.sources[k].sha256, text: DATA.prompts[k] };
    });
    for (var k in prompts) prompts[k].text_sha256 = await sha256(prompts[k].text);
    var rec = {
      format: 'policy-harm-analyzer-record/2',
      generated: localTime(),
      tool: { name: 'Privacy Policy Analyser', subtitle: 'LLM coding against reference harm trees', version: VERSION, location: 'scripts/policy-analyzer/' + VERSION, method: 'Thesis methodology chapter: Coding and Assessment; Instrument Freeze and Validation' },
      environment: { user_agent: navigator.userAgent, language: navigator.language, time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone },
      project: clone(S.project),
      status: {
        automated: true,
        notes: [
          'Labels are produced by language models. High-stakes labels are reviewed by a person (decisions.review).',
          'Applicability, minimisation and potential mismatches are human decisions (decisions.applicability, decisions.measures).',
          'Figures are detection summaries; they are not corrected for model error, which requires a double-coded validation sample.',
          'Absence means not found by the models in the captured text.'
        ],
        reviewed: R ? R.reviewStats : null
      },
      inputs: {
        policy: { source: S.text.policySource || null, characters: S.text.policy.length, sha256: await sha256(S.text.policy), text: S.text.policy },
        interface: { source: S.text.interfaceSource || null, characters: S.text.interface.length, sha256: await sha256(S.text.interface), text: S.text.interface },
        units: (run ? run.units : units()).map(function (u) { return { id: u.id, surface: u.surface, heading: u.heading, text: u.text }; })
      },
      instruments: {
        reference_model: {
          frozen_file: DATA.sources.model.path, frozen_sha256: DATA.sources.model.sha256,
          edited: modelEdited(), edits: clone(S.modelEdits),
          model_sha256: await sha256(JSON.stringify(model)), model: clone(model),
          model_at_run: modelAtRun ? clone(modelAtRun) : undefined
        },
        prompts: prompts,
        rules: {
          unit: 'one policy paragraph or one block of interface text',
          span_check: 'a label whose span is not in its unit is dropped and counted as a model failure',
          combination: 'routine labels kept when every model returns them (agreed), else uncertain; high-stakes labels are the union and checked by a person; minimisation is a proposal',
          applicability: 'proposed from the coded text; CO1 and EX1 assumed present; EX2 and EX3 uncertain; a non-finding is uncertain; decided by the analyst',
          coverage: 'level 0 silent, 1 component, 2 capability, 3 named harm of the category on a pathway the text reaches; denials count as mentions',
          scenarios: 'A: agreed labels and applicable pathways; B: adds uncertain labels and uncertain pathways'
        }
      },
      models: run ? run.configs : S.models.map(function (m, i) { return { name: modelNames()[i], provider: m.provider, model: m.model }; }),
      settings: { units_per_request: S.settings.chunk, stage1_runs: S.settings.runs, paraphrase_run: !!S.settings.paraphrase, count_hedged_as_present: !!S.settings.countPossible }
    };
    if (run) {
      rec.run = {
        id: run.id, started: run.started, finished: run.finished, duration_seconds: run.seconds, settings: run.opts,
        calls: [].concat.apply([], run.results.map(function (r) { return r.calls || []; })),
        per_model: run.results.map(function (r) {
          return { model: r.name, served_by: r.servedBy, calls: (r.calls || []).length, errors: r.errors, milliseconds: r.ms,
            tokens_in: r.tokensIn, tokens_out: r.tokensOut, raw_outputs: r.raw, labels: r.labels, paraphrase_labels: r.wording || [], failures: r.failures };
        })
      };
      rec.decisions = {
        review: Object.keys(S.review).map(function (k) { return Object.assign({ key: k }, S.review[k]); }),
        applicability: Object.keys(R.proposal).map(function (id) {
          return { component: id, proposed: R.proposal[id].state, basis: R.proposal[id].basis, decided: R.states[id],
            changed_by_analyst: !!S.overrides[id], note: S.overrides[id] ? S.overrides[id].note || null : null, at: S.overrides[id] ? S.overrides[id].at : null };
        }),
        measures: Object.keys(S.removes).map(function (k) { return { claim: k, removes_component: S.removes[k] }; })
      };
      rec.results = {
        combined_labels: R.all.map(function (r) {
          return { key: r.key, unit: r.unit, surface: r.surface, stage: r.stage, code: r.code, node: r.node, harm: r.harm, status: r.status,
            decision: r.decision, models: Object.keys(r.by), span: r.span, review: S.review[r.key] ? S.review[r.key].verdict : null };
        }),
        step1: { components: R.states, capabilities: R.ev.capabilities, pathways: R.ev.pathways, harms: R.ev.harms, pathway_counts: R.pathCounts },
        rq1_coverage: {
          shares: { policy_A: R.shares.policyA, policy_B: R.shares.policyB, interface_A: R.hasInterface ? R.shares.ifA : null, interface_B: R.hasInterface ? R.shares.ifB : null },
          pathways: R.paths.map(function (p) {
            return { id: p.id, harm: p.harm, capability: p.capability, applicable: R.ev.pathways[p.id], basis: p.basis,
              assumption_dependent: A.assumptionDependent(R.model, p),
              policy_A: R.cov.policyA[p.id], policy_B: R.cov.policyB[p.id], interface_A: R.hasInterface ? R.cov.ifA[p.id] : null };
          })
        },
        rq2_stance: { named_harms: R.harmRecords, counts: R.stanceCounts, without_named_harm: R.secondary },
        rq3_protection: { claims: R.claimRecords, reassurance: R.secondary.rea },
        rq4_surfaces: R.hasInterface ? rq4(R) : null,
        model_agreement: { families: R.agreement.families, by_value: R.agreement.values, shared_labels: R.agreement.shared, adds: R.agreement.adds,
          per_model: R.perModel, coverage_level_deviation: R.levelDeviation, applicability_deviation: R.applicabilityDeviation }
      };
    }
    return rec;
  }

  function rq4(R) {
    var rows = [], c = { interface_lower: 0, interface_higher: 0, same: 0 };
    R.paths.forEach(function (p) {
      if (R.ev.pathways[p.id] !== 'present') return;
      var a = R.cov.policyA[p.id].level, b = R.cov.ifA[p.id].level;
      if (a > b) c.interface_lower++; else if (b > a) c.interface_higher++; else c.same++;
      rows.push({ pathway: p.id, harm: p.harm, policy: a, interface: b });
    });
    return { counts: c, pathways: rows };
  }

  async function exportYAML() {
    var rec = await record();
    var text = Y.stringify(rec, 'Privacy Policy Analyser record (' + VERSION + ').\nEverything needed to check or repeat this analysis: inputs, instruments, prompts,\nmodels and settings, every call, raw model output, human decisions and results. API keys are never included.');
    download('policy-analysis_' + slug() + '.yaml', 'application/yaml', text);
    toast('Record exported (' + Math.round(text.length / 1024) + ' KB).', 'ok');
    return text;
  }

  function importRecord(text) {
    var rec;
    try { rec = Y.parse(text); } catch (e) { toast('This file could not be read as a record: ' + e.message, 'bad'); return; }
    if (!rec || !/^policy-harm-analyzer-record\//.test(rec.format || '')) { toast('This is not a Privacy Policy Analyser record.', 'bad'); return; }
    if (S.run && !confirm('Open this record? It replaces the current workspace.')) return;
    var w = defaults();
    w.project = rec.project || w.project;
    w.text.policy = rec.inputs && rec.inputs.policy ? rec.inputs.policy.text || '' : '';
    w.text.interface = rec.inputs && rec.inputs.interface ? rec.inputs.interface.text || '' : '';
    w.text.policySource = rec.inputs && rec.inputs.policy ? rec.inputs.policy.source || '' : '';
    if (rec.instruments && rec.instruments.reference_model) { w.model = rec.instruments.reference_model.model; w.modelEdits = rec.instruments.reference_model.edits || []; }
    if (rec.settings) w.settings = { chunk: rec.settings.units_per_request, runs: rec.settings.stage1_runs, paraphrase: rec.settings.paraphrase_run, countPossible: rec.settings.count_hedged_as_present };
    if (rec.models && rec.models.length) w.models = rec.models.map(function (m) { return { provider: m.provider, model: m.model, label: m.name, key: '', effort: m.effort || undefined, temperature: m.temperature === null ? '' : m.temperature, baseUrl: m.provider === 'compatible' && m.endpoint ? m.endpoint.replace(/\/chat\/completions$/, '') : undefined }; });
    if (rec.run) {
      w.run = { id: rec.run.id, started: rec.run.started, finished: rec.run.finished, seconds: rec.run.duration_seconds, opts: rec.run.settings,
        units: rec.inputs.units, names: rec.run.per_model.map(function (r) { return r.model; }), configs: rec.models,
        modelEdited: rec.instruments.reference_model.edited, model: rec.instruments.reference_model.model,
        results: rec.run.per_model.map(function (r) {
          return { name: r.model, servedBy: r.served_by, errors: r.errors, ms: r.milliseconds, tokensIn: r.tokens_in, tokensOut: r.tokens_out,
            raw: r.raw_outputs || [], labels: r.labels || [], wording: r.paraphrase_labels || [], failures: r.failures || [],
            calls: (rec.run.calls || []).filter(function (c) { return c.model === r.model; }), flags: {} };
        }) };
      (rec.decisions && rec.decisions.review || []).forEach(function (d) { w.review[d.key] = { verdict: d.verdict, note: d.note || '', at: d.at, by: d.by }; });
      (rec.decisions && rec.decisions.applicability || []).forEach(function (d) { if (d.changed_by_analyst) w.overrides[d.component] = { state: d.decided, note: d.note || '', at: d.at }; });
      (rec.decisions && rec.decisions.measures || []).forEach(function (d) { w.removes[d.claim] = d.removes_component; });
    }
    w.ui.tab = 'project';
    S = w; S.progress = {}; root.PA.app.S = S;
    changed(); renderAll();
    toast('Record opened' + (rec.run ? ': ' + rec.run.per_model.length + ' models, ' + rec.inputs.units.length + ' units.' : '.'), 'ok');
  }

  // ---------- Other exports ----------

  function download(name, type, data) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(data instanceof Blob ? data : new Blob([data], { type: type }));
    a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }

  function slug() {
    var app = (S.project.app || 'app').replace(/[^\w-]+/g, '_').slice(0, 40);
    return app + '_' + localTime().slice(0, 16).replace(/[T:]/g, '-');
  }

  function exportCSV() {
    if (!S.run) return;
    var rows = [['model', 'run', 'stage', 'unit', 'surface', 'code', 'node', 'harm', 'status', 'framing', 'strength', 'unsure', 'span', 'review']];
    var R = build();
    S.run.results.forEach(function (r) {
      r.labels.concat((r.wording || []).map(function (l) { var c = Object.assign({}, l); c.run = 'paraphrase'; return c; })).forEach(function (l) {
        var v = S.review[A.labelKey(l)];
        rows.push([l.model, l.run, l.stage, l.unit, l.surface, l.code, l.node || '', l.harm || '', l.status || '', l.framing || '', l.strength || '', l.unsure ? 1 : 0, l.span, v ? v.verdict : '']);
      });
    });
    download('labels_' + slug() + '.csv', 'text/csv', '﻿' + rows.map(function (r) {
      return r.map(function (c) { c = String(c); return /[",\n;]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c; }).join(',');
    }).join('\r\n'));
    return R;
  }

  // ---------- Rendering ----------

  var V = root.PA.views;

  function toast(msg, cls) {
    var t = document.createElement('div');
    t.className = 'toast ' + (cls || ''); t.textContent = msg;
    $('toasts').appendChild(t);
    setTimeout(function () { t.style.opacity = '0'; t.style.transition = 'opacity .3s'; setTimeout(function () { t.remove(); }, 320); }, cls === 'bad' ? 6500 : 3500);
  }

  function counts() {
    var R = build();
    return {
      text: units().length || null,
      models: S.models.length,
      review: R ? R.reviewStats.pending : null,
      trees: modelEdited() ? 'edited' : null
    };
  }

  function renderNav() {
    var c = counts(), cur = S.ui.tab;
    $('nav').innerHTML = V.TABS.map(function (g) {
      return '<div class="nav-group"><div class="nav-label">' + g.group + '</div>' + g.items.map(function (t) {
        var badge = '';
        if (t.id === 'text' && c.text) badge = '<span class="count">' + c.text + '</span>';
        if (t.id === 'models') badge = '<span class="count' + (c.models < 2 ? ' warn' : '') + '">' + c.models + '</span>';
        if (t.id === 'review' && c.review !== null) badge = '<span class="count ' + (c.review ? 'warn' : 'ok') + '">' + (c.review || '✓') + '</span>';
        if (t.id === 'trees' && c.trees) badge = '<span class="count warn">edited</span>';
        return '<button data-tab="' + t.id + '"' + (t.id === cur ? ' aria-current="page"' : '') + '>' + V.icon(t.icon) + '<span>' + t.title + '</span>' + badge + '</button>';
      }).join('') + '</div>';
    }).join('');
  }

  function renderFoot() {
    var R = build();
    $('side-foot').innerHTML =
      '<div class="row-s"><span><span class="dot ' + (S.run ? 'ok' : '') + '"></span>' + (S.run ? 'Run ' + S.run.finished.slice(0, 16).replace('T', ' ') : 'No run yet') + '</span></div>' +
      (R ? '<div class="row-s"><span>Reviewed</span><span class="num">' + (R.reviewStats.accepted + R.reviewStats.rejected) + ' / ' + R.reviewStats.total + '</span></div>' : '') +
      '<div class="row-s"><span>Reference model</span><span>v' + DATA.model.version + (modelEdited() ? ' + edits' : '') + '</span></div>' +
      '<div class="row-s"><span>' + (S.saveError ? '<span class="dot bad"></span>Not saved' : '<span class="dot ok"></span>Saved in this browser') + '</span></div>';
  }

  function renderView() {
    var tab = V.byId(S.ui.tab) || V.byId('project');
    var ctx = ctxObj();
    $('view-title').textContent = tab.title;
    $('view-crumb').textContent = tab.crumb ? tab.crumb(ctx) : '';
    $('top-actions').innerHTML = tab.actions ? tab.actions(ctx) : '';
    $('top-actions').onclick = null;
    // A fresh element per render: views bind their listeners in mount(), and
    // reusing the element would stack them, so one click would act several times.
    var old = $('view');
    var keep = old.dataset.tab === tab.id ? old.scrollTop : 0;
    var view = old.cloneNode(false);
    old.parentNode.replaceChild(view, old);
    view.className = 'view' + (tab.full ? ' full' : '');
    view.innerHTML = tab.render(ctx);
    view.dataset.tab = tab.id;
    if (tab.mount) tab.mount(view, ctx);
    view.scrollTop = keep;
  }

  function renderAll() { renderNav(); renderView(); renderFoot(); }

  function go(tab) {
    if (S.ui.tab === tab) return;
    var prev = V.byId(S.ui.tab);
    if (prev && prev.unmount) prev.unmount();
    S.ui.tab = tab; save(); renderAll();
    $('view').scrollTop = 0; $('view').focus({ preventScroll: true });
  }

  function ctxObj() {
    return { S: S, R: build(), DATA: DATA, units: units, modelNames: modelNames, editedIds: editedIds, modelEdited: modelEdited,
      running: !!running, P: P };
  }

  // ---------- Start ----------

  function init() {
    if (!DATA) { document.body.innerHTML = '<p style="padding:2em;font-family:sans-serif">output/data.js is missing. Run <code>python build_data.py</code> in this folder first.</p>'; return; }
    load();
    $('nav').addEventListener('click', function (e) { var b = e.target.closest('button[data-tab]'); if (b) go(b.dataset.tab); });
    // Light or dark: a per-browser preference, not part of the analysis record.
    function syncTheme() {
      var light = document.documentElement.dataset.theme === 'light', label = light ? 'Switch to dark theme' : 'Switch to light theme';
      $('theme-toggle').setAttribute('aria-label', label); $('theme-toggle').title = label;
    }
    $('theme-toggle').addEventListener('click', function () {
      var light = document.documentElement.dataset.theme !== 'light';
      if (light) document.documentElement.dataset.theme = 'light'; else delete document.documentElement.dataset.theme;
      try { localStorage.setItem('pa.theme', light ? 'light' : 'dark'); } catch (e) { /* storage unavailable */ }
      syncTheme();
    });
    syncTheme();
    document.addEventListener('keydown', function (e) {
      if (e.target.matches('input, textarea, select')) return;
      if (e.altKey && /^[1-9]$/.test(e.key)) {
        var flat = [].concat.apply([], V.TABS.map(function (g) { return g.items; }));
        var t = flat[+e.key - 1]; if (t) { e.preventDefault(); go(t.id); }
      }
      var tab = V.byId(S.ui.tab);
      if (tab && tab.key) tab.key(e, ctxObj());
    });
    window.addEventListener('beforeunload', function (e) { if (running) { e.preventDefault(); e.returnValue = ''; } });
    renderAll();
  }

  root.PA.app = {
    get S() { return S; }, set S(v) { S = v; },
    VERSION: VERSION, changed: changed, save: save, go: go, render: renderView, renderAll: renderAll, renderNav: renderNav, renderFoot: renderFoot,
    toast: toast, download: download, slug: slug, startRun: startRun, stop: function () { if (running) running.abort(); },
    testModel: testModel, build: build, record: record, exportYAML: exportYAML, importRecord: importRecord, exportCSV: exportCSV,
    logEdit: logEdit, editedIds: editedIds, modelEdited: modelEdited, units: units, modelNames: modelNames, defaults: defaults,
    reset: function () { S = defaults(); S.progress = {}; changed(); renderAll(); },
    isRunning: function () { return !!running; }, localTime: localTime, clone: clone, sha256: sha256
  };
  document.addEventListener('DOMContentLoaded', init);
})(window);
