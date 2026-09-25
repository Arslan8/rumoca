"""NetworkSan — defects in the shape of the connection graph.

Every other sanitizer here reasons about one declaration or one equation.
This one's subject is the network: components joined at nodes, each node
equating a potential and conserving a flow.

What that buys is a class of question the others cannot form. "Is this
resistance positive?" needs a contract saying what the component is. "Does the
power entering this component over all its ports stay non-negative?" needs
nothing but the ports — it is the definition of passivity, and it is checkable
against a run without anybody declaring an intent.

    static    a port wired to nothing; a component wired to nothing;
              a node whose members disagree about what they carry
    runtime   the conservation law at a node; the power balance of a component

The static half reports nothing as a defect that is merely unusual. An
unconnected port is the ordinary consequence of compiling a sub-circuit
standalone, and it is reported so a reader can *stop* being puzzled by the
structural findings it causes, not so anyone fixes it.
"""

from __future__ import annotations

from ..analysis.context import AnalysisContext
from ..findings.finding import Finding, Severity
from ..findings.location import locate
from ..instrumentation.capability import Capability
from ..instrumentation.connector import requests as connector_requests
from ..instrumentation.request import InstrumentationRequest
from ..network import NodeKind, build, component_power, port_power
from ..runtime.anchors import CanonicalAnchor, EntityKind
from ..runtime.observations import ObservationStream

#: How far a conservation residual may drift before it is worth reporting,
#: relative to the largest flow at the node. A solver holds an algebraic
#: constraint to its own tolerance and no tighter; an absolute threshold would
#: report every megawatt-scale node and miss every microamp one.
CONSERVATION_TOLERANCE = 1e-6


