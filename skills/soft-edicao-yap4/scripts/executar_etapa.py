#!/usr/bin/env python3
"""Executa uma etapa com identidade verificável, lock e prazo; não escolhe dependências."""
import argparse, datetime, fcntl, hashlib, json, os, signal, subprocess, time
from pathlib import Path

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('trabalho', type=Path)
    ap.add_argument('etapa')
    ap.add_argument('--input', action='append', default=[], type=Path)
    ap.add_argument('--output', action='append', default=[], type=Path)
    ap.add_argument('--timeout', type=float, default=3600)
    ap.add_argument('--lock', type=Path, default=Path.home()/'.cache/video-etapas/pesado.lock')
    args, cmd = ap.parse_known_args()
    if cmd and cmd[0] == '--': cmd = cmd[1:]
    if not cmd or not args.input or not args.output or not 0 < args.timeout <= 3600:
        ap.error('informe comando, entradas, saídas e timeout entre 0 e 3600 s')
    if not args.etapa.replace('-', '').replace('_', '').isalnum():
        ap.error('etapa deve ser identificador simples')
    t0 = time.monotonic()
    d = args.trabalho/'conferencia/etapas'; d.mkdir(parents=True, exist_ok=True)
    path = d/(args.etapa+'.json'); log = d/(args.etapa+'.log')
    identidade = dict(comando=cmd, entradas={str(p.resolve()):sha(p) for p in args.input}, esquema=1)
    try:
        old = json.loads(path.read_text())
        if old.get('status') == 'PASSA' and old.get('identidade') == identidade and old.get('saidas') == {str(p.resolve()):sha(p) for p in args.output}:
            print('CACHE COERENTE', path); return 0
    except (OSError, ValueError): pass
    record = dict(status='EM_EXECUCAO', inicio_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), identidade=identidade, log=str(log))
    def save(status, causa=''):
        record.update(status=status, causa=causa, duracao_s=round(time.monotonic()-t0, 3))
        tmp = path.with_suffix('.novo'); tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2)); tmp.replace(path)
    save('AGUARDANDO_FILA')
    args.lock.parent.mkdir(parents=True, exist_ok=True)
    with args.lock.open('a') as lk:
        while True:
            try: fcntl.flock(lk, fcntl.LOCK_EX|fcntl.LOCK_NB); break
            except BlockingIOError:
                if time.monotonic()-t0 >= args.timeout:
                    save('BLOQUEADO', 'prazo de fila esgotado'); return 124
                time.sleep(min(.2, max(.001, args.timeout-(time.monotonic()-t0))))
        save('EM_EXECUCAO')
        with log.open('w') as out:
            p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                rc = p.wait(timeout=max(.001, args.timeout-(time.monotonic()-t0)))
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGTERM)
                try: p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(p.pid, signal.SIGKILL); p.wait(timeout=3)
                save('BLOQUEADO', 'prazo esgotado; somente grupo próprio interrompido; saídas parciais não validadas'); return 124
        if rc:
            save('REPROVA', 'comando retornou '+str(rc)); return rc if rc > 0 else 1
        try: record['saidas']={str(p.resolve()):sha(p) for p in args.output}
        except OSError as e:
            save('REPROVA', str(e)); return 1
        save('PASSA'); print('PASSA', path); return 0
if __name__ == '__main__': raise SystemExit(main())
