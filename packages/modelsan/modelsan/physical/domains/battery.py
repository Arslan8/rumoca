"""Battery and energy-storage rules.

State of charge is the clearest case of an invariant that is neither a
declaration check nor a bound on a single parameter: it is dimensionless, it
must hold throughout the run, and it is bounded on *both* sides. It exercises
parts of the representation the single-sided parameter rules do not.
"""

from __future__ import annotations

from ..invariant import Comparison, Domain, Enforcement
from ..rules import QuantityRule, RulePack

BATTERY = Domain("battery")

PACK = RulePack(
    domain=BATTERY,
    description="Electrochemical storage.",
    rules=[
        QuantityRule(
            rule_id="battery.soc.lower_bound",
            domain=BATTERY,
            quantities=frozenset({"StateOfCharge", "SOC"}),
            op=Comparison.GE, bound=0.0,
            origin="a cell cannot hold negative charge",
            enforcement=Enforcement.RUNTIME, severity="high",
        ),
        QuantityRule(
            rule_id="battery.soc.upper_bound",
            domain=BATTERY,
            quantities=frozenset({"StateOfCharge", "SOC"}),
            op=Comparison.LE, bound=1.0,
            origin="a cell cannot hold more than its capacity; SOC is "
                   "normalised to it",
            enforcement=Enforcement.RUNTIME, severity="high",
        ),
        QuantityRule(
            rule_id="battery.capacity.positive",
            domain=BATTERY,
            quantities=frozenset({"ElectricCharge", "Capacity"}),
            units=frozenset({"A.h", "C"}),
            op=Comparison.GT, bound=0.0,
            origin="capacity is the divisor that normalises charge into SOC",
            enforcement=Enforcement.STATIC, parameters_only=True,
        ),
    ],
)
