// Renders the analysis as HTML. Policy text and model output are untrusted:
// everything taken from them goes through esc().
(function (root) {
  'use strict';
  var A = root.PA.analysis;

  function esc(s) {
    return String(s === null || s === undefined ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pct(x) { return x === null || x === undefined || isNaN(x) ? '–' : (100 * x).toFixed(0) + '%'; }
  function num(x, d) { return x === null || x === undefined || isNaN(x) ? '–' : x.toFixed(d === undefined ? 2 : d); }
  function badge(state) { return '<span class="st st-' + esc(state) + '">' + esc(state) + '</span>'; }
  function lvl(l) { return '<span class="lv lv' + l + '">' + l + '</span>'; }
  function table(head, rows, cls) {
    return '<div class="tw"><table class="' + (cls || '') + '"><thead><tr>' + head.map(function (h) { return '<th>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + (rows.length ? rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('')
        : '<tr><td colspan="' + head.length + '" class="muted">None.</td></tr>') + '</tbody></table></div>';
  }

  var LEVEL_NAMES = ['0 silent', '1 component', '2 capability', '3 harm'];
  var ALPHA_NOTE = 'α ≥ .800 reliable, .667–.800 tentative, below .667 unreliable (Krippendorff); undefined without variation.';

  function exprHTML(expr, model, states) {
    if (typeof expr === 'string') {
      var c = model.components[expr];
      return '<span class="cmp o-' + esc(c.origin) + '" title="' + esc(c.label + ' – ' + c.feature) + '">' + esc(expr) +
        (states ? ' ' + badge(states[expr]) : '') + '</span>';
    }
    var op = Object.keys(expr)[0];
    return '<span class="op">(' + expr[op].map(function (e) { return exprHTML(e, model, states); }).join(' <b>' + op.toUpperCase() + '</b> ') + ')</span>';
  }

  // ---------- Harm trees ----------
  function trees(model, ev, states, covP, covI) {
    return Object.keys(model.harms).map(function (h) {
      var harm = model.harms[h];
      var body = harm.pathways.map(function (p) {
        var cap = model.capabilities[p.capability];
        return '<li><div class="pw"><b>' + esc(p.id) + '</b> ' + (ev ? badge(ev.pathways[p.id]) : '') +
          (covP ? ' policy ' + lvl(covP[p.id].level) : '') + (covI ? ' interface ' + lvl(covI[p.id].level) : '') +
          ' <span class="muted">' + esc(p.basis) + '</span> – ' + esc(p.consequence) + (p.tag ? ' <span class="tag">' + esc(p.tag) + '</span>' : '') + '</div>' +
          '<div class="capline"><b>' + esc(p.capability) + '</b> ' + esc(cap.label) + ' <span class="muted">(' + esc(cap.actor) + ')</span> ' +
          (ev ? badge(ev.capabilities[p.capability]) : '') + '</div>' +
          '<div class="needs">needs ' + exprHTML(cap.needs, model, states) + '</div>' +
          '<div class="src muted">' + esc((p.sources || []).join('; ')) + '</div></li>';
      }).join('');
      return '<details class="tree"' + (ev && ev.harms[h] !== 'absent' ? ' open' : '') + '><summary><b>' + esc(h) + '</b> ' + esc(harm.label) +
        (ev ? ' ' + badge(ev.harms[h]) : '') + '</summary><ul>' + body + '</ul></details>';
    }).join('');
  }

  function legend() {
    return '<p class="legend">Origins: <span class="cmp o-core">core</span> <span class="cmp o-context">digital context</span> ' +
      '<span class="cmp o-implementation">implementation choice</span> <span class="cmp o-external">event outside the app</span>. ' +
      'Levels: ' + LEVEL_NAMES.map(function (n, i) { return lvl(i) + ' ' + n.slice(2); }).join(' ') + '.</p>';
  }

  // ---------- Sections ----------

  function summary(R) {
    var warn = [
      'Automated coding. Every high-stakes label (named harm, generic risk, stance, framing, strength, reassurance) is marked <i>to check</i>; a person must confirm it.',
      'Applicability, minimisation and potential mismatches are decided by people. The page proposes; the analyst decides in the tables below.',
      'Figures are detection summaries of what the models found. They are not corrected estimates: that needs the double-coded validation sample.',
      'Absence means “not found by the models in the captured text”, not that the provider is silent.'
    ];
    var sp = R.shares;
    return '<section id="r-summary"><h2>Summary</h2>' +
      '<p><b>' + esc(R.app || 'Unnamed app') + '</b> · ' + esc(R.date) + ' · ' + R.units.policy + ' policy units' +
      (R.units.interface ? ', ' + R.units.interface + ' interface units' : '') + ' · models: ' + R.models.map(esc).join(', ') + '</p>' +
      '<p class="muted">Instruments: reference model v' + esc(R.sources.modelVersion) + ' (' + esc(R.sources.model) + '), prompts ' +
      esc(R.sources.prompts) + '.</p>' +
      '<div class="cards">' +
      card('Applicable pathways', R.pathCounts.present + ' of ' + R.pathCounts.total, R.pathCounts.uncertain + ' uncertain, ' + R.pathCounts.absent + ' not applicable') +
      card('Policy: harm named (level 3)', pct(sp.policyA.shares[3]), 'of applicable pathways; with uncertain: ' + pct(sp.policyB.shares[3])) +
      card('Policy: silent (level 0)', pct(sp.policyA.shares[0]), 'of applicable pathways; with uncertain: ' + pct(sp.policyB.shares[0])) +
      card('Named-harm mentions', R.harmMentions, R.toCheck + ' labels to check by a person') +
      card('Protection claims', R.claims, R.reassurance + ' reassurance without a measure') +
      card('Model agreement', R.alphaComponents === null ? '–' : 'α ' + num(R.alphaComponents), 'components across all models') +
      '</div><ul class="warn">' + warn.map(function (w) { return '<li>' + w + '</li>'; }).join('') + '</ul></section>';
  }
  function card(t, v, s) { return '<div class="card"><div class="ct">' + t + '</div><div class="cv">' + v + '</div><div class="cs">' + s + '</div></div>'; }

  function rq1(R) {
    var model = R.model;
    var rows = A.pathways(model).map(function (p) {
      return [esc(p.id), esc(p.harm), esc(p.capability), badge(R.ev.pathways[p.id]),
        lvl(R.covPolicyA[p.id].level) + (R.covPolicyB[p.id].level !== R.covPolicyA[p.id].level ? ' <span class="muted">(' + R.covPolicyB[p.id].level + ' with uncertain)</span>' : '') +
          (R.covPolicyA[p.id].denied ? ' <span class="tag">denied</span>' : '') +
          (R.covPolicyA[p.id].categoryOnly ? ' <span class="tag">harm named for the category only</span>' : ''),
        R.hasInterface ? lvl(R.covIfA[p.id].level) : '–',
        esc(R.covPolicyB[p.id].evidence.slice(0, 6).join(', ')),
        esc(p.basis) + (A.assumptionDependent(model, p) ? ' · assumption' : '')];
    });
    var shareRows = [['Policy, scenario A (applicable)', R.shares.policyA], ['Policy, scenario B (+ uncertain)', R.shares.policyB]];
    if (R.hasInterface) shareRows.push(['Interface, scenario A', R.shares.ifA], ['Interface, scenario B', R.shares.ifB]);
    var harmRows = Object.keys(model.harms).map(function (h) {
      var ps = model.harms[h].pathways.filter(function (p) { return R.ev.pathways[p.id] === 'present'; });
      var best = ps.reduce(function (m, p) { return Math.max(m, R.covPolicyA[p.id].level); }, -1);
      var catOnly = ps.some(function (p) { return R.covPolicyA[p.id].categoryOnly; });
      return [esc(h) + ' ' + esc(model.harms[h].label), badge(R.ev.harms[h]), ps.length,
        best < 0 ? '–' : lvl(best),
        best === 3 ? 'Named; check that consequence, data, actor and access match'
          : (catOnly ? 'Named for the category, but not on an applicable pathway the text reaches'
            : (best >= 0 ? 'No named harm of this category found by the models' : ''))];
    });
    return '<section id="r-rq1"><h2>RQ1 · Coverage</h2>' +
      '<p>Each applicable pathway gets the highest level the text reaches. Routine labels count when every model returned them (scenario A uses only these and applicable pathways); “with uncertain” adds one-model and unsure labels. Level 3 is a category-level candidate until a person checks it.</p>' +
      table(['Basis', 'n', LEVEL_NAMES[0], LEVEL_NAMES[1], LEVEL_NAMES[2], LEVEL_NAMES[3]], shareRows.map(function (r) {
        return [r[0], r[1].n].concat(r[1].shares.map(pct));
      })) +
      '<h3>By harm category</h3>' + table(['Harm', 'Applies', 'Applicable pathways', 'Highest policy level', 'Note'], harmRows) +
      '<h3>By pathway</h3>' + table(['Pathway', 'Harm', 'Capability', 'Applicable', 'Policy level', 'Interface level', 'Evidence units', 'Basis'], rows, 'small') +
      '</section>';
  }

  function rq2(R) {
    var rows = R.harmRecords.map(function (h) {
      return [esc(h.unit), esc(h.harm), '<q>' + esc(h.span) + '</q>', esc(h.foundBy.join(', ')),
        R.models.map(function (m) { return esc((h.stances[m] || []).join(', ') || '–'); }).join('<br>'),
        esc(h.union.join(', ') || '–') + (h.union.indexOf('S-MIN') >= 0 ? ' <span class="tag">S-MIN proposal: people decide</span>' : '')];
    });
    var counts = Object.keys(R.stanceCounts).map(function (k) { return [esc(k), R.stanceCounts[k]]; });
    return '<section id="r-rq2"><h2>RQ2 · Stance</h2>' +
      '<p>Stance attaches to named harms only. Every row is the union of the models and must be checked by a person.</p>' +
      table(['Unit', 'Harm', 'Span', 'Named by', 'Stance per model (' + R.models.map(esc).join(' / ') + ')', 'Union'], rows) +
      '<h3>Counts (union, before checking)</h3>' + table(['Stance', 'Mentions'], counts) +
      '<p>Without a named harm (secondary analysis): generic risk <b>' + R.secondary.gen + '</b>, generic responsibility <b>' + R.secondary.grs +
      '</b>, reassurance <b>' + R.secondary.rea + '</b>.</p></section>';
  }

  function rq3(R) {
    var comps = Object.keys(R.model.components);
    var rows = R.claimRecords.map(function (c, i) {
      var sel = '<select data-claim="' + i + '"><option value="">– choose –</option>' + comps.map(function (id) {
        return '<option value="' + id + '"' + (c.removes === id ? ' selected' : '') + '>' + id + ' ' + esc(R.model.components[id].label) + '</option>';
      }).join('') + '</select>';
      var open = c.removes ? (c.leftOpen.length ? '<span class="warn-t">' + esc(c.leftOpen.join(', ')) + '</span>' : 'none') : '<span class="muted">choose a component</span>';
      return [esc(c.unit), esc(c.code), '<q>' + esc(c.span) + '</q>', esc(c.framing || '–'), esc(c.strength || '–'),
        esc(c.foundBy.join(', ')) + (c.decision === 'uncertain' ? ' <span class="tag">uncertain</span>' : ''), sel,
        c.removes ? esc(c.closes.join(', ') || 'none') : '–', open];
    });
    return '<section id="r-rq3"><h2>RQ3 · Protection</h2>' +
      '<p>For each claimed measure, choose the component it would remove if it worked as described. The trees are then evaluated again. Of the applicable pathways that contain that component, those that close are cut by the measure; those that stay open (another route remains) are candidate mismatches, which a person decides. C-REA is reassurance without a measure.</p>' +
      table(['Unit', 'Measure', 'Span', 'Framing', 'Strength', 'Found by', 'Would remove', 'Pathways it cuts', 'Pathways it leaves open'], rows, 'small') + '</section>';
  }

  function rq4(R) {
    if (!R.hasInterface) return '<section id="r-rq4"><h2>RQ4 · Surfaces</h2><p class="muted">Add interface text (from the walkthrough) to compare the policy with the interface.</p></section>';
    var rows = [], higher = 0, lower = 0, same = 0;
    A.pathways(R.model).forEach(function (p) {
      if (R.ev.pathways[p.id] !== 'present') return;
      var a = R.covPolicyA[p.id].level, b = R.covIfA[p.id].level;
      if (a > b) lower++; else if (b > a) higher++; else same++;
      if (a !== b) rows.push([esc(p.id), esc(p.harm), lvl(a), lvl(b), a > b ? 'interface says less' : 'interface says more']);
    });
    return '<section id="r-rq4"><h2>RQ4 · Surfaces</h2><p>Applicable pathways: interface lower than policy <b>' + lower + '</b>, higher <b>' + higher +
      '</b>, same <b>' + same + '</b>. The policy is a full document; the interface text covers the recorded routes only.</p>' +
      table(['Pathway', 'Harm', 'Policy', 'Interface', 'Difference'], rows) + '</section>';
  }

  function agreementSection(R) {
    var G = R.agreement;
    var fam = [];
    G.families.forEach(function (f) {
      f.pairs.forEach(function (p) {
        fam.push([esc(f.name), esc(p.a) + ' × ' + esc(p.b), p.both, p.onlyA, p.onlyB, pct(p.agreement), num(p.kappa), num(p.pabak),
          num(p.positiveAgreement), num(p.alpha), pct(p.prevalence)]);
      });
      if (R.models.length > 2) fam.push([esc(f.name), '<i>all models</i>', '', '', '', '', '', '', '', num(f.alphaAll), '']);
    });
    var adds = R.models.map(function (m) { var a = G.adds[m]; return [esc(m), a.total, a.only, pct(a.shareOfUnion)]; });
    var per = G.values.map(function (v) {
      return [esc(v.value), v.stage].concat(R.models.map(function (m) { return v.by[m] || 0; })).concat([v.union, v.allModels, num(v.positiveAgreement)]);
    });
    var perModel = R.models.map(function (m) {
      var s = R.perModel[m];
      return [esc(m), esc(s.servedBy || ''), s.labels, s.failures, s.errors, s.calls, (s.ms / 1000).toFixed(1) + ' s',
        s.tokensIn ? s.tokensIn + ' / ' + s.tokensOut : '–', s.stability === null ? '–' : num(s.stability),
        s.wording === null ? '–' : num(s.wording)];
    });
    var levelDiff = R.levelDeviation.map(function (d) {
      return [esc(d.id), esc(d.harm)].concat(R.models.map(function (m) { return lvl(d.levels[m]); }));
    });
    var applDiff = R.applicabilityDeviation.map(function (d) {
      return [esc(d.id)].concat(R.models.map(function (m) { return badge(d.states[m]); }));
    });
    return '<section id="r-agree"><h2>Model–model deviation</h2>' +
      '<p>Agreement is a robustness check, not accuracy: model errors are correlated, so two models can agree and both be wrong. Accuracy needs human reference labels. Statistics use one binary indicator per unit and coded value. ' + ALPHA_NOTE + '</p>' +
      table(['Family', 'Pair', 'Both', 'Only first', 'Only second', 'Raw agreement', 'Cohen κ', 'PABAK', 'Positive agr.', 'Krippendorff α', 'Prevalence'], fam, 'small') +
      '<h3>Labels found by every model</h3><p>' + G.shared.n + ' of ' + G.union + ' labels. Same status (asserted, possible, denied): ' + pct(G.shared.statusAgreement) +
      '; same framing: ' + pct(G.shared.framingAgreement) + '; same strength: ' + pct(G.shared.strengthAgreement) +
      '; mean span overlap (token Jaccard): ' + num(G.shared.meanSpanJaccard) + '.</p>' +
      '<h3>What each model adds</h3>' + table(['Model', 'Labels', 'Found by it alone', 'Share of all labels'], adds) +
      '<h3>Per model</h3>' + table(['Model', 'Served by', 'Labels', 'Invalid spans', 'Failed calls', 'Calls', 'Time', 'Tokens in / out', 'Run-to-run α', 'Prompt vs paraphrase α'], perModel, 'small') +
      '<h3>Coverage level by model</h3><p>Pathways whose policy level differs when each model\'s labels are used alone (' + R.levelDeviation.length + ' of ' + R.pathCounts.total + ').</p>' +
      table(['Pathway', 'Harm'].concat(R.models.map(esc)), levelDiff) +
      '<h3>Applicability proposal by model</h3><p>Components whose proposed state differs by model (' + R.applicabilityDeviation.length + ').</p>' +
      table(['Component'].concat(R.models.map(esc)), applDiff) +
      '<h3>By coded value</h3>' + table(['Value', 'Stage'].concat(R.models.map(esc)).concat(['Union', 'All models', 'Positive agr.']), per, 'small') +
      '</section>';
  }

  function labelsSection(R) {
    var rows = R.combined.map(function (r) {
      return [esc(r.unit), esc(r.code), esc(r.node || r.harm || ''), esc(r.status || ''), esc(r.decision), esc(Object.keys(r.by).join(', ')), '<q>' + esc(r.span) + '</q>'];
    });
    var fails = R.failures.map(function (f) { return [esc(f.model), f.stage, esc(f.unit || ''), esc(f.code || ''), esc(f.reason), esc(f.span || '')]; });
    return '<section id="r-labels"><h2>All combined labels</h2>' +
      '<p><i>agreed</i>: every model, none unsure · <i>uncertain</i>: one model only or unsure (a validation stratum) · <i>check</i>: high-stakes, union, a person decides · <i>proposal</i>: decided by people only.</p>' +
      table(['Unit', 'Code', 'Node / harm', 'Status', 'Decision', 'Models', 'Span'], rows, 'small') +
      '<h3>Dropped labels and failures</h3>' + table(['Model', 'Stage', 'Unit', 'Code', 'Reason', 'Span'], fails, 'small') + '</section>';
  }

  function render(R) {
    return summary(R) + rq1(R) + rq2(R) + rq3(R) + rq4(R) + agreementSection(R) +
      '<section id="r-trees"><h2>Harm trees for this app</h2>' + legend() + trees(R.model, R.ev, R.states, R.covPolicyA, R.hasInterface ? R.covIfA : null) + '</section>' +
      labelsSection(R);
  }

  root.PA.report = { render: render, trees: trees, legend: legend, esc: esc, badge: badge, exprHTML: exprHTML };
})(window);
