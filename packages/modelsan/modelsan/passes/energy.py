"""A worked instrumentation pass: integrate the power crossing every port.

The question this exists to answer is whether an *arbitrary* pass is possible
against an IR with no instructions. This one adds state, adds equations that
define it in terms of variables it did not create, and leaves an artifact that
validates, simulates and reports a quantity the model never contained.

Physically: a passive component's port power integrates to a non-negative
energy. `NetworkSan` can check that against a trajectory, but only if the
trajectory contains the integral — and a numerical integral computed afterwards
from sampled output is a different and worse quantity than one the solver
carried as a state. So the pass puts it in the model.
"""

from __future__ import annotations

from ..network import build as build_network
from ..network.power import PowerForm, component_power
from rumoca_bitcode.builder import Builder

PASS_NAME = "modelsan.passes.energy"


def inject_port_energy(model, components: list[str] | None = None) -> dict:
    """Add `der(E_<component>) = sum of port powers` for each component.

    Only where every term is known: a balance with an unknown term integrates
    to a number whose sign means nothing, and a pass that emitted it would be
    manufacturing the evidence a later check reads.
    """
    network = build_network(model)
    if network.absent:
        return {"skipped": "this artifact carries no connection graph"}

    builder = model.builder(PASS_NAME)
    chosen = components if components is not None else sorted(network.components)
    instrumented: list[str] = []

    for path in chosen:
        balance = component_power(network, path)
        if not balance.complete:
            continue
        total = None
        for term in balance.terms:
            node = _term_expression(builder, term)
            if node is None:
                total = None
                break
            total = node if total is None else builder.add(total, node)
        if total is None:
            continue

        label = (path or "top").replace(".", "_")
        state = builder.add_state(f"energy_{label}", start=0.0)
        builder.add_derivative_equation(state, total)
        builder.add_trace_point(state, f"energy:{path or '<top level>'}")
        instrumented.append(path or "<top level>")

    added = builder.finish()
    added["components"] = instrumented
    return added


def _term_expression(builder: Builder, term) -> int | None:
    """One port power as an expression, or None if it cannot be written.

    `der(potential) * flow` is written with a derivative coordinate rather than
    by differentiating anything: the potential of a mechanical flange is a
    state, so the solver already carries its derivative and the pass is naming
    it, not computing it.
    """
    flow = builder.coordinate(term.flow.id, _role_of(term.flow))
    if term.form is PowerForm.FLOW_IS_POWER:
        node = flow
    elif term.form is PowerForm.PRODUCT:
        potential = builder.coordinate(term.potential.id,
                                       _role_of(term.potential))
        node = builder.multiply(potential, flow)
    elif term.form is PowerForm.RATE_PRODUCT:
        if getattr(term.potential, "role", "") != "state":
            return None
        rate = builder.derivative(term.potential.id)
        node = builder.multiply(rate, flow)
    else:
        return None
    if term.sign < 0:
        node = builder.unary("negate", node)
    return node


def _role_of(variable) -> str:
    """The coordinate kind a reference to this variable must use."""
    role = getattr(variable, "role", "algebraic")
    return {"state": "state", "parameter": "parameter", "input": "input",
            "discrete_real": "discrete_real",
            "discrete_value": "discrete_value"}.get(role, "algebraic")
