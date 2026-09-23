# Signed/zero resistance or conductance is explicitly supported

Group `signed-electrical-element` · 2 report instances · false-positives

The component documentation explicitly permits positive, zero and negative values. Its constitutive equation is v=R_actual*i or i=G_actual*v. A universal strictly-positive physical-domain rule contradicts this contract; a particular singular circuit would require its own topology-specific evidence.

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

Read the per-report evidence: members can share a declaration while having different runtime outcomes. Source-proof reuse is not a claim that every instance was independently simulated.

| ID | Model | Target |
|---|---|---|
| [DECL-0043](../false-positives/DECL-0043.md) | — | `G` |
| [DECL-0604](../false-positives/DECL-0604.md) | — | `R` |
