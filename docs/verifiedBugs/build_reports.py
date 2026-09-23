#!/usr/bin/env python3
"""Render an exhaustive ledger from evidence and narrowly scoped source reviews.

A failed run is NOT a verdict. Rules below name reviewed declarations, their
actual equations and counterexamples. Unmatched reports stay unresolved.
"""
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
import re
from audit import ROOT, OUT, inventory, command

MSL=ROOT/'target/corpus/ModelicaStandardLibrary-4.1.0/Modelica'
AN='Electrical/Analog/'
OP=AN+'Examples/OpAmps/'
FC='Magnetic/FluxTubes/'
SOURCES={}

def review(status,group,title,reason,action,refs=(),tests=''):
    return dict(status=status,group=group,title=title,reason=reason,
                action=action,refs=list(refs),tests=tests)

def fp(group,title,reason,refs=()):
    return review('false-positives',group,title,reason,
                  'Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.',refs)

def bug(group,title,reason,action,refs=(),tests=''):
    return review('confirmed',group,title,reason,action,refs,tests or
                  'Add a nominal regression and the exact boundary witness below. Require a clear domain diagnostic (or a documented finite limiting model), never NaN/Inf or an unrelated solver error. Re-run both engines.')

def norm(path):
    for marker in ['Modelica 4.1.0/', 'ModelicaStandardLibrary-4.1.0/Modelica/']:
        if marker in path:return path.split(marker,1)[1]
    return path

def source_for(row,ev):
    meta=ev.get('variables',{}).get(row['target'],{})
    if meta.get('source'):
        path=Path(meta['source'])
        if not path.is_absolute():path=ROOT/path
        return path,meta.get('line',1),meta
    declaration=row['fields'].get('Declaration','')
    if ':' in declaration:
        rel,line=declaration.rsplit(':',1)
        if '/' in rel and (MSL/rel).exists():return MSL/rel,int(line),meta
    return None,None,meta

