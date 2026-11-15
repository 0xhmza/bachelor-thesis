// The views (tabs) of the Privacy Policy Analyser. Each view renders HTML from
// the workspace and the computed results, and binds its own events. Policy
// text and model output are untrusted: everything from them goes through esc().
(function (root) {
  'use strict';
  var A = root.PA.analysis;
  var app = function () { return root.PA.app; };

  // ---------- Helpers ----------

  function esc(s) {
    return String(s === null || s === undefined ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pct(x) { return x === null || x === undefined || isNaN(x) ? '–' : (100 * x).toFixed(0) + '%'; }
  function num(x, d) { return x === null || x === undefined || isNaN(x) ? '–' : x.toFixed(d === undefined ? 2 : d); }
  function badge(state, text) { return '<span class="badge ' + esc(state) + '">' + esc(text || state) + '</span>'; }
  function lvl(l) { return '<span class="lv lv' + l + '">L' + l + '</span>'; }
  function cmp(model, id) {
    var c = model.components[id];
    return '<span class="cmp o-' + esc(c ? c.origin : 'external') + '" title="' + esc(c ? c.label : 'unknown') + '">' + esc(id) + '</span>';
  }
  function table(head, rows, opts) {
    opts = opts || {};
    return '<div class="tw' + (opts.tall ? ' tall' : '') + '"><table><thead><tr>' + head.map(function (h) {
      var n = /^#/.test(h); return '<th' + (n ? ' class="num"' : '') + '>' + (n ? h.slice(1) : h) + '</th>';
    }).join('') + '</tr></thead><tbody>' + (rows.length ? rows.map(function (r) {
      return '<tr' + (r.cls ? ' class="' + r.cls + '"' : '') + '>' + (r.cells || r).map(function (c, i) {
        return '<td' + (/^#/.test(head[i]) ? ' class="num"' : '') + '>' + c + '</td>';
      }).join('') + '</tr>';
    }).join('') : '<tr><td colspan="' + head.length + '" class="faint">None.</td></tr>') + '</tbody></table></div>';
  }
  function empty(title, text, action) {
    return '<div class="view-inner"><div class="card empty"><h3>' + title + '</h3><p class="muted">' + text + '</p>' + (action || '') + '</div></div>';
  }
  function needRun() {
    return empty('No results yet', 'Add the policy text and two models, then run the coding. Results appear here.',
      '<button class="btn primary" data-go="run">Go to Run</button>');
  }
  function bindGo(el) {
    el.addEventListener('click', function (e) { var b = e.target.closest('[data-go]'); if (b) app().go(b.dataset.go); });
  }
  function stack(shares) {
    var colors = ['var(--lv0)', 'var(--lv1)', 'var(--lv2)', 'var(--lv3)'];
    return '<div class="stack" title="' + shares.map(function (s, i) { return 'L' + i + ' ' + pct(s); }).join(', ') + '">' +
      shares.map(function (s, i) { return '<i style="width:' + (100 * (s || 0)) + '%;background:' + colors[i] + '"></i>'; }).join('') + '</div>';
  }

  var ICONS = {
    folder: 'M2 4.5h4l1.5 1.5H14v6.5a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z',
    text: 'M3 3h10M3 6h10M3 9h7M3 12h9',
    cpu: 'M5 5h6v6H5zM6.5 2v2M9.5 2v2M6.5 12v2M9.5 12v2M2 6.5h2M2 9.5h2M12 6.5h2M12 9.5h2',
    play: 'M5 3.5v9l7-4.5z',
    tree: 'M6 2h4v3H6zM8 5v2M4 7h8M4 7v2M12 7v2M2 9h4v4H2zM10 9h4v4h-4z',
    doc: 'M4 2h6l3 3v9H4zM10 2v3h3M6 8h5M6 11h5',
    highlight: 'M3 13h10M5 10l5-7 2 1.5-5 7H5z',
    check: 'M3 8.5l3 3 7-7',
    toggle: 'M2 5.5h12M2 10.5h12M5 4v3M11 9v3',
    layers: 'M8 2l6 3-6 3-6-3zM2 8l6 3 6-3M2 11l6 3 6-3',
    message: 'M2 3h12v8H6l-3 3v-3H2z',
    shield: 'M8 2l5 2v4c0 3-2.2 5-5 6-2.8-1-5-3-5-6V4z',
    columns: 'M2 3h5v10H2zM9 3h5v10H9z',
    scale: 'M8 2v12M3 14h10M3 5h10M5 5l-2 5h4zM11 5l-2 5h4z',
    download: 'M8 2v8M5 7l3 3 3-3M3 13h10'
  };
  function icon(name) {
    return '<svg class="ico" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + ICONS[name] + '"/></svg>';
  }

  var FAMILY_OF = function (r) {
    if (r.stage === 2) return 'stance';
    if (r.stage === 3) return 'prot';
    if (r.code === 'L-CMP') return 'cmp';
    if (r.code === 'L-CAP') return 'cap';
    if (r.code === 'L-HRM') return 'hrm';
    if (r.code === 'L-GEN' || r.code === 'S-GRS') return 'gen';
    return 'gen';
  };
  var FAMILY_NAMES = { cmp: 'Component', cap: 'Capability', hrm: 'Named harm', gen: 'Generic risk / other', prot: 'Protection', stance: 'Stance' };
  var FAMILY_COLORS = { cmp: '#7fa6cf', cap: '#b58cf0', hrm: '#e5675e', gen: '#e2b54a', prot: '#43b98a', stance: '#f08a63' };

  function labelText(r) { return r.code + (r.node ? ' ' + r.node : '') + (r.harm && r.stage !== 2 ? ' ' + r.harm : '') + (r.stage === 2 ? ' (' + r.harm + ')' : ''); }

  // Text of a unit with the spans of the given labels marked.
  function marked(text, labels, selKey) {
    var cuts = {}, ranges = [];
    labels.forEach(function (r) {
      var g = A.spanRange(r.span, text);
      if (!g) return;
      ranges.push({ a: g[0], b: g[1], r: r });
      cuts[g[0]] = 1; cuts[g[1]] = 1;
    });
    cuts[0] = 1; cuts[text.length] = 1;
    var pts = Object.keys(cuts).map(Number).sort(function (x, y) { return x - y; });
    var out = '';
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1], seg = esc(text.slice(a, b));
      var on = ranges.filter(function (g) { return g.a <= a && g.b >= b; });
      if (!on.length) { out += seg; continue; }
      var fam = FAMILY_OF(on[0].r);
      var title = on.map(function (g) { return labelText(g.r) + ' · ' + g.r.decision + ' · ' + Object.keys(g.r.by).join(', '); }).join('\n');
      var sel = selKey && on.some(function (g) { return g.r.key === selKey; });
      out += '<mark class="f-' + fam + (on.length > 1 ? ' multi' : '') + '" style="' + (sel ? 'outline:1px solid var(--accent);' : '') + '" title="' + esc(title) + '" data-unit="' + esc(on[0].r.unit) + '">' + seg + '</mark>';
    }
    return out;
  }

  // ---------- Tabs ----------

  var TABS = [
    { group: 'Setup', items: [
      { id: 'project', title: 'Project', icon: 'folder' },
      { id: 'text', title: 'Text', icon: 'text' },
      { id: 'models', title: 'Models', icon: 'cpu' },
      { id: 'run', title: 'Run', icon: 'play' }] },
    { group: 'Instruments', items: [
      { id: 'trees', title: 'Harm trees', icon: 'tree' },
      { id: 'prompts', title: 'Prompts', icon: 'doc' }] },
    { group: 'Review', items: [
      { id: 'coded', title: 'Coded text', icon: 'highlight' },
      { id: 'review', title: 'Review queue', icon: 'check' },
      { id: 'applicability', title: 'Applicability', icon: 'toggle' }] },
    { group: 'Results', items: [
      { id: 'coverage', title: 'RQ1 Coverage', icon: 'layers' },
      { id: 'stance', title: 'RQ2 Stance', icon: 'message' },
      { id: 'protection', title: 'RQ3 Protection', icon: 'shield' },
      { id: 'surfaces', title: 'RQ4 Surfaces', icon: 'columns' },
      { id: 'agreement', title: 'Model agreement', icon: 'scale' }] },
    { group: 'Record', items: [
      { id: 'export', title: 'Export', icon: 'download' }] }
  ];
  var VIEWS = {};
  function byId(id) {
    var meta = null;
    TABS.forEach(function (g) { g.items.forEach(function (t) { if (t.id === id) meta = t; }); });
    if (!meta || !VIEWS[id]) return null;
    return Object.assign({ id: id, title: meta.title }, VIEWS[id]);
  }

  // ---------- Project ----------

  VIEWS.project = {
    crumb: function (c) { return c.S.project.app || 'Unnamed project'; },
    render: function (c) {
      var S = c.S, R = c.R, us = c.units();
      var steps = [
        ['text', 'Policy text added', us.some(function (u) { return u.surface === 'policy'; }), us.length + ' units'],
        ['models', 'Two or more models set up', S.models.length >= 2 && S.models.every(function (m) { return m.model && (m.key || !c.P[m.provider].needsKey); }), S.models.length + ' models'],
        ['run', 'Text coded by every model', !!S.run, S.run ? S.run.finished.slice(0, 16).replace('T', ' ') : 'not run'],
        ['review', 'High-stakes labels reviewed', R && R.reviewStats.pending === 0 && R.reviewStats.total > 0, R ? (R.reviewStats.accepted + R.reviewStats.rejected) + ' of ' + R.reviewStats.total : '–'],
        ['applicability', 'Applicability decided', R && Object.keys(S.overrides).length > 0, R ? Object.keys(S.overrides).length + ' components changed' : '–'],
        ['export', 'Record exported', false, 'YAML with everything']
      ];
      return '<div class="view-inner"><p class="lead">Codes one health tracker\'s privacy policy and interface text with several language models, against the reference harm trees of the thesis, then reports coverage (RQ1), stance (RQ2), protection (RQ3), surfaces (RQ4) and how far the models deviate. People review every high-stakes label and decide applicability.</p>' +
        '<div class="grid g2"><div class="card"><h3>Project</h3>' +
        '<label class="field"><span>App</span><input data-p="app" value="' + esc(S.project.app) + '" placeholder="App name and platform"></label>' +
        '<label class="field"><span>Analyst</span><input data-p="analyst" value="' + esc(S.project.analyst) + '" placeholder="Who reviews and decides"></label>' +
        '<label class="field"><span>Notes</span><textarea data-p="notes" rows="4" placeholder="Capture date, app version, anything a reader needs">' + esc(S.project.notes) + '</textarea></label>' +
        '<p class="xs faint">Created ' + esc(S.project.created) + '. Everything is kept in this browser and goes into the exported record.</p></div>' +
        '<div class="card"><h3>Workflow</h3><div class="tw"><table><tbody>' + steps.map(function (s, i) {
          return '<tr><td style="width:30px"><span class="dot ' + (s[2] ? 'ok' : '') + '"></span></td><td><a href="#" data-go="' + s[0] + '">' + (i + 1) + '. ' + s[1] + '</a></td><td class="faint small">' + esc(s[3]) + '</td></tr>';
        }).join('') + '</tbody></table></div>' +
        '<h4>Shortcuts</h4><p class="small muted"><kbd>Alt</kbd>+<kbd>1</kbd>…<kbd>9</kbd> switch tabs · in the review queue <kbd>A</kbd> accept, <kbd>R</kbd> reject, <kbd>J</kbd>/<kbd>K</kbd> next and previous · in the trees, scroll to zoom, drag to pan, double-click a capability to fold it.</p></div></div>' +
        '<div class="card"><h3>Workspace</h3><div class="row">' +
        '<button class="btn" data-act="example">Load constructed example</button>' +
        '<label class="btn" style="cursor:pointer">Open record (.yaml)<input type="file" accept=".yaml,.yml" data-act="open" hidden></label>' +
        '<button class="btn danger" data-act="reset">New empty project</button></div>' +
        '<p class="xs faint" style="margin-top:10px">A record exported from the Export tab reopens the whole analysis: text, models (without keys), settings, raw output, review and applicability decisions, and tree edits.</p></div></div>';
    },
    mount: function (el, c) {
      bindGo(el);
      el.addEventListener('input', function (e) {
        var k = e.target.dataset.p; if (!k) return;
        c.S.project[k] = e.target.value; app().changed(false);
        if (k === 'app') document.getElementById('view-crumb').textContent = e.target.value || 'Unnamed project';
      });
      el.addEventListener('click', function (e) {
        var a = e.target.closest('[data-act]'); if (!a) return;
        if (a.dataset.go) return;
        if (a.dataset.act === 'example') {
          var X = root.PA_EXAMPLE;
          c.S.project.app = X.app; c.S.text.policy = X.policy; c.S.text.interface = X.interface; c.S.text.policySource = 'constructed example';
          app().changed(); app().renderAll(); app().toast('Example loaded. Choose models next, or the offline demo coders.', 'ok');
        }
        if (a.dataset.act === 'reset' && confirm('Start a new empty project? Export the record first if you need this one.')) app().reset();
      });
      el.addEventListener('change', function (e) {
        if (e.target.dataset.act !== 'open' || !e.target.files[0]) return;
        var r = new FileReader(); r.onload = function () { app().importRecord(String(r.result)); }; r.readAsText(e.target.files[0]);
      });
    }
  };

  // ---------- Text ----------

  function unitList(us) {
    if (!us.length) return '<p class="faint small">No units yet.</p>';
    return '<div class="units">' + us.slice(0, 400).map(function (u) {
      return '<div class="unit"><div class="uid">' + esc(u.id) + '</div><div>' + (u.heading ? '<div class="uh">' + esc(u.heading) + '</div>' : '') + '<div class="ut">' + esc(u.text) + '</div></div></div>';
    }).join('') + '</div>';
  }

  VIEWS.text = {
    crumb: function (c) { var us = c.units(); return us.filter(function (u) { return u.surface === 'policy'; }).length + ' policy units · ' + us.filter(function (u) { return u.surface === 'interface'; }).length + ' interface units'; },
    render: function (c) {
      var S = c.S;
      return '<div class="view-inner wide"><div class="split" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)"><div>' +
        '<div class="card"><div class="row" style="margin-bottom:8px"><h3 style="margin:0">Privacy policy</h3><span class="grow"></span>' +
        '<label class="btn sm" style="cursor:pointer">Open .txt / .html<input type="file" accept=".txt,.md,.html,.htm" data-file="policy" hidden></label></div>' +
        '<label class="field"><span>Source (URL or file, capture date)</span><input data-t="policySource" value="' + esc(S.text.policySource) + '" placeholder="https://… , captured 2026-11-06"></label>' +
        '<textarea data-t="policy" rows="16" placeholder="Paste the privacy policy. Paragraphs separated by a blank line become coding units; a short line without a full stop is a heading.">' + esc(S.text.policy) + '</textarea></div>' +
        '<div class="card"><div class="row" style="margin-bottom:8px"><h3 style="margin:0">Interface text <span class="faint small">(optional, RQ4)</span></h3><span class="grow"></span>' +
        '<label class="btn sm" style="cursor:pointer">Open file<input type="file" accept=".txt,.md,.html,.htm" data-file="interface" hidden></label></div>' +
        '<label class="field"><span>Source (walkthrough, app version, screen)</span><input data-t="interfaceSource" value="' + esc(S.text.interfaceSource) + '" placeholder="Walkthrough of v4.2, Android 16"></label>' +
        '<textarea data-t="interface" rows="7" placeholder="Onboarding, consent and privacy-settings text, one block per screen element, a blank line between blocks.">' + esc(S.text.interface) + '</textarea></div></div>' +
        '<div class="card sticky"><h3>Coding units</h3><p class="xs faint">What every model receives. ' + (S.run ? 'The current results were coded from the units saved with the run.' : '') + '</p><div id="unit-preview">' + unitList(c.units()) + '</div></div></div></div>';
    },
    mount: function (el, c) {
      var t = null;
      el.addEventListener('input', function (e) {
        var k = e.target.dataset.t; if (!k) return;
        c.S.text[k] = e.target.value; app().changed(false);
        clearTimeout(t);
        t = setTimeout(function () { document.getElementById('unit-preview').innerHTML = unitList(c.units()); app().renderNav(); document.getElementById('view-crumb').textContent = VIEWS.text.crumb(c); }, 250);
      });
      el.addEventListener('change', function (e) {
        var k = e.target.dataset.file; if (!k || !e.target.files[0]) return;
        var f = e.target.files[0], r = new FileReader();
        r.onload = function () {
          var s = String(r.result);
          c.S.text[k] = /\.html?$/i.test(f.name) || /^\s*</.test(s) ? A.htmlToText(s) : s;
          c.S.text[k + 'Source'] = f.name + ' (opened ' + app().localTime().slice(0, 10) + ')';
          app().changed(false); app().render(); app().renderNav();
        };
        r.readAsText(f);
      });
    }
  };

  // ---------- Models ----------

  VIEWS.models = {
    crumb: function (c) { return c.S.models.length + ' models · keys stay in this browser'; },
    actions: function () { return '<button class="btn" data-act="demo">Use offline demo coders</button><button class="btn primary" data-act="add">Add model</button>'; },
    render: function (c) {
      var S = c.S, P = c.P, names = c.modelNames();
      var us = c.units(), per = Math.ceil(us.length / Math.max(1, S.settings.chunk || 15)) * ((+S.settings.runs || 1) + (S.settings.paraphrase ? 1 : 0));
      return '<div class="view-inner"><p class="lead">The method codes every unit with two models of different families, with the same prompts. Prefer an open-weight model for one of them. A key is sent only to its own provider.</p>' +
        S.models.map(function (m, i) {
          var p = P[m.provider];
          var f = function (label, html) { return '<label class="field"><span>' + label + '</span>' + html + '</label>'; };
          return '<div class="model" data-i="' + i + '"><div class="model-head"><span class="idx">' + (i + 1) + '</span><strong>' + esc(names[i]) + '</strong><span class="faint small">' + esc(p.name) + '</span><span class="grow" style="flex:1"></span>' +
            '<button class="btn sm" data-test="' + i + '">Test connection</button><button class="btn sm ghost danger" data-del="' + i + '" aria-label="Remove model">Remove</button></div><div class="model-body">' +
            f('Name', '<input data-f="label" value="' + esc(m.label || '') + '" placeholder="Model ' + (i + 1) + '">') +
            f('Provider', '<select data-f="provider">' + Object.keys(P).map(function (k) { return '<option value="' + k + '"' + (k === m.provider ? ' selected' : '') + '>' + esc(P[k].name) + '</option>'; }).join('') + '</select>') +
            f('Model id', '<input data-f="model" value="' + esc(m.model || '') + '" placeholder="' + (m.provider === 'demo' ? 'demo-a or demo-b' : 'exact model id') + '">') +
            (m.provider === 'demo' ? '' : f('API key' + (p.needsKey ? '' : ' (optional)'), '<input data-f="key" type="password" autocomplete="off" spellcheck="false" value="' + esc(m.key || '') + '">')) +
            (m.provider === 'compatible' || m.provider === 'bridge' ? f('Base URL', '<input data-f="baseUrl" value="' + esc(m.baseUrl || p.baseUrl) + '">') : '') +
            (m.provider === 'anthropic' ? f('Effort', '<select data-f="effort">' + ['low', 'medium', 'high', 'xhigh', 'max'].map(function (e) { return '<option' + (e === (m.effort || 'high') ? ' selected' : '') + '>' + e + '</option>'; }).join('') + '</select>') : '') +
            (/openai|gemini|compatible/.test(m.provider) ? f('Temperature', '<input data-f="temperature" value="' + esc(m.temperature === undefined ? '' : m.temperature) + '" placeholder="model default">') : '') +
            '</div><div class="hint">' + esc(p.hint) + '</div></div>';
        }).join('') +
        '<label class="check" style="margin:4px 0 20px"><input type="checkbox" data-s="remember"' + (S.remember ? ' checked' : '') + '> Remember API keys in this browser (otherwise they are forgotten when the page closes)</label>' +
        '<div class="card"><h3>Coding settings</h3><div class="grid g4">' +
        '<label class="field"><span>Units per request</span><input type="number" min="1" max="60" data-set="chunk" value="' + esc(S.settings.chunk) + '"></label>' +
        '<label class="field"><span>Stage 1 runs per model</span><input type="number" min="1" max="3" data-set="runs" value="' + esc(S.settings.runs) + '"></label>' +
        '<label class="field"><span>Paraphrased prompt</span><select data-set="paraphrase"><option value="">no</option><option value="1"' + (S.settings.paraphrase ? ' selected' : '') + '>also run stage1_coverage_v2p</option></select></label>' +
        '<label class="field"><span>Hedged mentions (“may”)</span><select data-set="countPossible"><option value="1">count as present</option><option value=""' + (S.settings.countPossible ? '' : ' selected') + '>leave uncertain</option></select></label>' +
        '</div><p class="small muted">About <strong class="num">' + per + '</strong> stage 1 calls per model, plus stage 2 and 3 calls for the named harms and protection claims found. Two or three runs measure run-to-run stability; the paraphrased prompt measures sensitivity to wording.</p></div></div>';
    },
    mount: function (el, c) {
      var S = c.S;
      el.addEventListener('input', function (e) {
        var box = e.target.closest('.model');
        if (box && e.target.dataset.f) {
          var m = S.models[+box.dataset.i], f = e.target.dataset.f;
          m[f] = e.target.value;
          if (f === 'provider') { m.model = c.P[m.provider].model; if (c.P[m.provider].baseUrl) m.baseUrl = c.P[m.provider].baseUrl; app().changed(false); app().render(); return; }
          app().changed(false);
          if (f === 'label') box.querySelector('.model-head strong').textContent = c.modelNames()[+box.dataset.i];
        }
        if (e.target.dataset.set) {
          var k = e.target.dataset.set, v = e.target.value;
          S.settings[k] = (k === 'paraphrase' || k === 'countPossible') ? !!v : +v;
          app().changed(k === 'countPossible');
        }
      });
      el.addEventListener('change', function (e) {
        if (e.target.dataset.s === 'remember') { S.remember = e.target.checked; app().changed(false); }
        if (e.target.dataset.set) { app().render(); }
      });
      el.addEventListener('click', function (e) {
        if (e.target.dataset.del !== undefined) { S.models.splice(+e.target.dataset.del, 1); app().changed(false); app().renderAll(); }
        if (e.target.dataset.test !== undefined) app().testModel(+e.target.dataset.test);
      });
      document.getElementById('top-actions').onclick = function (e) {
        var a = e.target.closest('[data-act]'); if (!a) return;
        if (a.dataset.act === 'add') S.models.push({ provider: 'openai', model: '', key: '', label: '' });
        if (a.dataset.act === 'demo') S.models = [{ provider: 'demo', model: 'demo-a', label: 'Demo A' }, { provider: 'demo', model: 'demo-b', label: 'Demo B' }];
        app().changed(false); app().renderAll();
      };
    }
  };

  // ---------- Run ----------

  VIEWS.run = {
    crumb: function (c) { return c.running ? 'Coding…' : (c.S.run ? 'Last run ' + c.S.run.finished.slice(0, 16).replace('T', ' ') : 'Not run yet'); },
    actions: function (c) {
      return c.running ? '<button class="btn bad" data-act="stop">Stop</button>' : '<button class="btn primary" data-act="start">' + icon('play') + 'Run coding</button>';
    },
    render: function (c) {
      var S = c.S, names = c.modelNames(), us = c.units(), prog = S.progress || {};
      var bars = Object.keys(prog).length ? Object.keys(prog).map(function (n) {
        var p = prog[n];
        return '<div class="mprog"><strong>' + esc(n) + '</strong><progress max="' + p.total + '" value="' + p.done + '"></progress><span class="faint small num">' + p.done + ' / ' + p.total + ' calls</span></div>';
      }).join('') : '<p class="faint small">Progress per model appears here during a run.</p>';
      var res = '';
      if (S.run && !c.running) {
        var R = c.R;
        res = '<div class="grid g4">' +
          stat('Units coded', S.run.units.length, S.run.units.filter(function (u) { return u.surface === 'interface'; }).length + ' interface') +
          stat('Duration', S.run.seconds + ' s', S.run.started.slice(0, 16).replace('T', ' ')) +
          stat('Calls', S.run.results.reduce(function (a, r) { return a + (r.calls || []).filter(function (x) { return x.ok; }).length; }, 0), S.run.results.reduce(function (a, r) { return a + r.errors; }, 0) + ' failed') +
          stat('Tokens in / out', S.run.results.reduce(function (a, r) { return a + (r.tokensIn || 0); }, 0) + ' / ' + S.run.results.reduce(function (a, r) { return a + (r.tokensOut || 0); }, 0), 'models that report them') +
          '</div><div class="row" style="margin-bottom:16px"><button class="btn primary" data-go="review">Review ' + R.reviewStats.pending + ' high-stakes labels</button><button class="btn" data-go="coded">See the coded text</button></div>';
      }
      return '<div class="view-inner">' +
        '<div class="card"><h3>Ready to code</h3><p class="muted small">' + us.length + ' units · models: ' + names.map(esc).join(', ') + ' · ' + S.settings.chunk + ' units per request · ' + S.settings.runs + ' stage 1 run' + (S.settings.runs > 1 ? 's' : '') + (S.settings.paraphrase ? ' + paraphrase' : '') + '</p>' +
        '<p class="xs faint">Stage 1 codes nodes, harms and risks in every unit; stage 2 codes the stance of each named harm (union of the models); stage 3 describes each protection claim (union). The prompts are the frozen files under 04_Study/4.6_Coding/Prompts.</p>' + bars + '</div>' + res +
        '<div class="card flush"><div class="card-head"><h3>Log</h3></div><ul class="log">' + (S.runLog || []).map(function (l) {
          return '<li class="' + esc(l.cls) + '">' + esc(l.t) + '  ' + esc(l.msg) + '</li>';
        }).join('') + '</ul></div></div>';
    },
    mount: function (el) {
      bindGo(el);
      document.getElementById('top-actions').onclick = function (e) {
        var a = e.target.closest('[data-act]'); if (!a) return;
        if (a.dataset.act === 'start') app().startRun(); else app().stop();
        setTimeout(app().render, 0);
      };
    }
  };
  function stat(k, v, s) { return '<div class="stat"><div class="k">' + k + '</div><div class="v">' + v + '</div><div class="s">' + s + '</div></div>'; }

  // ---------- Harm trees ----------

  var treeView = null;

  function inspector(c) {
    var S = c.S, M = S.model, sel = S.ui.selected, R = c.R;
    var ids = Object.keys(M.components);
    var problems = A.checkModel(M);
    var html = '';
    var palette = '<div class="palette">' + ids.map(function (id) { return '<span class="cmp o-' + M.components[id].origin + '" data-ins="' + id + '" title="' + esc(M.components[id].label) + '">' + id + '</span>'; }).join('') + '</div>';
    var capOptions = function (cur) { return Object.keys(M.capabilities).map(function (k) { return '<option value="' + k + '"' + (k === cur ? ' selected' : '') + '>' + k + ' – ' + esc(M.capabilities[k].label) + '</option>'; }).join(''); };
    var harmOptions = function (cur) { return Object.keys(M.harms).map(function (h) { return '<option value="' + h + '"' + (h === cur ? ' selected' : '') + '>' + h + ' – ' + esc(M.harms[h].label) + '</option>'; }).join(''); };
    var types = ['K-INF', 'K-TRK', 'K-ACC', 'K-DIS', 'K-INC'];
    var field = function (label, inner) { return '<label class="field"><span>' + label + '</span>' + inner + '</label>'; };

    if (sel && sel.mode === 'add-pathway') {
      html += '<div class="section"><h3>Add a pathway</h3><p class="xs faint">A pathway is a capability that can lead to a harm. Pick an existing capability or define a new one with its term.</p>' +
        field('Harm', '<select data-n="harm">' + harmOptions(sel.harm) + '<option value="__new">+ New harm category…</option></select>') +
        '<div data-newharm hidden class="grid g2">' + field('ID', '<input data-n="harmId" placeholder="H-NEW">') + field('Label', '<input data-n="harmLabel" placeholder="Category name">') + '</div>' +
        field('Capability', '<select data-n="cap"><option value="__new">+ New capability…</option>' + capOptions('K5') + '</select>') +
        '<div data-newcap>' + field('Capability label', '<input data-n="capLabel" placeholder="What the actor can do">') +
        '<div class="grid g2">' + field('Actor', '<input data-n="capActor" placeholder="Who gains it">') + field('Type', '<select data-n="capType">' + types.map(function (t) { return '<option>' + t + '</option>'; }).join('') + '</select>') + '</div>' +
        field('Needs (term)', '<input class="mono" data-n="term" placeholder="IM3 AND (CX2 OR CX3)">') + '<div data-termmsg class="xs faint">Click components to insert them. Use AND, OR and brackets.</div>' + palette + '</div>' +
        field('Consequence', '<input data-n="consequence" placeholder="The harm this pathway leads to">') +
        '<div class="grid g2">' + field('Basis', '<select data-n="basis"><option>documented</option><option>argued</option></select>') + field('Tag', '<input data-n="tag" placeholder="T-REL (optional)">') + '</div>' +
        field('Sources (one per line, with page or section)', '<textarea data-n="sources" rows="2" placeholder="knabenhans2026harms App. A"></textarea>') +
        '<div class="row"><button class="btn primary" data-do="add-pathway">Add pathway</button><button class="btn ghost" data-do="cancel">Cancel</button></div></div>';
    } else if (sel && sel.mode === 'add-component') {
      html += '<div class="section"><h3>Add a component</h3><p class="xs faint">A feature that can be checked on an app. New components are not in the frozen prompts, so the models cannot code them: set their applicability by hand.</p>' +
        field('Origin', '<select data-n="origin"><option value="implementation">implementation choice (IM)</option><option value="core">core functionality (CO)</option><option value="context">digital context (CX)</option><option value="external">event outside the app (EX)</option></select>') +
        field('Label', '<input data-n="label" placeholder="Short name">') + field('Feature to check', '<textarea data-n="feature" rows="3" placeholder="What makes it present on an app"></textarea>') +
        '<div class="row"><button class="btn primary" data-do="add-component">Add component</button><button class="btn ghost" data-do="cancel">Cancel</button></div></div>';
    } else if (sel && sel.type === 'comp') {
      var comp = M.components[sel.id];
      var usedBy = Object.keys(M.capabilities).filter(function (k) { return A.leaves(M.capabilities[k].needs).indexOf(sel.id) >= 0; });
      html += '<div class="section"><div class="row"><span class="cmp o-' + comp.origin + '">' + sel.id + '</span><strong>' + esc(comp.label) + '</strong></div>' +
        (R ? '<p class="small" style="margin-top:8px">Applicability: ' + badge(R.states[sel.id]) + ' <span class="faint xs">' + esc(R.proposal[sel.id] ? R.proposal[sel.id].basis : '') + '</span></p>' : '') +
        '<p class="xs faint">Used by ' + (usedBy.join(', ') || 'no capability') + '.</p>' +
        field('Label', '<input data-n="label" value="' + esc(comp.label) + '">') +
        field('Origin', '<select data-n="origin">' + ['core', 'context', 'implementation', 'external'].map(function (o) { return '<option' + (o === comp.origin ? ' selected' : '') + '>' + o + '</option>'; }).join('') + '</select>') +
        field('Feature to check', '<textarea data-n="feature" rows="3">' + esc(comp.feature) + '</textarea>') +
        '<div class="row"><button class="btn primary" data-do="save-component">Save</button>' + (usedBy.length ? '' : '<button class="btn danger" data-do="delete-component">Delete</button>') + '</div></div>';
    } else if (sel && sel.type === 'cap') {
      var harm = M.harms[sel.harm], pw = harm && harm.pathways.filter(function (p) { return p.id === sel.pathway; })[0];
      if (pw) {
        var cap = M.capabilities[pw.capability];
        var shared = [];
        Object.keys(M.harms).forEach(function (h) { M.harms[h].pathways.forEach(function (p) { if (p.capability === pw.capability) shared.push(p.id); }); });
        html += '<div class="section"><h3>Pathway ' + esc(pw.id) + '</h3>' +
          (R ? '<p class="small">Applicable: ' + badge(R.ev.pathways[pw.id]) + ' · policy ' + lvl(R.cov.policyA[pw.id].level) + '</p>' : '') +
          field('Harm', '<select data-n="harm">' + harmOptions(sel.harm) + '</select>') +
          field('Consequence', '<input data-n="consequence" value="' + esc(pw.consequence) + '">') +
          '<div class="grid g2">' + field('Basis', '<select data-n="basis"><option' + (pw.basis === 'documented' ? ' selected' : '') + '>documented</option><option' + (pw.basis === 'argued' ? ' selected' : '') + '>argued</option></select>') +
          field('Tag', '<input data-n="tag" value="' + esc(pw.tag || '') + '">') + '</div>' +
          field('Capability', '<select data-n="cap">' + capOptions(pw.capability) + '</select>') +
          field('Sources (one per line)', '<textarea data-n="sources" rows="3">' + esc((pw.sources || []).join('\n')) + '</textarea>') +
          '<div class="row"><button class="btn primary" data-do="save-pathway">Save pathway</button><button class="btn danger" data-do="delete-pathway">Delete</button></div></div>' +
          '<div class="section"><h3>Capability ' + esc(pw.capability) + '</h3><p class="xs faint">Shared by ' + shared.join(', ') + '. A change applies to every pathway that uses it.</p>' +
          field('Label', '<input data-n="capLabel" value="' + esc(cap.label) + '">') +
          '<div class="grid g2">' + field('Actor', '<input data-n="capActor" value="' + esc(cap.actor) + '">') + field('Type', '<select data-n="capType">' + types.map(function (t) { return '<option' + (t === cap.type ? ' selected' : '') + '>' + t + '</option>'; }).join('') + '</select>') + '</div>' +
          field('Needs (term)', '<input class="mono" data-n="term" value="' + esc(A.termToString(cap.needs)) + '">') + '<div data-termmsg class="xs faint">AND requires every input; OR any one. Brackets group.</div>' + palette +
          '<button class="btn primary" data-do="save-capability">Save capability</button></div>';
      }
    } else if (sel && sel.type === 'harm') {
      var hh = M.harms[sel.id];
      html += '<div class="section"><h3>' + esc(sel.id) + ' ' + esc(hh.label) + '</h3><p class="small muted">' + hh.pathways.length + ' pathways' + (R ? ' · ' + badge(R.ev.harms[sel.id]) : '') + '</p>' +
        field('Label', '<input data-n="harmLabel" value="' + esc(hh.label) + '">') +
        '<div class="row"><button class="btn primary" data-do="save-harm">Save</button><button class="btn" data-do="new-pathway" data-harm="' + sel.id + '">Add pathway here</button>' + (hh.pathways.length ? '' : '<button class="btn danger" data-do="delete-harm">Delete</button>') + '</div></div>';
    } else {
      html += '<div class="section"><h3>Inspector</h3><p class="small muted">Select a harm, capability or component in the tree to see and edit it. Add pathways and components with the buttons above the tree.</p>' +
        '<h4>Reading the tree</h4><p class="small muted">From the bottom: components combine (AND, OR) into a capability held by an actor; any capability can lead to the harm. Border colour is the component\'s origin, as in the thesis. After a run, fills show applicability: white present, amber uncertain, grey absent; L0–L3 is the policy coverage level of an applicable pathway.</p></div>';
    }
    html += '<div class="section"><h3>Model check</h3>' + (problems.length ? '<ul class="editlog" style="color:var(--bad-text)">' + problems.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>' : '<p class="ok-t">Every node exists, every component is used, no OR+ remains, every pathway has a source.</p>') + '</div>';
    html += '<div class="section"><h3>Edits</h3>' + (S.modelEdits.length ? '<ol class="editlog">' + S.modelEdits.slice(-12).map(function (e) { return '<li>' + esc(e.at.slice(11, 16)) + ' ' + esc(e.op) + ' ' + esc(e.target) + '</li>'; }).join('') + '</ol>' : '<p class="xs faint">The frozen reference model v' + c.DATA.model.version + ' (' + esc(c.DATA.sources.model.path) + '). Edits are logged and go into the record.</p>') +
      (c.modelEdited() ? '<div class="row" style="margin-top:10px"><button class="btn sm" data-do="export-model">Model as YAML</button><button class="btn sm danger" data-do="reset-model">Reset to frozen v' + c.DATA.model.version + '</button></div>' : '') + '</div>';
    return html;
  }

  function treeCtx(c) {
    var S = c.S, R = c.R;
    return { model: S.model, harm: S.ui.harm, theme: S.ui.theme, orient: S.ui.orient || 'lr', selected: S.ui.selected && S.ui.selected.key,
      states: R && S.ui.overlay !== false ? R.states : null, ev: R && S.ui.overlay !== false ? R.ev : null,
      levels: R && S.ui.overlay !== false ? R.cov.policyA : null, edited: c.editedIds() };
  }

  function bindInspector(host, c) {
    var S = c.S, M = S.model;
    var val = function (n) { var e = host.querySelector('[data-n="' + n + '"]'); return e ? e.value.trim() : ''; };
    var termInput = host.querySelector('[data-n="term"]');
    function checkTerm() {
      var msg = host.querySelector('[data-termmsg]'); if (!termInput || !msg) return null;
      try { var t = A.parseTerm(termInput.value, Object.keys(M.components)); msg.className = 'ok-t'; msg.textContent = 'Valid: ' + A.termToString(t); return t; }
      catch (e) { msg.className = 'err-t'; msg.textContent = e.message; return null; }
    }
    if (termInput) { termInput.addEventListener('input', checkTerm); if (termInput.value) checkTerm(); }
    var harmSel = host.querySelector('select[data-n="harm"]'), capSel = host.querySelector('select[data-n="cap"]');
    if (S.ui.selected && S.ui.selected.mode === 'add-pathway') {
      var syncNew = function () {
        host.querySelector('[data-newharm]').hidden = harmSel.value !== '__new';
        host.querySelector('[data-newcap]').hidden = capSel.value !== '__new';
      };
      capSel.value = '__new'; harmSel.addEventListener('change', syncNew); capSel.addEventListener('change', syncNew); syncNew();
    }
    // One handler per inspector element: it is re-rendered in place, so
    // addEventListener would stack handlers bound to forms that no longer exist.
    host.onclick = function (e) {
      var ins = e.target.closest('[data-ins]');
      if (ins && termInput) {
        var v = termInput.value, s = termInput.selectionStart || v.length;
        var add = (v && !/[\s(]$/.test(v.slice(0, s)) ? ' AND ' : '') + ins.dataset.ins;
        termInput.value = v.slice(0, s) + add + v.slice(s); termInput.focus(); checkTerm(); return;
      }
      var b = e.target.closest('[data-do]'); if (!b) return;
      var sel = S.ui.selected, op = b.dataset.do, a = app();
      function done(msg, select) { S.ui.selected = select === undefined ? null : select; a.changed(); a.render(); if (msg) a.toast(msg, 'ok'); }
      if (op === 'cancel') return done();
      if (op === 'new-pathway') { S.ui.selected = { mode: 'add-pathway', harm: b.dataset.harm }; return a.render(); }
      if (op === 'add-pathway') {
        var h = harmSel.value;
        if (h === '__new') {
          var hid = val('harmId').toUpperCase().replace(/\s+/g, '-'), hl = val('harmLabel');
          if (!/^H-[A-Z0-9-]+$/.test(hid) || M.harms[hid] || !hl) return a.toast('A new harm needs an unused ID such as H-NEW and a label.', 'bad');
          M.harms[hid] = { label: hl, pathways: [] }; h = hid; a.logEdit('add harm', hid, hl);
        }
        var capId = capSel.value;
        if (capId === '__new') {
          var term = checkTerm(); if (!term) return a.toast('The capability needs a valid term.', 'bad');
          if (!val('capLabel') || !val('capActor')) return a.toast('The capability needs a label and an actor.', 'bad');
          capId = A.nextId(Object.keys(M.capabilities), 'K');
          M.capabilities[capId] = { label: val('capLabel'), actor: val('capActor'), type: val('capType'), needs: term };
          a.logEdit('add capability', capId, A.termToString(term));
        }
        var sources = val('sources').split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
        if (!val('consequence') || !sources.length) return a.toast('A pathway needs a consequence and at least one source.', 'bad');
        var all = []; Object.keys(M.harms).forEach(function (x) { M.harms[x].pathways.forEach(function (p) { all.push(p.id); }); });
        var pid = A.nextId(all, 'P');
        var pathway = { id: pid, capability: capId, consequence: val('consequence'), basis: val('basis'), sources: sources };
        if (val('tag')) pathway.tag = val('tag');
        M.harms[h].pathways.push(pathway);
        S.ui.harm = h;
        a.logEdit('add pathway', pid, h + ' via ' + capId);
        return done('Pathway ' + pid + ' added to ' + h + '.', { type: 'cap', harm: h, pathway: pid, key: h + '/' + pid });
      }
      if (op === 'add-component') {
        var origin = val('origin'), prefix = { core: 'CO', context: 'CX', implementation: 'IM', external: 'EX' }[origin];
        if (!val('label') || !val('feature')) return a.toast('A component needs a label and a feature to check.', 'bad');
        var cid = A.nextId(Object.keys(M.components), prefix);
        M.components[cid] = { origin: origin, label: val('label'), feature: val('feature') };
        a.logEdit('add component', cid, val('label'));
        return done(cid + ' added. Use it in a capability term; until then the model check lists it as unused.', { type: 'comp', id: cid, key: 'comp:' + cid });
      }
      if (op === 'save-component') {
        Object.assign(M.components[sel.id], { label: val('label'), origin: val('origin'), feature: val('feature') });
        a.logEdit('edit component', sel.id); return done('Saved.', sel);
      }
      if (op === 'delete-component') { delete M.components[sel.id]; a.logEdit('delete component', sel.id); return done('Deleted.'); }
      if (op === 'save-pathway' || op === 'delete-pathway') {
        var list = M.harms[sel.harm].pathways, idx = list.findIndex(function (p) { return p.id === sel.pathway; });
        if (op === 'delete-pathway') { if (!confirm('Delete pathway ' + sel.pathway + '?')) return; list.splice(idx, 1); a.logEdit('delete pathway', sel.pathway); return done('Deleted.'); }
        var p = list[idx], target = val('harm');
        p.consequence = val('consequence'); p.basis = val('basis'); p.capability = val('cap');
        p.sources = val('sources').split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
        if (val('tag')) p.tag = val('tag'); else delete p.tag;
        if (target !== sel.harm) { list.splice(idx, 1); M.harms[target].pathways.push(p); }
        a.logEdit('edit pathway', p.id, target);
        return done('Saved.', { type: 'cap', harm: target, pathway: p.id, key: target + '/' + p.id });
      }
      if (op === 'save-capability') {
        var t2 = checkTerm(); if (!t2) return a.toast('Fix the term first.', 'bad');
        var capKey = M.harms[sel.harm].pathways.filter(function (p) { return p.id === sel.pathway; })[0].capability;
        Object.assign(M.capabilities[capKey], { label: val('capLabel'), actor: val('capActor'), type: val('capType'), needs: t2 });
        a.logEdit('edit capability', capKey, A.termToString(t2)); return done('Saved.', sel);
      }
      if (op === 'save-harm') { M.harms[sel.id].label = val('harmLabel'); a.logEdit('edit harm', sel.id); return done('Saved.', sel); }
      if (op === 'delete-harm') { delete M.harms[sel.id]; S.ui.harm = Object.keys(M.harms)[0]; a.logEdit('delete harm', sel.id); return done('Deleted.'); }
      if (op === 'reset-model') {
        if (!confirm('Discard every edit and return to the frozen reference model?')) return;
        S.model = a.clone(c.DATA.model); S.modelEdits = []; S.ui.harm = 'H-PSY'; return done('Reset to the frozen model.');
      }
      if (op === 'export-model') {
        a.download('reference_model_edited_' + a.slug() + '.yaml', 'application/yaml', root.PA.yaml.stringify({ version: String(c.DATA.model.version) + '+edits', based_on: c.DATA.sources.model.path, edits: S.modelEdits, components: M.components, capabilities: M.capabilities, harms: M.harms }));
      }
    };
  }

  VIEWS.trees = {
    full: true,
    crumb: function (c) { var M = c.S.model; return Object.keys(M.harms).length + ' harms · ' + Object.keys(M.capabilities).length + ' capabilities · ' + Object.keys(M.components).length + ' components' + (c.modelEdited() ? ' · edited' : ' · frozen v' + c.DATA.model.version); },
    actions: function () { return '<button class="btn" data-act="add-component">Add component</button><button class="btn primary" data-act="add-pathway">Add pathway</button>'; },
    render: function (c) {
      var S = c.S, M = S.model;
      var harms = ['*'].concat(Object.keys(M.harms));
      return '<div class="tree-wrap"><div class="tree-main"><div class="tree-toolbar"><div class="seg" role="group" aria-label="Harm">' + harms.map(function (h) {
        return '<button data-harm="' + h + '" aria-pressed="' + (S.ui.harm === h) + '" title="' + esc(h === '*' ? 'All harms, folded at the capabilities' : M.harms[h].label) + '">' + (h === '*' ? 'All' : esc(h.replace('H-', ''))) + '</button>';
      }).join('') + '</div><span style="flex:1"></span>' +
        '<div class="seg" role="group" aria-label="Orientation"><button data-orient="td" aria-pressed="' + (S.ui.orient === 'td') + '" title="Top-down, as in the thesis">↓ Top-down</button><button data-orient="lr" aria-pressed="' + (S.ui.orient !== 'td') + '" title="Left to right, easier to read on screen">→ Left-right</button></div>' +
        '<div class="seg" role="group" aria-label="Canvas"><button data-theme="paper" aria-pressed="' + (S.ui.theme === 'paper') + '">Paper</button><button data-theme="dark" aria-pressed="' + (S.ui.theme === 'dark') + '">Dark</button></div>' +
        (c.R ? '<label class="check small"><input type="checkbox" data-overlay' + (S.ui.overlay !== false ? ' checked' : '') + '> Show this app</label>' : '') +
        '<button class="btn sm" data-tool="fold">Fold</button><button class="btn sm" data-tool="unfold">Unfold</button>' +
        '<button class="btn sm" data-tool="svg">SVG</button><button class="btn sm" data-tool="png">PNG</button></div>' +
        '<div class="tree-host" id="tree-host"><div class="tree-legend">' +
        '<span><i class="sw" style="border-color:#1A1A1A"></i>core</span><span><i class="sw" style="border-color:#496D91"></i>digital context</span><span><i class="sw" style="border-color:#A33B3B"></i>implementation</span><span><i class="sw" style="border-color:#535B63;border-style:dashed"></i>outside the app</span>' +
        (c.R && S.ui.overlay !== false ? '<span><i class="sw" style="border-color:#bbb;background:#F0C987"></i>uncertain</span><span><i class="sw" style="border-color:#bbb;background:#e6e6e6"></i>absent</span>' : '') + '</div>' +
        '<div class="tree-zoom"><button class="btn sm" data-tool="in" aria-label="Zoom in">+</button><button class="btn sm" data-tool="out" aria-label="Zoom out">−</button><button class="btn sm" data-tool="fit" aria-label="Fit">⤢</button></div></div></div>' +
        '<aside class="inspector" id="inspector">' + inspector(c) + '</aside></div>';
    },
    mount: function (el, c) {
      var S = c.S, prev = treeView;
      treeView = new root.PA.tree.TreeView(el.querySelector('#tree-host'), { onSelect: function (n) {
        if (n.type === 'cap') S.ui.selected = { type: 'cap', harm: n.harm, pathway: n.pathway.id, key: n.key };
        else if (n.type === 'comp') S.ui.selected = { type: 'comp', id: n.id, key: n.key };
        else if (n.type === 'harm') S.ui.selected = { type: 'harm', id: n.id, key: n.key };
        app().save();
        var ins = document.getElementById('inspector'); ins.innerHTML = inspector(c); bindInspector(ins, c);
        treeView.render(treeCtx(c));
      } });
      if (prev && prev.harmKey === S.ui.harm) { treeView.zoom = prev.zoom; treeView.pan = prev.pan; treeView.collapsed = prev.collapsed; treeView.fitted = true; }
      treeView.harmKey = S.ui.harm;
      treeView.render(treeCtx(c));
      bindInspector(el.querySelector('#inspector'), c);
      el.querySelector('.tree-toolbar').addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        if (b.dataset.harm) { S.ui.harm = b.dataset.harm; S.ui.selected = null; treeView = null; app().save(); return app().render(); }
        if (b.dataset.theme) { S.ui.theme = b.dataset.theme; app().save(); return app().render(); }
        if (b.dataset.orient) { S.ui.orient = b.dataset.orient; treeView = null; app().save(); return app().render(); }
        var t = b.dataset.tool;
        if (t === 'fold') treeView.collapseAll(true);
        if (t === 'unfold') treeView.collapseAll(false);
        if (t === 'svg') app().download('harm-tree_' + (S.ui.harm === '*' ? 'all' : S.ui.harm) + '.svg', 'image/svg+xml', treeView.exportSVG());
        if (t === 'png') treeView.exportPNG(function (blob) { app().download('harm-tree_' + (S.ui.harm === '*' ? 'all' : S.ui.harm) + '.png', 'image/png', blob); });
      });
      el.querySelector('.tree-toolbar').addEventListener('change', function (e) { if (e.target.hasAttribute('data-overlay')) { S.ui.overlay = e.target.checked; app().save(); app().render(); } });
      el.querySelector('.tree-zoom').addEventListener('click', function (e) {
        var t = e.target.closest('button'); if (!t) return;
        if (t.dataset.tool === 'in') treeView.zoomBy(1.25); if (t.dataset.tool === 'out') treeView.zoomBy(0.8); if (t.dataset.tool === 'fit') treeView.fit();
      });
      document.getElementById('top-actions').onclick = function (e) {
        var a = e.target.closest('[data-act]'); if (!a) return;
        S.ui.selected = { mode: a.dataset.act, harm: S.ui.harm === '*' ? Object.keys(S.model.harms)[0] : S.ui.harm };
        var ins = document.getElementById('inspector'); ins.innerHTML = inspector(c); bindInspector(ins, c); ins.scrollTop = 0;
      };
      if (!this._resize) { this._resize = function () { if (treeView && S.ui.tab === 'trees') treeView.fit(); }; window.addEventListener('resize', this._resize); }
    }
  };

  // ---------- Prompts ----------

  VIEWS.prompts = {
    crumb: function () { return 'Frozen instrument bundle · read-only'; },
    render: function (c) {
      var D = c.DATA;
      var rows = [['stage1', 'Stage 1 · nodes, harms, risks (Axis A)'], ['stage1p', 'Stage 1 paraphrase · wording sensitivity'], ['stage2', 'Stage 2 · stance (Axis B)'], ['stage3', 'Stage 3 · protection (Axis C)']];
      return '<div class="view-inner"><p class="lead">Every model receives the same prompt as its system text and the units as JSON lines. The text below is exactly what is sent; the record stores it with its hash.</p>' +
        rows.map(function (r) {
          var s = D.sources[r[0]];
          return '<div class="card flush"><div class="card-head"><h3>' + r[1] + '</h3><span class="spacer"></span><span class="chip">' + esc(s.path.split('/').pop()) + '</span><span class="chip">v' + esc(s.version) + '</span>' +
            '<button class="btn sm" data-copy="' + r[0] + '">Copy</button></div><div class="card-body"><p class="xs faint mono">sha256 ' + esc(s.sha256) + '</p><pre class="code">' + esc(D.prompts[r[0]]) + '</pre></div></div>';
        }).join('') + '</div>';
    },
    mount: function (el, c) {
      el.addEventListener('click', function (e) {
        var b = e.target.closest('[data-copy]'); if (!b) return;
        navigator.clipboard.writeText(c.DATA.prompts[b.dataset.copy]).then(function () { app().toast('Prompt copied.', 'ok'); });
      });
    }
  };

  // ---------- Coded text ----------

  VIEWS.coded = {
    crumb: function (c) { return c.R ? c.R.all.length + ' combined labels on ' + c.R.run.units.length + ' units' : 'No run yet'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var S = c.S, f = S.ui.textFilter;
      var labels = R.all.filter(function (r) {
        return (f.family === 'all' || FAMILY_OF(r) === f.family) && (f.decision === 'all' || r.decision === f.decision);
      });
      var byUnit = {};
      labels.forEach(function (r) { (byUnit[r.unit] = byUnit[r.unit] || []).push(r); });
      var us = R.run.units.filter(function (u) { return f.surface === 'all' || u.surface === f.surface; });
      var seg = function (key, opts) {
        return '<div class="seg" role="group">' + opts.map(function (o) { return '<button data-f="' + key + '" data-v="' + o[0] + '" aria-pressed="' + (f[key] === o[0]) + '">' + o[1] + '</button>'; }).join('') + '</div>';
      };
      var selU = S.ui.codedUnit;
      var side = '<div class="card sticky"><h3>' + (selU ? 'Unit ' + esc(selU) : 'Labels') + '</h3>';
      if (selU) {
        var ls = R.all.filter(function (r) { return r.unit === selU; });
        side += ls.length ? ls.map(function (r) {
          var v = S.review[r.key];
          return '<div style="padding:8px 0;border-bottom:1px solid var(--border)"><div class="row"><span class="swatch" style="background:' + FAMILY_COLORS[FAMILY_OF(r)] + '"></span><strong class="small">' + esc(labelText(r)) + '</strong>' +
            badge(r.decision) + (v ? badge(v.verdict) : '') + '</div><div class="xs muted" style="margin-top:4px">' + esc(Object.keys(r.by).join(', ')) + (r.status ? ' · ' + esc(r.status) : '') + '</div><div class="small" style="margin-top:4px"><q>' + esc(r.span) + '</q></div>' +
            Object.keys(r.by).map(function (m) { return '<div class="xs faint">' + esc(m) + ': ' + esc(r.by[m].reason || '') + (r.by[m].unsure ? ' (unsure)' : '') + '</div>'; }).join('') + '</div>';
        }).join('') : '<p class="faint small">No labels on this unit.</p>';
      } else side += '<p class="small muted">Click a unit to see each label, which models returned it, their reasons, and the review decision.</p>';
      side += '<h4>Legend</h4>' + Object.keys(FAMILY_NAMES).map(function (k) { return '<div class="xs"><span class="swatch" style="background:' + FAMILY_COLORS[k] + '"></span>' + FAMILY_NAMES[k] + '</div>'; }).join('') + '<p class="xs faint" style="margin-top:8px">A double underline marks overlapping labels.</p></div>';
      return '<div class="view-inner wide"><div class="row" style="margin-bottom:14px">' +
        seg('surface', [['all', 'All'], ['policy', 'Policy'], ['interface', 'Interface']]) +
        seg('family', [['all', 'All labels'], ['cmp', 'Components'], ['cap', 'Capabilities'], ['hrm', 'Harms'], ['gen', 'Generic'], ['stance', 'Stance'], ['prot', 'Protection']]) +
        seg('decision', [['all', 'Any'], ['agreed', 'Agreed'], ['uncertain', 'Uncertain'], ['check', 'To check']]) + '</div>' +
        '<div class="split"><div class="card flush"><div class="units" style="padding:6px">' + us.map(function (u) {
          var ls = byUnit[u.id] || [];
          return '<div class="unit' + (selU === u.id ? ' sel' : '') + '" data-unit="' + esc(u.id) + '"><div class="uid">' + esc(u.id) + '</div><div>' + (u.heading ? '<div class="uh">' + esc(u.heading) + '</div>' : '') +
            '<div class="ut">' + marked(u.text, ls) + '</div>' + (ls.length ? '<div class="chips">' + ls.map(function (r) { return '<span class="chip" style="border-color:' + FAMILY_COLORS[FAMILY_OF(r)] + '55">' + esc(labelText(r)) + '</span>'; }).join('') + '</div>' : '') + '</div></div>';
        }).join('') + '</div></div>' + side + '</div></div>';
    },
    mount: function (el, c) {
      bindGo(el);
      el.addEventListener('click', function (e) {
        var s = e.target.closest('.seg button[data-f]');
        if (s) { c.S.ui.textFilter[s.dataset.f] = s.dataset.v; app().save(); return app().render(); }
        var u = e.target.closest('[data-unit]');
        if (u) { c.S.ui.codedUnit = u.dataset.unit; app().save(); app().render(); }
      });
    }
  };

  // ---------- Review queue ----------

  function reviewList(c) {
    var R = c.R, S = c.S, f = S.ui.reviewFilter;
    return R.reviewItems.filter(function (r) {
      var v = S.review[r.key];
      return f === 'all' || (f === 'pending' && !v) || (v && v.verdict === f);
    });
  }

  function reviewDetail(c, r) {
    var S = c.S, R = c.R;
    if (!r) return '<div class="card empty"><h3>Nothing selected</h3><p class="muted">' + (R.reviewStats.pending ? 'Choose a label on the left.' : 'Every high-stakes label is reviewed.') + '</p></div>';
    var us = R.run.units, i = us.findIndex(function (u) { return u.id === r.unit; }), u = us[i];
    var v = S.review[r.key];
    var what = r.stage === 2 ? 'Stance of a named harm' : r.stage === 3 ? 'Protection claim: measure, framing and strength' : r.decision === 'proposal' ? 'Minimisation (people decide)' : 'High-stakes label';
    var rows = Object.keys(r.by).map(function (m) {
      var l = r.by[m];
      return [esc(m), esc([l.status || l.target, l.framing, l.strength].filter(Boolean).join(' · ') || '–'),
        '<q>' + esc(l.span) + '</q><div class="xs faint" style="margin-top:3px">' + esc(l.reason || '') + (l.unsure ? ' <span class="badge uncertain">unsure</span>' : '') + '</div>'];
    });
    var missing = R.models.filter(function (m) { return !r.by[m]; });
    return '<div class="card"><div class="row"><span class="swatch" style="background:' + FAMILY_COLORS[FAMILY_OF(r)] + '"></span><h3 style="margin:0">' + esc(labelText(r)) + '</h3>' + badge(r.decision) + (v ? badge(v.verdict) : badge('pending')) + '<span style="flex:1"></span><span class="faint small">' + esc(what) + '</span></div>' +
      '<div class="reader" style="margin-top:14px">' + (i > 0 ? '<p class="ctx">' + esc(us[i - 1].text) + '</p>' : '') +
      '<p><span class="chip">' + esc(u.id) + '</span> ' + marked(u.text, [r], r.key) + '</p>' + (i < us.length - 1 ? '<p class="ctx">' + esc(us[i + 1].text) + '</p>' : '') + '</div>' +
      '<h4>What each model returned</h4>' + table(['Model', 'Status or framing', 'Span and reason'], rows) +
      (missing.length ? '<p class="small muted" style="margin-top:8px">Not returned by ' + missing.map(esc).join(', ') + '.</p>' : '') +
      '<label class="field" style="margin-top:14px"><span>Note (why accepted or rejected; for stances, which stance holds)</span><textarea data-note rows="2">' + esc(v ? v.note : '') + '</textarea></label>' +
      '<div class="row"><button class="btn ok" data-v="accepted">Accept <kbd>A</kbd></button><button class="btn bad" data-v="rejected">Reject <kbd>R</kbd></button>' + (v ? '<button class="btn ghost" data-v="">Undo</button>' : '') +
      '<span style="flex:1"></span><button class="btn ghost" data-step="-1">Previous <kbd>K</kbd></button><button class="btn ghost" data-step="1">Next <kbd>J</kbd></button></div></div>';
  }

  function reviewStep(c, d) {
    var list = reviewList(c), S = c.S;
    var i = list.findIndex(function (r) { return r.key === S.ui.reviewSel; });
    var n = list[Math.max(0, Math.min(list.length - 1, i + d))];
    S.ui.reviewSel = n ? n.key : null; app().save(); app().render();
  }

  function decide(c, verdict) {
    var S = c.S, key = S.ui.reviewSel; if (!key) return;
    var note = document.querySelector('[data-note]');
    var list = reviewList(c), i = list.findIndex(function (r) { return r.key === key; });
    if (verdict) S.review[key] = { verdict: verdict, note: note ? note.value : '', at: app().localTime(), by: S.project.analyst || null };
    else delete S.review[key];
    app().changed();
    var next = reviewList(c);
    if (S.ui.reviewFilter === 'pending' && verdict) S.ui.reviewSel = next[Math.min(i, next.length - 1)] ? next[Math.min(i, next.length - 1)].key : null;
    app().renderNav(); app().renderFoot(); app().render();
  }

  VIEWS.review = {
    crumb: function (c) { var s = c.R && c.R.reviewStats; return s ? s.accepted + ' accepted · ' + s.rejected + ' rejected · ' + s.pending + ' pending' : 'No run yet'; },
    actions: function (c) { return c.R ? '<button class="btn" data-act="bulk" title="Accept every pending label that all models returned">Accept all labels every model returned</button>' : ''; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var S = c.S, list = reviewList(c);
      if (!S.ui.reviewSel || !list.some(function (r) { return r.key === S.ui.reviewSel; })) S.ui.reviewSel = list[0] ? list[0].key : null;
      var sel = R.reviewItems.filter(function (r) { return r.key === S.ui.reviewSel; })[0];
      var st = R.reviewStats;
      return '<div class="view-inner wide"><div class="row" style="margin-bottom:12px"><div class="seg" role="group">' + [['pending', 'Pending ' + st.pending], ['accepted', 'Accepted ' + st.accepted], ['rejected', 'Rejected ' + st.rejected], ['all', 'All ' + st.total]].map(function (o) {
        return '<button data-rf="' + o[0] + '" aria-pressed="' + (S.ui.reviewFilter === o[0]) + '">' + o[1] + '</button>';
      }).join('') + '</div><div style="flex:1;max-width:300px"><progress max="' + Math.max(1, st.total) + '" value="' + (st.accepted + st.rejected) + '"></progress></div><span class="small faint">Rejected labels leave the results; accepted ones are recorded with your note.</span></div>' +
        '<div class="split" style="grid-template-columns:340px minmax(0,1fr)"><div class="card flush"><div class="queue">' + (list.length ? list.map(function (r) {
          var v = S.review[r.key];
          return '<div class="qi' + (r.key === S.ui.reviewSel ? ' sel' : '') + '" data-key="' + esc(r.key) + '"><span class="small"><span class="swatch" style="background:' + FAMILY_COLORS[FAMILY_OF(r)] + '"></span><strong>' + esc(labelText(r)) + '</strong></span>' +
            '<span>' + (v ? badge(v.verdict) : '<span class="faint xs">' + Object.keys(r.by).length + '/' + R.models.length + '</span>') + '</span><span class="qt">' + esc(r.unit) + ' · ' + esc(r.span) + '</span></div>';
        }).join('') : '<p class="faint small" style="padding:16px">No labels here.</p>') + '</div></div>' +
        '<div>' + reviewDetail(c, sel) + '</div></div></div>';
    },
    mount: function (el, c) {
      el.addEventListener('click', function (e) {
        var f = e.target.closest('[data-rf]'); if (f) { c.S.ui.reviewFilter = f.dataset.rf; c.S.ui.reviewSel = null; app().save(); return app().render(); }
        var q = e.target.closest('.qi'); if (q) { c.S.ui.reviewSel = q.dataset.key; app().save(); return app().render(); }
        var v = e.target.closest('[data-v]'); if (v) return decide(c, v.dataset.v);
        var s = e.target.closest('[data-step]'); if (s) return reviewStep(c, +s.dataset.step);
      });
      var top = document.getElementById('top-actions');
      top.onclick = function (e) {
        if (!e.target.closest('[data-act="bulk"]')) return;
        var n = 0, R = c.R;
        R.reviewItems.forEach(function (r) {
          if (!c.S.review[r.key] && Object.keys(r.by).length === R.models.length) { c.S.review[r.key] = { verdict: 'accepted', note: 'bulk: returned by every model', at: app().localTime(), by: c.S.project.analyst || null }; n++; }
        });
        app().changed(); app().renderAll(); app().toast(n + ' labels accepted. Check the ones only one model returned by hand.', 'ok');
      };
      var sel = el.querySelector('.qi.sel'); if (sel) sel.scrollIntoView({ block: 'nearest' });
    },
    key: function (e, c) {
      if (!c.R) return;
      var k = e.key.toLowerCase();
      if (k === 'a') decide(c, 'accepted'); else if (k === 'r') decide(c, 'rejected');
      else if (k === 'j' || e.key === 'ArrowDown') { e.preventDefault(); reviewStep(c, 1); }
      else if (k === 'k' || e.key === 'ArrowUp') { e.preventDefault(); reviewStep(c, -1); }
    }
  };

  // ---------- Applicability ----------

  VIEWS.applicability = {
    crumb: function (c) { var R = c.R; if (!R) return 'Step 1'; return R.pathCounts.present + ' of ' + R.pathCounts.total + ' pathways applicable · ' + Object.keys(c.S.overrides).length + ' components changed'; },
    actions: function (c) { return c.R ? '<button class="btn" data-act="reset">Reset to proposal</button>' : ''; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var S = c.S, M = S.model;
      var rows = Object.keys(M.components).map(function (id) {
        var comp = M.components[id], p = R.proposal[id], o = S.overrides[id], cur = o ? o.state : p.state;
        var inPrompt = !!c.DATA.model.components[id];
        return { cls: o ? 'changed' : '', cells: [cmp(M, id), '<strong>' + esc(comp.label) + '</strong><div class="xs faint">' + esc(comp.feature) + '</div>' + (inPrompt ? '' : '<div class="xs" style="color:var(--warn)">Not in the frozen prompts: decide by hand.</div>'),
          badge(p.state) + '<div class="xs faint" style="margin-top:4px">' + esc(p.basis) + '</div>',
          '<select data-comp="' + id + '">' + ['present', 'absent', 'uncertain'].map(function (s) { return '<option' + (s === cur ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select>',
          '<input data-cnote="' + id + '" value="' + esc(o ? o.note || '' : '') + '" placeholder="Evidence: listing, walkthrough screen…">'] };
      });
      return '<div class="view-inner"><p class="lead">The proposal uses the coded text only. Stored data are assumed accessible to an attacker; authority and insurer use stay uncertain; a component not mentioned stays uncertain. Confirm or change each state with the store listing and the walkthrough, and note the evidence. The trees and results update at once.</p>' +
        '<div class="grid g4">' + stat('Applicable pathways', R.pathCounts.present, 'of ' + R.pathCounts.total) + stat('Uncertain pathways', R.pathCounts.uncertain, 'reported in scenario B') + stat('Not applicable', R.pathCounts.absent, 'pathways') + stat('Harm categories', Object.keys(R.ev.harms).filter(function (h) { return R.ev.harms[h] === 'present'; }).length, 'with an applicable pathway') + '</div>' +
        table(['ID', 'Component', 'Proposal from the text', 'Decision', 'Evidence note'], rows) + '</div>';
    },
    mount: function (el, c) {
      bindGo(el);
      var S = c.S;
      el.addEventListener('change', function (e) {
        var id = e.target.dataset.comp; if (!id) return;
        if (e.target.value === c.R.proposal[id].state && !(S.overrides[id] && S.overrides[id].note)) delete S.overrides[id];
        else S.overrides[id] = { state: e.target.value, note: S.overrides[id] ? S.overrides[id].note : '', at: app().localTime() };
        app().changed(); app().render(); app().renderFoot();
      });
      el.addEventListener('input', function (e) {
        var id = e.target.dataset.cnote; if (!id) return;
        var cur = S.overrides[id] ? S.overrides[id].state : c.R.proposal[id].state;
        S.overrides[id] = { state: cur, note: e.target.value, at: app().localTime() };
        app().changed(false);
      });
      document.getElementById('top-actions').onclick = function (e) {
        if (!e.target.closest('[data-act="reset"]')) return;
        if (confirm('Discard every applicability decision?')) { S.overrides = {}; app().changed(); app().render(); }
      };
    }
  };

  // ---------- Results ----------

  function resultsBanner(c) {
    var R = c.R, s = R.reviewStats, out = '';
    if (s.pending) out += '<div class="callout"><strong>' + s.pending + ' high-stakes labels are not reviewed yet.</strong> They count in these results until a person rejects them. <a href="#" data-go="review">Open the review queue</a>.</div>';
    if (c.modelEdited()) out += '<div class="callout info">The reference model has local edits (' + c.S.modelEdits.length + '). Results use the edited trees; the record lists every edit.</div>';
    return out;
  }

  VIEWS.coverage = {
    crumb: function () { return 'How far up the tree the text goes for each applicable pathway'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var M = R.model;
      var shareRows = [['Policy · scenario A', R.shares.policyA], ['Policy · scenario B', R.shares.policyB]];
      if (R.hasInterface) shareRows.push(['Interface · scenario A', R.shares.ifA], ['Interface · scenario B', R.shares.ifB]);
      var harmRows = Object.keys(M.harms).map(function (h) {
        var ps = M.harms[h].pathways.filter(function (p) { return R.ev.pathways[p.id] === 'present'; });
        var best = ps.reduce(function (m, p) { return Math.max(m, R.cov.policyA[p.id].level); }, -1);
        var catOnly = ps.some(function (p) { return R.cov.policyA[p.id].categoryOnly; });
        return [esc(h) + ' <span class="muted">' + esc(M.harms[h].label) + '</span>', badge(R.ev.harms[h]), ps.length, best < 0 ? '<span class="faint">–</span>' : lvl(best),
          '<span class="small muted">' + (best === 3 ? 'Named; check that consequence, data, actor and access match' : catOnly ? 'Named for the category, not on a pathway the text reaches' : best >= 0 ? 'No named harm of this category found by the models' : '') + '</span>'];
      });
      var pathRows = R.paths.map(function (p) {
        var a = R.cov.policyA[p.id], b = R.cov.policyB[p.id];
        return [esc(p.id), esc(p.harm), esc(p.capability) + ' <span class="faint small">' + esc(M.capabilities[p.capability].label) + '</span>', badge(R.ev.pathways[p.id]),
          lvl(a.level) + (b.level !== a.level ? ' <span class="faint xs">B: L' + b.level + '</span>' : '') + (a.denied ? ' <span class="chip">denied</span>' : '') + (a.categoryOnly ? ' <span class="chip">category only</span>' : ''),
          R.hasInterface ? lvl(R.cov.ifA[p.id].level) : '<span class="faint">–</span>', '<span class="mono xs">' + esc(b.evidence.slice(0, 6).join(' ')) + '</span>',
          esc(p.basis) + (A.assumptionDependent(M, p) ? ' · <span class="faint">assumption</span>' : '')];
      });
      return '<div class="view-inner">' + resultsBanner(c) +
        '<div class="grid g4">' + stat('Applicable pathways', R.pathCounts.present + ' / ' + R.pathCounts.total, R.pathCounts.uncertain + ' uncertain') +
        stat('Harm named (L3)', pct(R.shares.policyA.shares[3]), 'policy, scenario A') + stat('Silent (L0)', pct(R.shares.policyA.shares[0]), 'policy, scenario A') +
        stat('Scenario B, L3', pct(R.shares.policyB.shares[3]), 'with uncertain labels and pathways') + '</div>' +
        '<div class="card"><h3>Share of pathways at each level</h3><p class="small muted">Scenario A: labels every model returned, applicable pathways. Scenario B adds one-model and unsure labels and uncertain pathways. Level 3 is a category-level candidate until a person checks it.</p>' +
        table(['Basis', '#n', 'Distribution', '#L0 silent', '#L1 component', '#L2 capability', '#L3 harm'], shareRows.map(function (r) { return [r[0], r[1].n, stack(r[1].shares)].concat(r[1].shares.map(pct)); })) + '</div>' +
        '<h4>By harm category</h4>' + table(['Harm', 'Applies', '#Applicable pathways', 'Highest policy level', 'Note'], harmRows) +
        '<h4>By pathway</h4>' + table(['Pathway', 'Harm', 'Capability', 'Applicable', 'Policy (A)', 'Interface (A)', 'Evidence units', 'Basis'], pathRows) + '</div>';
    },
    mount: function (el) { bindGo(el); }
  };

  VIEWS.stance = {
    crumb: function (c) { return c.R ? c.R.harmRecords.length + ' named harms' : 'How each named harm is presented'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var rows = R.harmRecords.map(function (h) {
        return [esc(h.unit), esc(h.harm), '<q>' + esc(h.span) + '</q>', esc(h.foundBy.join(', ')),
          R.models.map(function (m) { return '<div class="small"><span class="faint">' + esc(m) + ':</span> ' + esc((h.stances[m] || []).join(', ') || '–') + '</div>'; }).join(''),
          esc(h.union.join(', ') || '–') + (h.union.indexOf('S-MIN') >= 0 ? ' <span class="badge proposal">S-MIN: people decide</span>' : ''), h.verdict ? badge(h.verdict) : badge('pending')];
      });
      var total = R.harmRecords.length || 1;
      var counts = Object.keys(R.stanceCounts).sort().map(function (k) { return [esc(k), R.stanceCounts[k], '<div class="bar"><i style="width:' + (100 * R.stanceCounts[k] / total) + '%"></i></div>']; });
      return '<div class="view-inner">' + resultsBanner(c) + '<p class="lead">Stance attaches to named harms only. S-ACK acknowledged, S-QUA qualified, S-MIN minimised, S-RSP responsibility shifted, S-DEN denied or prevented.</p>' +
        table(['Unit', 'Harm', 'Span', 'Named by', 'Stance per model', 'Union', 'Review'], rows) +
        '<div class="grid g2" style="margin-top:16px"><div><h4>Stances (union, after review)</h4>' + table(['Stance', '#Harms', 'Share'], counts) + '</div>' +
        '<div><h4>Without a named harm (secondary)</h4>' + table(['Code', '#Units'], [['L-GEN generic risk', R.secondary.gen], ['S-GRS generic responsibility', R.secondary.grs], ['C-REA reassurance', R.secondary.rea]]) + '</div></div></div>';
    },
    mount: function (el) { bindGo(el); }
  };

  VIEWS.protection = {
    crumb: function (c) { return c.R ? c.R.claimRecords.length + ' claimed measures · ' + c.R.secondary.rea + ' reassurances' : 'Claimed measures and the pathways they cut'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var M = R.model, comps = Object.keys(M.components);
      var rows = R.claimRecords.map(function (cl, i) {
        var sel = '<select data-claim="' + i + '"><option value="">– choose –</option>' + comps.map(function (id) { return '<option value="' + id + '"' + (cl.removes === id ? ' selected' : '') + '>' + id + ' ' + esc(M.components[id].label) + '</option>'; }).join('') + '</select>';
        return [esc(cl.unit), '<span class="chip">' + esc(cl.code) + '</span>', '<q>' + esc(cl.span) + '</q>', esc(cl.framing || '–') + '<div class="xs faint">' + esc(cl.strength || '') + '</div>',
          esc(cl.foundBy.join(', ')) + (cl.decision === 'uncertain' ? ' ' + badge('uncertain') : ''), sel,
          cl.removes ? (cl.closes.length ? '<span class="mono xs">' + esc(cl.closes.join(' ')) + '</span>' : '<span class="faint">none</span>') : '<span class="faint">–</span>',
          cl.removes ? (cl.leftOpen.length ? '<span class="mono xs" style="color:var(--bad-text)">' + esc(cl.leftOpen.join(' ')) + '</span>' : '<span class="faint">none</span>') : '<span class="faint">–</span>'];
      });
      return '<div class="view-inner">' + resultsBanner(c) + '<p class="lead">For each claimed measure, choose the component it would remove if it worked as described. The trees are evaluated again. Of the applicable pathways that contain that component, those that close are cut; those that stay open (another route remains) are candidate mismatches, which a person decides.</p>' +
        table(['Unit', 'Measure', 'Span', 'Framing', 'Found by', 'Would remove', 'Cuts', 'Leaves open'], rows) + '</div>';
    },
    mount: function (el, c) {
      bindGo(el);
      el.addEventListener('change', function (e) {
        var i = e.target.dataset.claim; if (i === undefined) return;
        var key = c.R.claimRecords[+i].key;
        if (e.target.value) c.S.removes[key] = e.target.value; else delete c.S.removes[key];
        app().changed(); app().render();
      });
    }
  };

  VIEWS.surfaces = {
    crumb: function () { return 'Policy compared with interface text'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      if (!R.hasInterface) return empty('No interface text', 'Add the interface text from the walkthrough (Text) and run the coding again to compare the two surfaces.', '<button class="btn" data-go="text">Go to Text</button>');
      var lower = 0, higher = 0, same = 0, rows = [];
      R.paths.forEach(function (p) {
        if (R.ev.pathways[p.id] !== 'present') return;
        var a = R.cov.policyA[p.id].level, b = R.cov.ifA[p.id].level;
        if (a > b) lower++; else if (b > a) higher++; else same++;
        rows.push({ cls: a !== b ? 'changed' : '', cells: [esc(p.id), esc(p.harm), lvl(a), lvl(b), a > b ? 'interface says less' : b > a ? 'interface says more' : '<span class="faint">same</span>'] });
      });
      return '<div class="view-inner">' + resultsBanner(c) + '<div class="grid g3">' + stat('Interface says less', lower, 'applicable pathways') + stat('Interface says more', higher, 'applicable pathways') + stat('Same level', same, 'applicable pathways') + '</div>' +
        '<p class="small muted">The policy is a full document; the interface text covers the recorded routes only, so a difference describes the captured material, not what users see.</p>' +
        table(['Pathway', 'Harm', 'Policy', 'Interface', 'Difference'], rows) + '</div>';
    },
    mount: function (el) { bindGo(el); }
  };

  VIEWS.agreement = {
    crumb: function (c) { return c.R ? c.R.models.join(' × ') : 'Deviation between the models'; },
    render: function (c) {
      var R = c.R; if (!R) return needRun();
      var G = R.agreement;
      var famRows = [];
      G.families.forEach(function (f) {
        f.pairs.forEach(function (p) {
          famRows.push([esc(f.name), esc(p.a) + ' × ' + esc(p.b), p.both, p.onlyA, p.onlyB, pct(p.agreement), num(p.kappa), num(p.pabak),
            '<div class="row" style="gap:8px;flex-wrap:nowrap"><div class="bar" style="flex:1"><i style="width:' + (100 * (p.positiveAgreement || 0)) + '%"></i></div><span class="num">' + num(p.positiveAgreement) + '</span></div>', num(p.alpha), pct(p.prevalence)]);
        });
        if (R.models.length > 2) famRows.push([esc(f.name), '<em>all models</em>', '', '', '', '', '', '', '', num(f.alphaAll), '']);
      });
      var perRows = R.models.map(function (m) {
        var s = R.perModel[m], a = G.adds[m];
        return [esc(m), esc(s.servedBy || ''), s.labels, a.only + ' <span class="faint xs">(' + pct(a.shareOfUnion) + ')</span>', s.invalidSpans, s.errors, s.calls, (s.ms / 1000).toFixed(1) + ' s', (s.tokensIn || s.tokensOut ? (s.tokensIn || 0) + ' / ' + (s.tokensOut || 0) : '–'), num(s.stability), num(s.wording)];
      });
      var lv = R.levelDeviation.map(function (d) { return [esc(d.id), esc(d.harm)].concat(R.models.map(function (m) { return lvl(d.levels[m]); })); });
      var ap = R.applicabilityDeviation.map(function (d) { return [cmp(R.model, d.id)].concat(R.models.map(function (m) { return badge(d.states[m]); })); });
      var per = G.values.map(function (v) { return ['<span class="mono">' + esc(v.value) + '</span>', v.stage].concat(R.models.map(function (m) { return v.by[m] || 0; })).concat([v.union, v.allModels, num(v.positiveAgreement)]); });
      return '<div class="view-inner"><div class="callout info">Agreement is a robustness check, not accuracy. Model errors are correlated, so two models can agree and both be wrong; accuracy needs human reference labels. α ≥ .800 reliable, .667–.800 tentative (Krippendorff); undefined without variation. Positive agreement suits rare codes, where κ and α are unstable.</div>' +
        '<div class="grid g4">' + stat('Shared labels', G.shared.n + ' / ' + G.union, 'found by every model') + stat('Same status', pct(G.shared.statusAgreement), 'asserted, possible, denied') +
        stat('Span overlap', num(G.shared.meanSpanJaccard), 'mean token Jaccard') + stat('Coverage differs', R.levelDeviation.length + ' / ' + R.pathCounts.total, 'pathways, each model alone') + '</div>' +
        '<h4>By label family</h4>' + table(['Family', 'Pair', '#Both', '#Only 1st', '#Only 2nd', '#Raw agr.', '#Cohen κ', '#PABAK', 'Positive agreement', '#Krippendorff α', '#Prevalence'], famRows) +
        '<h4>Per model</h4>' + table(['Model', 'Served by', '#Labels', '#Alone', '#Invalid spans', '#Failed calls', '#Calls', '#Time', '#Tokens in / out', '#Run-to-run α', '#Paraphrase α'], perRows) +
        '<div class="grid g2" style="margin-top:4px"><div><h4>Coverage level, each model alone</h4>' + table(['Pathway', 'Harm'].concat(R.models.map(esc)), lv) + '</div>' +
        '<div><h4>Applicability proposal, each model alone</h4>' + table(['Component'].concat(R.models.map(esc)), ap) + '</div></div>' +
        '<h4>By coded value</h4>' + table(['Value', '#Stage'].concat(R.models.map(function (m) { return '#' + esc(m); })).concat(['#Union', '#All models', '#Positive agr.']), per, { tall: true }) +
        (R.failures.length ? '<h4>Dropped labels and failed calls</h4>' + table(['Model', '#Stage', 'Unit', 'Code', 'Reason', 'Span'], R.failures.map(function (f) { return [esc(f.model), f.stage, esc(f.unit || ''), esc(f.code || ''), esc(f.reason), '<span class="xs">' + esc(f.span || '') + '</span>']; }), { tall: true }) : '') + '</div>';
    }
  };

  // ---------- Export ----------

  VIEWS.export = {
    crumb: function () { return 'A complete, reopenable record of this analysis'; },
    render: function (c) {
      var S = c.S;
      var parts = [
        ['format, generated, tool, environment', 'Record format, local time with offset, tool version and location, browser and time zone'],
        ['project', 'App, analyst, notes'],
        ['status', 'What is automated and what people decided; review counts'],
        ['inputs', 'Policy and interface text with source, length and SHA-256; every coding unit'],
        ['instruments', 'Reference model (frozen file and hash, every edit, the model used), the four prompts in full with file and text hashes, the coding rules'],
        ['models, settings', 'Provider, model id, endpoint, effort or temperature, JSON mode (never the key); units per request, runs, paraphrase'],
        ['run', 'Start, end, duration; every call with its stage, part, attempt, time, tokens and status; per model the raw output, labels, paraphrase labels and dropped labels'],
        ['decisions', 'Every review verdict with note, time and analyst; applicability proposed and decided with evidence; components each measure removes'],
        ['results', 'Combined labels; Step 1 states; RQ1 shares and per-pathway levels; RQ2 stances; RQ3 claims; RQ4 surfaces; model agreement']
      ];
      return '<div class="view-inner"><div class="grid g2"><div class="card"><h3>Analysis record (YAML)</h3><p class="small muted">Everything needed to check or repeat this analysis, in one file that any YAML reader opens. API keys are never written.</p>' +
        '<div class="row" style="margin:12px 0"><button class="btn primary" data-x="yaml">' + icon('download') + 'Export record</button><button class="btn" data-x="preview">Preview</button></div>' +
        (S.run ? '' : '<p class="xs" style="color:var(--warn)">No run yet: the record holds the inputs, instruments and settings only.</p>') +
        table(['Section', 'Contents'], parts.map(function (p) { return ['<span class="mono xs">' + p[0] + '</span>', '<span class="small">' + p[1] + '</span>']; })) + '</div>' +
        '<div><div class="card"><h3>Reopen</h3><p class="small muted">Open a record to restore the whole workspace: text, models (enter keys again), settings, raw output, decisions and tree edits.</p>' +
        '<label class="btn" style="cursor:pointer">Open record (.yaml)<input type="file" accept=".yaml,.yml" data-x="open" hidden></label></div>' +
        '<div class="card"><h3>Other formats</h3><div class="row"><button class="btn" data-x="csv"' + (S.run ? '' : ' disabled') + '>Labels (.csv)</button><button class="btn" data-x="print"' + (S.run ? '' : ' disabled') + '>Printable results</button><button class="btn" data-go="trees">Tree figures (SVG, PNG)</button></div>' +
        '<p class="xs faint" style="margin-top:10px">The CSV has one row per model label, with its run, stage, status and review verdict. The printable view joins RQ1–RQ4 and the model agreement for print or PDF.</p></div></div></div>' +
        '<div id="yaml-preview"></div></div>';
    },
    mount: function (el, c) {
      bindGo(el);
      el.addEventListener('click', async function (e) {
        var b = e.target.closest('[data-x]'); if (!b) return;
        var x = b.dataset.x;
        if (x === 'yaml') await app().exportYAML();
        if (x === 'csv') app().exportCSV();
        if (x === 'preview') {
          var rec = await app().record();
          var text = root.PA.yaml.stringify(rec);
          var lines = text.split('\n');
          document.getElementById('yaml-preview').innerHTML = '<div class="card flush"><div class="card-head"><h3>Preview</h3><span class="spacer"></span><span class="faint small num">' + lines.length + ' lines · ' + Math.round(text.length / 1024) + ' KB · first 400 lines</span></div><div class="card-body"><pre class="code">' + esc(lines.slice(0, 400).join('\n')) + '</pre></div></div>';
        }
        if (x === 'print') printable(c);
      });
      el.addEventListener('change', function (e) {
        if (e.target.dataset.x !== 'open' || !e.target.files[0]) return;
        var r = new FileReader(); r.onload = function () { app().importRecord(String(r.result)); }; r.readAsText(e.target.files[0]);
      });
    }
  };

  function printable(c) {
    var w = window.open('', '_blank');
    if (!w) { app().toast('The browser blocked the new window.', 'bad'); return; }
    var css = new URL('style.css', location.href).href;
    var parts = ['coverage', 'stance', 'protection', 'surfaces', 'agreement'].map(function (id) {
      var v = byId(id); return '<h2 style="margin:28px 0 10px;font-size:20px">' + v.title + '</h2>' + v.render(c);
    }).join('');
    w.document.write('<!doctype html><html><head><meta charset="utf-8"><title>Results – ' + esc(c.S.project.app || 'app') + '</title><link rel="stylesheet" href="' + css + '"><style>body{background:#fff;color:#111;padding:24px}.view-inner{padding:0}.callout{color:#111}</style></head><body>' +
      '<h1 style="font-size:24px">' + esc(c.S.project.app || 'App') + '</h1><p>Run ' + esc(c.S.run.finished) + ' · models ' + c.R.models.map(esc).join(', ') + ' · reviewed ' + (c.R.reviewStats.accepted + c.R.reviewStats.rejected) + ' of ' + c.R.reviewStats.total + '</p>' + parts + '</body></html>');
    w.document.close();
  }

  root.PA.views = { TABS: TABS, byId: byId, icon: icon, esc: esc };
})(window);
