"""Semantic binding: what a model object means, and on whose authority.

The case that motivates all of this is real and is in the corpus. Chua's diode
declares `SI.Conductance Ga = -0.757576`. The quantity is genuinely
Conductance, the unit is genuinely S, and both agree at the highest confidence
the matcher can report — so a rule keyed on either flagged a stock MSL example
whose negative conductance is the entire point of the device. Only the
declaring class tells the two apart.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "rumoca-bitcode"),
                str(Path(__file__).resolve().parents[1])]

from modelsan.physical.invariant import Comparison, Domain, Enforcement   # noqa: E402
from modelsan.physical.matching import Premise                            # noqa: E402
from modelsan.physical.rules import RulePack, SemanticRule                # noqa: E402
from modelsan.semantics import (                                          # noqa: E402
    BindingSource,
    ClassCatalog,
    ClassSemantics,
    ComponentTypeProvider,
    ConnectorProvider,
    NameHeuristicProvider,
    QuantityProvider,
    SemanticBinder,
    SemanticBinding,
    SemanticConfig,
    SemanticRole,
    UserProvider,
    builtin_catalog,
)
from modelsan.semantics import role as roles                              # noqa: E402


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


class FakeVar:
    def __init__(self, id, name, quantity=None, unit=None, declaring_class=None,
                 connector_role=None, parameter=True):
        self.id, self.name = id, name
        self.physical_quantity, self.unit = quantity, unit
        self.declaring_class = declaring_class
        self.quantity = connector_role
        self.is_parameter = parameter
        self.minimum = self.maximum = self.start = self.binding = None
        self.source = None


class FakeModel:
    def __init__(self, variables):
        self.variables = variables
        self.equations = self.initial_equations = self.expressions = self.events = []


# ── roles ────────────────────────────────────────────────────────────────────


def test_roles_are_open_and_refinement_is_within_a_namespace():
    print("\n== roles are an open vocabulary ==")
    role = SemanticRole("hvac.supply_air_temperature")
    check(role.namespace == "hvac", "a new namespace needs no registration")
    check(SemanticRole("automotive.wheel.angular_velocity").refines(
        SemanticRole("automotive.wheel")), "a dotted prefix is a refinement")
    # Two vocabularies describing the same object are not in a prefix relation,
    # and pretending they are would make every physical role a parent of an
    # unrelated application one.
    check(not SemanticRole("automotive.wheel.angular_velocity").refines(
        SemanticRole("physical.angular_velocity")),
        "a different namespace is not a refinement")


# ── priority 4: the existing unit/quantity inference, preserved ──────────────


def test_quantity_beats_unit_and_unit_still_works():
    print("\n== declared quantity and unit both bind, at different authority ==")
    model = FakeModel([
        FakeVar(1, "body.m", quantity="Mass", unit="kg"),
        FakeVar(2, "thing.x", unit="kg"),          # unit only, no quantity
        FakeVar(3, "opaque.z"),                     # nothing
    ])
    bindings = {b.target_name: b for b in QuantityProvider().bind(model)}
    check(bindings["body.m"].source is BindingSource.QUANTITY,
          "a declared quantity binds at QUANTITY authority")
    check(bindings["thing.x"].source is BindingSource.UNIT,
          "a bare unit still binds, at the weaker UNIT authority")
    check(bindings["thing.x"].is_weak and not bindings["body.m"].is_weak,
          "only the unit-only binding is weak")
    check("opaque.z" not in bindings, "no metadata binds nothing")


# ── priority 2: the declaring class, which is the discriminator ──────────────


def test_declaring_class_separates_three_kinds_of_component():
    print("\n== the class says which of three situations this is ==")
    unrestricted = FakeVar(1, "Ro.R", quantity="Resistance", unit="Ohm",
                           declaring_class="Modelica.Electrical.Analog.Basic.Resistor")
    chua = FakeVar(2, "Nr.Ga", quantity="Conductance", unit="S",
                   declaring_class="Modelica.Electrical.Analog.Examples."
                                   "Utilities.NonlinearResistor")
    inertia = FakeVar(3, "load.J", quantity="Inertia", unit="kg.m2",
                      declaring_class="Modelica.Mechanics.Rotational."
                                      "Components.Inertia")
    found = {b.target_name: b.role
             for b in ComponentTypeProvider(builtin_catalog()).bind(
                 FakeModel([unrestricted, chua, inertia]))}
    check(found["Ro.R"] == roles.UNRESTRICTED_RESISTANCE,
          "MSL documents Basic.Resistor's R as permitted to be negative")
    check(found["Nr.Ga"] == roles.ACTIVE_CONDUCTANCE,
          "Chua's diode is active, and says so")
    check(found["load.J"] == roles.ROTATIONAL_INERTIA,
          "a rigid rotating body is the case where the bound does hold")
    # All three carry a declared quantity and a unit. That is the whole point:
    # the quantity cannot tell these apart and the declaring class can.
    check(chua.physical_quantity == "Conductance",
          "the active one still genuinely measures a conductance")


def test_a_documented_latitude_suppresses_the_passive_bound():
    print("\n== the component's own documentation outranks the rule ==")
    # MSL states, in Basic/Resistor.mo and Basic/Conductor.mo:
    #   "The Resistance R is allowed to be positive, zero, or negative."
    # These were catalogued as passive, which made a negative resistance a
    # HIGH-severity violation on a component whose library explicitly permits
    # it. 114 of the corpus's conductance violations came from this.
    resistor = FakeVar(1, "R1.R", quantity="Resistance", unit="Ohm",
                       declaring_class="Modelica.Electrical.Analog.Basic.Resistor")
    roles_found = builtin_catalog().roles_for(
        "Modelica.Electrical.Analog.Basic.Resistor", "R")
    check(roles_found == [roles.UNRESTRICTED_RESISTANCE],
          "Basic.Resistor is catalogued as unrestricted, not passive")

    from modelsan.physical.domains.electrical import PACK
    rule = next(r for r in PACK.rules if r.rule_id == "elec.resistance.positive")
    semantics = SemanticBinder().bind(FakeModel([resistor]))
    # The rule stands down, and says so rather than going quiet: a refuted
    # premise is a result a reader can check, where a missing match is
    # indistinguishable from a rule nobody wrote.
    found = rule.applies(resistor, semantics)
    check(found is not None, "the rule records that it was considered")
    check(found.premise is Premise.REFUTED,
          f"so the positivity premise is refuted, not asserted ({found.premise})")
    check(found.refuted_by == roles.UNRESTRICTED_RESISTANCE,
          "and names the role that refuted it")

    # The bound still holds where nothing grants latitude.
    unknown = FakeVar(2, "other.R", quantity="Resistance", unit="Ohm")
    check(rule.applies(unknown, SemanticBinder().bind(FakeModel([unknown]))) is not None,
          "an uncatalogued resistance is still checked, as an assumption")


def test_catalog_family_never_overrides_a_specific_entry():
    print("\n== a family match does not speak over a named class ==")
    catalog = ClassCatalog().register(
        ClassSemantics(klass="Basic.Resistor", members={"R": roles.PASSIVE_RESISTANCE}),
        ClassSemantics(klass="Electrical", members={"R": roles.ACTIVE_RESISTANCE},
                       exact=False))
    check(catalog.roles_for("Basic.Resistor", "R") == [roles.PASSIVE_RESISTANCE],
          "the exact entry wins outright")
    check(catalog.roles_for("Electrical.Other.Thing", "R") == [roles.ACTIVE_RESISTANCE],
          "the family applies where nothing specific claimed the class")


# ── priority 3: connector context ────────────────────────────────────────────


def test_connector_role_and_domain_bind_without_reading_a_name():
    print("\n== a flange's flow member is a torque, whatever it is called ==")
    model = FakeModel([
        FakeVar(1, "inertia.flange_a.tau", connector_role="flow",
                declaring_class="Modelica.Mechanics.Rotational.Interfaces.Flange_a"),
        FakeVar(2, "pin.i", connector_role="flow",
                declaring_class="Modelica.Electrical.Analog.Interfaces.PositivePin"),
    ])
    found = {b.target_name: b.role for b in ConnectorProvider().bind(model)}
    check(found["inertia.flange_a.tau"] == "physical.torque", "rotational flow is torque")
    check(found["pin.i"] == "physical.current", "electrical flow is current")


def test_connector_inference_stands_down_against_a_declared_quantity():
    print("\n== a family guess does not overrule a labelled member ==")
    # Modelica.Thermal.FluidHeatFlow.Interfaces.FlowPort.p is a *pressure*
    # potential whose class path contains the word Thermal. Asserting the
    # family rule regardless produced 640 spurious conflicts over the corpus,
    # 90 of them exactly this.
    pressure = FakeVar(1, "port.p", quantity="AbsolutePressure", unit="Pa",
                       connector_role="potential",
                       declaring_class="Modelica.Thermal.FluidHeatFlow."
                                       "Interfaces.FlowPort")
    unlabelled = FakeVar(2, "port.T", connector_role="potential",
                         declaring_class="Modelica.Thermal.HeatTransfer."
                                         "Interfaces.HeatPort")
    found = {b.target_name: b.role
             for b in ConnectorProvider().bind(FakeModel([pressure, unlabelled]))}
    check("port.p" not in found,
          "the connector rule drops out where the member is labelled otherwise")
    check(found.get("port.T") == "physical.absolute_temperature",
          "and still fires for a member that carries no quantity of its own")

    # And the whole point: no conflict is manufactured.
    conflicts = SemanticBinder().bind(FakeModel([pressure])).conflicts
    check(conflicts == [], "no conflict is reported for a member that never disagreed")


def test_a_signal_connector_does_not_get_physical_connector_semantics():
    print("\n== a RealInput is not a potential ==")
    # `Modelica.Electrical.Analog.Basic.VariableResistor.R` is a `RealInput`.
    # The bitcode marks it `potential` because it is not a flow member, and its
    # declaring class contains "Electrical" — so the family rule called it an
    # electric potential. It is a resistance, and its unit says so. A causal
    # signal carries no conservation law for "potential" to mean anything about.
    signal = FakeVar(1, "vr.R", unit="Ohm", connector_role="potential",
                     declaring_class="Modelica.Electrical.Analog.Basic."
                                     "VariableResistor")
    found = {b.target_name: b.role for b in ConnectorProvider().bind(FakeModel([signal]))}
    check("vr.R" not in found, "the unit contradicts the family guess, so it drops")
    check(SemanticBinder().bind(FakeModel([signal])).conflicts == [],
          "and no conflict is manufactured")


def test_compatible_readings_are_not_a_conflict():
    print("\n== position and length are one claim at two specificities ==")
    # A translational connector's potential is a position; a position is a
    # length. Both readings are right, the more specific should win, and
    # reporting them against each other was 458 of 640 spurious conflicts.
    position = FakeVar(1, "mass.s", unit="m", connector_role="potential",
                       declaring_class="Modelica.Mechanics.Translational."
                                       "Interfaces.Flange_a")
    found = SemanticBinder().bind(FakeModel([position]))
    check(found.conflicts == [], "compatible readings do not conflict")
    check(found.has("physical.position"),
          "and the more specific reading is the one kept")


# ── priority 1: the user, and priority 5: heuristics ─────────────────────────


def test_user_mappings_win_and_globs_match_a_subtree():
    print("\n== the user is the final authority ==")
    model = FakeModel([
        FakeVar(1, "chassis.v", quantity="Velocity", unit="m/s"),
        FakeVar(2, "wheel.fl.w", quantity="AngularVelocity", unit="rad/s"),
    ])
    binder = SemanticBinder(user_mappings={
        "chassis.v": "automotive.vehicle_speed", "wheel.*": "automotive.wheel"})
    found = binder.bind(model)
    check(found.get("automotive.vehicle_speed").target_name == "chassis.v",
          "an exact mapping binds")
    check(found.get("automotive.wheel").target_name == "wheel.fl.w",
          "a trailing * matches a path prefix")
    # The physical reading is not destroyed by the application one; they are
    # different vocabularies and a rule may be written against either.
    check(found.has("physical.velocity"), "the inferred physical role survives")


def test_heuristics_are_off_by_default_and_weak_when_on():
    print("\n== a name is a hint, never a premise ==")
    model = FakeModel([FakeVar(1, "battery.soc", unit="1")])
    check(not SemanticBinder().bind(model).has("battery.state_of_charge"),
          "heuristics do not run unless asked for")
    binding = SemanticBinder(heuristics=True).bind(model).get("battery.state_of_charge")
    check(binding is not None and binding.is_weak,
          "when enabled a name binds only at the weakest authority")


def test_a_mistyped_user_mapping_is_reported():
    print("\n== a mapping that matches nothing is not silence ==")
    model = FakeModel([FakeVar(1, "chassis.v", quantity="Velocity")])
    found = SemanticBinder(user_mappings={"chasis.v": "automotive.vehicle_speed"}).bind(model)
    check(found.unmatched_patterns == ("chasis.v",),
          "the typo is surfaced rather than failing quietly")


# ── conflict and ambiguity ───────────────────────────────────────────────────


def test_a_user_binding_that_contradicts_the_model_is_applied_and_reported():
    print("\n== the user wins, and the disagreement stays visible ==")
    model = FakeModel([FakeVar(1, "x", quantity="ThermodynamicTemperature", unit="K")])
    found = SemanticBinder(user_mappings={"x": "automotive.vehicle_speed"}).bind(model)
    check(found.get("automotive.vehicle_speed") is not None,
          "the explicit binding is applied")
    check(len(found.conflicts) == 1, "and the contradiction is recorded")
    check("physical.absolute_temperature" in found.conflicts[0].describe(),
          "the report says what the model's own metadata claimed")


def test_an_ambiguous_role_binds_nothing():
    print("\n== several candidates means no answer, not the first one ==")
    role = SemanticRole("automotive.wheel.angular_velocity")

    class Guesser:
        name, source = "guess", BindingSource.HEURISTIC

        def bind(self, model):
            return [SemanticBinding(role=role, target_id=v.id, target_name=v.name,
                                    source=BindingSource.HEURISTIC,
                                    evidence={"name_pattern": "w*"})
                    for v in model.variables]

    model = FakeModel([FakeVar(1, "w1", quantity="AngularVelocity"),
                       FakeVar(2, "w2", quantity="AngularVelocity")])
    found = SemanticBinder(providers=[Guesser()]).bind(model)
    check(found.get(role) is None, "an ambiguous role has no unique answer")
    check(len(found.ambiguities) == 1, "and the ambiguity is reported")
    check(found.ambiguities[0].candidates == ("w1", "w2"), "with both candidates named")
    # Distinguishable from "nothing filled it", which reports no ambiguity.
    check(SemanticBinder(providers=[]).bind(model).ambiguities == [],
          "an unfilled role is not an ambiguous one")


def test_explicit_bindings_are_not_reported_as_ambiguous():
    print("\n== the user naming four wheels is not an ambiguity ==")
    model = FakeModel([FakeVar(i, f"w{i}", quantity="AngularVelocity")
                       for i in range(1, 5)])
    found = SemanticBinder(user_mappings={
        f"w{i}": "automotive.wheel.angular_velocity" for i in range(1, 5)}).bind(model)
    check(found.ambiguities == [], "deliberate multiplicity is not a guess")
    check(len(found.all("automotive.wheel.angular_velocity")) == 4,
          "all four remain reachable")


# ── rules written against roles ──────────────────────────────────────────────


def test_a_rule_stands_down_on_an_excluded_role_and_grades_on_a_confirming_one():
    print("\n== the rule keys on what the object is, not what it measures ==")
    # A synthetic catalog, because MSL turns out to contain no conductance that
    # is documented as passive — Basic.Conductor explicitly is not. This tests
    # the rule mechanism, not the library.
    catalog = ClassCatalog().register(
        ClassSemantics(klass="Vendor.PassiveShunt",
                       members={"G": roles.PASSIVE_CONDUCTANCE}),
        ClassSemantics(klass="Vendor.NegativeImpedanceConverter",
                       members={"G": roles.ACTIVE_CONDUCTANCE}))

    rule = SemanticRule(
        rule_id="elec.conductance.positive", domain=Domain("electrical"),
        quantities=frozenset({"Conductance"}), units=frozenset({"S"}),
        op=Comparison.GT, bound=0.0, origin="passive conductor",
        confirming_roles=frozenset({roles.PASSIVE_CONDUCTANCE}),
        excluded_roles=frozenset({roles.ACTIVE_CONDUCTANCE}),
        enforcement=Enforcement.STATIC, parameters_only=True)

    passive = FakeVar(1, "shunt.G", quantity="Conductance", unit="S",
                      declaring_class="Vendor.PassiveShunt")
    active = FakeVar(2, "nic.G", quantity="Conductance", unit="S",
                     declaring_class="Vendor.NegativeImpedanceConverter")
    unknown = FakeVar(3, "mystery.G", quantity="Conductance", unit="S")
    semantics = SemanticBinder(catalog=catalog).bind(
        FakeModel([passive, active, unknown]))

    refuted = rule.applies(active, semantics)
    check(refuted is not None and refuted.premise is Premise.REFUTED,
          "an active conductance refutes the passive bound rather than "
          f"matching it ({refuted and refuted.premise})")

    confirmed = rule.applies(passive, semantics)
    check(confirmed is not None and confirmed.semantic_role == roles.PASSIVE_CONDUCTANCE,
          "a passive conductance is, and the role is recorded")
    check(rule.severity_for(confirmed) == "high",
          "an established premise is reported at full severity")

    # Coverage must not collapse to the catalogued classes: a negative
    # conductance is still anomalous where nothing is known either way.
    assumed = rule.applies(unknown, semantics)
    check(assumed is not None and assumed.semantic_role is None,
          "an uncatalogued class still matches on the declared quantity")
    check(rule.severity_for(assumed) == "medium",
          "but as an assumption, at lower severity")


def test_an_application_rule_needs_a_binding_to_fire_at_all():
    print("\n== a profile is not a binding ==")
    from modelsan.semantics.profiles import profile_packs

    pack = profile_packs(["automotive"])[0]
    rule = next(r for r in pack.rules if r.rule_id == "auto.wheel.radius.positive")
    radius = FakeVar(1, "fl.r", quantity="Length", unit="m")
    model = FakeModel([radius])

    check(rule.applies(radius, SemanticBinder().bind(model)) is None,
          "selecting the profile does not say which length is a wheel radius")
    bound = SemanticBinder(user_mappings={"fl.r": "automotive.wheel.radius"}).bind(model)
    check(rule.applies(radius, bound) is not None,
          "the mapping is what makes the rule applicable")


# ── configuration ────────────────────────────────────────────────────────────


def test_config_is_read_from_outside_the_model():
    print("\n== semantics live outside the Modelica source ==")
    config = SemanticConfig.from_dict({
        "semantics": {"vehicle.chassis.v": "automotive.vehicle_speed"},
        "physicalsan": {"profiles": ["automotive"]}}, origin="semantics.toml")
    check(config.mappings["vehicle.chassis.v"] == "automotive.vehicle_speed",
          "mappings are read")
    check(config.profiles == ("automotive",), "profiles are read")
    check(bool(SemanticConfig()) is False, "an empty config is falsy")


def test_provenance_reaches_the_binding():
    print("\n== every binding says where it came from ==")
    model = FakeModel([FakeVar(1, "R.R", quantity="Resistance", unit="Ohm",
                               declaring_class="Modelica.Electrical.Analog."
                                               "Basic.Resistor")])
    found = SemanticBinder(user_mappings={}).bind(model)
    by_source = {b.source: b for b in found.roles_of(1)}
    check(BindingSource.QUANTITY in by_source, "the quantity binding is kept")
    check(BindingSource.COMPONENT_TYPE in by_source, "so is the class binding")
    evidence = by_source[BindingSource.COMPONENT_TYPE].evidence
    check(evidence["declaring_class"].endswith("Basic.Resistor"),
          "and it names the class that justified it")
    check("bindings" in found.summary() and found.summary()["conflicts"] == 0,
          "the map summarises itself for a report")


def main() -> int:
    failures = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            try:
                function()
            except AssertionError as error:
                failures += 1
                print(f"  FAILED: {error}")
    print(f"\n{'all semantic binding tests passed' if not failures else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
