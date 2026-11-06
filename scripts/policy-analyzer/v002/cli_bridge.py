"""Local bridge that lets the analyser call Claude Code or Codex, for testing.

    python cli_bridge.py [--port 8790]

It serves an OpenAI-compatible endpoint on 127.0.0.1 only and runs each
request through the command-line tool you are logged in to (`claude -p` or
`codex exec`), so the page can be tried without API keys. In the Models tab
choose "Local CLI bridge (testing only)" and paste the bridge key it prints.

For testing the page only. The CLIs add their own system behaviour and can
change models with an update, so their output is not a frozen model call and
must not be used for the study's coding. Each request runs in an empty
temporary folder with tools, settings, MCP servers and project rules off.

Models: "claude-code" or "claude-code:<model>" (for example
claude-code:sonnet), "codex" or "codex:<model>".
"""
import argparse
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TIMEOUT = 600
LOCAL_ORIGIN = re.compile(r'^(null|https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?)$')
SLOTS = threading.Semaphore(2)  # at most two CLI runs at once
WORKDIR = tempfile.mkdtemp(prefix='pa-cli-bridge-')
KEY = secrets.token_urlsafe(24)


def run_claude(system, user, model):
    exe = shutil.which('claude')
    if not exe:
        raise RuntimeError('claude is not on PATH')
    args = [exe, '-p', '--output-format', 'json', '--system-prompt', system,
            '--tools', '', '--setting-sources', '', '--strict-mcp-config',
            '--disable-slash-commands', '--no-session-persistence']
    if model:
        args += ['--model', model]
    proc = subprocess.run(args, input=user, capture_output=True, text=True, encoding='utf-8',
                          cwd=WORKDIR, timeout=TIMEOUT)
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError('claude: ' + (proc.stderr or proc.stdout)[:400])
    if out.get('is_error'):
        raise RuntimeError('claude: ' + str(out.get('result'))[:400])
    usage = out.get('usage') or {}
    served = ', '.join((out.get('modelUsage') or {}).keys()) or (model or 'claude-code default')
    return out.get('result') or '', usage.get('input_tokens'), usage.get('output_tokens'), None, 'claude-code/' + served


def run_codex(system, user, model):
    exe = shutil.which('codex')
    if not exe:
        raise RuntimeError('codex is not on PATH')
    last = os.path.join(WORKDIR, 'last-%s.txt' % secrets.token_hex(6))
    args = [exe, 'exec', '-', '--skip-git-repo-check', '--ephemeral', '--ignore-rules',
            '-s', 'read-only', '-C', WORKDIR, '-o', last, '--color', 'never']
    if model:
        args += ['-m', model]
    prompt = 'Instructions:\n' + system + '\n\nInput:\n' + user + '\n'
    proc = subprocess.run(args, input=prompt, capture_output=True, text=True, encoding='utf-8',
                          cwd=WORKDIR, timeout=TIMEOUT)
    log = (proc.stdout or '') + (proc.stderr or '')
    if proc.returncode != 0 or not os.path.exists(last):
        raise RuntimeError('codex: ' + log.strip()[-400:])
    with open(last, encoding='utf-8') as f:
        text = f.read()
    os.remove(last)
    m = re.search(r'^model:\s*(\S+)', log, re.M)
    t = re.search(r'tokens used\s*\n?\s*([\d,]+)', log)
    # Codex reports one total that includes its own instructions, not input and output.
    return text, None, None, int(t.group(1).replace(',', '')) if t else None, 'codex/' + (m.group(1) if m else (model or 'default'))


class Handler(BaseHTTPRequestHandler):
    server_version = 'pa-cli-bridge/1'

    def cors(self):
        origin = self.headers.get('Origin')
        if origin and LOCAL_ORIGIN.match(origin):
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')
            self.send_header('Access-Control-Allow-Headers', 'authorization, content-type')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    def reply(self, code, obj):
        data = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        origin = self.headers.get('Origin')
        if origin and not LOCAL_ORIGIN.match(origin):
            self.reply(403, {'error': {'message': 'only pages on this computer may use the bridge'}})
            return False
        if self.headers.get('Authorization', '') != 'Bearer ' + KEY:
            self.reply(401, {'error': {'message': 'wrong or missing bridge key'}})
            return False
        return True

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_GET(self):
        if self.path.rstrip('/') != '/v1/models':
            return self.reply(404, {'error': {'message': 'not found'}})
        if not self.allowed():
            return
        self.reply(200, {'object': 'list', 'data': [{'id': m, 'object': 'model'} for m in ('claude-code', 'codex')]})

    def do_POST(self):
        if self.path.rstrip('/') != '/v1/chat/completions':
            return self.reply(404, {'error': {'message': 'not found'}})
        if not self.allowed():
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            msgs = body.get('messages') or []
            system = '\n\n'.join(m['content'] for m in msgs if m.get('role') == 'system')
            user = '\n\n'.join(m['content'] for m in msgs if m.get('role') != 'system')
            name, _, sub = str(body.get('model', '')).partition(':')
            runner = {'claude-code': run_claude, 'codex': run_codex}.get(name)
            if not runner:
                return self.reply(400, {'error': {'message': 'model must be claude-code[:model] or codex[:model]'}})
            started = time.time()
            with SLOTS:
                text, tin, tout, total, served = runner(system or 'Follow the instructions in the input.', user, sub or None)
            print('%s %s %.1fs' % (time.strftime('%H:%M:%S'), served, time.time() - started), flush=True)
            self.reply(200, {'id': 'bridge-' + secrets.token_hex(6), 'object': 'chat.completion', 'model': served,
                             'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': text}, 'finish_reason': 'stop'}],
                             'usage': {'prompt_tokens': tin, 'completion_tokens': tout, 'total_tokens': total if total is not None else ((tin or 0) + (tout or 0) or None)}})
        except subprocess.TimeoutExpired:
            self.reply(504, {'error': {'message': 'the CLI did not answer within %d s' % TIMEOUT}})
        except Exception as e:  # report every failure to the page
            self.reply(500, {'error': {'message': str(e)}})

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--port', type=int, default=8790)
    port = ap.parse_args().port
    srv = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print('Local CLI bridge on http://127.0.0.1:%d/v1 (testing only)' % port)
    print('Bridge key: ' + KEY)
    print('Models: claude-code[:model], codex[:model]. Ctrl+C stops it.', flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        shutil.rmtree(WORKDIR, ignore_errors=True)


if __name__ == '__main__':
    main()
