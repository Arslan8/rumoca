# FINDING-03505: `SMains` in `ThyristorBridge2mPulse_DC_Drive`

| Field | Value |
|---|---|
| Verdict | confirmed |
| Review group | `divisor-reachable-zero` |
| Original tier | Candidate |
| Sanitizer result | `divisor-reachable-zero` |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive |
| Target | `SMains` |
| Declaration/site | `target/msl/ModelicaStandardLibrary-4.1.0/Modelica 4.1.0/Electrical/PowerConverters/Examples/ACDC/RectifierBridge2mPulse/ThyristorBridge2mPulse_DC_Drive.mo:14` |
| Original report | [FINDING-thyristorbridge2mpulse-dc-drive-smains-divzero.md](../../bugs/FINDING-thyristorbridge2mpulse-dc-drive-smains-divzero.md) |
| Original SHA-256 | `09090fd5cd6b105253f2862a0ca8e396cd882c084c324706bf08ae62e87ca1c9` |

## Verification and root cause

The exact reported witness was placed in a generated Modelica subclass before translation. The unmodified model executed cleanly, while OpenModelica rejected the trigger with a numerical failure such as division by zero, a non-finite result, or a singular system.

## Proposed fix

Constrain or assert the complete denominator away from zero before evaluating the division. If zero has a meaningful limit, implement an explicit algebraic branch; do not hide it with an epsilon.

## Fix validation

Retest nominal values, the exact reported witness, nearby valid boundaries, and any relational equality or conditional branch involved. Preserve the intended ideal/algebraic behavior of delegated components.

## Evidence basis

Rumoca supplied the source-resolved arithmetic witness; independent OpenModelica source translation and execution reproduced the attributed failure against a clean paired baseline.

## OpenModelica paired execution

- Outcome: `confirmed-by-omc`
- Unmodified baseline: `clean`
- Source-instantiated trigger: `failed`

Generated test program:

```modelica
model V2OMC_14ad8884096a43c2
  extends Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierBridge2mPulse.ThyristorBridge2mPulse_DC_Drive(SMains=0);
end V2OMC_14ad8884096a43c2;
```

Relevant OMC diagnostic:

```text
messages = "Failed to build model: V2OMC_14ad8884096a43c2",
"Error: Division by zero in 17.365806793490524 / 0.0
[/var/lib/jenkins/ws/LINUX_BUILDS/tmp.build/openmodelica-1.27.0~dev.beta.2/OMCompiler/Compiler/BackEnd/BackendDAETransform.mo:347:7-347:48:writable] Error: Internal error BackendDAETransform.analyseStrongComponentBlock failed
[/var/lib/jenkins/ws/LINUX_BUILDS/tmp.build/openmodelica-1.27.0~dev.beta.2/OMCompiler/Compiler/BackEnd/BackendDAETransform.mo:351:7-351:90:writable] Error: Internal error function analyseStrongComponentBlock failed
[/var/lib/jenkins/ws/LINUX_BUILDS/tmp.build/openmodelica-1.27.0~dev.beta.2/OMCompiler/Compiler/BackEnd/BackendDAETransform.mo:202:5-202:89:writable] Error: Internal error function analyseStrongComponentScalar failed
[/var/lib/jenkins/ws/LINUX_BUILDS/tmp.build/openmodelica-1.27.0~dev.beta.2/OMCompiler/Compiler/BackEnd/BackendDAETransform.mo:113:7-113:113:writable] Error: Internal error function strongComponentsScalar failed (sorting strong components)
[/var/lib/jenkins/ws/LINUX_BUILDS/tmp.build/openmodelica-1.27.0~dev.beta.2/OMCompiler/Compiler/BackEnd/BackendDAEUtil.mo:7979:5-7979:89:writable] Error: Internal error Transformation module sort components failed
```

## Original claim

A permitted assignment, given in full below, drives the **complete denominator** to zero, and nothing on the path excludes it. It does **not** claim that any model sets those values, or that the model fails when it does — a vanishing denominator in a quotient nothing reads is harmless.

## Scope

Confirmed means independently reproduced execution evidence survived the semantic controls. Candidate means useful static/source evidence exists but a false positive is still possible. Advisory means the analyzer explicitly asks about unknown intent and makes no defect claim. False-positive means the stated defect claim is refuted; it does not certify every connected topology. Unresolved entries are deliberately not called real or fake.

[v2 verification index](../README.md)
