"""What crosses a port, and whether the component is entitled to it.

The reason to build a connection graph rather than another declaration rule is
that a port carries *power*, and power is the quantity a physical claim can be
made about without knowing anything else about the component. A passive element
dissipates: the power entering it over all its ports is non-negative. Nothing
at declaration level can say that, and it does not need a component contract to
be meaningful.

The trap is that `potential * flow` is power in some domains and not in others:

    electrical      v * i                    a product
    translational   der(s) * f               a product with a derivative
    rotational      der(phi) * tau           the same
    thermal         Q_flow                   the flow *is* the power
    fluid           m_flow * h + ...         neither, without the medium

So the rule is looked up per domain and the answer is `UNKNOWN` where no rule
applies, rather than multiplying two numbers because both happen to be there.
That is the same discipline the intent policy applies to signs: state the
premise, and where there is none, say so.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PowerForm(str, Enum):
    PRODUCT = "product"
    """`potential * flow` is the power crossing the port."""

    RATE_PRODUCT = "rate_product"
    """`der(potential) * flow` is. The potential is a position or an angle and
    the conjugate is its rate, not the potential itself."""

    FLOW_IS_POWER = "flow_is_power"
    """The flow member is already a power. A thermal port's `Q_flow` is watts;
    multiplying it by a temperature would produce nothing physical."""

    UNKNOWN = "unknown"
    """No rule covers this domain. Nothing is claimed."""


@dataclass(frozen=True)
class PowerRule:
    form: PowerForm
    reason: str
    potential_quantity: str = ""
    flow_quantity: str = ""


#: Keyed on the flow member's declared quantity, because that is the reliable
#: half: a rotational flange's potential is an angle and its flow is a torque,
#: and the torque is what names the domain unambiguously.
BY_FLOW_QUANTITY: dict[str, PowerRule] = {
    "ElectricCurrent": PowerRule(
        PowerForm.PRODUCT,
        "electrical: power is v*i, with the potential a voltage",
        potential_quantity="ElectricPotential", flow_quantity="ElectricCurrent"),
    "Force": PowerRule(
        PowerForm.RATE_PRODUCT,
        "translational: power is der(s)*f; the potential is a position, and "
        "its conjugate is a velocity",
        potential_quantity="Position", flow_quantity="Force"),
    "Torque": PowerRule(
        PowerForm.RATE_PRODUCT,
        "rotational: power is der(phi)*tau; the potential is an angle",
        potential_quantity="Angle", flow_quantity="Torque"),
    "HeatFlowRate": PowerRule(
        PowerForm.FLOW_IS_POWER,
        "thermal: Q_flow is already a power, and T is not a factor of it",
        potential_quantity="ThermodynamicTemperature",
        flow_quantity="HeatFlowRate"),
    "Power": PowerRule(
        PowerForm.FLOW_IS_POWER,
        "the flow member is declared a power, so it is one; FluidHeatFlow's "
        "thermal ports use `Power` where HeatTransfer's use `HeatFlowRate`",
        flow_quantity="Power"),
    "EnergyFlowRate": PowerRule(
        PowerForm.FLOW_IS_POWER,
        "an energy flow rate is a power",
        flow_quantity="EnergyFlowRate"),
    "MassFlowRate": PowerRule(
        PowerForm.UNKNOWN,
        "fluid: the power crossing a fluid port depends on the medium's "
        "enthalpy, which is not recoverable from the connector alone"),
    "MagneticFlux": PowerRule(
        PowerForm.UNKNOWN,
        "magnetic: V_m and Phi are conjugate in the magnetic analogy, but "
        "their product is not a power"),
}


@dataclass(frozen=True)
class PortPower:
    """How to compute the power entering one port, or why it cannot be."""

    port: object
    form: PowerForm
    reason: str
    potential: object = None
    flow: object = None
    sign: int = 1

    @property
    def known(self) -> bool:
        return self.form is not PowerForm.UNKNOWN

    def render(self) -> str:
        """The expression, as a reader would write it."""
        if self.form is PowerForm.FLOW_IS_POWER:
            return _signed(self.sign, getattr(self.flow, "name", "?"))
        if self.form is PowerForm.PRODUCT:
            return _signed(self.sign, f"{_name(self.potential)} * {_name(self.flow)}")
        if self.form is PowerForm.RATE_PRODUCT:
            return _signed(self.sign,
                           f"der({_name(self.potential)}) * {_name(self.flow)}")
        return "unknown"


def _name(variable) -> str:
    return getattr(variable, "name", "?")


def _signed(sign: int, text: str) -> str:
    return text if sign >= 0 else f"-({text})"


def port_power(port) -> list[PortPower]:
    """One entry per flow member: how the power through it is computed.

    A connector with several flow members — a MultiBody frame conserves a
    force and a torque — contributes several terms, and they are returned
    separately rather than summed, because a reader checking one of them
    should not have to take the others on trust.
    """
    found: list[PortPower] = []
    for flow, sign in port.flows:
        quantity = getattr(flow, "physical_quantity", None) or ""
        rule = BY_FLOW_QUANTITY.get(quantity)
        if rule is None:
            found.append(PortPower(
                port=port, form=PowerForm.UNKNOWN, flow=flow, sign=sign,
                reason=(f"no power rule covers a flow declared "
                        f"`{quantity or 'without a quantity'}`")))
            continue
        if rule.form is PowerForm.UNKNOWN:
            found.append(PortPower(port=port, form=PowerForm.UNKNOWN, flow=flow,
                                   sign=sign, reason=rule.reason))
            continue
        potential = _conjugate(port, rule)
        if rule.form is not PowerForm.FLOW_IS_POWER and potential is None:
            found.append(PortPower(
                port=port, form=PowerForm.UNKNOWN, flow=flow, sign=sign,
                reason=(f"{rule.reason}, and no potential member of this "
                        f"connector declares `{rule.potential_quantity}`")))
            continue
        found.append(PortPower(port=port, form=rule.form, reason=rule.reason,
                               potential=potential, flow=flow, sign=sign))
    return found


def _conjugate(port, rule: PowerRule):
    """The potential member the rule pairs with the flow."""
    for potential in port.potentials:
        if getattr(potential, "physical_quantity", None) == rule.potential_quantity:
            return potential
    # One potential and no quantity match: a connector that declares exactly
    # one potential leaves no ambiguity about which one is meant, and MSL
    # quantities are not always present on a nested connector's members.
    if len(port.potentials) == 1:
        return port.potentials[0]
    return None


@dataclass
class ComponentPower:
    """Every port power of one component, and whether the set is complete."""

    component: str
    terms: list[PortPower]

    @property
    def complete(self) -> bool:
        """Whether a balance over this component would be a whole balance.

        A component with one unknown term has no usable balance: the missing
        term could be any size, so a negative sum proves nothing. Reporting a
        partial balance as a violation is the shape of error this project keeps
        finding, and the flag exists to make it unavailable.
        """
        return bool(self.terms) and all(term.known for term in self.terms)

    def render(self) -> str:
        return " + ".join(term.render() for term in self.terms) or "0"


def component_power(network, component: str) -> ComponentPower:
    terms: list[PortPower] = []
    for port in network.ports_of(component):
        terms.extend(port_power(port))
    return ComponentPower(component=component, terms=terms)
