"""The sources a Semantic Binder consults, one class per priority level.

Every provider answers the same question — *what does this object mean* — and
returns bindings tagged with the authority behind them. The binder does not
know what any of them does; adding a source means adding a class here and
registering it, not editing the binder.

The levels, weakest first, are the brief's:

    5  heuristic       a name pattern. Never sufficient alone.
    4  unit/quantity   declared metadata. What physics it is.
    3  connector       connector role and what it is wired to.
    2  component type  the class that declared it. What it *is*.
    1  user            an explicit mapping. Final authority.
"""

from __future__ import annotations

import re
from typing import Protocol, runtime_checkable

from .binding import BindingSource, SemanticBinding
from .catalog import ClassCatalog
from .role import SemanticRole, compatible


@runtime_checkable
class SemanticProvider(Protocol):
    """A source of semantic bindings."""

    name: str
    source: BindingSource

    def bind(self, model) -> list[SemanticBinding]: ...


# ── priority 4: declared quantity and unit ───────────────────────────────────

#: MLS §4.8 quantity -> physical role. The quantity is an assertion the *type*
#: author made, which is why this is a real signal and not a guess.
QUANTITY_ROLES: dict[str, str] = {
    "Mass": "physical.mass",
    "Length": "physical.length",
    "Area": "physical.area",
    "Volume": "physical.volume",
    "Density": "physical.density",
    "ThermodynamicTemperature": "physical.absolute_temperature",
    "AbsolutePressure": "physical.pressure",
    "Pressure": "physical.pressure",
    "AngularVelocity": "physical.angular_velocity",
    "Velocity": "physical.velocity",
    "Resistance": "physical.resistance",
    "Conductance": "physical.conductance",
    "Capacitance": "physical.capacitance",
    "Inductance": "physical.inductance",
    "SelfInductance": "physical.inductance",
    "MomentOfInertia": "physical.moment_of_inertia",
    "Inertia": "physical.moment_of_inertia",
}

#: Unit -> physical role, used only when no quantity is declared. Weaker on
#: purpose: `Ohm` is shared by a passive resistance and an equivalent one, and
#: `kg.m2` by a moment of inertia and anything else with those dimensions.
UNIT_ROLES: dict[str, str] = {
    "kg": "physical.mass",
    "m": "physical.length",
    "m2": "physical.area",
    "m3": "physical.volume",
    "kg/m3": "physical.density",
    "K": "physical.absolute_temperature",
    "Pa": "physical.pressure",
    "rad/s": "physical.angular_velocity",
    "m/s": "physical.velocity",
    "Ohm": "physical.resistance",
    "S": "physical.conductance",
    "F": "physical.capacitance",
    "H": "physical.inductance",
    "kg.m2": "physical.moment_of_inertia",
}


class QuantityProvider:
    """The existing unit-based inference, preserved and made explicit.

    The brief's requirement is that this keeps working and becomes *one source
    of evidence* rather than the whole model. Quantity and unit are reported as
    separate authorities so a rule can demand the stronger one.
    """

    name = "quantity"
    source = BindingSource.QUANTITY

    def bind(self, model) -> list[SemanticBinding]:
        found = []
        for variable in model.variables:
            quantity = getattr(variable, "physical_quantity", None)
            unit = getattr(variable, "unit", None)
            role = QUANTITY_ROLES.get(quantity or "")
            if role:
                found.append(SemanticBinding(
                    role=SemanticRole(role), target_id=variable.id,
                    target_name=variable.name, source=BindingSource.QUANTITY,
                    evidence={"quantity": quantity, **({"unit": unit} if unit else {})},
                    target_kind="parameter" if variable.is_parameter else "variable"))
                continue
            role = UNIT_ROLES.get(unit or "")
            if role:
                found.append(SemanticBinding(
                    role=SemanticRole(role), target_id=variable.id,
                    target_name=variable.name, source=BindingSource.UNIT,
                    evidence={"unit": unit},
                    target_kind="parameter" if variable.is_parameter else "variable"))
        return found


# ── priority 2: the class that declared it ───────────────────────────────────


