# FINDING-00332: Zero trapezoid edge duration is handled by branch reachability

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-trapezoid-edge |
| Model | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate |
| Target | V2.signalSource.falling |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-heatingpnp-norgate-v2-signalsource-falling-divunresolved.md](../../v2/bugs/FINDING-heatingpnp-norgate-v2-signalsource-falling-divunresolved.md) — reviewed as `FINDING-00332-heatingpnp-norgate-v2-signalsource-falling.md`, which a later run renamed |
| Original SHA-256 | fc272f37722d2d757eacdce281b8e655f4f20c011e52f9b5495cf81da18a28f7 |

## Why this is a false positive

rising and falling explicitly have min=0. The division by rising is inside time<T_start+T_rising; when rising=0 that interval is empty. The falling division is similarly confined to an empty interval when falling=0. Zero therefore produces an instantaneous edge rather than a reachable divide-by-zero.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Sources.mo:898`. Role: `parameter`; binding: `5`; effective min: `0`; effective max: `None`. 

[Blocks/Sources.mo — source snapshot](../evidence/sources/565331012685bd19-Sources.mo)

```modelica
896:     parameter SI.Time width(final min=0) = 0.5
897:       "Width duration of trapezoid";
898:     parameter SI.Time falling(final min=0) = 0
899:       "Falling duration of trapezoid";
900:     parameter SI.Time period(final min=Modelica.Constants.small, start=1)
901:       "Time for one period";
```

[Blocks/Sources.mo — source snapshot](../evidence/sources/565331012685bd19-Sources.mo)

```modelica
891:   block Trapezoid "Generate trapezoidal signal of type Real"
892:     parameter Real amplitude=1 "Amplitude of trapezoid"
893:     annotation(Dialog(groupImage="modelica://Modelica/Resources/Images/Blocks/Sources/Trapezoid.png"));
894:     parameter SI.Time rising(final min=0) = 0
895:       "Rising duration of trapezoid";
896:     parameter SI.Time width(final min=0) = 0.5
897:       "Width duration of trapezoid";
898:     parameter SI.Time falling(final min=0) = 0
899:       "Falling duration of trapezoid";
900:     parameter SI.Time period(final min=Modelica.Constants.small, start=1)
901:       "Time for one period";
902:     parameter Integer nperiod=-1
903:       "Number of periods (< 0 means infinite number of periods)";
904:     extends Interfaces.SignalSource;
905:   protected
906:     parameter SI.Time T_rising=rising
907:       "End time of rising phase within one period";
908:     parameter SI.Time T_width=T_rising + width
909:       "End time of width phase within one period";
910:     parameter SI.Time T_falling=T_width + falling
911:       "End time of falling phase within one period";
912:     SI.Time T_start "Start time of current period";
913:     Integer count "Period count";
914:   initial algorithm
915:     count := integer((time - startTime)/period);
916:     T_start := startTime + count*period;
917:   equation
918:     //The following formulation causes a state event
919:     //when integer((time - startTime)/period) > pre(count) then
920:     //A formulation causing a time event is more efficient:
921:     when time >= (pre(count) + 1)*period + startTime then
922:       count = pre(count) + 1;
923:       T_start = time;
924:     end when;
925:     y = offset + (if (time < startTime or nperiod == 0 or (nperiod > 0 and
926:       count >= nperiod)) then 0 else if (time < T_start + T_rising) then
927:       amplitude*(time - T_start)/rising else if (time < T_start + T_width)
928:        then amplitude else if (time < T_start + T_falling) then amplitude*(
929:       T_start + T_falling - time)/falling else 0);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f11c770db9a26ad4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-trapezoid-edge.md) · [Index](../README.md)
