# FINDING-01020: `R1` in `PI`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `opamp-design-pi` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI |
| Target | `R1` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo:6` |
| Original report | [FINDING-pi-r1-unbounded.md](../../bugs/FINDING-pi-r1-unbounded.md) |
| Original SHA-256 | `bd75934f8043451609344955ddf79256d54d5f9bca4f9db0f256c680982b89a2` |

## Why this remains a candidate

The source binding is C=T/k/R1. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Proposed fix if confirmed

Validate the denominator parameters at OpAmpCircuits.PI, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

## Confirmation required

Establish a clean executable baseline, apply the exact witness before translation where appropriate, and reproduce the attributed failure independently. Also rule out inherited constraints, assertions, inactive conditional components, sentinel values, and legal algebraic limits.

## Evidence basis

Matched model/target source-semantic review from the first audit; the v2 report is static-only and has no failing execution witness.

## OpenModelica paired execution

- Outcome: `unresolved-baseline-fails`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_ababedb2f599bbf1
  extends Modelica.Electrical.Analog.Examples.OpAmps.OpAmpCircuits.PI(R1=-1);
end V2OMC_ababedb2f599bbf1;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_ababedb2f599bbf1",
"[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/PI.mo:8:3-8:38:writable] Error: Parameter T has neither value nor start value, and is fixed during initialization (fixed=true).
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-00910.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
