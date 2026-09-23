"""ConservationSanitizer: does the equation system implement the balance it owes?

The comparison is between two coefficient maps, so the diagnostic is exact —
a key in the contract and not the equation is a *missing term*, not "mass
conservation failed".
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "rumoca-bitcode"),
                str(Path(__file__).resolve().parents[1])]

from modelsan.conservation.compare import compare                 # noqa: E402
from modelsan.conservation.contract import (                      # noqa: E402
    Applicability, Contract, Role, Term, Verdict,
)
from modelsan.conservation.residual import Normalised             # noqa: E402

NAMES = {1: "m_in", 2: "m_out", 3: "mass", 4: "m_third", 5: "source"}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def contract(*terms, excluded=()) -> Contract:
    return Contract(quantity="mass", scope="tank", terms=list(terms),
                    excluded=excluded, applicability=Applicability.ESTABLISHED)


def observed(**coefficients) -> Normalised:
    mapping = {}
    for name, value in coefficients.items():
        derivative = name.startswith("d_")
        key = next(k for k, v in NAMES.items() if v == name.removeprefix("d_"))
        mapping[(key, derivative)] = float(value)
    return Normalised(mapping)


FLUX_IN = Term(1, "m_in", Role.FLUX)
FLUX_OUT = Term(2, "m_out", Role.SINK)
STORAGE = Term(3, "mass", Role.STORAGE, derivative=True)


def test_1_stateless_balance_is_conserved():
    print("\n== m_in + m_out = 0, no storage ==")
    result = compare(contract(FLUX_IN, Term(2, "m_out", Role.FLUX)),
                     observed(m_in=1, m_out=1), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED, f"got {result.verdict}")


def test_2_missing_boundary_flux_is_a_violation():
    print("\n== a third port exists and the equation omits it ==")
    result = compare(
        contract(FLUX_IN, Term(2, "m_out", Role.FLUX), Term(4, "m_third", Role.FLUX)),
        observed(m_in=1, m_out=1), NAMES)
    check(result.verdict is Verdict.PROVEN_VIOLATION, f"got {result.verdict}")
    check(result.missing == ["m_third"], f"must name the term, got {result.missing}")


def test_3_storage_is_conserved():
    print("\n== m_in - m_out - der(mass) = 0 ==")
    result = compare(contract(FLUX_IN, FLUX_OUT, STORAGE),
                     observed(m_in=1, m_out=-1, d_mass=-1), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED, f"got {result.verdict}")


def test_4_missing_storage_is_a_violation():
    print("\n== a vessel whose equation forgets to accumulate ==")
    result = compare(contract(FLUX_IN, FLUX_OUT, STORAGE),
                     observed(m_in=1, m_out=-1), NAMES)
    check(result.verdict is Verdict.PROVEN_VIOLATION, f"got {result.verdict}")
    check(result.missing == ["der(mass)"],
          f"the missing term must be named, got {result.missing}")


def test_5_a_mis_scaled_term_is_reported_with_both_coefficients():
    print("\n== m_in - 2*m_out - der(mass) = 0 ==")
    result = compare(contract(FLUX_IN, FLUX_OUT, STORAGE),
                     observed(m_in=1, m_out=-2, d_mass=-1), NAMES)
    check(result.verdict is Verdict.PROVEN_VIOLATION, f"got {result.verdict}")
    name, expected, seen = result.mis_scaled[0]
    check((name, expected, seen) == ("m_out", -1.0, -2.0),
          f"expected -1 observed -2 on m_out, got {result.mis_scaled}")


def test_6_a_source_is_not_lost_mass():
    print("\n== an explicit source term belongs in the balance ==")
    result = compare(
        contract(FLUX_IN, FLUX_OUT, Term(5, "source", Role.SOURCE), STORAGE),
        observed(m_in=1, m_out=-1, source=1, d_mass=-1), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED,
          f"a source must not read as an imbalance, got {result.verdict}")


def test_8_an_explicitly_excluded_term_suppresses_its_own_absence():
    print("\n== a documented approximation is not a violation ==")
    result = compare(
        contract(FLUX_IN, FLUX_OUT, STORAGE, excluded=("mass",)),
        observed(m_in=1, m_out=-1), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED,
          f"an excluded term's absence is documented, got {result.verdict}")


def test_9_conservation_does_not_absorb_distribution():
    print("\n== total conserved, individual split wrong ==")
    # §21: `port1 + port2 = total` can hold while each port is individually
    # wrong. That is a distribution defect and belongs to another rule;
    # claiming it here would overstate what this pass establishes.
    result = compare(contract(FLUX_IN, Term(2, "m_out", Role.FLUX)),
                     observed(m_in=1, m_out=1), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED,
          "the conservation property holds and must be reported as holding")


def test_scale_invariance():
    print("\n== 2a + 2b - 2der(m) is the same balance as a + b - der(m) ==")
    result = compare(contract(FLUX_IN, FLUX_OUT, STORAGE),
                     observed(m_in=2, m_out=-2, d_mass=-2), NAMES)
    check(result.verdict is Verdict.PROVEN_CONSERVED,
          f"a uniformly scaled balance is the same balance, got {result.verdict}")


def test_a_nonlinear_equation_is_unknown_not_a_violation():
    print("\n== what cannot be normalised is UNKNOWN ==")
    result = compare(contract(FLUX_IN, FLUX_OUT),
                     Normalised.failed("product of two variables"), NAMES)
    check(result.verdict is Verdict.UNKNOWN,
          f"an unnormalisable equation must not read as a violation, got {result.verdict}")


def main() -> int:
    failures = 0
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            try:
                function()
            except AssertionError as error:
                failures += 1
                print(f"  FAILED: {error}")
    print(f"\n{'all conservation tests passed' if not failures else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
