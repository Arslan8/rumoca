# FINDING-05090: `idealPump.medium.rho` in `WaterPump`

| Field | Value |
|---|---|
| Verdict | candidate |
| Review group | `fluid-medium-rho` |
| Original tier | Candidate |
| Sanitizer result | `physical-bound-permits-zero` |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.WaterPump |
| Target | `idealPump.medium.rho` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Thermal/FluidHeatFlow/Media/Medium.mo:4` |
| Original report | [FINDING-waterpump-idealpump-medium-rho-bound.md](../../bugs/FINDING-waterpump-idealpump-medium-rho-bound.md) |
| Original SHA-256 | `5d81d2dea17b4be6ccb88221d5bd10f4e0c21357a5ed0c5e563f9fa2a155f229` |

## Why this remains a candidate

The Medium record gives rho no strictly-positive bound or assertion. FluidHeatFlow.BaseClasses.TwoPort evaluates V_flow=flowPort_a.m_flow/medium.rho. Therefore zero is admitted by the material record and makes the common consumer undefined. The report instances share this declaration-level defect; nominal models blocked in the current Rumoca runtime are not falsely described as independently simulated.

## Proposed fix if confirmed

Require and validate medium.rho>0 at the medium/TwoPort contract, and guard evaluation so an actionable material-domain error occurs before division. Prefer a reusable medium-property validation function or assertion; do not clamp a nonphysical zero to epsilon.

## Confirmation required

Establish a clean executable baseline, apply the exact witness before translation where appropriate, and reproduce the attributed failure independently. Also rule out inherited constraints, assertions, inactive conditional components, sentinel values, and legal algebraic limits.

## Evidence basis

Matched model/target source-semantic review from the first audit; the v2 report is static-only and has no failing execution witness.

## OpenModelica paired execution

- Outcome: `witness-executes-cleanly`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `clean`

Generated test program:

```modelica
model V2OMC_2c618670f0c83505
  extends Modelica.Thermal.FluidHeatFlow.Examples.WaterPump(idealPump.medium.rho=0);
end V2OMC_2c618670f0c83505;
```

Relevant OMC diagnostic:

```text
messages = "LOG_SUCCESS       | info    | The initialization finished successfully without homotopy method.
LOG_SUCCESS       | info    | The simulation finished successfully.
```

## Original claim

The declaration carries `min=0`, and the physical role bound to this variable requires strictly greater than zero. It does **not** claim that zero is *reachable* — the bound permits it, which is a property of the declaration, not an observation of a failure.

## Earlier independent review

[Prior report](../../../verifiedBugs/confirmed/FINDING-04714.md)

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