class NetworkSan:
    name = "network"

    requires = {
        "static": frozenset({Capability.CANONICAL_MODEL,
                             Capability.CONNECTION_GRAPH}),
        "runtime": frozenset({Capability.OBSERVE_CONNECTOR}),
    }

    # ── static ───────────────────────────────────────────────────────────────

    def analyze(self, model, context: AnalysisContext) -> list[Finding]:
        network = build(model)
        if network.absent:
            # Nothing to say, and saying nothing must not look like a clean
            # bill of health: the planner reports the pass unsupported when
            # `CONNECTION_GRAPH` is missing, and this is the same fact.
            return []

        findings: list[Finding] = []
        findings += self._mismatched_nodes(network)
        findings += self._unconnected_ports(network)
        findings += self._boundary_ports(network)
        findings += self._isolated_components(network)
        return findings

    def _boundary_ports(self, network) -> list[Finding]:
        """An interface connector of the model itself, with no outside.

        Distinct from an unconnected port, and the distinction matters. An
        unconnected port has nothing attached and MLS §9.2 forces its flow to
        zero, which balances. A *boundary* port is wired to the model's own
        internals and open on the other side: nothing forces anything, the
        node is a half-node, and a structural matching reports an unmatched
        unknown without being able to say that compiling a sub-circuit
        standalone is the reason.

        This project asserted for some time that unconnected connectors
        explained its structural findings. Measured directly, only 4 of the 24
        models involved have one; the boundary ports are the actual mechanism.
        """
        found = []
        for node in network.nodes:
            boundary = node.boundary
            if not boundary or node.kind is NodeKind.UNCONNECTED:
                continue
            found.append(Finding(
                sanitizer=self.name,
                kind="network-boundary-port",
                severity=Severity.LOW,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.VARIABLE, flow.id, flow.name)
                    for flow, _ in node.flows],
                source_locations=locate(node.flows[0][0]) if node.flows else [],
                evidence={
                    "node": str(node),
                    "boundary_connectors": ", ".join(boundary),
                    "wired_to": ", ".join(c for c in node.connectors
                                          if c not in boundary) or "nothing",
                    "note": "this connector belongs to the model itself, not "
                            "to a component inside it: the model is an "
                            "interface compiled on its own, so the node is "
                            "open on one side. Nothing forces its flow, which "
                            "is why a structural matching reports an unmatched "
                            "unknown here. Not a defect in the model"}))
        return found

    def _mismatched_nodes(self, network) -> list[Finding]:
        """A *balance* whose members do not agree about what they carry.

        The subject is the conservation law, not the node. A MultiBody frame
        conserves a force and a torque at the same node, in two separate sums
        — asking whether the node's flows share a quantity reported every
        frame in the corpus as a unit error, which was the check's shape being
        wrong rather than the models'.

        Within one sum the requirement is real: summing an ampere with a
        newton-metre is not a constraint, it is a unit error that typechecks
        because both are `Real`.
        """
        found = []
        for node in network.nodes:
            for balance in node.balances:
                quantities = balance.quantities
                if len(quantities) <= 1:
                    continue
                found.append(Finding(
                    sanitizer=self.name,
                    kind="network-balance-quantity-mismatch",
                    severity=Severity.HIGH,
                    canonical_anchors=[
                        CanonicalAnchor(EntityKind.VARIABLE, flow.id, flow.name)
                        for flow, _ in balance.terms],
                    source_locations=locate(balance.terms[0][0]),
                    evidence={
                        "node": str(node),
                        "connectors": ", ".join(node.connectors),
                        "balance": balance.render(),
                        "quantities": ", ".join(sorted(quantities)),
                        "required": "one conservation law sums one quantity",
                        "note": "these flows are summed to zero by a single "
                                "equation, so they must measure the same "
                                "thing"}))
        return found

    def _unconnected_ports(self, network) -> list[Finding]:
        """A connector nothing was wired to. Informational, never a defect.

        MLS §9.2 sets an unconnected flow to zero, which is exactly right for
        a sub-circuit compiled standalone and exactly what makes it look
        structurally singular. Twenty-two of the twenty-four models in this
        corpus with structural findings are that case, and until now nothing
        said so in the place a reader was looking.
        """
        found = []
        for node in network.nodes:
            if node.kind is not NodeKind.UNCONNECTED:
                continue
            connector = node.connectors[0] if node.connectors else str(node)
            owner = next((p.component for p in network.ports if p.connector == connector), "")
            component = network.components.get(owner)
            anchors = [CanonicalAnchor(EntityKind.VARIABLE, flow.id, flow.name)
                       for flow, _ in node.flows]
            found.append(Finding(
                sanitizer=self.name,
                kind="network-port-unconnected",
                severity=Severity.LOW,
                canonical_anchors=anchors,
                source_locations=locate(node.flows[0][0]) if node.flows else [],
                evidence={
                    "connector": connector,
                    "component": component.label if component else owner,
                    "component_class": (component.class_name if component
                                        else None) or "unknown",
                    "flows_forced_to_zero": ", ".join(
                        flow.name for flow, _ in node.flows),
                    "note": "nothing is connected to this port, so MLS §9.2 "
                            "forces its flow to zero. That is correct for a "
                            "component compiled on its own and is not a "
                            "defect; it is recorded because it is the "
                            "commonest reason a model looks structurally "
                            "singular"}))
        return found

    def _isolated_components(self, network) -> list[Finding]:
        """A component every one of whose ports is unconnected.

        Stronger than a dangling port: the instance contributes equations and
        exchanges nothing with the rest of the model. Still not a defect on
        its own — a source with its output unread is a normal thing to find in
        a test harness — so it is reported at the same strength and left to a
        reader.
        """
        found = []
        for path, component in sorted(network.components.items()):
            if not component.ports:
                continue
            nodes = [network.node(port.node) for port in component.ports]
            if not all(node is not None and node.kind is NodeKind.UNCONNECTED
                       for node in nodes):
                continue
            found.append(Finding(
                sanitizer=self.name,
                kind="network-component-isolated",
                severity=Severity.LOW,
                canonical_anchors=[],
                source_locations=[],
                evidence={
                    "component": component.label,
                    "component_class": component.class_name or "unknown",
                    "ports": ", ".join(port.connector
                                       for port in component.ports),
                    "note": "every port of this instance is unconnected, so "
                            "it exchanges nothing with the rest of the model "
                            "while still contributing its equations"}))
        return found

    # ── instrumentation ──────────────────────────────────────────────────────

    def requests(self, model, context: AnalysisContext
                        ) -> list[InstrumentationRequest]:
        """Both members of every port, tagged with the node they share."""
        network = build(model)
        if network.absent:
            return []
        return connector_requests(network, requested_by=self.name)

    # ── runtime ──────────────────────────────────────────────────────────────

    def observe(self, stream: ObservationStream, model,
                context: AnalysisContext, testcase) -> list[Finding]:
        """Check the two things a network asserts and a run can contradict."""
        network = build(model)
        if network.absent:
            return []
        from ..network.observations import Samples
        identifiers = {v.id for port in network.ports for v in port.potentials}
        identifiers |= {v.id for port in network.ports for v, _ in port.flows}
        samples = Samples(stream, identifiers)
        if samples.reason:
            return [Finding(sanitizer=self.name, kind="network-observation-incomplete",
                            severity=Severity.INFO, test_case=testcase,
                            evidence={"reason": samples.reason, "note": "coverage gap, not a model defect"})]
        findings = self._conservation(samples, network)
        findings += self._power(samples, network, context)
        for finding in findings:
            finding.test_case = testcase
        return findings

    def _conservation(self, stream, network) -> list[Finding]:
        """At every node, the signed flows sum to zero. At every step."""
        found = []
        # A multi-field connector owns separate conservation laws. Combining
        # them can hide equal-and-opposite violations of different quantities.
        for node, balance in ((node, balance) for node in network.nodes for balance in node.balances):
            if not balance.terms:
                continue
            series = [(flow, sign, _series(stream, flow))
                      for flow, sign in balance.terms]
            if any(values is None for _, _, values in series):
                continue
            length = min(len(values) for _, _, values in series)
            worst = 0.0
            scale = 0.0
            at = 0
            for index in range(length):
                total = sum(sign * values[index] for _, sign, values in series)
                magnitude = max(abs(values[index]) for _, _, values in series)
                if abs(total) > abs(worst):
                    worst, scale, at = total, magnitude, index
            if abs(worst) <= CONSERVATION_TOLERANCE * max(scale, 1e-30):
                continue
            found.append(Finding(
                sanitizer=self.name,
                kind="network-conservation-violated",
                severity=Severity.HIGH,
                canonical_anchors=[
                    CanonicalAnchor(EntityKind.VARIABLE, flow.id, flow.name)
                    for flow, _, _ in series],
                source_locations=locate(balance.terms[0][0]),
                evidence={
                    "node": str(node),
                    "required": " + ".join(
                        f"{'-' if sign < 0 else '+'}{flow.name}"
                        for flow, sign, _ in series) + " = 0",
                    "worst_residual": worst,
                    "largest_flow_there": scale,
                    "at_sample": at,
                    "tolerance": f"{CONSERVATION_TOLERANCE} relative",
                    "note": "the conservation law this node asserts does not "
                            "hold in the observed trajectory; either the "
                            "solver is not holding the constraint or the "
                            "observations are not of the same instant"}))
        return found

    def _power(self, stream, network, context) -> list[Finding]:
        """A component that is known **dissipative** must not source energy.

        Dissipative, not passive, and the difference is not pedantry. Running
        the energy pass on `ChuaCircuit` gives `energy_C1 = -1.06 J`: the
        capacitor starts charged at 4 V and discharges, so it delivers net
        energy over the window while being a perfectly ordinary passive
        component. A check on "passive" fires on correct physics.

        A storage element obeys `E_in(t) = E_stored(t) - E_stored(0)`, which
        is only bounded below once the stored energy is known — and that needs
        the constitutive law, not the ports. A resistor stores nothing, so
        `E_in >= 0` holds unconditionally, and that is the check.

        The premise is the same one the physical rules use: only a contract
        supplies it, and without one this says nothing.
        """
        found = []
        passive = _dissipative_components(network, context)
        for path in sorted(passive):
            balance = component_power(network, path)
            if not balance.complete:
                continue
            total = _integrate(stream, balance)
            if total is None or total >= -CONSERVATION_TOLERANCE:
                continue
            component = network.components[path]
            found.append(Finding(
                sanitizer=self.name,
                kind="network-passive-component-sources-power",
                severity=Severity.HIGH,
                canonical_anchors=[],
                source_locations=[],
                evidence={
                    "component": component.label,
                    "component_class": component.class_name or "unknown",
                    "power": balance.render(),
                    "energy_over_run": total,
                    "premise": passive[path],
                    "note": "the power entering this component over all its "
                            "ports is negative on net, so over the run it "
                            "delivered energy to the rest of the model; a "
                            "passive element cannot"}))
        return found


