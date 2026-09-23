"""Semantic roles: what a model object *represents*.

A role is deliberately a plain dotted string subclass, not an enum. The set of
things a model can represent is open — nobody can enumerate in advance that
someone will need `hvac.supply_air_temperature` — and an enum would mean
editing this module to add a domain, which is exactly what the architecture
forbids.

Two levels are in use, and the distinction matters:

    physical.mass                     what physics says it is
    automotive.wheel.angular_velocity what the application says it is

A physical role is recoverable from declared metadata: `quantity="Mass"` is an
assertion the type author made. An application role usually is not — nothing in
`rad/s` distinguishes a wheel from a fan — so it comes from the declaring class,
from context, or from the user. `refines` expresses the relationship: an
application role may refine a physical one, and refining is not conflicting.
"""

from __future__ import annotations


class SemanticRole(str):
    """A dotted role name. Open by construction."""

    __slots__ = ()

    @property
    def namespace(self) -> str:
        """The leading segment: `physical`, `automotive`, `battery`, ..."""
        return self.split(".", 1)[0]

    @property
    def parts(self) -> tuple[str, ...]:
        return tuple(self.split("."))

    def refines(self, other: "SemanticRole") -> bool:
        """Whether this role is a strictly more specific spelling of `other`.

        Only true for a dotted prefix within one namespace:
        `automotive.wheel.angular_velocity` refines `automotive.wheel`, but not
        `physical.angular_velocity` — those are two different vocabularies
        describing the same object, and the relation between them is declared
        by a profile rather than inferred from the spelling.
        """
        return self != other and self.startswith(other + ".")


# ── physical roles: recoverable from declared metadata ───────────────────────

MASS = SemanticRole("physical.mass")
LENGTH = SemanticRole("physical.length")
AREA = SemanticRole("physical.area")
VOLUME = SemanticRole("physical.volume")
DENSITY = SemanticRole("physical.density")
ABSOLUTE_TEMPERATURE = SemanticRole("physical.absolute_temperature")
PRESSURE = SemanticRole("physical.pressure")
ANGULAR_VELOCITY = SemanticRole("physical.angular_velocity")
VELOCITY = SemanticRole("physical.velocity")
RESISTANCE = SemanticRole("physical.resistance")
CONDUCTANCE = SemanticRole("physical.conductance")
CAPACITANCE = SemanticRole("physical.capacitance")
INDUCTANCE = SemanticRole("physical.inductance")
MOMENT_OF_INERTIA = SemanticRole("physical.moment_of_inertia")

# ── component roles: what a declaring class says the object *is* ─────────────
#
# These are the discriminator the quantity cannot supply. `physical.resistance`
# is true of a passive resistor and of a negative-impedance converter alike;
# `component.passive.resistance` is true of only the first, and is what a rule
# asserting `R > 0` must actually require.

PASSIVE_RESISTANCE = SemanticRole("component.passive.resistance")
PASSIVE_CONDUCTANCE = SemanticRole("component.passive.conductance")
PASSIVE_CAPACITANCE = SemanticRole("component.passive.capacitance")
PASSIVE_INDUCTANCE = SemanticRole("component.passive.inductance")
ROTATIONAL_INERTIA = SemanticRole("component.rotational.inertia")
TRANSLATIONAL_MASS = SemanticRole("component.translational.mass")

# ── active components: where the passive bound does *not* hold ───────────────
#
# The counterpart to the passive roles, and the reason they exist. Chua's diode
# declares `SI.Conductance Ga = -0.75`: quantity and unit both genuinely say
# conductance, and a rule keyed on either reports a violation on a stock MSL
# example whose negative conductance is the entire point of the device.

ACTIVE_RESISTANCE = SemanticRole("component.active.resistance")
ACTIVE_CONDUCTANCE = SemanticRole("component.active.conductance")

#: A component whose own documentation permits the sign a passive bound forbids.
#:
#: Distinct from `active.*`, which says the component *is* a source. This says
#: only that the library declines to restrict it, which is weaker and is the
#: more common case. `Modelica.Electrical.Analog.Basic.Resistor` states "The
#: Resistance R is allowed to be positive, zero, or negative" — so a checker
#: asserting `R > 0` there is contradicting the component, not the user.
UNRESTRICTED_RESISTANCE = SemanticRole("component.unrestricted.resistance")
UNRESTRICTED_CONDUCTANCE = SemanticRole("component.unrestricted.conductance")

#: A winding resistance: nonnegative, and neither positive nor unrestricted.
#:
#: The third answer the passive/unrestricted pair could not express. Copper
#: resistance is not signed --- a negative stator resistance is a defect and
#: should be reported --- but zero is the ideal lossless winding, which
#: machine examples use deliberately, so the bound is `>= 0` rather than `> 0`.
#: Reporting it under the passive rule made a supported idealisation look like
#: a defect; leaving it unrestricted would stop a negative value being reported
#: at all.
MACHINE_WINDING_RESISTANCE = SemanticRole("component.machine.winding_resistance")
MACHINE_WINDING_CONDUCTANCE = SemanticRole("component.machine.winding_conductance")

#: Any of these on an object means a passive bound must not be asserted.
ACTIVE_ROLES = frozenset({ACTIVE_RESISTANCE, ACTIVE_CONDUCTANCE,
                          UNRESTRICTED_RESISTANCE, UNRESTRICTED_CONDUCTANCE})

#: Roles whose own rule replaces the passive one rather than silencing it.
SCOPED_RESISTANCE_ROLES = frozenset({MACHINE_WINDING_RESISTANCE,
                                     MACHINE_WINDING_CONDUCTANCE})


#: Role pairs that describe the same quantity at different specificity.
#:
#: A translational connector's potential is a position, and a position is a
#: length; both readings are correct and the more specific one should win
#: without either being reported as a disagreement. Kept as an explicit set
#: rather than inferred from units, because `m` is shared by a position, a
#: length and a displacement and only some of those pairings are compatible.
COMPATIBLE: frozenset[frozenset[SemanticRole]] = frozenset({
    frozenset({SemanticRole("physical.position"), LENGTH}),
    frozenset({SemanticRole("physical.angle"), SemanticRole("physical.angular_position")}),
})


def compatible(left: SemanticRole, right: SemanticRole) -> bool:
    """Whether two roles are the same claim at different specificity."""
    return left == right or frozenset({left, right}) in COMPATIBLE
