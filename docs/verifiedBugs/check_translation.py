#!/usr/bin/env python3
"""Compare translation at the trigger with a post-translation override.

This is essential for L=0, C=0, m=0, J=0: the translator may remove a state.
The scripts, source wrappers and full compiler output are retained as evidence.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
from audit import ROOT, OUT, inventory, command

def modification(target,value, final=False):
    parts=target.split('.')
    mod=f'{"final " if final else ""}{parts[-1]}={value:.17g}'
    for part in reversed(parts[:-1]): mod=f'{part}({mod})'
    return mod

def job(model, rows, prefix='omc-'):
    key=hashlib.sha256(model.encode()).hexdigest()[:16]
    work=ROOT/'target/bug-review-20260915'/(prefix+key)
    work.mkdir(parents=True,exist_ok=True)
    sources=[]
    cases=[('Baseline',None,None)]
    for r in rows: cases.append((r['id'].replace('-',''),r['target'],r['trigger']))
    for r in rows: cases.append(('Final'+r['id'].replace('-',''),r['target'],r['trigger']))
    for name,target,value in cases:
        mod='' if target is None else '('+modification(target,value,name.startswith('Final'))+')'
        sources.append(f'model {name}\n  extends {model}{mod};\nend {name};')
    source='\n'.join(sources)+'\n'
    (work/'Cases.mo').write_text(source)
    root=ROOT/'target/corpus/ModelicaStandardLibrary-4.1.0'
    lines=['setCommandLineOptions("--numProcs=1 --evaluateFinalParameters=true");', 'setCompiler("gcc");', 'setCXXCompiler("g++");',
           f'loadFile("{root}/Modelica/package.mo");',f'loadFile("{root}/ModelicaTest/package.mo");',
           'loadFile("Cases.mo");','getErrorString();']
    for name,target,value in cases:
        lines += [f'print("AUDIT_CASE {name}\\n");',
                  f'simulate({name}, stopTime=0.5, numberOfIntervals=100, outputFormat="csv");',
                  'getErrorString();']
    # Run the baseline executable with the historical trigger as a second check.
    for name,target,value in cases[1:]:
        if name.startswith('Final'):continue
        lines += [f'print("AUDIT_OVERRIDE {name}\\n");',
                  f'system("./Baseline -override {target}={value:.17g} -r={name}_override.csv");']
    script='\n'.join(lines)+'\n'
    (work/'verify.mos').write_text(script)
    result=command(['omc',str(work/'verify.mos')],cwd=work,timeout=150)
    result.update(model=model,cases=cases,modelica_source=source,mos=script)
    (OUT/'evidence'/(prefix+key+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(model,result['status'],result['returncode'],flush=True)

if __name__ == '__main__':
    rows=[r for r in inventory() if r['id'].startswith('BUG-')]
    models={}
    for r in rows:models.setdefault(r['model'],[]).append(r)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda x:job(*x),models.items()):pass