#: Roles whose components store energy, so a negative energy-in is ordinary
#: discharge rather than a violation. Excluded from the balance check for that
#: reason and not because the check is hard: it would be wrong.
STORAGE_ROLES = ("PASSIVE_CAPACITANCE", "PASSIVE_INDUCTANCE")

#: Roles whose components store nothing, so every joule that enters is
#: dissipated and `E_in >= 0` holds at every instant.
DISSIPATIVE_ROLES = ("PASSIVE_RESISTANCE", "PASSIVE_CONDUCTANCE")


def _dissipative_components(network, context) -> dict[str, str]:
    """Components a contract establishes as storing nothing.

    A storage element is deliberately absent: see `_power`. `energy_C1` in
    ChuaCircuit is -1.06 J and the capacitor is behaving correctly.
    """
    from ..semantics import role as roles

    found: dict[str, str] = {}
    semantics = getattr(context, "semantics", None)
    if semantics is None:
        return found
    dissipative = {getattr(roles, name) for name in DISSIPATIVE_ROLES
                   if hasattr(roles, name)}
    storage = {getattr(roles, name) for name in STORAGE_ROLES
               if hasattr(roles, name)}
    for path, component in network.components.items():
        bound = set()
        for port in component.ports:
            for variable in port.potentials:
                bound |= set(semantics.role_names(variable.id))
        if bound & storage:
            continue
        if bound & dissipative:
            found[path] = ("a component contract marks this dissipative: it "
                           "stores no energy, so every joule entering it is "
                           "dissipated")
    return found


