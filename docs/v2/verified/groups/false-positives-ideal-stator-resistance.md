# False positives and explicit non-defects: `ideal-stator-resistance`

**4 report instances**

[Back to False positives and explicit non-defects](../false-positives.md) · [Overview](../README.md)

## Common decision rule

Rs is passed to Polyphase.Basic.Resistor, which delegates to the scalar resistor contract that explicitly allows positive, zero, or negative resistance. Zero removes copper loss; the source does not divide by Rs. A real machine-data recommendation is not a universal equation-domain requirement.

## Reports

| ID | Model | Target | Independent evidence | Student report |
|---|---|---|---|---|
| [DECL-0708](../false-positives/DECL-0708.md) | — | `Rs` | Source/semantic review | [DECL-partialbasicinductionmachine-rs-11.md](../../bugs/DECL-partialbasicinductionmachine-rs-11.md) |
| [FINDING-02270](../false-positives/FINDING-02270.md) | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start | `aims.Rs` | Source/semantic review | [FINDING-ims-start-aims-rs-unbounded.md](../../bugs/FINDING-ims-start-aims-rs-unbounded.md) |
| [FINDING-02817](../false-positives/FINDING-02817.md) | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_VoltageSource | `smpm.Rs` | Source/semantic review | [FINDING-smpm-voltagesource-smpm-rs-unbounded.md](../../bugs/FINDING-smpm-voltagesource-smpm-rs-unbounded.md) |
| [FINDING-05214](../false-positives/FINDING-05214.md) | ModelicaTest.Electrical.Machines.SMPM_VoltageSourceWithLosses | `smpm.Rs` | Source/semantic review | [FINDING-smpm-voltagesourcewithlosses-smpm-rs-unbounded.md](../../bugs/FINDING-smpm-voltagesourcewithlosses-smpm-rs-unbounded.md) |