def select(row,path,line,meta,ev):
    rel=norm(str(path)) if path else ''
    member=re.sub(r'\[.*','',row['target'].split('.')[-1])
    kind=row['kind']
    physical=kind.startswith('physical-') or row['id'].startswith('DECL-')
    # Explicit arithmetic, reviewed at source and exercised independently.
    if rel==AN+'Ideal/IdealizedOpAmpLimited.mo' and member in ('Vps','Vns') or row['id']=='FINDING-00781':
        return bug('opamp-supply-span','Equal op-amp supplies divide by zero',
          'The source defines i_s = p_s/(vps-vns) with no nonzero-span assertion. In LCOscillator and Comparator, Vns=-15; setting Vps=-15 makes the denominator exactly zero. The correct equality witness is -15, not Vps=0. Both nominal examples pass; the actual equality fails in Rumoca and in ordinary and final-evaluated OpenModelica models.',
          'In IdealizedOpAmpLimited validate vps > vns (including useSupply=true pins), and make the zero-span behavior explicit. Do not divide before validation; use a guarded expression plus a domain assertion. If collapsed supplies are to be supported, specify and implement their power/current behavior rather than substituting an epsilon.',
          [(AN+'Ideal/IdealizedOpAmpLimited.mo',21,21)],
          'Test unequal nominal supplies, both equal-supply values, reversed rails, and dynamic supply pins crossing equality. Preserve normal clipping and power accounting.')
    if rel==FC+'Shapes/FixedShape/GenericFluxTube.mo' and member in ('l','area'):
        length=member=='l'
        return bug('flux-length' if length else 'flux-area',
          'Zero flux-tube length divides by zero' if length else 'Zero flux-tube area makes the model undefined',
          ('G_m = mu_0*mu_r*A/l is evaluated with l=0. The numerator is nonzero for the nominal positive area/permeability. Baseline passes; the l=0 source-modified and final-evaluated models explicitly report division by zero.' if length else
           'A=area; G_m=mu_0*mu_r*A/l; the inherited equations use R_m=1/G_m and B=Phi/A. area=0 makes both reciprocals undefined. Runtime overrides report division by zero; final-evaluated translation is structurally singular. This is not merely dividing a storage equation while selecting a state.'),
          'Validate strictly positive l and area at GenericFluxTube and guard reciprocal evaluation. Add meaningful positive parameter bounds for editor feedback, plus assertions for runtime enforcement. If zero geometry is intended, introduce a separate limiting magnetic element with consistent equations instead of evaluating 1/0.',
          [(FC+'Shapes/FixedShape/GenericFluxTube.mo',1,25),(FC+'BaseClasses/FixedShape.mo',28,38)])
    if rel==FC+'Material/SoftMagnetic/BaseData.mo' and member=='B_myMax' and row.get('model','') in ('ModelicaTest.Magnetic.FluxTubes.Sensors','ModelicaTest.Magnetic.FluxTubes.Sources'):
        return bug('inactive-flux-normalization','Inactive material data still enter an unguarded division',
          'These instances set nonLinearPermeability=false, so B_myMax is documented as unused. Nevertheless FixedShape unconditionally defines B_N=abs(B/material.B_myMax). At B_myMax=0 this auxiliary equation is undefined. Rumoca and post-translation OpenModelica overrides fail; OpenModelica recompilation succeeds after removing the unused B_N equation. Therefore the original claim of a robust two-tool active-material failure is overstated, but the unconditional inactive-branch calculation is a source-verified defect.',
          'Make B_N conditional: if nonLinearPermeability then abs(B/material.B_myMax) else 0. Validate B_myMax>0 only in the nonlinear branch. Do not reject unused material settings in linear mode. Verify that the compiler preserves lazy conditional evaluation.',
          [(FC+'BaseClasses/FixedShape.mo',6,17),(FC+'BaseClasses/FixedShape.mo',28,33)],
          'Linear mode with B_myMax=0 must remain finite, both after recompilation and with supported overrides; nonlinear mode with zero must produce an explicit domain diagnostic; retain the positive nonlinear baseline.')
    if rel==OP+'LCOscillator.mo' and member in ('C','L','R','f'):
        return bug('oscillator-design','LC oscillator design divides by zero',
          'The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.',
          'Validate f>0, L>0, C>0 and R>0 at this example/design layer, with guarded derived-parameter calculations and actionable assertions. Do not prohibit zero in every primitive capacitor/inductor/resistor.',
          [(rel,5,13)])
    if rel==OP+'Multivibrator.mo' and member in ('f','R','R1','R2'):
        return bug('multivibrator-design','Multivibrator capacitance formula has zero divisors',
          'C=1/f/(2*R*log(1+2*R1/R2)). f=0 or R=0 zeros a factor, R2=0 divides inside the logarithm, and R1=0 makes log(1)=0. All four witnesses fail independently after successful baselines, including final-evaluated recompilation.',
          'Validate strictly positive f,R,R1,R2 for this positive-resistance oscillator design before computing C; guard the derived expression and issue a clear domain assertion. If other sign combinations are supported, validate both the logarithm argument and the complete denominator explicitly.',
          [(rel,4,10)],'Regression-test each zero independently and a negative log argument, as well as positive nominal values.')
    if rel==OP+'ControlCircuit.mo' and member in ('T1','T2'):
        return bug('control-design','Control-circuit time constants create zero divisions',
          'kp=T2/(2*T1), Ti=T2 and PIA.C=Ti/kp/PIA.R1. T1=0 directly divides by zero; T2=0 sets both Ti and kp to zero and yields 0/0 in PIA.C. These are explicit design formulas, not just solver-selected state divisions. Both triggers fail after clean baselines.',
          'Validate T1>0 and T2>0 at ControlCircuit; use guarded design formulas so invalid input reports the time-constant constraint before parameter evaluation produces NaN/Inf. Keep the analog/block comparison consistent.',
          [(rel,4,7),(OP+'OpAmpCircuits/PI.mo',5,9)])
    circuits={
      'Der':({'R','f'},'C=k/(2*pi*f*R)'),
      'Integrator':({'R','f','k'},'C=1/k/(2*pi*f*R)'),
      'Derivative':({'R1'},'C=T/R1'),
      'FirstOrder':({'R2'},'C=T/R2'),
      'PI':({'R1','k'},'C=T/k/R1'),
    }
    for name,(members,formula) in circuits.items():
        if rel==OP+f'OpAmpCircuits/{name}.mo' and member in members:
            return bug('opamp-design-'+name.lower(),f'{name} circuit has an unguarded design denominator',
              f'The source binding is {formula}. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.',
              f'Validate the denominator parameters at OpAmpCircuits.{name}, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.',
              [(rel,4,10)])
    if rel in {OP+n+'.mo' for n in ('Comparator','Differentiator','HighPass','Integrator','InvertingAmplifier','LowPass','NonInvertingAmplifier','VoltageFollower')} | {AN+'Examples/InvertingAmp.mo'} and member=='f':
        return bug('trapezoid-frequency','Example waveform timing divides by zero frequency',
          'The source uses f directly in trapezoid timing (rising=0.2/f, width=0.3/f, falling=0.2/f, period=1/f). f=0 is not handled and gives undefined parameter bindings. Rumoca reports non-finite evaluation after a clean baseline. OpenModelica baseline-executable overrides also report zero division; recompilation can instead hit a template/code-generation error, which is not counted as independent runtime confirmation.',
          'At the example frequency declaration, specify and assert f>0 and guard the timing calculations so the assertion can diagnose invalid input. If f=0 should mean DC, provide an explicit DC branch; do not silently clamp frequency to epsilon.',
          [(rel,1,45)])
    if rel in (OP+'HighPass.mo',OP+'LowPass.mo') and member=='fG':
        return bug('cutoff-frequency','Filter cutoff frequency divides by zero',
          'The component is instantiated with T=1/(2*pi*fG). fG=0 gives a literal zero denominator and no finite time constant. Both engines fail after clean baselines; OpenModelica also fails with final-evaluated fG=0.',
          'Require and assert fG>0 at the example design interface; guard the T calculation. If a zero-cutoff limiting filter is wanted, implement its limiting equations separately.',[(rel,5,20)])
    if rel=='Electrical/Machines/Utilities/SynchronousMachineData.mo' and member in ('xd','xdTransient','xq') and kind=='divisor-zero-when-parameters-equal':
        return bug('machine-reactance-equality','Equal machine reactances divide by zero',
          'The record defines xe=xmd^2/(xd-xdTransient), xrd with /(xdTransient-xdSubtransient), and xrq=xmq^2/(xq-xqSubtransient), without relational assertions. The equality in this report zeros the corresponding denominator. A minimal model using the actual library record tests the nominal data and all three equalities independently; the full reported machine cannot be simulated by the current Rumoca bitcode runtime. Verification is of the shared declaration, not a claim that the full machine was independently run.',
          'Validate xd>xdTransient>xdSubtransient and xq>xqSubtransient in the data-conversion layer (or explicitly define any supported degenerate machine representation). Guard parameter calculations and use a checked helper function with assertions, since record bindings may be evaluated before model initial equations.',
          [(rel,23,34),(rel,70,86)],'The nominal record projection must run; each equality must yield a clear relational-domain diagnostic rather than NaN/Inf. Also test reversed ordering and near-equal well-conditioned input.')
    # Exact report-instance counterexamples. Do not generalize their success to all circuits.
    zero_pass={'BUG-002','BUG-004','BUG-005','BUG-008','BUG-012','BUG-016','BUG-026'}
    init_controls={'BUG-001':'Mass1','BUG-003':'Mass2','BUG-007':'Mass3','BUG-009':'ParallelC2','BUG-013':'ChuaC1','BUG-014':'ChuaC2','BUG-015':'Shaft','BUG-017':'Arrows'}
    if row['id'] in zero_pass:
        return fp('translation-sensitive-zero','Runtime override does not prove a missing library bound',
          'The historical runtime-override failure reproduces, but the exact reported model simulates successfully when the same zero is set as a final parameter before translation with final-parameter evaluation enabled. The alleged unavoidable divide-by-zero is introduced by the chosen solved/state representation. This refutes the claimed necessity of globally banning zero; it does not promise every connected topology or tunable override is valid.')
    if row['id'] in init_controls:
        return fp('initialization-conflict','Zero-storage example has incompatible fixed initial conditions',
          'The nominal example runs. Recompiling with the reported zero removes a storage state and exposes inconsistent fixed initial equations, not an unavoidable reciprocal in the primitive component. Control '+init_controls[row['id']]+' keeps the zero and relaxes the relevant fixed initial conditions; it simulates successfully. The exact original trigger does fail, but its attribution to a generally invalid library min=0 is false. Fix the example initialization or constrain this particular example if it must retain those starts.')
    if (physical or row['id'].startswith('DECL-')) and rel==AN+'Basic/Inductor.mo' and member=='L':
        return fp('zero-inductor','Zero inductance is an explicitly supported algebraic limit',
          'The library documentation explicitly says L may be positive or zero, and the constitutive equation is L*der(i)=v rather than an unconditional division by L. At L=0 the element becomes the algebraic ideal-short constraint v=0. A translator or post-translation state representation that divides by L cannot be used to prove the source declaration wrong; connected topologies and fixed starts may still be inconsistent.',[(rel,2,11)])
    if physical and rel==AN+'Basic/Capacitor.mo' and member=='C':
        return fp('zero-capacitor','Zero capacitance is an explicitly supported algebraic limit',
          'The library documentation explicitly says C may be positive or zero, and the constitutive equation is i=C*der(v), with no source division by C. At C=0 the component imposes i=0. Several reported runtime-override failures disappear after source-level recompilation and compatible initialization. A particular topology may still be singular, but the blanket strictly-positive rule contradicts the component contract.',[(rel,2,11)])
    if physical and rel=='Mechanics/Rotational/Components/Inertia.mo' and member=='J':
        return fp('zero-rotational-inertia','Zero inertia is a massless algebraic component, not an intrinsic division',
          'The declared min is zero and the equation is J*a=flange_a.tau+flange_b.tau. At J=0 this becomes an algebraic torque-balance constraint; the source does not divide by J. Independent controls retain J=0 and simulate after incompatible fixed initialization is removed. Some topologies can be over/under-constrained, but that does not establish a universal J>0 defect.',[(rel,2,26)])
    if physical and rel=='Mechanics/Translational/Components/Mass.mo' and member=='m':
        return fp('zero-translational-mass','Zero mass is a massless algebraic component, not an intrinsic division',
          'The declared min is zero and the equation is m*a=flange_a.f+flange_b.f. At m=0 this becomes an algebraic force-balance constraint; the source does not divide by m. Independent controls retain m=0 and simulate after incompatible fixed initialization is removed. Some connected systems can be inconsistent, but the blanket strictly-positive attribution is false.',[(rel,2,16)])
    if (physical or row['id'].startswith('DECL-')) and rel in (AN+'Basic/Resistor.mo',AN+'Basic/Conductor.mo') and member in ('R','G'):
        return fp('signed-electrical-element','Signed/zero resistance or conductance is explicitly supported',
          'The component documentation explicitly permits positive, zero and negative values. Its constitutive equation is v=R_actual*i or i=G_actual*v. A universal strictly-positive physical-domain rule contradicts this contract; a particular singular circuit would require its own topology-specific evidence.',[(rel,13,23)])
    if (physical or row['id'].startswith('DECL-')) and rel in ('Electrical/Polyphase/Basic/Resistor.mo','Electrical/Polyphase/Basic/Conductor.mo') and member in ('R','G'):
        scalar=AN+'Basic/'+('Resistor.mo' if member=='R' else 'Conductor.mo')
        return fp('signed-polyphase-element','Polyphase resistance/conductance delegates to signed scalar elements',
          'This component is an array wrapper that passes each R or G to Basic.Resistor/Conductor. The scalar contract explicitly allows positive, zero and negative values and uses a multiplicative constitutive equation. A universal strictly-positive rule is therefore wrong here; a particular singular network requires topology-specific evidence.',[(rel,2,18),(scalar,13,23)])
    ideal={AN+'Interfaces/IdealSemiconductor.mo',AN+'Interfaces/IdealSwitch.mo',AN+'Ideal/IdealTwoWaySwitch.mo'} | {'Electrical/Polyphase/Ideal/'+n+'.mo' for n in ('IdealDiode','IdealThyristor','IdealClosingSwitch')}
    if physical and rel in ideal and member in ('Ron','Goff'):
        return fp('ideal-zero','Zero on-resistance/off-conductance is an intended ideal limit',
          'The scalar ideal component explicitly permits Ron=0 and Goff=0 and uses switching equations that do not unconditionally divide by either. Polyphase declarations use vector nonnegative bounds and delegate to those scalar components. The documentation warns that some connected circuits are singular: that is not evidence that every component must have strictly positive values. The reported blanket positivity/missing-bound claim is false.',[(AN+'Interfaces/IdealSwitch.mo',14,31),(AN+'Interfaces/IdealSemiconductor.mo',1,48)])
    if kind=='divisor-reachable-zero' and rel==AN+'Basic/Conductor.mo' and member in ('alpha','T_ref'):
        return fp('guarded-temperature-factor','The complete conductor denominator is already asserted positive',
          'The denominator is 1+alpha*(T_heatPort-T_ref), not alpha or T_ref alone. An existing assertion requires that complete expression >= Modelica.Constants.eps. In particular alpha=0 makes the denominator 1, not zero. The report ignores the constant term and existing whole-expression domain check. An invalid-temperature assertion is intended rejection, not a newly verified divide-by-zero bug.',[(rel,5,16)])
    if rel=='Thermal/FluidHeatFlow/Media/Medium.mo' and member in ('rho','cp'):
        quantity='density' if member=='rho' else 'specific heat capacity'
        equation='V_flow=flowPort_a.m_flow/medium.rho' if member=='rho' else 'T_a=flowPort_a.h/medium.cp and T_b=flowPort_b.h/medium.cp'
        return bug('fluid-medium-'+member,f'Zero medium {quantity} enters an unguarded division',
          f'The Medium record gives {member} no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates {equation}. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.',
          f'Require and validate medium.{member}>0 at the medium/TwoPort contract, and guard evaluation so an actionable material-domain error occurs before division. Prefer a reusable medium-property validation function or assertion; do not clamp a nonphysical zero to epsilon.',
          [(rel,2,12),('Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo',29,42)],
          f'Test the default medium, zero and negative {member}, and a small positive value in a minimal TwoPort descendant. Both flow directions must retain finite temperature/volume-flow calculations.')
    if rel=='Blocks/Continuous.mo' and line==354 and member=='T' and kind=='divisor-reachable-zero':
        return bug('first-order-time-constant','FirstOrder divides by an unconstrained zero time constant',
          'Blocks.Continuous.FirstOrder declares T without a positive bound and evaluates der(y)=(k*u-y)/T. T=0 is admitted by the declaration and makes that equation undefined, even though the transfer-function limit at T=0 is the algebraic gain y=k*u. The shared source defect is established independently of nominal models the current runtime cannot execute.',
          'Choose and document the contract. To support the natural zero-time-constant limit, formulate T*der(y)=k*u-y and handle state/initialization selection structurally. Otherwise require T>0 with a meaningful lower bound and an assertion evaluated before division. Do not silently replace zero by epsilon.',
          [(rel,348,377)],'Test T>0 dynamics, T=0 algebraic feedthrough, fixed-output initialization, and parameter changes if tunability is supported. Invalid negative T should follow the documented policy.')
    if rel=='Blocks/Continuous.mo' and line==768 and member=='k' and kind=='divisor-reachable-zero':
        return fp('asserted-limpid-gain','LimPID already asserts that controller gain is nonzero',
          'The anti-windup gain contains 1/(k*Ni), but the equation section explicitly asserts abs(k)>=Modelica.Constants.small with the diagnostic “Controller gain must be non-zero.” Ni also has a positive lower bound. The report overlooked the existing full domain enforcement; rejection at k=0 is intended behavior, not an unguarded missing-constraint bug.',[(rel,766,789),(rel,846,885)])
    if rel=='Blocks/Continuous.mo' and member=='unitTime' and kind=='divisor-reachable-zero' and line in (625,817):
        return fp('constant-unit-time','unitTime is an immutable nonzero unit constant',
          'unitTime is declared constant SI.Time unitTime=1 and exists only to satisfy unit checking in ratios. It is not a tunable parameter and cannot take the proposed zero witness. Treating it as a reachable divisor is a role-classification false positive.',[(rel,line-2,line+4)])
    if rel=='Blocks/Continuous.mo' and member=='Td' and kind=='divisor-reachable-zero' and line in (608,773):
        return fp('guarded-zero-derivative-time','Zero derivative time is explicitly handled',
          'Td has min=0. The derivative gain is Td/unitTime (Td is the numerator), while its filter time is max(Td/Nd, a strictly positive epsilon). Thus Td=0 disables the derivative contribution without producing a zero denominator. The report follows dependency reach rather than the complete guarded expression.',[(rel,line-3,line+5),(rel,831 if line==773 else 627,845 if line==773 else 640)])
    if rel=='Blocks/Continuous.mo' and line==1504 and member=='n' and kind=='divisor-reachable-zero':
        return bug('critical-damping-order','CriticalDamping accepts zero order then divides by it',
          'CriticalDamping declares Integer n=2 without min=1. It computes alpha=sqrt(2^(1/n)-1), allocates x[n], and indexes x[1] and x[n]. n=0 therefore causes division/index/domain failures. Filter order is structurally required to be at least one.',
          'Declare n(min=1)=2 and retain an explicit assertion for tools that do not enforce parameter bounds before structural evaluation. Ensure array dimensions and alpha are never evaluated for invalid n.',[(rel,1498,1524),(rel,1530,1538)],'Test n=1, n=2, larger orders, and n=0/negative with a deterministic order-domain diagnostic before array indexing or division.')
    if rel=='Blocks/Continuous.mo' and line==1506 and member=='normalized' and kind=='divisor-reachable-zero':
        return fp('critical-damping-boolean','normalized=false selects a safe explicit branch',
          'normalized is Boolean, not a numeric divisor. The binding is alpha=if normalized then sqrt(2^(1/n)-1) else 1.0. Setting it false makes alpha exactly one, so the later division by alpha remains safe. The detector confused branch control with denominator data.',[(rel,1498,1524)])
    if rel=='Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo' and member=='m' and kind=='divisor-reachable-zero':
        return fp('fixed-phase-count','The alleged zero divisor is constant m=3',
          'SpacePhasor declares constant Integer m=3. It is not a parameter and cannot be overridden to zero; the transformation matrices therefore divide by the fixed value three. The finding is a variable-role error, not a reachable boundary.',[(rel,2,13)])
    if rel=='Electrical/Machines/SpacePhasors/Components/SpacePhasor.mo' and member=='turnsRatio' and kind=='divisor-reachable-zero':
        return bug('space-phasor-turns-ratio','SpacePhasor permits zero turns ratio then divides by it',
          'turnsRatio is an unconstrained parameter and the equation v/turnsRatio=plug_p.pin.v-plug_n.pin.v divides by it directly. Zero is admitted but undefined. This is a declaration/equation defect even when the enclosing machine example is blocked by unrelated runtime limitations.',
          'Require and assert a nonzero turnsRatio before the transformation equation is evaluated. If negative ratios encode winding orientation, enforce abs(turnsRatio)>=small rather than positivity; if only magnitude is supported, document and enforce turnsRatio>0.',[(rel,2,29)],'Test nominal one, a valid non-unit ratio, the documented sign policy, zero, and near-zero values with a clear ratio-domain diagnostic.')
    if physical and rel=='Electrical/Machines/BasicMachines/Components/Inductor.mo' and member=='L':
        return fp('zero-space-phasor-inductance','Zero space-phasor inductance is an algebraic ideal limit',
          'Both axis equations are v_[j]=L[j]*der(i_[j]); L is a multiplier and is never divided. A zero entry sets the corresponding voltage drop to zero. The report applies a strictly-positive heuristic where the component equations support an ideal zero-leakage limit.',[(rel,2,16)])
    if physical and rel=='Electrical/Polyphase/Basic/Inductor.mo' and member=='L':
        return fp('zero-polyphase-inductance','Polyphase inductance delegates to zero-capable scalar inductors',
          'The polyphase component passes each L element to Basic.Inductor. That scalar component explicitly documents positive or zero inductance and uses L*der(i)=v. A universal positive-only finding contradicts the delegated contract.',[(rel,2,11),(AN+'Basic/Inductor.mo',2,11)])
    if rel=='Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo' and member=='pi' and kind=='divisor-reachable-zero':
        return fp('immutable-pi','The alleged divisor is the mathematical constant pi',
          'This declaration is protected constant Real pi=Modelica.Constants.pi. It is immutable and nonzero, so the proposed zero witness is unreachable. The detector lost constant-role information while following derived parameter expressions.',[(rel,1,6),(rel,112,120)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo' and member=='Rs':
        return fp('ideal-stator-resistance','Zero stator resistance is a supported ideal-loss limit',
          'Rs is passed to Polyphase.Basic.Resistor, which delegates to the scalar resistor contract that explicitly allows positive, zero, or negative resistance. Zero removes copper loss; the source does not divide by Rs. A real machine-data recommendation is not a universal equation-domain requirement.',[(rel,8,13),(rel,68,82),(AN+'Basic/Resistor.mo',14,22)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo' and member in ('Lszero','Lssigma'):
        return fp('ideal-stator-leakage','Zero stator leakage inductance is supported',
          'Lszero and Lssigma are passed to scalar/space-phasor inductors whose equations multiply current derivatives by L. Zero is the ideal no-leakage voltage-drop limit; there is no intrinsic reciprocal. The separate fsNominal-derived default formula can still require a positive nominal frequency.',[(rel,15,25),(rel,76,86),(AN+'Basic/Inductor.mo',2,11)])
    if rel=='Electrical/Machines/Interfaces/PartialBasicInductionMachine.mo' and member=='ZsRef':
        return fp('fixed-reference-impedance','ZsRef is fixed to the nonzero value one',
          'The reported parameter is protected final parameter ZsRef=1, used as a dimensional reference. It cannot be modified to zero in a valid extension, so a zero-domain report against it is unreachable.',[(rel,112,120)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Interfaces/PartialBasicDCMachine.mo' and member in ('Ra','La'):
        element='resistance' if member=='Ra' else 'inductance'
        return fp('ideal-dc-armature-'+member.lower(),f'Zero armature {element} is an ideal algebraic limit',
          ('Ra is passed to Basic.Resistor, whose contract explicitly supports zero and signed resistance; zero removes armature copper loss.' if member=='Ra' else 'La is passed to InductorDC, whose equation is v=L*der(i) outside quasi-static mode; zero removes the inductive voltage drop.')+' The partial machine source has no unconditional reciprocal of this parameter. A particular initialization can still be topology-dependent.',[(rel,13 if member=='Ra' else 22,26 if member=='Ra' else 30),(AN+'Basic/Resistor.mo' if member=='Ra' else 'Electrical/Machines/BasicMachines/Components/InductorDC.mo',2,22)])
    if physical and rel=='Electrical/Machines/BasicMachines/Components/AirGapDC.mo' and member=='Le':
        return fp('zero-dc-airgap-inductance','AirGapDC uses excitation inductance only as a multiplier',
          'The complete magnetic relation is psi_e=Le*ie. Le=0 produces zero excitation flux; this source does not divide by Le. Whether such an idealized machine remains useful is separate from the reported claim that the declaration necessarily causes an arithmetic failure.',[(rel,2,12)])
    if rel=='Electrical/Machines/Interfaces/PartialBasicDCMachine.mo' and member=='psi_eNominal' and kind=='divisor-reachable-zero':
        return bug('dc-machine-flux-scale','Zero nominal excitation flux divides the turns-ratio calculation',
          'PartialBasicDCMachine declares psi_eNominal without a positive/nonzero constraint and computes turnsRatio=ViNominal/(wNominal*psi_eNominal). Zero excitation flux therefore makes the machine scaling undefined. This is a direct source denominator even when a full example is blocked by unrelated runtime support.',
          'Define the intended sign convention, then require abs(psi_eNominal)>=small (or psi_eNominal>0) and validate it before computing turnsRatio. A zero-flux motor requires a separate degenerate formulation, not epsilon substitution.',[(rel,94,103)],'Test the nominal machine, valid polarity if supported, zero and near-zero flux, and zero nominal speed independently so diagnostics identify the correct invalid scale.')
    if rel=='Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo' and member=='wNominal' and kind=='divisor-reachable-zero':
        return bug('dc-data-nominal-speed','Zero nominal speed makes DC-machine scaling undefined',
          'DcPermanentMagnetData leaves wNominal unconstrained and forwards it to the machine/loss records. PartialBasicDCMachine computes turnsRatio=ViNominal/(wNominal*psi_eNominal). The data record therefore admits a value that makes a common consumer divide by zero.',
          'Require and validate a nonzero nominal speed using the documented motor/generator sign convention before turns-ratio and loss-reference calculations. If standstill data are needed, define a different identification input rather than dividing by speed.',[(rel,5,18),('Electrical/Machines/Interfaces/PartialBasicDCMachine.mo',94,103)],'Test positive nominal speed, supported reverse sign, zero, and near-zero speed in a minimal DC permanent-magnet machine/data projection.')
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Utilities/ParameterRecords/DcPermanentMagnetData.mo' and member in ('Jr','Js','Ra','La'):
        contract={'Jr':'massless rotor inertia','Js':'massless stator inertia','Ra':'zero-loss armature resistance','La':'zero armature inductance'}[member]
        return fp('ideal-dc-machine-data','DC machine-data field has a supported ideal limit',
          f'This field represents {contract} and is forwarded to a component that uses it multiplicatively: torque balance for inertia, v=R*i for resistance, or v=L*der(i) for inductance. None intrinsically requires division by the field. A specific drive train can still be inconsistent; the missing strictly-positive record bound alone is not a bug.',[(rel,4,30)])
    if physical and rel=='Electrical/Machines/BasicMachines/DCMachines/DC_PermanentMagnet.mo' and member=='Lme':
        return fp('fixed-permanent-magnet-scale','Lme is an immutable nonzero model constant',
          'DC_PermanentMagnet declares protected constant SI.Inductance Lme=1. It is a fixed equivalence scale, not a user parameter, and cannot reach the claimed zero witness. The finding lost constant/final role information.',[(rel,35,43)])
    if rel=='Mechanics/MultiBody/package.mo' and member in ('defaultWidthFraction','defaultFrameDiameterFraction') and kind=='divisor-reachable-zero':
        return bug('multibody-visual-scale','Zero MultiBody visualization fraction divides geometry by zero',
          'World exposes this parameter without a positive bound, while default body/frame dimensions divide a length by it. Zero is therefore admitted and makes animation geometry undefined. Although visual rather than physical dynamics, it is a real unguarded parameter-domain defect.',
          'Add a meaningful strictly-positive lower bound and explicit assertion for the fraction before dependent animation dimensions are evaluated. Keep animation=false paths lazy so unused visualization settings need not block physical simulation.',[(rel,120,136),(rel,42,72)],'Test animation enabled at defaults, zero and negative fractions with clear diagnostics, small positive values, and animation disabled with unused invalid visualization data according to the chosen lazy-evaluation contract.')
    if physical and rel in ('Mechanics/MultiBody/Parts/Body.mo','Mechanics/MultiBody/Parts/BodyShape.mo') and member in ('m','I_11','I_22','I_33'):
        return fp('zero-multibody-inertia','MultiBody Newton/Euler equations use mass and inertia multiplicatively',
          'The declaration intentionally has min=0. Newton/Euler equations are frame_a.f=m*(...) and frame_a.t=I*z_a+cross(w_a,I*w_a)+..., with no source reciprocal. Zero mass/inertia converts dynamics to algebraic balance constraints. A singular inertia tensor may make a chosen free-body state formulation unsuitable, but that topology/state-selection issue does not prove every zero bound is wrong.',[(rel,14,30),('Mechanics/MultiBody/Parts/Body.mo',239,261)])
    if physical and rel=='Mechanics/MultiBody/Parts/PointMass.mo' and member=='m':
        return fp('zero-multibody-point-mass','PointMass permits a massless algebraic point',
          'PointMass declares m(min=0), and its force equation multiplies acceleration/gravity by m. At zero it becomes a force-balance/kinematic connection rather than dividing by mass. A surrounding free-state formulation may need different state selection, but the component declaration is not intrinsically invalid.',[(rel,2,12),(rel,80,90)])
    if physical and rel=='Mechanics/MultiBody/Forces/LineForceWithMass.mo' and member=='m':
        return fp('optional-line-force-mass','The line-force point mass is explicitly optional',
          'The parameter is declared m(min=0)=0 and described as a point mass on the connection line; animation is conditional on m>0. Zero is the default no-added-mass configuration, so flagging it as an invalid physical bound contradicts the model design.',[(rel,18,31)])
    if physical and rel=='Mechanics/MultiBody/Forces/Spring.mo' and member in ('m','c'):
        return fp('zero-multibody-spring-option','MultiBody spring mass/stiffness has an intentional zero limit',
          ('m(min=0)=0 is the default optional point mass and is forwarded to LineForceWithMass.' if member=='m' else 'c(min=0) is forwarded to the translational Spring equation f=c*(s_rel-s_rel0), so zero transmits no elastic force.')+' The reported blanket positive-only constraint is inconsistent with these explicit component branches/equations.',[(rel,5,18),(rel,60,90)])
    if physical and rel=='Electrical/Analog/Interfaces/IdealSwitchWithArc.mo' and member in ('Ron','Goff'):
        return fp('ideal-arc-switch-zero','Arc-switch resistance/conductance are multiplicative ideal limits',
          'The quenched off-state is i=Goff*v and the closed state is v=Ron*i; neither parameter is divided. Ron=0 is the ideal closed switch and Goff=0 the ideal open switch, consistent with the base ideal-switch family. A particular connected circuit can still become structurally singular.',[(rel,2,30)])
    if rel=='Electrical/Analog/Lines/TLine.mo' and member in ('Z0','F'):
        if member=='Z0':
            reason='TLine explicitly asserts Z0>0 before its port equations divide by Z0. The declaration lacks a min modifier, but the claimed missing domain enforcement is false because an executable assertion supplies it.'
        else:
            reason='TDi is if F>0 then NL/F else TD, so F=0 selects the non-dividing TD branch. A second assertion requires F>0 or TD>0. The detector ignored conditional reachability and the existing relational assertion.'
        return fp('guarded-transmission-line','TLine already guards its parameter domain',reason,[(rel,2,23)])
    if physical and rel in ('Electrical/Machines/BasicMachines/Components/AirGapS.mo','Electrical/Machines/BasicMachines/Components/AirGapR.mo') and member in ('Lm','Lmd','Lmq','L'):
        return fp('zero-machine-airgap-inductance','Air-gap inductance is used as a flux multiplier',
          'The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.',[(rel,2,20)])
    if physical and rel=='Electrical/Polyphase/Basic/MultiStarResistance.mo' and member=='R':
        return fp('ideal-multistar-resistance','MultiStarResistance delegates to zero-capable resistor elements',
          'R is filled into Polyphase.Basic.Resistor, which delegates to scalar Basic.Resistor. That contract permits zero/signed resistance and uses v=R*i. Zero may create an ideal connection with topology consequences, but the parameter itself is not an unguarded divisor.',[(rel,2,16),(AN+'Basic/Resistor.mo',14,22)])
    if physical and rel=='Mechanics/Translational/Components/Vehicle.mo' and member in ('m','J','rho'):
        explanation={'m':'m is passed to Translational.Mass and used in force balance',
                     'J':'J is passed to Rotational.Inertia and used in torque balance',
                     'rho':'rho only multiplies the aerodynamic force coefficient'}[member]
        return fp('vehicle-zero-idealization','Vehicle parameter has a multiplicative zero limit',
          explanation+'. At zero it removes that inertia or aerodynamic term; the Vehicle source does not divide by it. A physical production vehicle has positive values, but this component also supports idealized/lumped configurations, so a blanket strictly-positive sanitizer finding is not a verified bug.',[(rel,2,36)])
    if rel=='Mechanics/Translational/Components/Vehicle.mo' and member=='vRef' and kind=='divisor-reachable-zero':
        return fp('fixed-vehicle-reference-speed','vRef is a protected nonzero constant',
          'Vehicle declares protected constant SI.Velocity vRef=1. It is an immutable unit/reference scale passed into the drag component and cannot reach zero through model parameter modification. The report lost constant/protected role information.',[(rel,27,37)])
    if rel=='Mechanics/Translational/Components/Vehicle.mo' and member=='vReg' and kind=='divisor-reachable-zero':
        return bug('vehicle-regularization-speed','Vehicle exposes zero regularization speed to reciprocal equations',
          'Vehicle declares vReg=1e-3 without propagating the positive bound of RollingResistance.v0, then passes final v0=vReg. Every regularization branch divides by v0. The outer parameter therefore appears to allow zero even though the consumer requires at least Modelica.Constants.eps.',
          'Mirror v0(final min=Modelica.Constants.eps) on Vehicle.vReg and add a clear assertion before constructing/evaluating regularization. Keep the exact positive bound consistent between wrapper and component.',[(rel,17,23),('Mechanics/Translational/Components/RollingResistance.mo',12,46)],'Test each Regularization enum at default, zero, negative and small positive vReg; invalid input must be rejected before exponent/division evaluation.')
    if rel=='Blocks/Sources.mo' and member in ('rising','falling') and kind=='divisor-reachable-zero' and line in (894,898):
        return fp('zero-trapezoid-edge','Zero trapezoid edge duration is handled by branch reachability',
          'rising and falling explicitly have min=0. The division by rising is inside time<T_start+T_rising; when rising=0 that interval is empty. The falling division is similarly confined to an empty interval when falling=0. Zero therefore produces an instantaneous edge rather than a reachable divide-by-zero.',[(rel,891,929)])
    if physical and rel=='Electrical/PowerConverters/DCAC/SinglePhase2Level.mo' and member in ('RonTransistor','GoffTransistor','RonDiode','GoffDiode'):
        return fp('ideal-converter-switch-zero','Converter switch parameters delegate to ideal semiconductor limits',
          'These values are forwarded to IdealGTOThyristor/IdealDiode, whose IdealSemiconductor equations multiply by Ron or Goff rather than divide. Zero is the exact closed/open ideal limit. Some bridge topologies can become structurally singular, but that requires circuit-specific evidence and does not justify a blanket source-parameter positivity claim.',[(rel,2,42),(AN+'Interfaces/IdealSemiconductor.mo',1,48)])
    if physical and rel=='Electrical/PowerConverters/ACDC/ThyristorBridge2mPulse.mo' and member in ('RonThyristor','GoffThyristor'):
        return fp('ideal-thyristor-bridge-zero','Bridge parameters explicitly allow the ideal thyristor limit',
          'RonThyristor and GoffThyristor have final min=0 and are forwarded to polyphase IdealThyristor, ultimately using IdealSemiconductor multiplicative switching equations. Zero is an intended ideal limit; a specific bridge/network may still require nonzero regularization for numerical structure.',[(rel,2,32),(AN+'Interfaces/IdealSemiconductor.mo',1,48)])
    if physical and rel=='Mechanics/Translational/Components/SpringDamper.mo' and member in ('c','d'):
        return fp('zero-spring-damper-term','Zero stiffness/damping disables one parallel force term',
          'The equations are f_c=c*(s_rel-s_rel0), f_d=d*v_rel and f=f_c+f_d. Both parameters are multipliers with min=0; zero cleanly removes the corresponding elastic or dissipative term. It is not an intrinsic division or invalid bound.',[(rel,2,18)])
    if rel=='Thermal/FluidHeatFlow/Sources/IdealPump.mo' and member=='wNominal' and kind=='divisor-reachable-zero':
        return bug('ideal-pump-speed','IdealPump permits zero nominal speed then divides by it',
          'IdealPump declares wNominal without a positive bound and evaluates both w/wNominal and a flow characteristic derived from it. Zero is admitted but undefined even though the low-actual-speed runtime branch is guarded; the nominal scale is evaluated before that branch can make it safe.',
          'Require wNominal>0 (or a documented nonzero signed convention) and assert it before pump-characteristic evaluation. Guard derived ratios so invalid configuration produces one clear parameter error.',[(rel,2,31)],'Test default, zero, negative according to the sign policy, near-zero positive, actual standstill w=0, and both flow directions.')
    if rel=='Thermal/FluidHeatFlow/Components/OneWayValve.mo' and member in ('V_flowNominal','dpNominal') and kind=='divisor-reachable-zero':
        return bug('one-way-valve-scales','OneWayValve divides by unconstrained nominal scales',
          'The valve declares V_flowNominal and dpNominal without positive bounds, then evaluates dpForward/V_flowNominal and V_flowBackward/dpNominal in its piecewise constitutive equations. Either zero scale is directly undefined.',
          'Require and assert strictly positive nominal flow magnitude and nominal backward pressure before forming the slopes. If signed configuration is intended, separate direction from positive magnitudes rather than allowing a zero denominator.',[(rel,2,25)],'Test nominal flow in both directions, each zero independently, negative sign-policy cases, and small positive scales with finite slopes.')
    if row['model']=='SwitchedRLC' and member=='R' and kind=='divisor-reachable-zero':
        return bug('example-rlc-resistance','SwitchedRLC divides directly by unconstrained resistance',
          'The local example declares R without a bound and computes i_R=V/R. R=0 is an immediate divide by zero; unlike the MSL Basic.Resistor formulation, this hand-written example chose explicit reciprocal form.',
          'Either require/assert abs(R)>0 before i_R evaluation, or reformulate the branch implicitly as R*i_R=V if the ideal zero-resistance limit is meant to be supported. Document whether negative active resistance is valid.',[(rel,7,20)],'Test nominal, zero, supported negative resistance, and the switching event at t=0.5 without non-finite current.')
    if row['model']=='SwitchedRLC_MSL' and physical and member in ('L','R','C'):
        return fp('msl-rlc-zero-component','MSL RLC wrapper delegates to zero/signed-capable primitive equations',
          'This local wrapper only passes L, R and C into Basic.Inductor, Basic.Resistor and Basic.Capacitor. Those source components use implicit/multiplicative equations; L and C explicitly document zero support, while R explicitly documents signed and zero support. A connected zero configuration may require retranslating states or different initialization, but the blanket physical-domain claim is not valid.',[(rel,5,22)])
    if row['model']=='Tank' and member in ('resistance','area') and kind=='divisor-reachable-zero':
        equation='flow_out=level/resistance' if member=='resistance' else 'der(level)=-flow_out/area'
        return bug('tank-zero-divisor','Tank permits a direct zero divisor',
          f'The local model declares {member} with no strictly-positive enforcement that excludes zero and evaluates {equation}. The nominal simulation is clean; zero makes the model undefined. For area, min=0 explicitly advertises the invalid boundary.',
          f'Require and assert {member}>0 before evaluating the tank equations. Use a physically meaningful positive lower bound for editor/tool feedback; do not clamp zero because that changes the time constant.',[(rel,1,9)],f'Test nominal draining, {member}=0, negative {member}, and small positive values with an explicit configuration diagnostic.')
    if rel=='Magnetic/FluxTubes/Examples/Utilities/TranslatoryArmatureAndStopper.mo' and physical and member in ('m','c','d'):
        return fp('armature-zero-mechanical-term','Armature example delegates to zero-capable mechanical terms',
          'm is passed to Translational.Mass, while c and d are passed to ElastoGap. Their source equations use mass, stiffness and damping multiplicatively; zero removes inertia/contact stiffness/damping rather than serving as a divisor. A stopper simulation may become underconstrained or physically unhelpful, but the blanket strictly-positive arithmetic claim is not established.',[(rel,5,45)])
    if rel=='Mechanics/Rotational/Components/SpringDamper.mo' and physical and member in ('c','d'):
        return fp('zero-rotational-spring-damper','Zero rotational stiffness/damping disables one torque term',
          'The component torque is the sum of c*phi_rel and d*w_rel terms. c and d have min=0 and are multipliers, so zero cleanly removes elasticity or damping; it is not an unguarded divisor.',[(rel,2,18)])
    if rel=='Mechanics/Translational/Examples/ElastoGap.mo' and physical and member=='d':
        return fp('zero-elastogap-example-damping','Zero example damping is supported by ElastoGap',
          'The example passes d to ElastoGap, whose contact damping force is d*v_rel and is limited by the spring force. d=0 removes dissipation without division. The physical-domain heuristic is too strict for this example parameter.',[(rel,40,50),('Mechanics/Translational/Components/ElastoGap.mo',29,40)])
    if rel in ('Mechanics/Rotational/Examples/CompareBrakingTorque.mo','Mechanics/Translational/Examples/CompareBrakingForce.mo') and member in ('w0','w_nominal','v0','v_nominal') and kind=='divisor-reachable-zero':
        rotational='Rotational' in rel
        prefix='w' if rotational else 'v'
        child='Mechanics/Rotational/Sources' if rotational else 'Mechanics/Translational/Sources'
        return bug('braking-speed-scales','Braking example fails to propagate positive speed-scale bounds',
          f'The outer example declares {member} without a positive bound and forwards it to force/torque sources whose corresponding parameter has min=Modelica.Constants.eps and appears in reciprocal normalization. Thus the example interface admits zero while every consumer requires a positive scale.',
          f'Mirror the child min=Modelica.Constants.eps attribute on {member} and assert it at the example boundary before source-component parameter evaluation.',[(rel,2,28),(child+('/SignTorque.mo' if rotational and member=='w0' else '/InverseSpeedDependentTorque.mo' if rotational else '/SignForce.mo' if member=='v0' else '/InverseSpeedDependentForce.mo'),1,25)],'Test zero and small-positive regularization/nominal scales for every braking law, plus nominal stopping trajectories.')
    if rel==FC+'Material/SoftMagnetic/BaseData.mo' and member=='B_myMax':
        return bug('flux-normalization-scale','Zero magnetic normalization scale divides by zero',
          'BaseData leaves B_myMax unconstrained. FixedShape unconditionally computes B_N=abs(B/material.B_myMax), so B_myMax=0 is undefined. In nonlinear material mode it is also a genuine normalization scale. The inactive-linear-mode instances are separately grouped because the calculation should be eliminated there entirely.',
          'Require B_myMax>0 for nonlinear permeability and conditionally evaluate B_N only in that branch. Add a checked material-record validation before normalization. Linear mode must not read unused nonlinear material data.',[(rel,5,13),(FC+'BaseClasses/FixedShape.mo',28,33)],'Test positive nonlinear material, zero/negative scale with an explicit material diagnostic, and linear mode with unused zero material data remaining finite.')
    if rel==FC+'Material/SoftMagnetic/BaseData.mo' and member in ('c_b','n') and kind=='divisor-reachable-zero':
        return fp('flux-denominator-operand','Zeroing this operand does not zero the complete denominator',
          'The complete denominator is 1+c_b*B_N+B_N^n. The reported parameter is only an operand inside that sum. At c_b=0 the constant and power terms remain; at n=0 the power term is one. The zero-probe rationale therefore does not establish denominator zero. Other negative or relational combinations may deserve a separate range analysis, but they are not this claimed zero witness.',[(rel,5,13),(FC+'BaseClasses/FixedShape.mo',28,34)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Thermal/FluidHeatFlow/BaseClasses/TwoPort.mo' and member=='m':
        return fp('zero-fluid-inventory','Zero stored fluid mass is explicitly supported',
          'TwoPort explicitly documents that m=0 neglects the temperature transient. Its equation uses if m>small then m*medium.cv*der(T) else an algebraic zero-storage energy balance. Zero is handled by a dedicated branch; a blanket strictly-positive mass rule is contrary to the component contract.',[(rel,2,12),(rel,43,63)])
    if rel=='Thermal/FluidHeatFlow/BaseClasses/SimpleFriction.mo' and member=='V_flowNominal' and kind=='divisor-reachable-zero':
        return fp('asserted-friction-flow-order','The friction denominator is protected by an ordering assertion',
          'The only difference denominator is (V_flowNominal-V_flowLaminar)^2. V_flowLaminar has min=Modelica.Constants.small, and the initial algorithm asserts V_flowNominal>V_flowLaminar before computing k. Consequently V_flowNominal cannot be zero or equal to the laminar value in an admissible initialization. The detector ignored the inherited positive bound and relational assertion.',[(rel,2,29)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Interfaces/PartialBasicMachine.mo' and member in ('Jr','Js'):
        return fp('zero-machine-inertia','Machine inertia delegates to the zero-capable algebraic inertia component',
          'Jr and Js are passed directly to Rotational.Components.Inertia. That component uses J*a=sum(tau), so J=0 produces an algebraic torque balance rather than an intrinsic reciprocal. Js is relevant only when the stator rotates. A particular drive train can have incompatible starts or constraints, but the declaration alone does not establish that both machine inertias must be strictly positive.',[(rel,2,40),('Mechanics/Rotational/Components/Inertia.mo',20,26)])
    if rel=='Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo' and member=='fsNominal' and kind=='divisor-reachable-zero':
        return bug('induction-data-frequency','Zero nominal frequency divides induction-machine data',
          'InductionMachineData leaves fsNominal without a positive bound, while Lssigma divides by 2*pi*fsNominal and multiple loss-reference angular velocities are proportional to it. The direct Lssigma binding is undefined at zero. The report instances share this record defect; tool-blocked full machines are not counted as successful runtime reproductions.',
          'Set a meaningful positive lower bound on fsNominal and validate fsNominal>0 before derived data bindings are evaluated. If DC/zero-frequency machine data are needed, provide a separate formulation rather than evaluating the AC per-unit conversion at zero.',[(rel,4,25),(rel,26,42)],
          'Project the actual record in a minimal model at nominal, zero, negative, and small positive fsNominal; invalid values must report the frequency domain before derived inductance evaluation.')
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo' and member in ('Jr','Js'):
        return fp('zero-machine-data-inertia','Machine-data inertia is not intrinsically a positive divisor',
          'These record fields are forwarded as Jr/Js to machine inertias. The consumer component uses J as a multiplier in torque balance, so zero is a massless algebraic limit. A report needs a specific incompatible drive-train topology or initialization; absence of a strictly-positive record bound alone is not a verified defect.',[(rel,4,10),('Electrical/Machines/Interfaces/PartialBasicMachine.mo',5,40)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo' and member=='Rs':
        return fp('signed-machine-data-resistance','Zero/signed machine resistance is an ideal electrical limit',
          'Rs is a stator resistance data field passed to resistor components. The underlying Basic.Resistor contract explicitly permits positive, zero and negative resistance and uses v=R_actual*i. A real machine normally has positive copper resistance, but the ideal zero-loss limit is mathematically supported; a blanket missing-bound finding is not a bug.',[(rel,8,14),(AN+'Basic/Resistor.mo',14,22)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Electrical/Machines/Utilities/ParameterRecords/InductionMachineData.mo' and member in ('Lszero','Lssigma'):
        return fp('zero-machine-data-leakage','Zero leakage inductance is a supported ideal limit',
          'Lszero and Lssigma represent zero-sequence/stray inductance. They are forwarded to inductor equations that multiply derivatives by L; zero removes the leakage voltage drop. The Basic.Inductor contract explicitly permits zero. This does not excuse fsNominal=0 in the default formula, which is documented as a separate confirmed frequency bug.',[(rel,17,25),(AN+'Basic/Inductor.mo',2,11)])
    if physical and rel=='Electrical/Machines/BasicMachines/Components/InductorDC.mo' and member=='L':
        return fp('zero-dc-machine-inductance','Zero DC-machine inductance is an algebraic ideal limit',
          'InductorDC uses v=if quasiStatic then 0 else L*der(i); it never divides by L. At L=0 the dynamic branch also imposes v=0. A missing positive bound is therefore not an intrinsic source defect, although a surrounding machine configuration may have incompatible state selections or constraints.',[(rel,2,10)])
    if rel=='Blocks/Sources.mo' and member=='duration' and line and 244<=line<=250:
        return fp('zero-duration-ramp','A zero-duration ramp is a supported step',
          'The declaration explicitly says duration=0 gives a Step. Division by duration occurs only after time>=startTime and while time<startTime+duration. For duration=0 those conditions cannot both hold, so that branch is unreachable. The independent Ramp control also runs at zero. A Rumoca projection failure for a step is not evidence of a reachable division in this source.',[(rel,244,254)])
    if rel==AN+'Examples/Utilities/SwitchedCapacitor.mo' and member in ('R','oneOhm'):
        return fp('switched-capacitor-guard','Signed resistance is intentional and the divisor is bounded away from zero',
          'The model explicitly represents positive or negative resistance. Its capacitance uses clock/max(eps*oneOhm,abs(R)), where protected constant oneOhm=1. Thus R=0 does not zero the denominator, negative R is handled by abs, and oneOhm is a fixed unit-conversion constant in this model rather than a reported adjustable parameter.',[(rel,1,7),(rel,29,30),(rel,70,74)])
    if physical and rel=='Electrical/Machines/Losses/CoreParameters.mo' and member=='GcRef':
        return fp('disabled-core-loss','Zero core-loss conductance deliberately disables losses',
          'GcRef is final and explicitly equals zero when PRef<=0; the default PRef is zero. Both DC and induction-machine Core consumers handle this branch by setting core-loss currents to zero. The reported default-value invariant violation is intended lossless behavior, not a failure.',[(rel,6,20),('Electrical/Machines/Losses/DCMachines/Core.mo',16,23),('Electrical/Machines/Losses/InductionMachines/Core.mo',23,30)])
    if physical and rel.startswith('Mechanics/MultiBody/Parts/') and member in ('I_21','I_31','I_32','I'):
        if path and ('min=-C.inf' in path.read_text() or member=='I' and 'Inertia tensor' in path.read_text()):
            return fp('signed-inertia-tensor','Tensor entries are not all strictly positive scalars',
              'Off-diagonal inertia tensor entries are signed (the declaration explicitly allows negative infinity as a lower bound); zero off-diagonal entries describe principal axes. The assembled tensor must satisfy matrix-level physical constraints, not elementwise strict positivity. This does not dismiss a separate invalid diagonal/eigenvalue report.',[(rel,max(1,line-2),line+3)])
    if kind=='physical-invariant-violated' and rel=='Mechanics/Translational/Components/Vehicle.mo' and member=='A':
        return fp('disabled-drag','Zero effective drag area switches off aerodynamic drag',
          'Here A enters f_nominal=-Cd*A*rho*vRef^2/2 as a multiplier; the speed normalization uses the separate protected vRef=1. A=0 is a no-aerodynamic-drag configuration, not a zero geometric divisor. The reported invariant is too broad for this effective coefficient.',[(rel,30,37)])
    if physical and rel==OP+'OpAmpCircuits/Buffer.mo' and member=='R2':
        return fp('unity-buffer','Zero feedback resistance is the unity-gain buffer',
          'R2=(k-1)*R1 deliberately gives zero at the default k=1. R2 feeds a Basic.Resistor, whose documented domain includes zero, and there is no reciprocal R2 in this buffer. Rejecting the nominal unity-gain configuration is a false positive.',[(rel,4,14),(AN+'Basic/Resistor.mo',14,22)])
    if kind=='physical-invariant-violated' and (rel=='Electrical/Machines/BasicMachines/Components/InductorDC.mo' and member=='L' or rel in ('Electrical/Machines/BasicMachines/DCMachines/DC_ElectricalExcited.mo','Electrical/Machines/BasicMachines/DCMachines/DC_SeriesExcited.mo') and member=='Lesigma'):
        return fp('zero-stray-inductance','Zero optional leakage inductance is intentional',
          'The derived stray inductance is Lesigma=Le*sigmae; sigmae=0 represents no stray part. It is passed into InductorDC, whose equation is v=if quasiStatic then 0 else L*der(i). At L=0 the element has zero voltage drop; it is not an unconditional source-level 1/L. A default zero optional leakage term is not an invariant violation.',[('Electrical/Machines/BasicMachines/Components/InductorDC.mo',5,9),(rel,max(1,line-2),line+3)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Thermal/HeatTransfer/Components/ThermalConductor.mo' and member=='G':
        return fp('zero-thermal-conductance','Zero thermal conductance is an insulating limit',
          'The complete constitutive equation is Q_flow=G*dT. G is only a multiplier; at zero the component transports no heat. There is no source reciprocal and the component represents a lumped effective conductance, so a blanket strictly-positive claim rejects the ordinary insulation/open-thermal-path limit. A larger network may still need another equation for each isolated temperature.',[(rel,2,10)])
    if (physical or row['id'].startswith('DECL-')) and rel=='Thermal/HeatTransfer/Components/HeatCapacitor.mo' and member=='C' and kind!='divisor-reachable-zero':
        return fp('zero-heat-capacity','Zero heat capacity is a no-storage algebraic limit',
          'The source equation is C*der(T)=port.Q_flow, not division by C. At C=0 it imposes zero stored heat flow and removes the temperature state. Thus the missing/zero-bound claim does not by itself prove a defect; fixed starts or isolated thermal topologies may still become inconsistent. The two divisor-reach reports for this declaration remain unresolved separately because they make a different compiler-IR claim.',[(rel,2,15)])
    if physical and rel in ('Mechanics/Translational/Components/Spring.mo','Mechanics/Rotational/Components/Spring.mo') and member=='c':
        return fp('zero-spring-stiffness','Zero stiffness is a force-free spring limit',
          'The constitutive equation multiplies displacement by c (f=c*(s_rel-s_rel0) or tau=c*(phi_rel-phi_rel0)). At c=0 it transmits no elastic force; there is no reciprocal and the declaration intentionally has min=0. A disconnected or under-constrained surrounding mechanism is topology-specific, not proof that the component bound is defective.',[(rel,2,10)])
    if physical and rel=='Mechanics/Translational/Components/ElastoGap.mo' and member=='c':
        return fp('zero-elastogap-stiffness','Zero ElastoGap stiffness is handled without division',
          'c has min=0 and only forms f_ref=c*s_ref. The normalization divides by the separately positive s_ref, not by c; at c=0 the contact spring force is zero and the limiter keeps damping force within that zero spring force. The reported strict-positivity rule confuses a multiplier with a divisor.',[(rel,2,12),(rel,29,40)])
    if physical and rel=='Magnetic/FundamentalWave/Components/EddyCurrent.mo' and member=='G':
        return fp('disabled-eddy-loss','The zero-loss branch is explicitly implemented',
          'G has min=0 and the equation section has if G>0 then loss equations else V_m.re=0; V_m.im=0. Zero is a supported lossless branch, not a missing strictly-positive bound.',[(rel,6,19)])
    if kind=='divisor-zero-when-parameters-equal' and rel==AN+'Basic/SaturatingInductor.mo':
        return fp('asserted-inductance-order','Saturating-inductor ordering is already asserted',
          'The source asserts Lzer>Lnom*(1+eps) and Linf<Lnom*(1-eps), and documents the same ordering. The reported positive-nominal equality violates these existing relational constraints; the claim that no assertion excludes it is false. This is not a claim that every compiler schedules diagnostic assertions before evaluating invalid initial equations.',[(rel,21,27)])
    baseline=ev.get('baseline',{}).get('outcome')
    if not row['model']:
        reason='This is a declaration-only census entry, with no enclosing executable model or failing witness. The source declaration was located and retained, but missing a local min is not sufficient: inherited types, intended signed/zero values, usage and guards still need a declaration-specific proof.'
        group='declaration-needs-proof'
    elif baseline!='clean':
        reason=f'The current Rumoca nominal run is {baseline or "unavailable"}, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.'
        group='baseline-blocked'
    else:
        reason='The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.'
        group='needs-semantic-proof'
    return review('unresolved',group,'Not yet established as a bug or a false positive',reason,
      'Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.')

def snapshot(path):
    if path in SOURCES:return SOURCES[path]
    data=path.read_bytes();sha=hashlib.sha256(data).hexdigest()
    dest=OUT/'evidence/sources'/f'{sha[:16]}-{path.name}'
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    info=dict(path=str(path.relative_to(ROOT)),sha256=sha,snapshot=str(dest.relative_to(OUT)))
    SOURCES[path]=info
    return info

def cell(value):return str(value or '—').replace('|','&#124;').replace('\n',' ')

def case_excerpt(evidence,name,marker='AUDIT_CASE '):
    tag=marker+name+'\n'
    if tag not in evidence.get('stdout',''):return None
    return evidence['stdout'].split(tag,1)[1].split('AUDIT_',1)[0]

def omc_summary(segment):
    if not segment:return 'not captured'
    if 'The simulation finished successfully.' in segment and re.search(r'resultFile = "[^"]+"',segment):return 'simulation succeeded'
    for key in ('division by zero','initialization problem is inconsistent','structurally singular','Template error','assertion','Failed to build','Error:'):
        if key in segment:
            return next(l.strip() for l in segment.splitlines() if key in l)[:350]
    return 'no confirmed successful simulation; inspect full output'


_CURRENT={}

def current_reports():
    """(model, target, kind) -> the report file that now carries that claim.

    Report filenames are derived from their content, so a rerun renames them.
    The review is frozen against the report it was written for; this is how a
    reader gets from that frozen name to the live page, and `withdrawn.md` is
    where the trail ends when a later run stopped making the claim.
    """
    if _CURRENT:
        return _CURRENT
    for p in sorted((ROOT/'docs'/'v2'/'bugs').glob('*.md')):
        head=p.read_text(errors='replace').split('## ',1)[0]
        f=dict(re.findall(r'^\| \*\*([^*]+)\*\* \| (.*?) \|$', head, re.M))
        model=f.get('Model','').strip('` ')
        target=(f.get('Reached as') or f.get('Parameter') or '').strip('` ')
        kind=(f.get('Reported as') or '').strip('` ')
        trigger=f.get('Trigger','')
        if trigger and '=' in trigger:
            target=trigger.split('=')[0].strip('` ')
        if model:
            _CURRENT.setdefault((model,target,kind), p.name)
            _CURRENT.setdefault((model,target), p.name)
    return _CURRENT


def original_link(row):
    """The report this review was written against.

    Reports are regenerated with every run and renamed with their content, and
    some claims stop being made at all. A review of a withdrawn claim is still
    a review, so the link has to keep resolving either way: to the live page
    when the claim survives, and to `withdrawn.md`, which lists it by model,
    kind and target, when it does not.
    """
    name=row['file']
    if (ROOT/'docs'/'v2'/'bugs'/name).exists():
        return f'[{name}](../../v2/bugs/{name})'
    index=current_reports()
    model, target, kind = row.get('model'), row.get('target'), row.get('kind')
    live=index.get((model,target,kind)) or index.get((model,target))
    if live:
        return (f'[{live}](../../v2/bugs/{live}) — reviewed as `{name}`, which a '
                f'later run renamed')
    return (f'`{name}` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no '
            f'longer makes this claim')

def write_report(row,decision,path,line,meta,ev,independent,controls):
    dest=OUT/decision['status']/(row['id']+'.md')
    dest.parent.mkdir(parents=True,exist_ok=True)
    fields=[('Verdict',decision['status']),('Scope / group',decision['group']),('Model',row['model'] or 'Declaration only'),('Target',row['target']),('Student classification',row['kind']),('Original report',original_link(row)),('Original SHA-256',row['sha256'])]
    text=f'# {row["id"]}: {decision["title"]}\n\n| Field | Value |\n|---|---|\n'+''.join(f'| {k} | {cell(v)} |\n' for k,v in fields)
    text+='\n## '+('Why this is a false positive' if decision['status']=='false-positives' else 'Verification and root cause' if decision['status']=='confirmed' else 'What remains unresolved')+'\n\n'+decision['reason']+'\n'
    text+='\n## Source evidence\n\n'
    refs=[]
    if path:
        refs.append((path,max(1,line-2),line+3))
        text+=f'Compiler/source-resolved declaration: `{norm(str(path))}:{line}`. '
        if meta:text+=f'Role: `{meta.get("role")}`; binding: `{meta.get("binding")}`; effective min: `{meta.get("minimum")}`; effective max: `{meta.get("maximum")}`. '
        text+='\n\n'
    for rel,start,end in decision['refs']:refs.append((MSL/rel,start,end))
    seen=set()
    for p,start,end in refs:
        if (p,start,end) in seen:continue
        seen.add((p,start,end));info=snapshot(p)
        lines=p.read_text().splitlines()
        text+=f'[{norm(str(p))} — source snapshot](../{info["snapshot"]})\n\n```modelica\n'+''.join(f'{i}: {lines[i-1]}\n' for i in range(start,min(end,len(lines))+1))+'```\n\n'
    if not refs:text+='No unambiguous source location recovered; do not infer a declaration from a shared basename.\n'
    text+='\n## Execution evidence\n\n'
    if ev:
        key=hashlib.sha256(row['model'].encode()).hexdigest()[:16]
        text+=f'[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/{key}.json). Baseline: **{ev.get("baseline",{}).get("outcome","unavailable")}**.\n\n'
        trials=[(k,v) for k,v in ev.get('trials',{}).items() if k.rsplit('=',1)[0]==row['target']]
        if trials:
            text+='| Probe | Outcome |\n|---|---|\n'+''.join(f'| `{cell(k)}` | {v["outcome"]} |\n' for k,v in trials)+'\n'
            for k,v in trials:
                if v['outcome']=='reported-failure':
                    try:details=json.loads(v['stdout']);detail='; '.join(x.get('detail','') for x in details)
                    except ValueError:detail=v['stdout']
                    text+='Diagnostic: '+detail[:700].replace('\n',' ')+'\n\n'
        else:text+='No independent runtime override was executed for this target in this audit; this is not a pass.\n\n'
    else:text+='No enclosing simulation exists in the declaration-only report. Any declaration verdict above rests on the displayed source proof and shared group evidence, not an invented successful run.\n\n'
    for ep,e in independent:
        matches=[case for case in e['cases'] if case[1]==row['target'] and not case[0].startswith('Final')]
        if not matches:continue
        text+=f'[Independent OpenModelica wrappers and complete output](../evidence/{ep.name}). Baseline: {omc_summary(case_excerpt(e,"Baseline"))}.\n\n'
        for name,target,value in matches:
            text+=f'- `{target}={value:g}` set before translation: {omc_summary(case_excerpt(e,name))}.\n'
            text+=f'- Same value declared final, with final-parameter evaluation: {omc_summary(case_excerpt(e,"Final"+name))}.\n'
        text+='\n'
    if decision['group'] in ('initialization-conflict','zero-duration-ramp','machine-reactance-equality'):
        text+='[Independent controls and actual library-record projections](../evidence/control-initialization.json) include source wrappers, compiler options, and full results.\n\n'
    text+=f'## {"Proposed fix" if decision["status"]=="confirmed" else "Recommended action"}\n\n{decision["action"]}\n'
    if decision['tests']:text+='\n## Fix validation\n\n'+decision['tests']+'\n'
    text+='\n## Scope and limitations\n\nA source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.\n\n[Group and related reports](../groups/'+decision['group']+'.md) · [Index](../README.md)\n'
    dest.write_text(text)
    return str(dest.relative_to(OUT))

def main():
    # Verdicts can change as source review improves. Remove only reports and
    # group pages generated by this script so stale copies cannot survive.
    for directory in ('confirmed','false-positives','unresolved','groups'):
        generated=OUT/directory
        generated.mkdir(exist_ok=True)
        for old in generated.glob('*.md'):
            old.unlink()
    rows=inventory()
    evidence={};independent=collections.defaultdict(list)
    for p in (OUT/'evidence').glob('*.json'):
        e=json.loads(p.read_text())
        if p.name.startswith('omc-'):independent[e['model']].append((p,e))
        elif 'model' in e:evidence[e['model']]=e
    controls=json.loads((OUT/'evidence/control-initialization.json').read_text())
    records=[];groups=collections.defaultdict(list)
    for row in rows:
        ev=evidence.get(row['model'],{})
        path,line,meta=source_for(row,ev)
        d=select(row,path,line,meta,ev)
        report=write_report(row,d,path,line,meta,ev,independent.get(row['model'],[]),controls)
        record=dict(id=row['id'],verdict=d['status'],group=d['group'],title=d['title'],model=row['model'],target=row['target'],source=norm(str(path)) if path else None,line=line,original=row['file'],report=report,reason=d['reason'],proposed_action=d['action'])
        records.append(record);groups[d['group']].append(record)
    (OUT/'groups').mkdir(exist_ok=True)
    for name,members in groups.items():
        text=f'# {members[0]["title"]}\n\nGroup `{name}` · {len(members)} report instances · {members[0]["verdict"]}\n\n'+members[0]['reason']+'\n\n'+members[0]['proposed_action']+'\n\n'
        text+='Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.\n\n| ID | Model | Target |\n|---|---|---|\n'
        text+=''.join(f'| [{r["id"]}](../{r["report"]}) | {cell(r["model"])} | `{cell(r["target"])}` |\n' for r in members)
        (OUT/'groups'/f'{name}.md').write_text(text)
    counts=collections.Counter(r['verdict'] for r in records)
    baselines=collections.Counter(e.get('baseline',{}).get('outcome','unavailable') for e in evidence.values())
    trials=collections.Counter(t['outcome'] for e in evidence.values() for t in e['trials'].values())
    for status in ('confirmed','false-positives','unresolved'):
        subset=[r for r in records if r['verdict']==status]
        text=f'# {status}: {len(subset)} reports\n\n[Overview](README.md) · [CSV ledger](index.csv)\n\n| ID | Model | Target | Review group |\n|---|---|---|---|\n'
        text+=''.join(f'| [{r["id"]}]({r["report"]}) | {cell(r["model"])} | `{cell(r["target"])}` | [{r["group"]}](groups/{r["group"]}.md) |\n' for r in subset)
        (OUT/f'{status}.md').write_text(text)
    (OUT/'index.json').write_text(json.dumps(records,indent=2)+'\n')
    with (OUT/'index.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    readme=f'''# Report verification — 2026-09-15–16

This audit accounts for **all {len(records):,} issue reports** in `docs/v2/bugs`: 26 BUG claims, 5,142 FINDING candidates and 911 DECL census entries. It does **not** certify all candidates as defects. Originals are preserved. This directory supersedes neither history nor upstream status; in particular, it does not inherit the verdicts in `docs/verified bugs` (with a space).

| Verdict | Reports | Browse |
|---|---:|---|
| Verified defect / unsafe unguarded calculation | {counts['confirmed']} | [Verified reports](confirmed.md) |
| False positive for the stated claim | {counts['false-positives']} | [Reasons and evidence](false-positives.md) |
| Unresolved — not called real or fake | {counts['unresolved']} | [Remaining evidence gaps](unresolved.md) |
| Total | {len(records)} | [Filterable CSV](index.csv) · [JSON](index.json) |

Counts are **report instances**, not unique bugs. The grouped table below prevents counting the same declaration repeatedly. Confirmed includes source-proved domain/guard defects on invalid input, not claims that default simulations fail. False positive means the specific claim is refuted, not that every use of the component is bug-free. **Unresolved work remains**; absent evidence is never called a false positive.

## Verified root-cause groups

| Group | Reports | Proposed-fix location |
|---|---:|---|
'''
    for name,members in sorted(groups.items()):
        if members[0]['verdict']=='confirmed':readme+=f'| [{members[0]["title"]}](groups/{name}.md) | {len(members)} | Per-report source, fix proposal and regression cases |\n'
    readme+='''
## What changed from the earlier “confirmed” list

All 26 BUG entries were checked with nominal execution, runtime overrides, source-level parameter modifications, and final-evaluated recompilation in OpenModelica. Some storage-zero override failures disappear when the model is retranslated. Others disappear after incompatible fixed initial conditions are relaxed; the zero is retained. Those failures do not justify globally banning zero mass, inertia, capacitance or inductance. The controls and full results are retained.

The direct arithmetic issues are separate: waveform/design frequencies, op-amp supply equality, magnetic geometry, design resistances/time constants, and machine reactance equalities. Inactive magnetic material normalization remains unconditionally evaluated in source; OpenModelica may optimize it away, so it is explicitly documented as compiler-dependent rather than falsely called a robust two-tool active-physics failure.

## Coverage and limitations

'''
    readme+=f'- Fresh Rumoca compile/nominal-run attempts: **{len(evidence)} distinct models**; outcomes: `{dict(baselines)}`.\n'
    readme+=f'- After clean baselines: **{sum(trials.values())} distinct runtime probes**; outcomes: `{dict(trials)}`. These are evidence, not automatic verdicts.\n'
    readme+=f'- Independent OpenModelica model batches: **{sum(len(v) for v in independent.values())}**, plus initialization controls and projections using the actual library record. Nominal and every wrapper result are parsed individually; an omc process exit code of zero alone is not success.\n'
    readme+='''- Source-resolved declarations and exact snapshots are retained, including compiler-provided effective bounds. Repeated findings reuse narrow, reviewed source proofs; no blanket “Ideal”, “Spice3”, or missing-min rule was used.
- The current bitcode runtime cannot simulate many nominal models (for example unsupported expression forms). Those blocked claims remain unresolved unless a separate source proof establishes/refutes them. No claim of exhaustive behavioral verification is made.
- The test horizon is 0–0.5 s, not an exhaustive exploration of all events, all parameter combinations or long-run stability. Declaration-only entries do not provide a complete executable model.
- For equality reports the witness is the partner value, not automatically zero. A nonzero-sum denominator is analyzed as a whole; existing assertions and unreachable branches matter.
- No library/compiler fixes were applied. Proposed fixes are specific to the actual design/geometry/domain layer, not blanket stricter bounds on SI types.

## Reproduce and inspect

Run from the repository root, with the existing Rumoca binary, Python bitcode package and GCC-backed OpenModelica available:

```sh
python3 docs/verifiedBugs/audit.py --jobs 4
python3 docs/verifiedBugs/check_translation.py
python3 docs/verifiedBugs/check_additional.py
python3 docs/verifiedBugs/check_controls.py
python3 docs/verifiedBugs/build_reports.py
```

`audit.py` resumes existing per-model evidence; it does not silently refresh cached results after a source/binary change. For a new revision use a fresh evidence location/archive the old run first. Every JSON evidence file retains exact commands, return codes, timeout status and output SHA-256/byte counts; repetitive compile logs are bounded to 32 KiB while simulation diagnostics remain complete. The source wrappers and `.mos` scripts are embedded in OpenModelica evidence; transient executables/bitcode live under `target/bug-review-20260915`.

[Input inventory with hashes](inventory.json) · [Source snapshot manifest](evidence/source-manifest.json) · [Environment](evidence/environment.json) · [Validation](validation.json)
'''
    (OUT/'README.md').write_text(readme)
    (OUT/'evidence/source-manifest.json').write_text(json.dumps(list(SOURCES.values()),indent=2)+'\n')
    environment={label:command(args,timeout=15) for label,args in {
       'commit':['git','rev-parse','HEAD'],'working_tree':['git','status','--porcelain'],
       'rumoca_version':[ROOT/'target/debug/rumoca','--version'],'omc_version':['omc','--version']}.items()}
    environment['rumoca_binary_sha256']=hashlib.sha256((ROOT/'target/debug/rumoca').read_bytes()).hexdigest()
    (OUT/'evidence/environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    assert len(records)==len({r['id'] for r in records})==6079
    assert set(r['id'] for r in records)==set(r['id'] for r in rows)
    # Ensure the README's validation link also works on a fresh first run.
    (OUT/'validation.json').write_text('{}\n')
    report_files=[p for directory in ('confirmed','false-positives','unresolved')
                  for p in (OUT/directory).glob('*.md')]
    broken=[]
    for markdown in OUT.rglob('*.md'):
        # A lightweight local-link audit; source excerpts can contain bracket
        # and parenthesis syntax that merely resembles Markdown links.
        prose=re.sub(r'```.*?```','',markdown.read_text(),flags=re.S)
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)',prose):
            target=raw.split('#',1)[0].replace('%20',' ')
            if target and '://' not in target and not target.startswith('#'):
                if not (markdown.parent/target).resolve().exists():
                    broken.append([str(markdown.relative_to(OUT)),raw])
    validation=dict(report_count=len(records),report_file_count=len(report_files),
      counts=dict(counts),groups={k:len(v) for k,v in groups.items()},
      all_input_ids_accounted_for=True,unique_ids=True,broken_internal_links=broken)
    assert len(report_files)==len(records)
    assert not broken
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':main()
