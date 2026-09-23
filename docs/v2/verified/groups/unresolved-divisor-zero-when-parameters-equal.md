# Unresolved reports: `divisor-zero-when-parameters-equal`

**9 report instances**

[Back to Unresolved reports](../unresolved.md) · [Overview](../README.md)

## Common decision rule

The static denominator witness remains arithmetically valid, but independent OpenModelica did not establish the claimed differential failure. The paired execution outcome was `not-reproduced-by-omc`; a clean short run is not enough to prove the path can never execute later.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [FINDING-00785](../unresolved/FINDING-00785.md) | Modelica.Electrical.Analog.Examples.OpAmps.Comparator | `opAmp.Vps` | OMC: `not-reproduced-by-omc` | [FINDING-comparator-opamp-vps-divequal.md](../../bugs/FINDING-comparator-opamp-vps-divequal.md) |
| [FINDING-02400](../unresolved/FINDING-02400.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xdTransient` | OMC: `not-reproduced-by-omc` | [FINDING-smee-dol-smeedata-xdtransient-divequal.md](../../bugs/FINDING-smee-dol-smeedata-xdtransient-divequal.md) |
| [FINDING-02403](../unresolved/FINDING-02403.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xdTransient` | OMC: `not-reproduced-by-omc` | [FINDING-smee-dol-smeedata-xdtransient-divequal-2.md](../../bugs/FINDING-smee-dol-smeedata-xdtransient-divequal-2.md) |
| [FINDING-02406](../unresolved/FINDING-02406.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xq` | OMC: `not-reproduced-by-omc` | [FINDING-smee-dol-smeedata-xq-divequal.md](../../bugs/FINDING-smee-dol-smeedata-xq-divequal.md) |
| [FINDING-02407](../unresolved/FINDING-02407.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL | `smeeData.xq` | OMC: `not-reproduced-by-omc` | [FINDING-smee-dol-smeedata-xq-divequal-2.md](../../bugs/FINDING-smee-dol-smeedata-xq-divequal-2.md) |
| [FINDING-02488](../unresolved/FINDING-02488.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xdTransient` | OMC: `not-reproduced-by-omc` | [FINDING-smee-generator-smeedata-xdtransient-divequal.md](../../bugs/FINDING-smee-generator-smeedata-xdtransient-divequal.md) |
| [FINDING-02491](../unresolved/FINDING-02491.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xdTransient` | OMC: `not-reproduced-by-omc` | [FINDING-smee-generator-smeedata-xdtransient-divequal-2.md](../../bugs/FINDING-smee-generator-smeedata-xdtransient-divequal-2.md) |
| [FINDING-02494](../unresolved/FINDING-02494.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xq` | OMC: `not-reproduced-by-omc` | [FINDING-smee-generator-smeedata-xq-divequal.md](../../bugs/FINDING-smee-generator-smeedata-xq-divequal.md) |
| [FINDING-02495](../unresolved/FINDING-02495.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator | `smeeData.xq` | OMC: `not-reproduced-by-omc` | [FINDING-smee-generator-smeedata-xq-divequal-2.md](../../bugs/FINDING-smee-generator-smeedata-xq-divequal-2.md) |
