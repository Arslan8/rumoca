#!/usr/bin/env python3
"""Bounded issue-derived probes of real MSL APIs; no library modifications.

The external expectations in summarize() are evaluation oracles. They are not
inserted into the models and cannot be credited as ModelSan discoveries.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
import subprocess
import sys

import probes

ROOT = probes.ROOT
HERE = Path(__file__).resolve().parent
CASES = {'GasControl': 4749, 'GasRoundTrip': 4749, 'WaterRoundTrip': 4750,
         'PulseControl': 3624, 'PulsePast': 3624, 'Delay': 4451, 'Quantization': 4459}


def sanitizer_run(artifact, executable):
    from modelsan.analysis.context import AnalysisContext
    from modelsan.backends.rumoca import RumocaBackend
    from modelsan.dae import load
    from modelsan.pipeline import Pipeline
    from modelsan.sanitizers import DEFAULT, DimensionSan, InitStaticSan, NetworkSan, StructureSan
    from modelsan.sanitizers.registry import SanitizerRegistry
    model = load(artifact)
    registry = SanitizerRegistry()
    for cls in (*DEFAULT, DimensionSan, InitStaticSan, NetworkSan, StructureSan):
        registry.register(cls())
    static, errors = [], []
    context = AnalysisContext(model)
    for sanitizer in registry.static_analyzers():
        try:
            static.extend(sanitizer.analyze(model, context))
        except Exception as error:
            errors.append({'sanitizer': sanitizer.name, 'error': repr(error)})
    backend = RumocaBackend(str(executable), t_end=1, timeout=30)
    try:
        outcome = Pipeline(registry, backend).run(model, str(artifact), model.name)
        return {'static': static, 'static_errors': errors, 'note': outcome.note,
                'coverage': outcome.coverage,
                'findings': [f for bug in outcome.database.bugs for f in bug.findings],
                'results': [{'status': r.status, 'failure': r.failure,
                             'metadata': r.backend_metadata, 'trace': r.trace}
                            for r in outcome.results]}
    finally:
        backend.close()


def summarize(name, rows):
    if not rows:
        return {'oracle': 'no trace; no verdict'}
    if 'RoundTrip' in name or name == 'GasControl':
        values = [float(r['recoveredT']) for r in rows]
        return {'oracle': 'temperature(entropy(state(p,300))) == 300 K',
                'recoveredT': values[0], 'max_error_K': max(abs(v-300) for v in values)}
    if name.startswith('Pulse'):
        r = next(r for r in rows if abs(float(r['time'])-0.1) < 1e-8)
        return {'oracle': 'periodic pulse active at t=0.1 for both phase-equivalent starts',
                'time': float(r['time']), 'actual': float(r['actual']), 'expected': 1}
    if name == 'Delay':
        r = next(r for r in rows if abs(float(r['time'])-0.175) < 1e-8)
        return {'oracle': 'previous sampled input; at t=.175 output should be sin(2*pi*.10)',
                'time': float(r['time']), 'actual': float(r['actual']),
                'expected': math.sin(2*math.pi*.1), 'current_sample': math.sin(2*math.pi*.15)}
    values = sorted(set(round(float(r['dut.y']), 10) for r in rows))
    return {'oracle': '2-bit quantizer has at most four distinct levels',
            'distinct_levels': values, 'count': len(values), 'maximum_expected': 4}


def run_case(name, output):
    work = output / name
    work.mkdir()
    executable = ROOT / 'target/debug/rumoca'
    library = ROOT / 'target/msl/ModelicaStandardLibrary-4.1.0'
    source = HERE / 'SemanticProbes.mo'
    model = 'SemanticProbes.' + name
    artifact = work / 'model.rbc'
    result = {'issue': CASES[name], 'model': model, 'kind': 'issue-derived API probe'}
    result['compile'] = probes.command([str(executable), 'compile', str(source), '--model', model,
        '--no-fold-parameter-bindings', '--source-root', str(library),
        '--cache-dir', str(output / 'cache'), '--emit-bitcode', str(artifact)],
        ROOT, work / 'compile', timeout=40)
    if result['compile']['exit'] == 0 and artifact.exists():
        try:
            result['modelsan'] = sanitizer_run(artifact, executable)
        except Exception as error:
            result['modelsan_error'] = repr(error)
    if name in ('GasControl', 'GasRoundTrip', 'WaterRoundTrip'):
        medium = ('Modelica.Media.Water.ConstantPropertyLiquidWater'
                  if name == 'WaterRoundTrip' else 'Modelica.Media.Air.SimpleAir')
        pressure = {'GasControl': 101325, 'GasRoundTrip': 102338.25,
                    'WaterRoundTrip': 100000}[name]
        script = work / 'evaluate.mos'
        script.write_text('\n'.join([
            f'setModelicaPath("{library}:" + getModelicaPath());',
            'loadModel(Modelica,{"4.1.0"});',
            f'getSourceFile({medium});',
            f'{medium}.setState_psX({pressure},{medium}.specificEntropy('
            f'{medium}.setState_pTX({pressure},300)));', 'getErrorString();'])+'\n')
        result['omc'] = probes.command(['omc', '--locale=C', str(script)], work, work/'omc', timeout=60)
        match = re.search(r'\bT = ([0-9.eE+-]+)', result['omc']['stdout'])
        if match:
            value = float(match.group(1))
            result['oracle_result'] = {'oracle': 'state_psX(p,entropy(state_pTX(p,300))).T == 300 K',
                'method': 'OMC scripting API evaluation; not a simulation trace',
                'pressure_Pa': pressure, 'recoveredT': value, 'error_K': value-300}
        return result
    script = work / 'probe.mos'
    script.write_text('\n'.join([
        'setCommandLineOptions("--numProcs=1");',
        f'setModelicaPath("{library}:" + getModelicaPath());',
        'loadModel(Modelica,{"4.1.0"});', f'loadFile("{source}");',
        'print("MSL="+getVersion(Modelica)+"\\n");',
        f'simulate({model},stopTime=1,numberOfIntervals=400,outputFormat="csv",fileNamePrefix="probe");',
        'print(getErrorString());'])+'\n')
    result['omc'] = probes.command(['omc', '--locale=C', str(script)], work, work/'omc', timeout=60)
    trace = work / 'probe_res.csv'
    if trace.exists():
        with trace.open() as handle:
            rows = list(csv.DictReader(handle))
        try:
            result['oracle_result'] = summarize(name, rows)
        except Exception as error:
            result['oracle_error'] = repr(error)
        result['trace_sha256'] = hashlib.sha256(trace.read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    result = {'omc_version': subprocess.check_output(['omc','--version'],text=True).strip(),
              'source_sha256': hashlib.sha256((HERE/'SemanticProbes.mo').read_bytes()).hexdigest(),
              'binary_sha256': hashlib.sha256((ROOT/'target/debug/rumoca').read_bytes()).hexdigest(),
              'cases': []}
    for name in CASES:
        print('Running '+name, flush=True)
        result['cases'].append(run_case(name, output))
        probes.write(output/'results.json', result)
        print(json.dumps({k:v for k,v in result['cases'][-1].items()
                          if k in ('model','oracle_result','modelsan_error','oracle_error')}),flush=True)


if __name__ == '__main__':
    main()
