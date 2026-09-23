# FINDING-00858: `derivative.R1` in `HighPass`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `opamp-design-derivative` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.HighPass |
| Target | `derivative.R1` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo:6` |
| Original report | [FINDING-highpass-derivative-r1-unbounded.md](../../bugs/FINDING-highpass-derivative-r1-unbounded.md) |
| Original SHA-256 | `4eecccafb6ce56538a574c94537b6c439bc7bd598dc0549fa187803706e7cc00` |

## Why this remains a candidate

The source binding is C=T/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Proposed fix if confirmed

Validate the denominator parameters at OpAmpCircuits.Derivative, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

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
model V2OMC_8dc344a745450e1b
  extends Modelica.Electrical.Analog.Examples.OpAmps.HighPass(derivative.R1=-1);
end V2OMC_8dc344a745450e1b;
```

Relevant OMC diagnostic:

```text
messages = "LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Derivative.mo:9:3-9:70:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Capacitor.mo:4:3-4:52:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-00820.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
