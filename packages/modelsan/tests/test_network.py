"""The connection graph, and what can be asked of it.

Every other analysis in this package has one declaration or one equation as its
subject. This one's subject is the network, and the point of building it is the
class of question that has no form at declaration level: what meets at this
node, what crosses this port, what does this component do to the power passing
through it.

The graph was unavailable until now for a concrete reason: the exporter emitted
the potential half of every connection and never the flow half, so a consumer
saw equalities and no conservation. These tests pin both halves.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.context import AnalysisContext                # noqa: E402
from modelsan.instrumentation import connector                       # noqa: E402
from modelsan.instrumentation.capability import Capability           # noqa: E402
from modelsan.network import (                                       # noqa: E402
    NodeKind, build, component_power, port_power)
from modelsan.network.power import PowerForm                         # noqa: E402
from modelsan.sanitizers import NetworkSan                           # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
ROOTS = ["target/msl/ModelicaStandardLibrary-4.1.0",
         "target/corpus/ModelicaStandardLibrary-4.1.0",
         "target/cmm/CMM-a642c381"]
_CACHE: dict[str, object] = {}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def corpus_model(name: str):
    if name in _CACHE:
        return _CACHE[name]
    path = None
    for line in (ROOT / "tools/sweep/ALL.list").read_text().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1].strip() == name:
            path = parts[0]
    _CACHE[name] = None
    if path is None or not RUMOCA.exists():
        return None
    work = tempfile.mkdtemp()
    artifact = Path(work) / "m.rbc"
    command = [str(RUMOCA), "compile", path, "--model", name,
               "--emit-bitcode", str(artifact)]
    for root in ROOTS:
        command += ["--source-root", root]
    subprocess.run(command, capture_output=True, cwd=ROOT)
    if artifact.exists():
        import rumoca_bitcode
        _CACHE[name] = (rumoca_bitcode.Model.load(artifact), artifact)
    return _CACHE[name]


CHUA = "Modelica.Electrical.Analog.Examples.ChuaCircuit"
FIRST = "Modelica.Mechanics.Rotational.Examples.First"
FREEBODY = "Modelica.Mechanics.MultiBody.Examples.Elementary.FreeBody"
COOLING = "Modelica.Thermal.FluidHeatFlow.Examples.SimpleCooling"


def _network(name):
    found = corpus_model(name)
    if found is None:
        print(f"  skip: {name} unavailable")
        return None, None
    model, artifact = found
    return model, build(model)


# ── the graph itself ─────────────────────────────────────────────────────────


def test_a_node_is_n_ary_not_a_pair():
    print("\n== five pins on one node is one node ==")
    model, net = _network(CHUA)
    if net is None:
        return
    ground = max(net.nodes, key=lambda node: node.degree)
    check(ground.degree == 5,
          f"Chua's ground joins five pins (got {ground.degree})")
    check(set(ground.connectors) ==
          {"C1.n", "C2.n", "Gnd.p", "Nr.n", "Ro.n"},
          f"and they are the right five ({sorted(ground.connectors)})")
    check(len(net.nodes) == 4, f"the circuit has four nodes (got {len(net.nodes)})")


def test_both_halves_of_every_connection_are_present():
    print("\n== a node equates a potential AND conserves a flow ==")
    model, net = _network(CHUA)
    if net is None:
        return
    for node in net.nodes:
        check(bool(node.potentials), f"{node} equates something")
        check(bool(node.balances), f"{node} conserves something")
    ground = max(net.nodes, key=lambda node: node.degree)
    terms = ground.balances[0].terms
    check(len(terms) == 5,
          f"the ground balance sums all five pin currents (got {len(terms)})")


def test_a_frame_conserves_two_things_at_one_node():
    print("\n== force and torque are separate laws at the same node ==")
    model, net = _network(FREEBODY)
    if net is None:
        return
    frames = [node for node in net.nodes if len(node.balances) > 1]
    check(bool(frames), "a MultiBody frame node has more than one balance")
    node = frames[0]
    quantities = {q for balance in node.balances for q in balance.quantities}
    check(quantities == {"Force", "Torque"},
          f"one force law and one torque law (got {sorted(quantities)})")
    for balance in node.balances:
        check(len(balance.quantities) == 1,
              f"and each law sums one quantity ({sorted(balance.quantities)})")


def test_an_unconnected_port_is_its_own_kind():
    print("\n== a dangling flange is not a node of two ==")
    model, net = _network(FIRST)
    if net is None:
        return
    dangling = [node for node in net.nodes if node.kind is NodeKind.UNCONNECTED]
    check(len(dangling) == 1, f"one dangling port (got {len(dangling)})")
    check(dangling[0].connectors == ("inertia3.flange_b",),
          f"the free end of the drive train ({dangling[0].connectors})")


def test_a_signal_connection_conserves_nothing():
    print("\n== a causal connector has no flow member ==")
    model, net = _network(FREEBODY)
    if net is None:
        return
    signal = [node for node in net.nodes if node.kind is NodeKind.SIGNAL]
    check(bool(signal), "the orientation objects form potential-only nodes")
    for node in signal:
        check(not node.balances, f"{node} asserts no conservation law")


def test_a_component_knows_its_class():
    print("\n== a node joins an inductor to a resistor, not L.n to Ro.p ==")
    model, net = _network(CHUA)
    if net is None:
        return
    check(net.components["L"].class_name ==
          "Modelica.Electrical.Analog.Basic.Inductor",
          f"L is an Inductor (got {net.components['L'].class_name})")
    check(net.components["Ro"].leaf_class == "Resistor",
          f"Ro is a Resistor (got {net.components['Ro'].leaf_class})")
    check("Ro" in net.neighbours("L"),
          f"and they are neighbours ({net.neighbours('L')})")


# ── what crosses a port ──────────────────────────────────────────────────────


def test_electrical_power_is_a_product():
    print("\n== v * i ==")
    model, net = _network(CHUA)
    if net is None:
        return
    balance = component_power(net, "Ro")
    check(balance.complete, f"both ports are known ({balance.render()})")
    check(all(term.form is PowerForm.PRODUCT for term in balance.terms),
          "each term is a potential times a flow")
    check("Ro.p.v * Ro.p.i" in balance.render(),
          f"rendered as the reader would write it ({balance.render()})")


def test_rotational_power_needs_a_derivative():
    print("\n== der(phi) * tau, not phi * tau ==")
    model, net = _network(FIRST)
    if net is None:
        return
    balance = component_power(net, "damper")
    check(balance.complete, f"both flanges are known ({balance.render()})")
    check(all(term.form is PowerForm.RATE_PRODUCT for term in balance.terms),
          "an angle's conjugate is an angular velocity, not the angle")
    check("der(" in balance.render(), f"and it shows ({balance.render()})")


def test_a_thermal_flow_is_already_a_power():
    print("\n== Q_flow is watts; T is not a factor of it ==")
    model, net = _network(COOLING)
    if net is None:
        return
    balance = component_power(net, "heatCapacitor")
    check(bool(balance.terms), "the port is recognised")
    check(all(term.form is PowerForm.FLOW_IS_POWER for term in balance.terms),
          f"multiplying by a temperature would produce nothing physical "
          f"({[t.form.value for t in balance.terms]})")


def test_a_domain_with_no_rule_declines_rather_than_guessing():
    print("\n== a fluid port's power needs the medium ==")
    model, net = _network(COOLING)
    if net is None:
        return
    balance = component_power(net, "pump")
    check(not balance.complete,
          "a component with an unknown term has no usable balance")
    unknown = [term for term in balance.terms if not term.known]
    check(bool(unknown), "and the unknown terms say so")
    check(any("enthalpy" in term.reason or "no power rule" in term.reason
              for term in unknown),
          f"with a reason ({[t.reason[:40] for t in unknown][:1]})")


# ── instrumentation ──────────────────────────────────────────────────────────


def test_an_observation_is_tagged_with_its_node():
    print("\n== a flow observed without its node answers nothing ==")
    model, net = _network(CHUA)
    if net is None:
        return
    observed = connector.observations(net)
    check(bool(observed), "every port member is observable")
    check({o.role for o in observed} == {"potential", "flow"},
          "both halves of every port")
    check(all(isinstance(o.node, int) for o in observed),
          "each carrying the node it belongs to")


def test_the_request_names_the_grouping_as_well_as_the_members():
    print("\n== observing the members is not observing the graph ==")
    model, net = _network(CHUA)
    if net is None:
        return
    requests = connector.requests(net)
    capabilities = {request.capability for request in requests}
    check(Capability.OBSERVE_CONNECTOR in capabilities,
          "the members are requested")
    check(Capability.CONNECTION_GRAPH in capabilities,
          "and so is knowing which node each belongs to")


def test_instrumenting_an_artifact_is_idempotent_and_valid():
    print("\n== trace points survive a write, a read and the validator ==")
    found = corpus_model(CHUA)
    if found is None:
        print("  skip: corpus model unavailable")
        return
    model, _ = found
    import rumoca_bitcode

    added = connector.instrument(model)
    check(added > 0, f"{added} connector trace points added")
    check(connector.instrument(model) == 0, "adding them twice adds nothing")

    work = Path(tempfile.mkdtemp()) / "instrumented.rbc"
    model.save(work)
    finished = subprocess.run(
        [str(RUMOCA), "bitcode", "check", str(work), "--strict"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          f"the instrumented artifact validates ({finished.stdout.strip()[-90:]})")

    reloaded = rumoca_bitcode.Model.load(work)
    check(len(reloaded.trace_points) == added, "and reloads with them")
    first = reloaded.trace_points[0]
    check(first.connection_set is not None,
          "each tagged with the node it belongs to")
    check(first.added_by == connector.ADDED_BY,
          f"and with who added it ({first.added_by})")


# ── the sanitizer ────────────────────────────────────────────────────────────


def _findings(name):
    found = corpus_model(name)
    if found is None:
        return None
    model, _ = found
    return NetworkSan().analyze(model, AnalysisContext(model))


def test_a_dangling_port_is_reported_and_not_as_a_defect():
    print("\n== the explanation for the structural findings ==")
    findings = _findings(FIRST)
    if findings is None:
        print("  skip: corpus model unavailable")
        return
    dangling = [f for f in findings if f.kind == "network-port-unconnected"]
    check(len(dangling) == 1, f"one report (got {len(dangling)})")
    check(dangling[0].severity.value == "low", "at low severity")
    check("not a defect" in str(dangling[0].evidence.get("note", "")),
          "saying so in as many words")
    check(dangling[0].evidence.get("component_class", "").endswith("Inertia"),
          f"and naming the class ({dangling[0].evidence.get('component_class')})")


def test_a_frame_is_not_reported_as_a_unit_mismatch():
    print("\n== two laws at one node is not one law over two quantities ==")
    findings = _findings(FREEBODY)
    if findings is None:
        print("  skip: corpus model unavailable")
        return
    mismatches = [f for f in findings
                  if f.kind == "network-balance-quantity-mismatch"]
    check(not mismatches,
          f"a force law and a torque law coexist ({len(mismatches)} reported)")


def test_a_fully_wired_circuit_yields_nothing():
    print("\n== silence where there is nothing to say ==")
    findings = _findings(CHUA)
    if findings is None:
        print("  skip: corpus model unavailable")
        return
    check(findings == [], f"Chua's circuit is fully wired (got {findings})")


def test_the_pass_declares_what_it_needs_rather_than_looking_clean():
    print("\n== an artifact with no graph is skipped, not passed ==")
    check(Capability.CONNECTION_GRAPH in NetworkSan.requires["static"],
          "the static half needs a connection graph")
    check(Capability.OBSERVE_CONNECTOR in NetworkSan.requires["runtime"],
          "the runtime half needs node-tagged observations")

    class Bare:
        name = "Bare"
        variables = equations = components = ()
        connection_sets = ()

    model = Bare()
    check(build(model).absent, "a model with no sets is marked absent")
    check(NetworkSan().analyze(model, AnalysisContext(model)) == [],
          "and the pass says nothing rather than saying clean")


def test_a_boundary_port_is_distinguished_from_an_unconnected_one():
    print("\n== a sub-circuit's own pin is open, not forced to zero ==")
    findings = _findings("Modelica.Electrical.Analog.Examples.OpAmps"
                         ".OpAmpCircuits.Add")
    if findings is None:
        print("  skip: corpus model unavailable")
        return
    boundary = [f for f in findings if f.kind == "network-boundary-port"]
    check(len(boundary) == 4, f"four interface pins (got {len(boundary)})")
    names = {c.strip() for f in boundary
             for c in f.evidence["boundary_connectors"].split(",")}
    check(names == {"n1", "n2", "p1", "p1_2", "p2"},
          f"the model's own connectors ({sorted(names)})")
    check(not [f for f in findings if f.kind == "network-port-unconnected"],
          "and none of them is an unconnected port: they are wired inside")
    check("not a defect" in str(boundary[0].evidence["note"]).lower(),
          "reported as an explanation, not an accusation")