class ComponentTypeProvider:
    """Roles implied by the fully qualified declaring class.

    This is the level that answers what unit and quantity cannot. Chua's diode
    declares `SI.Conductance Ga = -0.75`: the quantity is genuinely Conductance
    and the unit genuinely S, and a rule keyed on either reports a violation on
    a stock MSL example whose negative conductance is the point of the device.
    Only `Modelica.Electrical.Analog.Examples.Utilities.NonlinearResistor`
    distinguishes it from a passive conductor.
    """

    name = "component-type"
    source = BindingSource.COMPONENT_TYPE

    def __init__(self, catalog: ClassCatalog) -> None:
        self.catalog = catalog

    def bind(self, model) -> list[SemanticBinding]:
        found = []
        for variable in model.variables:
            declaring = getattr(variable, "declaring_class", None)
            if not declaring:
                continue
            member = variable.name.rsplit(".", 1)[-1]
            for role in self.catalog.roles_for(declaring, member,
                                               getattr(variable, "physical_quantity", None)):
                found.append(SemanticBinding(
                    role=role, target_id=variable.id, target_name=variable.name,
                    source=BindingSource.COMPONENT_TYPE,
                    evidence={"declaring_class": declaring, "member": member},
                    target_kind="parameter" if variable.is_parameter else "variable"))
        return found


# ── priority 3: connector role and context ───────────────────────────────────


class ConnectorProvider:
    """Roles implied by a connector member's role and its domain.

    Knowing a variable is the `flow` member of a rotational flange says it is a
    torque without any name being read, which is worth having for the members
    that carry no `quantity` of their own.

    It is an inference about a *family*, though, not a statement about the
    member, and it must stand down where the member says otherwise. Asserting
    it unconditionally produced 640 spurious conflicts over the corpus:

        Thermal.FluidHeatFlow.Interfaces.FlowPort.p
            connector says   potential in a "Thermal" path -> temperature
            the member says  quantity="Pressure"

    A pressure is what it is; the class path merely contains the word Thermal.
    The declared quantity is an authored assertion about this member and the
    connector rule is a guess about its neighbourhood, so where they disagree
    the guess is dropped rather than promoted over it.
    """

    name = "connector"
    source = BindingSource.CONNECTOR

    #: (declaring class contains, connector role) -> role
    RULES: tuple[tuple[str, str, str], ...] = (
        ("Mechanics.Rotational", "flow", "physical.torque"),
        ("Mechanics.Rotational", "potential", "physical.angle"),
        ("Mechanics.Translational", "flow", "physical.force"),
        ("Mechanics.Translational", "potential", "physical.position"),
        ("Electrical", "flow", "physical.current"),
        ("Electrical", "potential", "physical.electric_potential"),
        ("Thermal", "flow", "physical.heat_flow_rate"),
        ("Thermal", "potential", "physical.absolute_temperature"),
    )

    def bind(self, model) -> list[SemanticBinding]:
        found = []
        for variable in model.variables:
            role_kind = getattr(variable, "quantity", None)  # potential/flow/stream
            declaring = getattr(variable, "declaring_class", None)
            if not role_kind or not declaring:
                continue
            # Any declared metadata about *this member* beats a guess about
            # its neighbourhood — the unit as much as the quantity. Without the
            # unit the guess still won 92 times over the corpus, and every one
            # was a signal connector: `VariableResistor.R` is a `RealInput`,
            # marked `potential` only because it is not a flow member, and a
            # causal signal carries no conservation law for "potential in an
            # electrical component" to mean anything about. Its unit says Ohm.
            declared = (QUANTITY_ROLES.get(
                            getattr(variable, "physical_quantity", None) or "")
                        or UNIT_ROLES.get(getattr(variable, "unit", None) or ""))
            for marker, kind, role in self.RULES:
                if kind != role_kind or marker not in declaring:
                    continue
                if declared is not None and not compatible(
                        SemanticRole(declared), SemanticRole(role)):
                    break  # the member is labelled, and genuinely disagrees
                found.append(SemanticBinding(
                    role=SemanticRole(role), target_id=variable.id,
                    target_name=variable.name, source=BindingSource.CONNECTOR,
                    evidence={"connector_role": role_kind,
                              "declaring_class": declaring},
                    target_kind="connector"))
                break
        return found


