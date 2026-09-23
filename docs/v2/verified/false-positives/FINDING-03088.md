# FINDING-03088: `transformer.core.n12` in `IMC_Transformer`

| Field | Value |
|---|---|
| Verdict | false-positive |
| Review group | `divisor-introduced-by-translation` |
| Original tier | Candidate |
| Sanitizer result | `divisor-introduced-by-translation` |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | `transformer.core.n12` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/Machines/BasicMachines/Components/PartialCore.mo:13` |
| Original report | [FINDING-imc-transformer-transformer-core-n12-divgenerated-2.md](../../bugs/FINDING-imc-transformer-transformer-core-n12-divgenerated-2.md) |
| Original SHA-256 | `318ab9e1e3ae9c96ccae3f6144d6ac3255917707736d3e6863c4ebd19e796eeb` |

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
