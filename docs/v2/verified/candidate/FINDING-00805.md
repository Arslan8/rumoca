# FINDING-00805: `firstOrder1A.R2` in `ControlCircuit`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `opamp-design-firstorder` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit |
| Target | `firstOrder1A.R2` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo:7` |
| Original report | [FINDING-controlcircuit-firstorder1a-r2-unbounded.md](../../bugs/FINDING-controlcircuit-firstorder1a-r2-unbounded.md) |
| Original SHA-256 | `765f434af8ec5f082311a217b961d350ffe57afe546458e594a6e1b13f7fa52e` |

## Why this remains a candidate

The source binding is C=T/R2. The reported parameter is an explicit divisor with no zero handling. At the zero witness the nominal design cannot produce finite capacitance. This declaration has a reproduced instance in the evidence; a declaration-only report is linked to that shared proof, not claimed to have its own executable model.

## Proposed fix if confirmed

Validate the denominator parameters at OpAmpCircuits.FirstOrder, before evaluating C. Use positive domain constraints for the intended passive design and a guarded calculation plus clear assertions. If zero gain is supported, implement a dedicated zero-gain branch instead of dividing by it.

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
model V2OMC_dcb14edc8af1ff8e
  extends Modelica.Electrical.Analog.Examples.OpAmps.ControlCircuit(firstOrder1A.R2=-1);
end V2OMC_dcb14edc8af1ff8e;
```

Relevant OMC diagnostic:

```text
messages = "LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/OpAmpCircuits/FirstOrder.mo:9:3-9:70:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Capacitor.mo:4:3-4:52:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
"Warning: There are nonlinear iteration variables with default zero start attribute found in NLSJac28. For more information set -d=initialization. In OMEdit Tools->Options->Simulation->Show additional information from the initialization process, in OMNotebook call setCommandLineOptions(\"-d=initialization\").
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-00790.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
