#!/usr/bin/env python3
"""Independent translation checks for additional arithmetic-failure candidates."""
import concurrent.futures
import json
from audit import OUT, inventory
from check_translation import job

def main():
    reports=inventory()
    jobs={}
    for path in (OUT/'evidence').glob('*.json'):
        if path.name.startswith(('omc-', 'control-')): continue
        evidence=json.loads(path.read_text())
        for trial, result in evidence.get('trials',{}).items():
            if 'numeric evaluation produced a non-finite result' not in result['stdout']: continue
            target,value=trial.rsplit('=',1)
            matches=[r for r in reports if r['model']==evidence['model'] and r['target']==target]
            if any(r['id'].startswith('BUG-') for r in matches):continue
            r=dict(matches[0],trigger=float(value))
            jobs.setdefault(r['model'],[]).append(r)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda pair:job(*pair,prefix='omc-extra-'),jobs.items()))

if __name__=='__main__':main()