# ── priority 1: what the user said ───────────────────────────────────────────


class UserProvider:
    """Explicit mappings, the final authority.

    A pattern ending in `*` matches a path prefix, so a user can name a whole
    subtree without listing every member of it.
    """

    name = "user"
    source = BindingSource.USER

    def __init__(self, mappings: dict[str, str], origin: str = "user") -> None:
        self.mappings = mappings
        self.origin = origin

    def bind(self, model) -> list[SemanticBinding]:
        exact = {k: v for k, v in self.mappings.items() if not k.endswith("*")}
        globs = [(k[:-1], v) for k, v in self.mappings.items() if k.endswith("*")]
        found = []
        for variable in model.variables:
            role = exact.get(variable.name)
            pattern = variable.name
            if role is None:
                for prefix, candidate in globs:
                    if variable.name.startswith(prefix):
                        role, pattern = candidate, prefix + "*"
                        break
            if role is None:
                continue
            found.append(SemanticBinding(
                role=SemanticRole(role), target_id=variable.id,
                target_name=variable.name, source=BindingSource.USER,
                evidence={"origin": self.origin, "pattern": pattern},
                target_kind="parameter" if variable.is_parameter else "variable"))
        return found

    @property
    def unmatched(self) -> set[str]:
        """Patterns that matched nothing — a typo in a mapping is silent otherwise."""
        return getattr(self, "_unmatched", set())


class UserDeclarationProvider:
    """Roles a user assigned to a *declaration* rather than to an instance.

    `UserProvider` keys on the flattened instance path, which is right for
    "this particular knob in my plant model". A user who wants to say what
    `MyLibrary.Motor.Rs` means is talking about the class, and naming every
    instance of it by hand is exactly the work the declaring class exists to
    save. Same authority as `UserProvider`: the user outranks the catalogue.
    """

    name = "user-declaration"
    source = BindingSource.USER

    def __init__(self, roles: dict[str, str], origin: str = "user") -> None:
        self.roles = roles
        self.origin = origin

    def bind(self, model) -> list[SemanticBinding]:
        found = []
        for variable in model.variables:
            declaring = getattr(variable, "declaring_class", None)
            if not declaring:
                continue
            member = variable.name.rsplit(".", 1)[-1]
            role = self.roles.get(f"{declaring}.{member}")
            if role is None:
                continue
            found.append(SemanticBinding(
                role=SemanticRole(role), target_id=variable.id,
                target_name=variable.name, source=BindingSource.USER,
                evidence={"origin": self.origin,
                          "declaration": f"{declaring}.{member}"},
                target_kind="parameter" if variable.is_parameter else "variable"))
        return found


# ── priority 5: heuristics, weak by construction ─────────────────────────────


class NameHeuristicProvider:
    """Name patterns, emitted as the weakest source and never alone sufficient.

    Present because the brief asks for it as a hint level, and disabled by
    default: `R`, `m`, `v` and `T` are exactly the names a checker must not
    build a physical claim on.
    """

    name = "heuristic"
    source = BindingSource.HEURISTIC

    PATTERNS: tuple[tuple[str, str], ...] = (
        (r"(^|\.)soc$", "battery.state_of_charge"),
        (r"(^|\.)(vehicle_?speed|v_veh)$", "automotive.vehicle_speed"),
    )

    def bind(self, model) -> list[SemanticBinding]:
        found = []
        for variable in model.variables:
            lowered = variable.name.lower()
            for pattern, role in self.PATTERNS:
                if re.search(pattern, lowered):
                    found.append(SemanticBinding(
                        role=SemanticRole(role), target_id=variable.id,
                        target_name=variable.name, source=BindingSource.HEURISTIC,
                        evidence={"name_pattern": pattern},
                        target_kind="parameter" if variable.is_parameter else "variable"))
                    break
        return found
