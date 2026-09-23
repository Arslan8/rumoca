# FINDING-03006: `transformer.core.n12` in `AsymmetricalLoad`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-introduced-by-translation` |
| Original tier | Candidate |
| Sanitizer result | `divisor-introduced-by-translation` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | `transformer.core.n12` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/BasicMachines/Components/PartialCore.mo:13` |
| Original report | [FINDING-asymmetricalload-transformer-core-n12-divgenerated.md](../../bugs/FINDING-asymmetricalload-transformer-core-n12-divgenerated.md) |
| Original SHA-256 | `0f7ee23254c3ac41c6672769a9d922e48caaae80187e70881819d5d238c88504` |

## Why this is not a verified bug

The quotient is a compiler-solved representation of a source equation whose zero value is an algebraic/feature limit. It does not prove a source-level division contract defect.

## Regression action

Keep this as a regression proving the detector suppresses or labels the non-defect correctly.

## Evidence basis

The v2 report's own verdict/proof explicitly declines a defect claim.

## Original claim

Zero is a supported limit of this component; the quotient the dae shows is the compiler's solved form, not a division in the source. It does **not** claim that the source contract is wrong.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
