// Run with: node --test tests
const test = require('node:test');
const assert = require('node:assert');
const Y = require('../js/yaml.js');

test('round trip of nested records, blocks and awkward strings', () => {
  const rec = {
    format: 'policy-harm-analyzer/2',
    empty: [], none: {}, n: 3, f: 0.25, t: true, z: null,
    'key with space': 'x',
    yes: 'quoted key', // YAML 1.1 would read a plain yes as a boolean
    text: 'Line one\n  indented line\n\nafter a blank line',
    colon: 'a: b # not a comment',
    list: ['a', 2, null, { k: 'v', inner: [1, 2], block: 'x\ny\n' }, [1, [2]], { only: [] }],
    deep: { a: { b: { c: [{ d: 'e' }] } } },
    unicode: 'Ärztin – “Zitat” 🙂'
  };
  const text = Y.stringify(rec, 'header line');
  assert.match(text, /^# header line\n/);
  assert.deepStrictEqual(Y.parse(text), rec);
});

test('literal block keeps leading spaces of its first line', () => {
  const rec = { code: '  starts indented\nnext' };
  assert.deepStrictEqual(Y.parse(Y.stringify(rec)), rec);
});
