// Run with: node --test tests
// Checks the tree logic against scripts/instrument-test/v002/evaluate.py rules,
// the combination rules and the agreement statistics on hand-computed cases.
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const A = require('../js/analysis.js');

function loadModel() {
  const file = path.join(__dirname, '..', 'output', 'data.js');
  const text = fs.readFileSync(file, 'utf8');
  const sandbox = {};
  new Function('window', text)(sandbox);
  return sandbox.PA_DATA.model;
}

test('three-valued AND and OR', () => {
  const s = { a: 'present', b: 'absent', c: 'uncertain' };
  assert.equal(A.evaluate({ and: ['a', 'b'] }, s), 'absent');
  assert.equal(A.evaluate({ and: ['a', 'c'] }, s), 'uncertain');
  assert.equal(A.evaluate({ and: ['a', 'a'] }, s), 'present');
  assert.equal(A.evaluate({ or: ['b', 'c'] }, s), 'uncertain');
  assert.equal(A.evaluate({ or: ['b', 'a'] }, s), 'present');
  assert.equal(A.evaluate({ or: ['b', 'b'] }, s), 'absent');
  assert.throws(() => A.evaluate({ orplus: ['a'] }, s));
});

test('reference model v2: every node exists and K10 needs both parts of a combination', () => {
  const m = loadModel();
  for (const [k, c] of Object.entries(m.capabilities)) {
    for (const leaf of A.leaves(c.needs)) assert.ok(m.components[leaf], `${k} uses ${leaf}`);
  }
  const states = Object.fromEntries(Object.keys(m.components).map((k) => [k, 'absent']));
  states.CO2 = 'present';
  assert.equal(A.evaluateModel(m, states).capabilities.K10, 'absent');
  states.IM7 = 'present';
  assert.equal(A.evaluateModel(m, states).capabilities.K10, 'present');
  assert.equal(A.pathways(m).length, 21);
});

test('a measure that removes a component closes the pathways that need it', () => {
  const m = loadModel();
  const states = Object.fromEntries(Object.keys(m.components).map((k) => [k, 'absent']));
  Object.assign(states, { EX1: 'present', IM2: 'present' });
  assert.equal(A.evaluateModel(m, states).capabilities.K6, 'present');
  const after = A.afterMeasure(m, states, ['IM2']);
  assert.equal(after.P01, 'absent');
});

test('units, headings and spans', () => {
  const u = A.unitize('Title Here\n\nWe store your data.\n\n\nWe share it.', 'policy');
  assert.equal(u.length, 2);
  assert.equal(u[0].heading, 'Title Here');
  assert.ok(A.spanOk('store  your', u[0].text));
  assert.ok(!A.spanOk('sell your', u[0].text));
  const i = A.unitize('Privacy settings\n\nShare usage data', 'interface');
  assert.equal(i.length, 2);
});

test('JSON in fences and with prose around it', () => {
  assert.deepEqual(A.parseJSON('```json\n{"a":1}\n```'), { a: 1 });
  assert.deepEqual(A.parseJSON('Here: {"a":2} done'), { a: 2 });
});

test('combination: routine agreed or uncertain, high-stakes to check, minimisation a proposal', () => {
  const L = (model, code, extra) => Object.assign({ model, stage: 1, unit: 'P001', surface: 'policy', code, span: 'x', status: 'asserted' }, extra);
  const c = A.combine([
    L('a', 'L-CMP', { node: 'IM3' }), L('b', 'L-CMP', { node: 'IM3' }),
    L('a', 'L-CMP', { node: 'IM4' }),
    L('b', 'L-HRM', { harm: 'H-PSY' }),
    { model: 'a', stage: 2, unit: 'P001', surface: 'policy', harm: 'H-PSY', code: 'S-MIN', span: 'x' }
  ], ['a', 'b']);
  const by = Object.fromEntries(c.map((r) => [r.key, r.decision]));
  assert.equal(by['P001|L-CMP|IM3'], 'agreed');
  assert.equal(by['P001|L-CMP|IM4'], 'uncertain');
  assert.equal(by['P001|L-HRM|H-PSY'], 'check');
  assert.equal(by['P001|H-PSY|S-MIN'], 'proposal');
});