def _series(stream, variable):
    values = getattr(stream, "series", None)
    if callable(values):
        try:
            return list(values(variable.id))
        except Exception:
            return None
    return None


def _integrate(stream, balance) -> float | None:
    """Net energy over the run, by the trapezoid rule on the port powers."""
    times = getattr(stream, "times", None)
    times = list(times) if times is not None else None
    if not times or len(times) < 2:
        return None
    total = 0.0
    samples: list[float] = [0.0] * len(times)
    for term in balance.terms:
        flow = _series(stream, term.flow)
        if flow is None:
            return None
        if term.form.value == "flow_is_power":
            factor = [1.0] * len(flow)
        else:
            potential = _series(stream, term.potential)
            if potential is None:
                return None
            if term.form.value == "rate_product":
                potential = _derivative(potential, times)
            factor = potential
        for index in range(min(len(samples), len(flow), len(factor))):
            samples[index] += term.sign * factor[index] * flow[index]
    for index in range(1, min(len(times), len(samples))):
        step = times[index] - times[index - 1]
        total += 0.5 * step * (samples[index] + samples[index - 1])
    return total


def _derivative(values, times) -> list[float]:
    """A central difference. Crude, and enough to sign an energy integral."""
    out = [0.0] * len(values)
    for index in range(len(values)):
        if index == 0 or index >= len(times) - 1 or index >= len(values) - 1:
            continue
        span = times[index + 1] - times[index - 1]
        if span:
            out[index] = (values[index + 1] - values[index - 1]) / span
    return out
