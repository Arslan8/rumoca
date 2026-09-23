# SITE-0006: `duration` — a settable parameter reaches a denominator with nothing excluding zero

| | |
|---|---|
| **Declaration** | `Sources.mo:247` |
| **Parameter** | `duration` |
| **Reached as** | `I1.signalSource.duration`, `Ramp1.duration`, `V.signalSource.duration`, `V2.signalSource.duration` … |
| **Finding** | `divisor-reachable-zero` |
| **Severity** | high |
| **Sanitizer** | `divisor` |
| **Models reaching it** | 48 |
| **Evidence** | static analysis of the canonical DAE |
| **Status** | **candidate — not execution-confirmed** |

## The claim

a settable parameter reaches a denominator with nothing excluding zero

reaches a denominator and nothing excludes zero

## What this evidence is, and is not

Static reachability only. Whether zero actually breaks this model depends on topology — a vanishing divisor in an unused branch is harmless — so execution is the oracle.

A confirmed occurrence of this class would live in
[`docs/verified bugs/`](../verified%20bugs/INSTANCES.md) with its own `BUG-` id
and a two-tool reproduction. This file has neither; it records a site the
analysis reached so the result is not lost between runs.

## How it was matched
- **parameter**: `ramp.duration`
- **shape**: `direct`
- **path**: `ramp.duration`
- **declared_min**: `0.0`
- **divisor_sites**: `1`

## Models that reach it

| Model |
|---|
| `Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteController` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.ClockedWithDiscreteTextbookController` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.Continuous` |
| `Modelica.Clocked.Examples.SimpleControlledDrive.ExactlyClockedWithDiscreteController` |
| `Modelica.ComplexBlocks.Examples.TestConversionBlock` |
| `Modelica.Electrical.Analog.Examples.DemoPowerSupply` |
| `Modelica.Electrical.Analog.Examples.DifferenceAmplifier` |
| `Modelica.Electrical.Analog.Examples.HeatingMOSInverter` |
| `Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate` |
| `Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate` |
| `Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks` |
| `Modelica.Electrical.Analog.Examples.NandGate` |
| `Modelica.Electrical.Analog.Examples.ParallelResonance` |
| `Modelica.Electrical.Analog.Examples.SeriesResonance` |
| `Modelica.Electrical.Analog.Examples.ShowVariableResistor` |
| `Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive` |
| `Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator` |
| `Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad` |

…and 28 more; the full list is in `docs/runs/data/`.

## Reproducing

```bash
python3 tools/sweep/static_eval.py --list tools/sweep/ALL.list \
  --out results.jsonl --keep-parameter-chains
```
