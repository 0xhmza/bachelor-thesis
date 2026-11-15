// Calls to the language models. Keys stay in the page and go only to the
// provider of the model they belong to. Each call sends the frozen stage
// prompt as the system text and the units as the user text, and returns the
// raw text, which analysis.js parses and checks.
(function (root) {
  'use strict';

  var PROVIDERS = {
    anthropic: { name: 'Anthropic (Claude)', model: 'claude-opus-5-5', needsKey: true,
      hint: 'Messages API, called from the browser.' },
    openai: { name: 'OpenAI', model: '', needsKey: true,
      hint: 'Chat Completions API. Enter the model id you have access to.' },
    gemini: { name: 'Google Gemini', model: '', needsKey: true,
      hint: 'generateContent API. Enter the model id, for example from Google AI Studio.' },
    compatible: { name: 'OpenRouter / OpenAI-compatible', model: '', needsKey: false, baseUrl: 'https://openrouter.ai/api/v1',
      hint: 'Any OpenAI-compatible endpoint: OpenRouter, or a local Ollama (http://localhost:11434/v1) or LM Studio server. Prefer an open-weight model for one of the two.' },
    bridge: { name: 'Local CLI bridge (testing only)', model: 'codex', needsKey: true, baseUrl: 'http://127.0.0.1:8790/v1',
      hint: 'Runs Claude Code or Codex on this computer through cli_bridge.py (start it, paste the bridge key it prints). Models: codex, codex:<model>, claude-code, claude-code:<model>. For testing the page only: the CLIs add their own behaviour, so this is not a frozen model call for the study.' },
    demo: { name: 'Offline demo coder (no API)', model: 'demo-a', needsKey: false,
      hint: 'Keyword rules in the page, for trying the site. Not a language model; its labels mean nothing. Use demo-a and demo-b to see two coders differ.' }
  };

  function withTimeout(ms, signal) {
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, ms);
    if (signal) signal.addEventListener('abort', function () { ctrl.abort(); });
    return { signal: ctrl.signal, done: function () { clearTimeout(t); } };
  }

  async function postJSON(url, headers, body, signal) {
    var to = withTimeout(10 * 60 * 1000, signal);
    try {
      var res = await fetch(url, { method: 'POST', headers: headers, body: JSON.stringify(body), signal: to.signal });
      var text = await res.text();
      var data;
      try { data = JSON.parse(text); } catch (e) { data = null; }
      if (!res.ok) {
        var msg = data && (data.error && (data.error.message || data.error.type) || data.message) || text.slice(0, 300);
        var err = new Error('HTTP ' + res.status + ': ' + msg);
        err.status = res.status;
        throw err;
      }
      return data;
    } finally { to.done(); }
  }

  async function callAnthropic(cfg, system, user, signal) {
    var body = { model: cfg.model, max_tokens: 16000, system: system,
      messages: [{ role: 'user', content: user }], fallbacks: 'default' };
    if (cfg.effort) body.output_config = { effort: cfg.effort };
    var data = await postJSON('https://api.anthropic.com/v1/messages', {
      'content-type': 'application/json',
      'x-api-key': cfg.key,
      'anthropic-version': '2026-10-21',
      'anthropic-beta': 'server-side-fallback-2026-07-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    }, body, signal);
    if (data.stop_reason === 'refusal') {
      throw new Error('refused by the model' + (data.stop_details && data.stop_details.category ? ' (' + data.stop_details.category + ')' : ''));
    }
    if (data.stop_reason === 'max_tokens') throw new Error('output cut at max_tokens; lower the units per request');
    var text = (data.content || []).filter(function (b) { return b.type === 'text'; }).map(function (b) { return b.text; }).join('');
    return { text: text, usage: data.usage ? { input: data.usage.input_tokens, output: data.usage.output_tokens } : null,
      servedBy: data.model || cfg.model };
  }

  async function callOpenAICompatible(url, cfg, system, user, signal, jsonMode) {
    var body = { model: cfg.model, messages: [{ role: 'system', content: system }, { role: 'user', content: user }] };
    if (jsonMode) body.response_format = { type: 'json_object' };
    if (cfg.temperature !== '' && cfg.temperature !== undefined && cfg.temperature !== null) body.temperature = Number(cfg.temperature);
    var headers = { 'content-type': 'application/json' };
    if (cfg.key) headers.authorization = 'Bearer ' + cfg.key;
    var data = await postJSON(url, headers, body, signal);
    var choice = data.choices && data.choices[0];
    if (!choice) throw new Error('no choices in the response');
    if (choice.finish_reason === 'length') throw new Error('output cut at the length limit; lower the units per request');
    return { text: choice.message && choice.message.content || '',
      usage: data.usage ? { input: data.usage.prompt_tokens, output: data.usage.completion_tokens } : null,
      servedBy: data.model || cfg.model };
  }

  async function callGemini(cfg, system, user, signal) {
    var body = { systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: 'user', parts: [{ text: user }] }],
      generationConfig: { responseMimeType: 'application/json' } };
    if (cfg.temperature !== '' && cfg.temperature !== undefined) body.generationConfig.temperature = Number(cfg.temperature);
    var url = 'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(cfg.model) + ':generateContent';
    var data = await postJSON(url, { 'content-type': 'application/json', 'x-goog-api-key': cfg.key }, body, signal);
    var cand = data.candidates && data.candidates[0];
    if (!cand) throw new Error('no candidates' + (data.promptFeedback ? ' (' + JSON.stringify(data.promptFeedback) + ')' : ''));
    if (cand.finishReason === 'MAX_TOKENS') throw new Error('output cut at the token limit; lower the units per request');
    var text = (cand.content && cand.content.parts || []).map(function (p) { return p.text || ''; }).join('');
    var u = data.usageMetadata;
    return { text: text, usage: u ? { input: u.promptTokenCount, output: u.candidatesTokenCount } : null, servedBy: cfg.model };
  }

  async function call(cfg, system, user, signal) {
    var started = Date.now(), out;
    if (cfg.provider === 'anthropic') out = await callAnthropic(cfg, system, user, signal);
    else if (cfg.provider === 'openai') out = await callOpenAICompatible('https://api.openai.com/v1/chat/completions', cfg, system, user, signal, true);
    else if (cfg.provider === 'gemini') out = await callGemini(cfg, system, user, signal);
    else if (cfg.provider === 'compatible') {
      var base = String(cfg.baseUrl || PROVIDERS.compatible.baseUrl).replace(/\/+$/, '');
      out = await callOpenAICompatible(base + '/chat/completions', cfg, system, user, signal, cfg.jsonMode !== false);
    } else if (cfg.provider === 'bridge') {
      var bb = String(cfg.baseUrl || PROVIDERS.bridge.baseUrl).replace(/\/+$/, '');
      out = await callOpenAICompatible(bb + '/chat/completions', cfg, system, user, signal, false);
    } else if (cfg.provider === 'demo') out = { text: root.PA.demo.code(cfg.model, system, user), usage: null, servedBy: cfg.model };
    else throw new Error('unknown provider ' + cfg.provider);
    out.ms = Date.now() - started;
    return out;
  }

  // ---------- Offline demo coder ----------
  // Keyword rules that imitate the output format. Two variants miss and add
  // different things, so that the agreement view has something to show.

  var RULES = [
    { node: 'CO1', code: 'L-CMP', re: /\b(cycle|period|symptom|weight|heart rate|sleep|steps?|mood|health data|log(?:ged|s)?)\b/i },
    { node: 'CO2', code: 'L-CMP', re: /\b(predict\w*|estimat\w*|insights?|forecast\w*)\b/i },
    { node: 'CO3', code: 'L-CMP', re: /\b(history|retain\w*|for as long as)\b/i },
    { node: 'CX2', code: 'L-CMP', re: /\b(IP address|device (?:data|information))\b/i },
    { node: 'CX3', code: 'L-CMP', re: /\b(advertising identifier|device identifiers?|push token)\b/i, variant: 'a' },
    { node: 'IM1', code: 'L-CMP', re: /\b(account|e-?mail address)\b/i },
    { node: 'IM2', code: 'L-CMP', re: /\b(servers?|cloud|backup|synchroni[sz]\w*)\b/i },
    { node: 'IM3', code: 'L-CMP', re: /\b(analytics|crash report\w*|monitoring)\b/i },
    { node: 'IM4', code: 'L-CMP', re: /\b(advertis\w*|attribution|marketing partners?)\b/i },
    { node: 'IM5', code: 'L-CMP', re: /\b(processors?|service providers?|support tool)\b/i, variant: 'b' },
    { node: 'IM6', code: 'L-CMP', re: /\b(de-identified|pseudonymi[sz]ed|anonymi[sz]ed|research partners?)\b/i },
    { node: 'IM7', code: 'L-CMP', re: /\b(sell|sold|personali[sz]ed offers?|recommendations?)\b/i },
    { node: 'IM8', code: 'L-CMP', re: /\b(GPS|location|routes?)\b/i },
    { node: 'IM9', code: 'L-CMP', re: /\b(share with (?:your )?partner|community|friends)\b/i },
    { node: 'IM10', code: 'L-CMP', re: /\b(outside the (?:EU|EEA|European)|United States|third countr\w*)\b/i },
    { node: 'K2', code: 'L-CAP', re: /\b(infer\w*|derive\w*)\b/i },
    { node: 'K5', code: 'L-CAP', re: /\b(profil\w*|across (?:apps|services))\b/i, variant: 'a' },
    { node: 'K6', code: 'L-CAP', re: /\b(unauthori[sz]ed (?:access|party)|breach|hack\w*)\b/i },
    { node: 'K7', code: 'L-CAP', re: /\b(law enforcement|court order|authorit\w*|subpoena)\b/i },
    { harm: 'H-PSY', code: 'L-HRM', re: /\b(distress|anxiety|embarrass\w*|unwanted contact)\b/i },
    { harm: 'H-ECO', code: 'L-HRM', re: /\b(fraud|identity theft|higher premiums?)\b/i },
    { harm: 'H-DSC', code: 'L-HRM', re: /\b(discriminat\w*|unequal treatment)\b/i, variant: 'b' },
    { harm: 'H-AUT', code: 'L-HRM', re: /\b(prosecut\w*|restrict\w* your choices)\b/i },
    { code: 'L-GEN', re: /\b(could be used against you|risks?)\b/i },
    { code: 'S-GRS', re: /\byou are responsible\b/i },
    { code: 'P-NOT', re: /\b(notify you|as required by law)\b/i }
  ];
  var CLAIMS = [
    { code: 'T-ENC', re: /\bencrypt\w*\b/i, framing: 'F-FLW', strength: 'scoped' },
    { code: 'T-DEV', re: /\b(on your device|stays on (?:your )?(?:phone|device))\b/i, framing: 'F-FLW', strength: 'scoped' },
    { code: 'T-ANO', re: /\b(anonymi[sz]\w*|pseudonymi[sz]\w*|aggregat\w*)\b/i, framing: 'F-FLW', strength: 'partial' },
    { code: 'N-COM', re: /\b(never sell|do not sell|will not sell)\b/i, framing: 'F-FLW', strength: 'absolute' },
    { code: 'C-REA', re: /\b(safe with us|we take your privacy seriously|secure)\b/i },
    { code: 'T-SEC', re: /\b(access control|app lock|passcode)\b/i, framing: 'F-HRM', strength: 'partial', variant: 'b' }
  ];

  function hit(re, text) {
    var m = re.exec(text);
    if (!m) return null;
    // The demo quotes the matched words and a little context, all from the unit.
    var a = Math.max(0, text.lastIndexOf(' ', Math.max(0, m.index - 20)) + 1);
    var end = text.indexOf(' ', m.index + m[0].length + 15);
    return text.slice(a, end < 0 ? text.length : end).trim();
  }

  function denied(span) { return /\b(never|not|no)\b/i.test(span); }

  function demoCode(variant, system, user) {
    var v = /b$/.test(variant) ? 'b' : 'a';
    var units = user.split('\n').map(function (l) { try { return JSON.parse(l); } catch (e) { return null; } })
      .filter(function (u) { return u && u.unit && u.text; });
    if (/S-ACK/.test(system)) {
      return JSON.stringify({ harms: units.map(function (u) {
        var stances = [];
        var q = hit(/\b(unlikely|rare\w*|may|might)\b/i, u.text);
        var h = u.span || hit(/\w+/, u.text);
        if (h) stances.push({ code: 'S-ACK', span: h, reason: 'demo rule' });
        if (q) stances.push({ code: 'S-QUA', target: 'likelihood of the event', span: q, reason: 'demo rule' });
        if (v === 'b' && hit(/\bno cause for concern\b/i, u.text)) stances.push({ code: 'S-MIN', span: hit(/\bno cause for concern\b/i, u.text), reason: 'demo rule' });
        return { unit: u.unit, harm: u.harm, stances: stances };
      }) });
    }
    if (/T-3RD/.test(system) && /FRAMING/.test(system)) {
      return JSON.stringify({ claims: units.map(function (u) {
        var claims = [];
        CLAIMS.forEach(function (r) {
          if (r.variant && r.variant !== v) return;
          var s = hit(r.re, u.text);
          if (!s) return;
          var c = { code: r.code, span: s, reason: 'demo rule' };
          if (r.code !== 'C-REA') { c.actor = 'unclear'; c.data = 'unclear'; c.outcome = 'unclear'; c.conditions = 'unclear'; c.framing = r.framing; c.strength = v === 'b' && r.strength === 'absolute' ? 'scoped' : r.strength; }
          claims.push(c);
        });
        return { unit: u.unit, claims: claims };
      }).filter(function (c) { return c.claims.length; }) });
    }
    return JSON.stringify({ units: units.map(function (u) {
      var codes = [];
      RULES.forEach(function (r) {
        if (r.variant && r.variant !== v) return;
        var s = hit(r.re, u.text);
        if (!s) return;
        var c = { code: r.code, status: denied(s) ? 'denied' : (/\b(may|might|could)\b/i.test(s) ? 'possible' : 'asserted'), span: s, reason: 'demo rule' };
        if (r.node) c.node = r.node;
        if (r.harm) c.harm = r.harm;
        if (v === 'b' && r.code === 'L-CMP' && /\bmay\b/i.test(u.text)) c.unsure = true;
        codes.push(c);
      });
      var protection = CLAIMS.some(function (r) { return r.re.test(u.text); });
      return { unit: u.unit, codes: codes, flags: { harm: codes.some(function (c) { return c.code === 'L-HRM'; }), protection: protection } };
    }).filter(function (u) { return u.codes.length || u.flags.protection; }) });
  }

  root.PA = root.PA || {};
  root.PA.providers = PROVIDERS;
  root.PA.llm = { call: call };
  root.PA.demo = { code: demoCode };
})(window);
