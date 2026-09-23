# FINDING-00956: `R` in `Multivibrator`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `multivibrator-design` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator |
| Target | `R` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/Multivibrator.mo:9` |
| Original report | [FINDING-multivibrator-r-unbounded.md](../../bugs/FINDING-multivibrator-r-unbounded.md) |
| Original SHA-256 | `48fb2adfd09bbce499f20dc610c7e12e4ccee311855fc2315df15fca22b1875d` |

## Why this remains a candidate

C=1/f/(2*R*log(1+2*R1/R2)). f=0 or R=0 zeros a factor, R2=0 divides inside the logarithm, and R1=0 makes log(1)=0. All four witnesses fail independently after successful baselines, including final-evaluated recompilation.

## Proposed fix if confirmed

Validate strictly positive f,R,R1,R2 for this positive-resistance oscillator design before computing C; guard the derived expression and issue a clear domain assertion. If other sign combinations are supported, validate both the logarithm argument and the complete denominator explicitly.

## Confirmation required

Establish a clean executable baseline, apply the exact witness before translation where appropriate, and reproduce the attributed failure independently. Also rule out inherited constraints, assertions, inactive conditional components, sentinel values, and legal algebraic limits.

## Evidence basis

Matched model/target source-semantic review from the first audit; the v2 report is static-only and has no failing execution witness.

## OpenModelica paired execution

- Outcome: `witness-admitted-with-warning`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `clean`

Generated test program:

```modelica
model V2OMC_f2e0a244f5c365b1
  extends Modelica.Electrical.Analog.Examples.OpAmps.Multivibrator(R=-1);
end V2OMC_f2e0a244f5c365b1;
```

Relevant OMC diagnostic:

```text
messages = "LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/Multivibrator.mo:10:3-10:114:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Capacitor.mo:4:3-4:52:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_SUCCESS       | info    | The initialization finished successfully with 3 homotopy steps.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-00868.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
