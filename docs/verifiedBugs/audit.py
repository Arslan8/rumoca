#!/usr/bin/env python3
"""Capture bounded, independently parsed execution evidence for the reports.

Generated evidence is not an automatic bug verdict. In particular, changing a
parameter after translation need not preserve the validity of solved equations.
Run from the repository root. No student report or implementation is modified.
"""
import argparse
import ast
import concurrent.futures
import hashlib
import html
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/verifiedBugs'
sys.path[:0] = [str(ROOT / 'packages/rumoca-bitcode')]

FROZEN = Path(__file__).resolve().parent / 'inventory.json'


def inventory():
    """The reports this review was written against.

    Frozen, not re-scanned. A review is a statement about a specific report
    with a specific SHA-256, and the report directory is regenerated whenever the
    analysis changes --- filenames included. Re-reading it silently rewrites
    the thing being reviewed, and when the filenames stopped being numeric it
    instead matched nothing at all and emptied the ledger.

    Delete `inventory.json` to re-freeze against the current reports.
    """
    if FROZEN.exists():
        return json.loads(FROZEN.read_text())
    rows = _scan()
    FROZEN.write_text(json.dumps(rows, indent=1) + '\n')
    return rows


def _scan():
    rows = []
    for p in sorted((ROOT / 'docs/v2/bugs').glob('*.md')):
        if not re.match(r'(BUG|FINDING|DECL)-\d+', p.name):
            continue
        text = p.read_text()
        fields = dict(re.findall(r'^\| \*\*([^*]+)\*\* \| (.*?) \|$', text, re.M))
        evidence = dict(re.findall(r'^\| `([^`]+)` \| (.*?) \|$', text, re.M))
        binding = re.search(r"\{'quantity'.*\}", text)
        if binding:
            evidence.update(ast.literal_eval(binding[0]))
        fields = {k: html.unescape(v.strip('`')) for k, v in fields.items()}
        evidence = {k: html.unescape(v) if isinstance(v, str) else v for k, v in evidence.items()}
        target = fields.get('Reached as', fields.get('Parameter', ''))
        value = None
        if fields.get('Trigger'):
            target, value = fields['Trigger'].split('=')
            target, value = target.strip(), float(value)
        rows.append(dict(id=p.name.split('-')[0]+'-'+p.name.split('-')[1],
                         file=p.name, sha256=hashlib.sha256(text.encode()).hexdigest(),
                         model=fields.get('Model'), target=target, trigger=value,
                         kind=fields.get('Reported as', 'declaration-only'),
                         fields=fields, evidence=evidence))
    return rows

