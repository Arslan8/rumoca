"""Which roles a Modelica class implies for the members it declares.

This is library knowledge, and it lives here rather than in the binder for the
same reason rule packs live outside the engine: adding a library must not mean
editing the machinery. An entry says *this class declares this member, and the
member means this* — never anything about what value it should hold, which is
the rule's business.

Matching is on the fully qualified class, so
`Modelica.Electrical.Analog.Basic.Resistor` and
`Modelica.Electrical.Spice3.Basic.R_Resistor` are different components that
happen to share a leaf name, and neither is confused with
`...Examples.Utilities.NonlinearResistor`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import role as roles
from .role import SemanticRole


@dataclass(frozen=True)
class ClassSemantics:
    """What one class's members mean."""

    klass: str
    """Fully qualified Modelica class."""

    members: dict[str, SemanticRole] = field(default_factory=dict)
    """Declared member name -> role."""

    note: str = ""
    """Why this class earns these roles, for the reader of a finding."""

    exact: bool = True
    """When false, `klass` matches any class whose path contains it. Used for
    families — every `Modelica.Electrical.Analog.Basic.*` passive element —
    rather than for guessing."""


class ClassCatalog:
    """Registered class semantics, queried by the component-type provider."""

    def __init__(self) -> None:
        self._exact: dict[str, ClassSemantics] = {}
        self._contains: list[ClassSemantics] = []

    def register(self, *entries: ClassSemantics) -> "ClassCatalog":
        for entry in entries:
            if entry.exact:
                self._exact[entry.klass] = entry
            else:
                self._contains.append(entry)
        return self

    def roles_for(self, declaring_class: str, member: str,
                  quantity: str | None = None) -> list[SemanticRole]:
        """Roles this class gives `member`.

        An exact class match wins outright. A family match applies only when no
        exact entry claimed the class, so listing a family never overrides a
        specific statement about one of its members.
        """
        entry = self._exact.get(declaring_class)
        if entry is not None:
            found = entry.members.get(member)
            return [found] if found else []
        out = []
        for family in self._contains:
            if family.klass in declaring_class:
                found = family.members.get(member)
                if found:
                    out.append(found)
        return out

    def note_for(self, declaring_class: str) -> str:
        entry = self._exact.get(declaring_class)
        if entry is not None:
            return entry.note
        for family in self._contains:
            if family.klass in declaring_class:
                return family.note
        return ""

    def __len__(self) -> int:
        return len(self._exact) + len(self._contains)


#: The passive elements of `Modelica.Electrical.Analog.Basic`, named one by one.
#:
#: Listed individually rather than as a family because the point of this entry
#: is that membership in it is a claim about the physics of *that* component.
#: `NonlinearResistor` lives one package away, declares the same
#: `SI.Conductance`, and is deliberately absent: its Ga and Gb are negative by
#: design, and a family rule over `Electrical.Analog` would have swept it in.
MSL_ELECTRICAL = (
    # Not passive. MSL says so in the component's own documentation:
    #   "The Resistance R is allowed to be positive, zero, or negative."
    #   "The Conductance G is allowed to be positive, zero, or negative."
    # These were catalogued as passive and it was wrong — a negative resistance
    # here is a modelling choice the library explicitly supports, not a defect,
    # and asserting `R > 0` contradicts the component rather than the user.
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Basic.Resistor",
        members={"R": roles.UNRESTRICTED_RESISTANCE},
        note="MSL documents R as allowed to be positive, zero or negative",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Basic.Conductor",
        members={"G": roles.UNRESTRICTED_CONDUCTANCE},
        note="MSL documents G as allowed to be positive, zero or negative",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Basic.VariableResistor",
        members={"R": roles.UNRESTRICTED_RESISTANCE},
        note="same family, same documented latitude",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Basic.Capacitor",
        members={"C": roles.PASSIVE_CAPACITANCE},
        note="a passive capacitor stores C*v^2/2",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Basic.Inductor",
        members={"L": roles.PASSIVE_INDUCTANCE},
        note="a passive inductor stores L*i^2/2",
    ),
)

