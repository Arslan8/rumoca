# FINDING-00924: `L` in `LCOscillator`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `oscillator-design` |
| Original tier | Candidate |
| Sanitizer result | `physical-domain-unenforced` |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator |
| Target | `L` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo:8` |
| Original report | [FINDING-lcoscillator-l-unbounded.md](../../bugs/FINDING-lcoscillator-l-unbounded.md) |
| Original SHA-256 | `343f78904652211e5b2d63870deb7f4710bdeda882122c79d3ee71502e12795d` |

## Why this remains a candidate

The source computes C=1/((2*pi*f)^2*L) and gamma=(1-A)/(2*R*C). Setting the reported design parameter to zero makes an explicit denominator zero. This is separate from the zero-storage behavior of Basic.Capacitor/Inductor. The nominal example passes; the selected design-parameter perturbation fails.

## Proposed fix if confirmed

Validate f>0, L>0, C>0 and R>0 at this example/design layer, with guarded derived-parameter calculations and actionable assertions. Do not prohibit zero in every primitive capacitor/inductor/resistor.

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
model V2OMC_862c6a2959e53cbc
  extends Modelica.Electrical.Analog.Examples.OpAmps.LCOscillator(L=-1);
end V2OMC_862c6a2959e53cbc;
```

Relevant OMC diagnostic:

```text
messages = "LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Examples/OpAmps/LCOscillator.mo:9:3-9:92:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_ASSERT        | warning | [/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Analog/Basic/Capacitor.mo:4:3-4:52:writable]
|                 | |       | The following assertion has been violated at time 0.000000
LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

Nothing bounds this declaration at all, so it permits values the physical role forbids, including negative ones. It does **not** claim that any model actually sets such a value.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-00846.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
