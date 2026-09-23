"""What MSL components document about zero.

A component's own documentation is evidence, and for the cases in this file it
is the *decisive* evidence: `Modelica.Electrical.Analog.Basic.Inductor` says in
so many words that `L` may be zero, and no amount of looking at the flattened
DAE will tell you that.

Entries are `DECLARED`, never `PROVEN`. They record what the library says, and
a reader who disagrees with the library should be able to see that is what they
are disagreeing with. Where the source equations prove something stronger, the
proof wins: authority is `EQUATION > BOUND > USER_CONFIG > CLASS_CATALOG`.
"""

from __future__ import annotations

from .behavior import Confidence, Source, ZeroBehavior, ZeroContract

#: `Class.member` -> (behaviour, why). Each entry cites the component whose
#: documentation or constitutive equation establishes it.
CATALOG: dict[str, tuple[ZeroBehavior, str]] = {
    # Ideal switching elements. The documentation states the ideal limits
    # outright and warns that *some circuits* built from them are singular,
    # which is a statement about topologies rather than about the component.
    "Modelica.Electrical.Analog.Ideal.IdealSwitch.Ron": (
        ZeroBehavior.ALLOWED,
        "the ideal closed-switch resistance; zero is the documented ideal"),
    "Modelica.Electrical.Analog.Ideal.IdealSwitch.Goff": (
        ZeroBehavior.ALLOWED,
        "the ideal open-switch conductance; zero is the documented ideal"),

    # Storage elements. The constitutive equation multiplies a rate, so zero
    # gives the algebraic limit rather than an undefined quotient.
    "Modelica.Electrical.Analog.Basic.Inductor.L": (
        ZeroBehavior.ALGEBRAIC_LIMIT,
        "L*der(i) = v; at L = 0 the element is an ideal short, v = 0, which "
        "the component documentation states explicitly"),
    "Modelica.Electrical.Analog.Basic.Capacitor.C": (
        ZeroBehavior.ALGEBRAIC_LIMIT,
        "i = C*der(v); at C = 0 the element imposes i = 0, which the component "
        "documentation states explicitly"),

    # Mechanical inertias. Massless bodies are a normal modelling idiom.
    "Modelica.Mechanics.Rotational.Components.Inertia.J": (
        ZeroBehavior.ALGEBRAIC_LIMIT,
        "J*a = flange_a.tau + flange_b.tau; at J = 0 this is an algebraic "
        "torque balance, and the declaration carries min = 0 deliberately"),
    "Modelica.Mechanics.Translational.Components.Mass.m": (
        ZeroBehavior.ALGEBRAIC_LIMIT,
        "m*a = flange_a.f + flange_b.f; at m = 0 this is an algebraic force "
        "balance, and the declaration carries min = 0 deliberately"),

    # Pure multipliers: zero removes the effect and leaves the rest intact.
    "Modelica.Thermal.HeatTransfer.Components.ThermalConductor.G": (
        ZeroBehavior.FEATURE_DISABLED,
        "Q_flow = G*dT; at G = 0 the path is insulating, which is the ordinary "
        "open-thermal-path limit"),
    "Modelica.Mechanics.Rotational.Components.Spring.c": (
        ZeroBehavior.FEATURE_DISABLED,
        "tau = c*(phi_rel - phi_rel0); at c = 0 no elastic torque is "
        "transmitted"),
    "Modelica.Mechanics.Translational.Components.Spring.c": (
        ZeroBehavior.FEATURE_DISABLED,
        "f = c*(s_rel - s_rel0); at c = 0 no elastic force is transmitted"),

    # A parameter whose own binding names zero, in a library that folds
    # parameter bindings before the sanitizers see them. `CoreParameters` is
    #
    #     final parameter SI.Conductance GcRef = if PRef <= 0 then 0 else ...
    #
    # and the model consuming it writes `if PRef <= 0 then Gc = 0` beside it,
    # so zero is the documented *no core losses* configuration. The binding
    # rule in `infer.declared_value_contract` catches this whenever the
    # binding survives to the DAE; the default run folds it to a number, and
    # then only the catalogue can say what the number meant.
    "Modelica.Electrical.Machines.Losses.CoreParameters.GcRef": (
        ZeroBehavior.FEATURE_DISABLED,
        "GcRef = if PRef <= 0 then 0 else PRef/VRef^2/m, and Losses.Core "
        "selects Gc = 0 on the same condition: zero is how the library "
        "disables core losses"),

    # A signed quantity, where a positivity rule is simply the wrong rule.
    "Modelica.Electrical.Analog.Examples.Utilities.SwitchedCapacitor.R": (
        ZeroBehavior.ALLOWED,
        "the component is documented as a \"switched capacitor which can "
        "represent a positive or negative resistance\", and CauerLowPassSC "
        "instantiates four of them at R = -1; a positivity rule contradicts "
        "the component's stated purpose"),
    "Modelica.Electrical.Analog.Basic.Resistor.R": (
        ZeroBehavior.ALLOWED,
        "the component explicitly supports signed resistance, so neither a "
        "positivity rule nor a nonzero rule follows from the quantity alone"),
}

#: Members that inherit a contract from a base class rather than declaring it.
#: `Polyphase` components delegate to the scalar ones and must not be judged by
#: their own vector declarations.
DELEGATES: dict[str, str] = {
    "Modelica.Electrical.Polyphase.Ideal.IdealSwitch.Ron":
        "Modelica.Electrical.Analog.Ideal.IdealSwitch.Ron",
    "Modelica.Electrical.Polyphase.Ideal.IdealSwitch.Goff":
        "Modelica.Electrical.Analog.Ideal.IdealSwitch.Goff",
    "Modelica.Electrical.Polyphase.Basic.Inductor.L":
        "Modelica.Electrical.Analog.Basic.Inductor.L",
    "Modelica.Electrical.Polyphase.Basic.Capacitor.C":
        "Modelica.Electrical.Analog.Basic.Capacitor.C",
    "Modelica.Electrical.Polyphase.Basic.Resistor.R":
        "Modelica.Electrical.Analog.Basic.Resistor.R",
}

#: Families whose members share a contract. Matched on the *member* name when
#: the declaring class ends with one of these, because MSL declares the same
#: idiom in many parallel classes (`IdealClosingSwitch`, `IdealOpeningSwitch`,
#: `ControlledIdealClosingSwitch`, ...) with identical semantics.
FAMILIES: tuple[tuple[str, str, ZeroBehavior, str], ...] = (
    ("Ideal", "Ron", ZeroBehavior.ALLOWED,
     "an ideal switch family member; zero on-resistance is the documented ideal"),
    ("Ideal", "Goff", ZeroBehavior.ALLOWED,
     "an ideal switch family member; zero off-conductance is the documented ideal"),
)


def lookup(declaration: str) -> ZeroContract | None:
    """The catalogued contract for a `Class.member`, if there is one."""
    resolved = DELEGATES.get(declaration, declaration)
    entry = CATALOG.get(resolved)
    if entry is not None:
        behavior, reason = entry
        return ZeroContract(
            behavior=behavior, confidence=Confidence.DECLARED,
            source=Source.CLASS_CATALOG, reason=reason,
            canonical_declaration=resolved,
            match_kind="exact-declaration")

    if "." not in resolved:
        return None
    owner, _, member = resolved.rpartition(".")
    for marker, name, behavior, reason in FAMILIES:
        if name == member and marker in owner:
            return ZeroContract(
                behavior=behavior, confidence=Confidence.DECLARED,
                source=Source.CLASS_CATALOG, reason=reason,
                canonical_declaration=resolved, match_kind="prefix")
    return None
