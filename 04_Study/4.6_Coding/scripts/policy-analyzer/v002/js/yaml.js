// YAML for the analysis record. The emitter writes block YAML 1.2: mappings,
// sequences, double-quoted strings, literal blocks for multi-line text. The
// parser reads that same subset back, so a saved record can be reopened.
// Any YAML 1.2 reader (PyYAML, ruamel, js-yaml) reads the files.
(function (root) {
  'use strict';

  var PLAIN_KEY = /^[A-Za-z_][A-Za-z0-9_.\-]*$/;

  function quote(s) { return JSON.stringify(String(s)); }

  function scalar(v) {
    if (v === null || v === undefined) return 'null';
    if (typeof v === 'boolean') return v ? 'true' : 'false';
    if (typeof v === 'number') return isFinite(v) ? String(Math.round(v * 1e6) / 1e6) : 'null';
    return quote(v);
  }

  function key(k) { return PLAIN_KEY.test(k) && !/^(true|false|null|yes|no|on|off|y|n)$/i.test(k) ? k : quote(k); }

  function isMultiline(v) { return typeof v === 'string' && v.indexOf('\n') >= 0 && !/[\u0000-\u0008\u000b-\u001f\u007f]/.test(v); }

  function block(v, pad) {
    // Literal block with an explicit indentation indicator, so leading spaces survive.
    var keep = /\n$/.test(v) ? '' : '-';
    var lines = v.replace(/\n$/, '').split('\n');
    return '|2' + keep + '\n' + lines.map(function (l) { return l.length ? pad + '  ' + l : ''; }).join('\n');
  }

  function emit(v, indent) {
    indent = indent || 0;
    var pad = new Array(indent + 1).join(' ');
    if (Array.isArray(v)) {
      if (!v.length) return '[]';
      return v.map(function (item) {
        if (item && typeof item === 'object' && !Array.isArray(item) && Object.keys(item).length) {
          var inner = emit(item, indent + 2);
          return pad + '- ' + inner.slice(indent + 2);
        }
        if (Array.isArray(item) && item.length) return pad + '-\n' + emit(item, indent + 2);
        return pad + '- ' + (isMultiline(item) ? block(item, pad) : (item && typeof item === 'object' ? (Array.isArray(item) ? '[]' : '{}') : scalar(item)));
      }).join('\n');
    }
    if (v && typeof v === 'object') {
      var keys = Object.keys(v).filter(function (k) { return v[k] !== undefined; });
      if (!keys.length) return '{}';
      return keys.map(function (k) {
        var x = v[k];
        if (x && typeof x === 'object' && (Array.isArray(x) ? x.length : Object.keys(x).length)) {
          return pad + key(k) + ':\n' + emit(x, Array.isArray(x) ? indent : indent + 2);
        }
        if (isMultiline(x)) return pad + key(k) + ': ' + block(x, pad);
        return pad + key(k) + ': ' + (x && typeof x === 'object' ? (Array.isArray(x) ? '[]' : '{}') : scalar(x));
      }).join('\n');
    }
    return pad + scalar(v);
  }

  function stringify(v, header) {
    return (header ? header.split('\n').map(function (l) { return '# ' + l; }).join('\n') + '\n' : '') + emit(v, 0) + '\n';
  }

  // ---------- Parser for the emitted subset ----------

  function parse(text) {
    var lines = String(text).replace(/\r\n?/g, '\n').split('\n');
    var i = 0;

    function indentOf(l) { return l.match(/^ */)[0].length; }
    function skip() { while (i < lines.length && (/^\s*$/.test(lines[i]) || /^\s*#/.test(lines[i]))) i++; }

    function parseScalar(s) {
      s = s.trim();
      if (s === '' || s === 'null' || s === '~') return null;
      if (s === 'true') return true;
      if (s === 'false') return false;
      if (s === '[]') return [];
      if (s === '{}') return {};
      if (s[0] === '"') return JSON.parse(s);
      if (s[0] === "'") return s.slice(1, -1).replace(/''/g, "'");
      if (/^-?\d+(\.\d+)?([eE][-+]?\d+)?$/.test(s)) return Number(s);
      return s;
    }

    function readBlock(header, parentIndent) {
      var m = header.match(/^\|(\d)?([-+])?$/);
      var out = [], ind = null;
      while (i < lines.length) {
        var l = lines[i];
        if (l.trim() === '') { out.push(''); i++; continue; }
        var li = indentOf(l);
        if (ind === null) ind = m && m[1] ? parentIndent + +m[1] : li;
        if (li < ind) break;
        out.push(l.slice(ind)); i++;
      }
      while (out.length && out[out.length - 1] === '') out.pop();
      return out.join('\n') + (m && m[2] === '-' ? '' : '\n');
    }

    function splitKey(content) {
      var m = content.match(/^("(?:[^"\\]|\\.)*"|[^:"]+?):(?:\s+(.*)|\s*)$/);
      if (!m) return null;
      return { key: m[1][0] === '"' ? JSON.parse(m[1]) : m[1].trim(), rest: m[2] === undefined ? '' : m[2] };
    }

    function value(rest, ownIndent) {
      // rest: the text after "key:" or "- "
      if (rest === '') {
        skip();
        if (i >= lines.length) return null;
        var ni = indentOf(lines[i]);
        if (ni < ownIndent) return null;
        if (ni === ownIndent && !/^\s*- |^\s*-$/.test(lines[i])) return null;
        return node(ni);
      }
      if (/^\|/.test(rest)) return readBlock(rest.trim(), ownIndent);
      return parseScalar(rest);
    }

    function node(ind) {
      skip();
      if (i >= lines.length) return null;
      var first = lines[i].slice(ind);
      if (/^-( |$)/.test(first)) {
        var arr = [];
        while (i < lines.length) {
          skip();
          if (i >= lines.length) break;
          var l = lines[i];
          if (indentOf(l) !== ind || !/^-( |$)/.test(l.slice(ind))) break;
          var after = l.slice(ind + 1).replace(/^ /, '');
          var kv = splitKey(after);
          if (kv) {
            // "- key: value" opens a mapping indented by two.
            lines[i] = new Array(ind + 3).join(' ') + after;
            arr.push(mapping(ind + 2));
          } else {
            i++;
            arr.push(after === '' ? value('', ind + 1) : value(after, ind));
          }
        }
        return arr;
      }
      return mapping(ind);
    }

    function mapping(ind) {
      var obj = {};
      while (i < lines.length) {
        skip();
        if (i >= lines.length) break;
        var l = lines[i];
        if (indentOf(l) !== ind) break;
        var kv = splitKey(l.slice(ind));
        if (!kv) throw new Error('YAML line ' + (i + 1) + ': expected "key: value"');
        i++;
        obj[kv.key] = value(kv.rest, ind);
      }
      return obj;
    }

    skip();
    return node(0);
  }

  root.PA = root.PA || {};
  root.PA.yaml = { stringify: stringify, parse: parse };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.PA.yaml;
})(typeof window !== 'undefined' ? window : globalThis);