def command(args, cwd=ROOT, timeout=60):
    started = time.monotonic()
    env = {**os.environ, 'CC':'gcc', 'CXX':'g++', 'RAYON_NUM_THREADS':'1',
           'CARGO_BUILD_JOBS':'4', 'RUST_TEST_THREADS':'4'}
    p = subprocess.Popen([str(a) for a in args], cwd=cwd, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        stdout, stderr = p.communicate(timeout=timeout)
        status = 'completed'
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        stdout, stderr = p.communicate()
        status = 'timeout'
    return dict(command=[str(a) for a in args], cwd=str(cwd), status=status,
                returncode=p.returncode, seconds=round(time.monotonic()-started, 3),
                stdout=stdout, stderr=stderr)

def compact_result(result, limit=32768):
    """Bound repetitive compiler logs while retaining integrity metadata."""
    for key in ('stdout','stderr'):
        value=result.get(key,'')
        raw=value.encode()
        result[key+'_bytes']=len(raw)
        result[key+'_sha256']=hashlib.sha256(raw).hexdigest()
        if len(raw)>limit:
            half=limit//2
            result[key]=(raw[:half].decode(errors='replace')+
                f'\n... {len(raw)-limit} bytes omitted; verify with {key}_sha256 ...\n'+
                raw[-half:].decode(errors='replace'))
            result[key+'_truncated']=True
    return result

def simulation(artifact, override=None):
    args = [ROOT/'target/debug/rumoca','compile-bitcode',artifact,
            '--simulate','--check','--t-end','0.5']
    if override:
        args += ['--param', f'{override[0]}={override[1]:.17g}']
    r = command(args, timeout=15)
    try:
        findings = json.loads(r['stdout'])
    except ValueError:
        findings = None
    r['outcome'] = ('clean' if r['status']=='completed' and r['returncode']==0
                    and findings==[] else 'reported-failure' if isinstance(findings,list)
                    and findings else r['status'] if r['status']!='completed' else 'tool-error')
    return r

def model_job(job):
    model, rows, source, cache = job
    from rumoca_bitcode import Model
    key = hashlib.sha256(model.encode()).hexdigest()[:16]
    dest = OUT/'evidence'/f'{key}.json'
    if dest.exists():
        return json.loads(dest.read_text())
    artifact = cache/f'{key}.rbc'
    result = dict(model=model, source=source, variables={}, trials={})
    if source is None:
        result['error'] = 'Model absent from tools/sweep/ALL.list'
    else:
        args = [ROOT/'target/debug/rumoca','compile',source,'--model',model,
                '--emit-bitcode',artifact]
        for root in ['target/msl/ModelicaStandardLibrary-4.1.0',
                     'target/corpus/ModelicaStandardLibrary-4.1.0','target/cmm/CMM-a642c381']:
            if (ROOT/root).exists(): args += ['--source-root',root]
        result['compile'] = compact_result(command(args, timeout=60))
        if result['compile']['returncode']==0 and artifact.exists():
            try:
                dae = Model.load(artifact)
                wanted = {r['target'] for r in rows} | {r['evidence'].get('partner') for r in rows}
                for v in dae.variables:
                    if v.name not in wanted: continue
                    span = v.source.span
                    result['variables'][v.name] = dict(
                        name=v.name, role=v.role, declaring_class=v.declaring_class,
                        source=span.source.name if span.source else None, line=span.line,
                        binding=repr(v.binding), minimum=repr(v.minimum), maximum=repr(v.maximum),
                        raw=v._raw)
            except Exception as error:
                result['metadata_error'] = str(error)
            result['baseline'] = simulation(artifact)
            if result['baseline']['outcome']=='clean':
                for r in rows:
                    if r['trigger'] is not None:
                        value = r['trigger']
                    elif r['kind'] in ('physical-bound-permits-zero','divisor-reachable-zero'):
                        value = 0.
                    elif r['kind']=='divisor-zero-when-parameters-equal':
                        binding=result['variables'].get(r['evidence'].get('partner'),{}).get('binding')
                        try: value=float(binding)
                        except (TypeError, ValueError): continue
                    else: continue
                    trial = f'{r["target"]}={value:.17g}'
                    if trial not in result['trials']:
                        result['trials'][trial] = simulation(artifact,(r['target'],value))
    dest.write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--cache',default='target/bug-review-20260915')
    args=parser.parse_args()
    (OUT/'evidence').mkdir(parents=True,exist_ok=True)
    cache=ROOT/args.cache
    cache.mkdir(parents=True,exist_ok=True)
    rows=inventory()
    (OUT/'inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
    paths={parts[1]:parts[0] for l in (ROOT/'tools/sweep/ALL.list').read_text().splitlines()
           if len(parts:=l.strip().split('\t'))>=2}
    models={}
    for r in rows:
        if r['model']:models.setdefault(r['model'],[]).append(r)
    ordered=sorted(models,key=lambda m:(not any(r['id'].startswith('BUG-') for r in models[m]),m))
    print(f'{len(rows)} reports; {len(models)} distinct models',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures={pool.submit(model_job,(m,models[m],paths.get(m),cache)):m for m in ordered}
        for i,f in enumerate(concurrent.futures.as_completed(futures),1):
            try:
                result=f.result()
                print(i,len(models),result['model'],result.get('baseline',{}).get('outcome','compile-unavailable'),
                      len(result['trials']),flush=True)
            except Exception as error:
                print('ERROR',futures[f],repr(error),flush=True)

if __name__=='__main__':main()
