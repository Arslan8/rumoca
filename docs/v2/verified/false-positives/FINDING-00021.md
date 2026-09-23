# FINDING-00021: `mixingUnit.tau0` in `FilterOrder`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `illegal-divisor-witness` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder |
| Target | `mixingUnit.tau0` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:29` |
| Original report | [FINDING-filterorder-mixingunit-tau0-divzero-7.md](../../bugs/FINDING-filterorder-mixingunit-tau0-divzero-7.md) |
| Original SHA-256 | `08a883e2b5b8d1fecc241a72807801f86d4a37f12a6b01fa7d9be115920c0500` |

## Why this is not a verified bug

OpenModelica rejects the report's exact source modification because the named nested element is protected, final, otherwise non-modifiable, or violates a binding rule. The report therefore does not supply a legal executable witness for its claim.

## Regression action

Keep this report as a regression: the analysis must carry modifiability/visibility through qualified component paths and must not offer an illegal parameter assignment as a witness.

## Evidence basis

Independent OpenModelica source translation of the exact witness refuted its admissibility.

## OpenModelica paired execution

- Outcome: `refuted-illegal-witness`
- Unmodified baseline: `failed`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_5b233e06d327a3c9
  extends Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.FilterOrder(mixingUnit.tau0=0);
end V2OMC_5b233e06d327a3c9;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_5b233e06d327a3c9",
[/data/mrumoca/rumoca/target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:23:3-23:30:writable] Error: Protected element 'tau0' may not be modified, got 'tau0 = 0'.
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