#: The polyphase wrappers, which are arrays of the scalar elements.
#:
#: `Polyphase.Basic.Resistor` extends `TwoPlug` and instantiates
#: `Analog.Basic.Resistor resistor[m](final R=R)`. Its `R` is the scalar
#: component's `R` with an index on it, so it inherits the scalar contract:
#: judging the wrapper by its own declaration while the thing it configures is
#: documented as signed is the same parameter getting two different answers.
MSL_POLYPHASE = (
    ClassSemantics(
        klass="Modelica.Electrical.Polyphase.Basic.Resistor",
        members={"R": roles.UNRESTRICTED_RESISTANCE},
        note="an array of Analog.Basic.Resistor; inherits its signed contract",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Polyphase.Basic.Conductor",
        members={"G": roles.UNRESTRICTED_CONDUCTANCE},
        note="an array of Analog.Basic.Conductor; inherits its signed contract",
    ),
    ClassSemantics(
        klass="Modelica.Electrical.Polyphase.Basic.VariableResistor",
        members={"R": roles.UNRESTRICTED_RESISTANCE},
        note="same family, same documented latitude",
    ),
)

#: Machine windings: nonnegative, which is neither of the other two answers.
#:
#: A stator or rotor resistance is copper and cannot be negative, so the rule
#: must keep firing on a negative value. Zero is the ideal lossless winding and
#: the machine examples set it deliberately, so the bound is `>= 0`. The
#: parameter records are listed beside the machines because that is where a
#: user sets the value.
MSL_MACHINE_WINDINGS = tuple(
    ClassSemantics(klass=klass, members=members, exact=False, note=note)
    for klass, members, note in (
        ("Modelica.Electrical.Machines.Utilities.ParameterRecords",
         {"Rs": roles.MACHINE_WINDING_RESISTANCE,
          "Rr": roles.MACHINE_WINDING_RESISTANCE,
          "Rrd": roles.MACHINE_WINDING_RESISTANCE,
          "Rrq": roles.MACHINE_WINDING_RESISTANCE,
          "Re": roles.MACHINE_WINDING_RESISTANCE,
          "Ra": roles.MACHINE_WINDING_RESISTANCE,
          "R1": roles.MACHINE_WINDING_RESISTANCE,
          "R2": roles.MACHINE_WINDING_RESISTANCE},
         "machine parameter record: copper resistance, zero is the ideal "
         "lossless winding"),
        ("Modelica.Electrical.Machines.BasicMachines",
         {"Rs": roles.MACHINE_WINDING_RESISTANCE,
          "Rr": roles.MACHINE_WINDING_RESISTANCE,
          "Rrd": roles.MACHINE_WINDING_RESISTANCE,
          "Rrq": roles.MACHINE_WINDING_RESISTANCE,
          "Re": roles.MACHINE_WINDING_RESISTANCE,
          "Ra": roles.MACHINE_WINDING_RESISTANCE},
         "machine winding resistance; zero is the ideal lossless limit"),
        ("Modelica.Electrical.Machines.Interfaces",
         {"Ra": roles.MACHINE_WINDING_RESISTANCE,
          "Re": roles.MACHINE_WINDING_RESISTANCE,
          "Rs": roles.MACHINE_WINDING_RESISTANCE},
         "machine interface winding resistance; zero is the ideal lossless "
         "limit"),
    )
)

#: Components whose declared electrical quantity is legitimately negative.
#:
#: Listing these is what lets the passive rules keep firing on classes nobody
#: has catalogued: the claim "this is not passive" is the one that has to be
#: made explicitly, because it is the one that suppresses a real check.
MSL_ELECTRICAL_ACTIVE = (
    ClassSemantics(
        klass="Modelica.Electrical.Analog.Examples.Utilities.NonlinearResistor",
        members={"Ga": roles.ACTIVE_CONDUCTANCE, "Gb": roles.ACTIVE_CONDUCTANCE},
        note="Chua's diode: the negative slope of its characteristic is the "
             "device, not a mistake",
    ),
)

MSL_MECHANICAL = (
    ClassSemantics(
        klass="Modelica.Mechanics.Rotational.Components.Inertia",
        members={"J": roles.ROTATIONAL_INERTIA},
        note="a rigid rotating body has positive moment of inertia",
    ),
    ClassSemantics(
        klass="Modelica.Mechanics.Translational.Components.Mass",
        members={"m": roles.TRANSLATIONAL_MASS},
        note="a rigid translating body has positive mass",
    ),
)


def builtin_catalog() -> ClassCatalog:
    return ClassCatalog().register(
        *MSL_ELECTRICAL, *MSL_POLYPHASE, *MSL_MACHINE_WINDINGS,
        *MSL_ELECTRICAL_ACTIVE, *MSL_MECHANICAL)