test('Krippendorff alpha and Cohen kappa on a known table', () => {
  // 2 coders, 10 items: a=4 both, b=1, c=1, d=4 neither.
  const rows = [];
  for (let i = 0; i < 4; i++) rows.push([1, 1]);
  rows.push([1, 0]); rows.push([0, 1]);
  for (let i = 0; i < 4; i++) rows.push([0, 0]);
  const s = A.pairStats(rows, 0, 1);
  assert.equal(s.agreement, 0.8);
  assert.ok(Math.abs(s.kappa - 0.6) < 1e-9);
  // alpha = 1 - (n-1) * Do/De with n = 20 values: Do = 2/20 coincidences off-diagonal... = 0.6190...
  assert.ok(Math.abs(s.alpha - (1 - (19 * 4) / (2 * 10 * 10))) < 1e-9);
  assert.equal(A.krippendorffAlpha([[1, 1], [1, 1]]), null);
});

test('coverage levels and applicability proposal', () => {
  const m = loadModel();
  const L = (code, extra) => Object.assign({ model: 'a', stage: 1, unit: 'P001', surface: 'policy', code, span: 'x', status: 'asserted' }, extra);
  const comb = A.combine([L('L-CMP', { node: 'IM3' }), L('L-CMP', { node: 'CX3' }), L('L-HRM', { harm: 'H-PSY' }), L('L-CMP', { node: 'IM7', status: 'denied' })], ['a']);
  const cov = A.coverage(m, comb, 'policy', 'agreed');
  assert.equal(cov.P05.level, 3); // K5 -> H-PSY named
  assert.equal(cov.P20.level, 1); // K5 -> H-SOC: only components
  assert.equal(cov.P02.level, 1); // K8 via IM7: a denial is still a mention
  assert.equal(cov.P02.denied, true);
  assert.equal(cov.P07.level, 0); // K7 needs EX2, IM2 or CX1: none mentioned
  assert.equal(cov.P07.categoryOnly, true); // H-PSY is named, but not for this pathway
  const prop = A.proposeApplicability(m, comb, {});
  assert.equal(prop.IM3.state, 'present');
  assert.equal(prop.IM7.state, 'absent');
  assert.equal(prop.IM12.state, 'uncertain');
  assert.equal(prop.EX1.state, 'present');
  assert.equal(prop.EX2.state, 'uncertain');
});

test('term view: print, parse, round trip and errors', () => {
  const m = loadModel();
  const ids = Object.keys(m.components);
  for (const [k, c] of Object.entries(m.capabilities)) {
    const s = A.termToString(c.needs);
    assert.deepStrictEqual(A.parseTerm(s, ids), c.needs, k + ': ' + s);
  }
  assert.equal(A.termToString(m.capabilities.K5.needs), '(IM3 OR IM4) AND (CX2 OR CX3)');
  assert.throws(() => A.parseTerm('IM3 AND IM4 OR CX2', ids), /brackets/);
  assert.throws(() => A.parseTerm('IM3 AND (IM4', ids), /bracket/);
  assert.throws(() => A.parseTerm('IM99', ids), /unknown component/);
  assert.deepStrictEqual(A.parseTerm('im3 and cx2', ids), { and: ['IM3', 'CX2'] });
});

test('model check finds broken trees', () => {
  const m = JSON.parse(JSON.stringify(loadModel()));
  assert.deepStrictEqual(A.checkModel(m), []);
  m.components.IM99 = { origin: 'implementation', label: 'x', feature: 'y' };
  m.harms['H-PSY'].pathways.push({ id: 'P05', capability: 'K42', consequence: 'c', basis: 'argued', sources: [] });
  const p = A.checkModel(m).join('\n');
  assert.match(p, /IM99 is in no capability/);
  assert.match(p, /duplicate pathway P05/);
  assert.match(p, /unknown capability K42/);
  assert.equal(A.nextId(Object.keys(m.components), 'IM'), 'IM100');
});
