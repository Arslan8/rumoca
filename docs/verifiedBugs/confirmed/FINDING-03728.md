# FINDING-03728: Zero magnetic normalization scale divides by zero

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | flux-normalization-scale |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap |
| Target | lowerYoke.material.B_myMax |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-quadraticcoreairgap-loweryoke-material-b-mymax-divzero.md](../../v2/bugs/FINDING-quadraticcoreairgap-loweryoke-material-b-mymax-divzero.md) — reviewed as `FINDING-03728-quadraticcoreairgap-loweryoke-material-b-mymax.md`, which a later run renamed |
| Original SHA-256 | 43610c0de6e90bea04ec596830443f04177927eec9951797d22b5c195da35cca |

## Verification and root cause

BaseData leaves B_myMax unconstrained. FixedShape unconditionally computes B_N=abs(B/material.B_myMax), so B_myMax=0 is undefined. In nonlinear material mode it is also a genuine normalization scale. The inactive-linear-mode instances are separately grouped because the calculation should be eliminated there entirely.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Material/SoftMagnetic/BaseData.mo:9`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Material/SoftMagnetic/BaseData.mo — source snapshot](../evidence/sources/a2ba34fa697b5b4d-BaseData.mo)

```modelica
7:   parameter SI.RelativePermeability mu_i=1
8:     "Initial relative permeability at B=0";
9:   parameter SI.MagneticFluxDensity B_myMax=1
10:     "Flux density at maximum relative permeability";
11:   parameter Real c_a=1 "Coefficient of approximation function";
12:   parameter Real c_b=1 "Coefficient of approximation function";
```

[Magnetic/FluxTubes/Material/SoftMagnetic/BaseData.mo — source snapshot](../evidence/sources/a2ba34fa697b5b4d-BaseData.mo)

```modelica
5:   extends Modelica.Icons.Record;
6:   parameter String label="SoftMagnetic" "Name of material";
7:   parameter SI.RelativePermeability mu_i=1
8:     "Initial relative permeability at B=0";
9:   parameter SI.MagneticFluxDensity B_myMax=1
10:     "Flux density at maximum relative permeability";
11:   parameter Real c_a=1 "Coefficient of approximation function";
12:   parameter Real c_b=1 "Coefficient of approximation function";
13:   parameter Real n=1 "Exponent of approximation function";
```

[Magnetic/FluxTubes/BaseClasses/FixedShape.mo — source snapshot](../evidence/sources/e6a90b5ee04b025e-FixedShape.mo)

```modelica
28:   Real B_N "Absolute value of normalized B";
29: 
30: equation
31:   B_N = abs(B/material.B_myMax);
32:   mu_r = if nonLinearPermeability then
33:     1 + (material.mu_i - 1 + material.c_a*B_N)/(1 + material.c_b*B_N + B_N^material.n) else mu_rConst;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2c1757c0e25514b8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Require B_myMax>0 for nonlinear permeability and conditionally evaluate B_N only in that branch. Add a checked material-record validation before normalization. Linear mode must not read unused nonlinear material data.

## Fix validation

Test positive nonlinear material, zero/negative scale with an explicit material diagnostic, and linear mode with unused zero material data remaining finite.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/flux-normalization-scale.md) · [Index](../README.md)
