# FINDING-03722: Zeroing this operand does not zero the complete denominator

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | flux-denominator-operand |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap |
| Target | rightLeg.material.c_b |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03722-quadraticcoreairgap-rightleg-material-c-b.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | a093ae804575bd3a0f5e737164ebb91190693a8ccc1c699ed13d2a24e441d7c5 |

## Why this is a false positive

The complete denominator is 1+c_b*B_N+B_N^n. The reported parameter is only an operand inside that sum. At c_b=0 the constant and power terms remain; at n=0 the power term is one. The zero-probe rationale therefore does not establish denominator zero. Other negative or relational combinations may deserve a separate range analysis, but they are not this claimed zero witness.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Material/SoftMagnetic/BaseData.mo:12`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Material/SoftMagnetic/BaseData.mo — source snapshot](../evidence/sources/a2ba34fa697b5b4d-BaseData.mo)

```modelica
10:     "Flux density at maximum relative permeability";
11:   parameter Real c_a=1 "Coefficient of approximation function";
12:   parameter Real c_b=1 "Coefficient of approximation function";
13:   parameter Real n=1 "Exponent of approximation function";
14: 
15:   annotation (defaultComponentPrefixes="parameter",
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
34: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2c1757c0e25514b8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/flux-denominator-operand.md) · [Index](../README.md)
