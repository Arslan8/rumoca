#!/usr/bin/env python3
"""Controls: translate zero-storage examples with compatible initialization."""
import json
import re
from audit import ROOT, OUT, command

CASES={
 'Mass1': 'Modelica.Mechanics.Translational.Examples.Damper(mass1(final m=0,v(fixed=false),s(fixed=false)))',
 'Mass2': 'Modelica.Mechanics.Translational.Examples.Damper(mass2(final m=0,v(fixed=false),s(fixed=false)))',
 'Mass3': 'Modelica.Mechanics.Translational.Examples.Damper(mass3(final m=0,v(fixed=false),s(fixed=false)))',
 'Arrows': 'Modelica.Mechanics.Translational.Examples.WhyArrows(inertia2(final m=0,v(fixed=false),s(fixed=false)))',
 'ChuaC1': 'Modelica.Electrical.Analog.Examples.ChuaCircuit(C1(final C=0,v(fixed=false)),C2(v(fixed=false)),L(i(fixed=false)))',
 'ChuaC2': 'Modelica.Electrical.Analog.Examples.ChuaCircuit(C2(final C=0,v(fixed=false)),C1(v(fixed=false)),L(i(fixed=false)))',
 'Shaft': 'Modelica.Mechanics.Rotational.Examples.ElasticBearing(shaft(final J=0),springDamper(phi_rel(fixed=false),w_rel(fixed=false)))',
 'Ramp': 'Modelica.Clocked.Examples.SimpleControlledDrive.Continuous(ramp(final duration=0))',
 'ParallelC2': 'Modelica.Electrical.Analog.Examples.ParallelResonance(capacitor2(final C=0,v(fixed=false)),inductor2(i(fixed=false)))',
}

def main():
    work=ROOT/'target/bug-review-20260915/controls'
    work.mkdir(parents=True,exist_ok=True)
    source='\n'.join(f'model {name}\n extends {base};\nend {name};' for name,base in CASES.items())
    record=ROOT/'target/corpus/ModelicaStandardLibrary-4.1.0/Modelica/Electrical/Machines/Utilities/SynchronousMachineData.mo'
    defaults=re.findall(r'parameter\s+[\w.]+\s+(\w+)\(start=([^()]+)\)',record.read_text())
    binding=','.join(f'{k}={v}' for k,v in defaults)
    source+=f'\nmodel MachineNominal\n parameter Modelica.Electrical.Machines.Utilities.SynchronousMachineData d({binding});\n Real y;\nequation\n y=d.xe+d.xrd+d.xrq;\nend MachineNominal;\n'
    extra={'MachineNominal':'Nominal library record projection'}
    for name,mod in [('MachineXd','xd=0.1375'),('MachineXdTransient','xdTransient=0.121428571'),('MachineXq','xq=0.148387097')]:
        source+=f'model {name}\n extends MachineNominal(d(final {mod}));\nend {name};\n'
        extra[name]=mod
    (work/'Cases.mo').write_text(source)
    script='\n'.join(['setCommandLineOptions("--numProcs=1 --evaluateFinalParameters=true");',
       'setCompiler("gcc");','setCXXCompiler("g++");',
       f'loadFile("{ROOT}/target/corpus/ModelicaStandardLibrary-4.1.0/Modelica/package.mo");',
       'loadFile("Cases.mo");','getErrorString();']+
       [f'print("AUDIT_CONTROL {name}\\n"); simulate({name},stopTime=0.5,numberOfIntervals=100,outputFormat="csv");getErrorString();' for name in {**CASES,**extra}])
    (work/'verify.mos').write_text(script)
    result=command(['omc',str(work/'verify.mos')],cwd=work,timeout=150)
    result.update(cases={**CASES,**extra},modelica_source=source,mos=script)
    (OUT/'evidence/control-initialization.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],result['returncode'])

if __name__=='__main__':main()
