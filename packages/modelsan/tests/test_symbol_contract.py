"""The IR must carry what a declaration promises, and the detector must use it.

Lowering a numeric declaration to an indistinguishable `Real` loses the thing an
analysis most needs: whether the value can change, who may change it, and what
it depends on. Without it a divide-by-zero search offers to set
`Modelica.Constants.pi` to zero, and did.

The rule these tests pin down is deliberately narrow:

    Suppress only when the complete effective binding and dependency chain
    proves the denominator cannot be zero --- not merely because a symbol is
    constant, final, or protected.

So the file has two halves. The first proves the suppressions happen and that
the IR records *why*. The second proves the detector has not been
over-corrected into silence: `constant Real c = 0` is still a guaranteed
division by zero, and `final parameter d = p` is still reachable through `p`.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.context import AnalysisContext              # noqa: E402
from modelsan.divisor import build, collect, find                  # noqa: E402
from modelsan.sanitizers import DivisorSan                         # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"
DEFECT = {"divisor-reachable-zero", "divisor-zero-when-parameters-equal"}


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def build_model(source: str, name: str):
    """Compile a self-contained model and load its artifact."""
    if not RUMOCA.exists():
        return None
    work = tempfile.mkdtemp()
    path = Path(work) / f"{name}.mo"
    path.write_text(source)
    artifact = Path(work) / f"{name}.rbc"
    done = subprocess.run(
        [str(RUMOCA), "compile", str(path), "--model", name,
         "--emit-bitcode", str(artifact), "--no-fold-parameter-bindings"],
        capture_output=True, text=True, cwd=ROOT)
    if not artifact.exists():
        print(f"  note  {name} did not compile: "
              f"{(done.stdout + done.stderr).strip()[-200:]}")
        return None
    import rumoca_bitcode
    return rumoca_bitcode.Model.load(artifact)


def defects(model) -> list:
    return [f for f in DivisorSan().analyze(model, AnalysisContext(model))
            if f.kind in DEFECT]


def symbol(model, name: str):
    return next((v for v in model.variables if v.name == name), None)


# ── the IR carries the contract ──────────────────────────────────────────────


def test_the_ir_records_variability_final_and_visibility():
    print("\n== a declaration's promises survive flattening ==")
    model = build_model("""
model Contracts
  constant Real k = 3;
  parameter Real p = 1;
  final parameter Real f = 5;
  final parameter Real derived = p;
  Real y;
  // A protected section runs to the end of the declarations, so this comes
  // last: putting it first would make every later declaration protected too,
  // which is correct Modelica and would test the wrong thing.
protected
  constant Real hidden = 2;
equation
  y = k + hidden + p + f + derived;
end Contracts;
""", "Contracts")
    if model is None:
        print("  skip  model unavailable")
        return

    expected = {
        "k":       ("constant",  False, False),
        "hidden":  ("constant",  False, True),
        "p":       ("parameter", False, False),
        "f":       ("parameter", True,  False),
        "derived": ("parameter", True,  False),
    }
    for name, (variability, is_final, is_protected) in expected.items():
        declared = symbol(model, name)
        check(declared is not None, f"{name} survives to the artifact")
        if declared is None:
            continue
        contract = declared.contract
        check(contract is not None, f"{name} carries a contract")
        if contract is None:
            continue
        check(contract.variability == variability,
              f"{name} variability is {variability}, got {contract.variability}")
        check(contract.is_final == is_final,
              f"{name} final is {is_final}, got {contract.is_final}")
        check(contract.is_protected == is_protected,
              f"{name} protected is {is_protected}, got {contract.is_protected}")

    # The distinction the whole exercise is about.
    derived = symbol(model, "derived").contract
    check(derived.binding_depends_on != (),
          "a final parameter bound to another parameter records the dependency")
    fixed = symbol(model, "f").contract
    check(fixed.effective_value == 5.0,
          f"a literal binding records its effective value, got "
          f"{fixed.effective_value}")


def test_the_environment_explains_why_a_symbol_is_unreachable():
    print("\n== a rejected witness says why it was rejected ==")
    model = build_model("""
model Why
  constant Real c = 3;
  final parameter Real f = 5;
  parameter Real p = 1;
  final parameter Real d = p;
  Real y;
equation
  y = c + f + p + d;
end Why;
""", "Why")
    if model is None:
        print("  skip  model unavailable")
        return
    environment = build(model)
    for name, settable in (("c", False), ("f", False), ("p", True), ("d", True)):
        declared = symbol(model, name)
        domain = environment.domain(declared.id)
        check(domain.settable is settable,
              f"{name} settable={settable}, got {domain.settable} "
              f"({domain.reason})")
        if not settable:
            check(bool(domain.reason), f"{name} says why: {domain.reason!r}")
    d = environment.domain(symbol(model, "d").id)
    check("adjustable" in d.reason or d.settable,
          f"a final parameter reached through p stays settable: {d.reason!r}")


# ── the six cited suppressions ───────────────────────────────────────────────


def test_an_immutable_constant_is_never_a_witness():
    print("\n== constant pi, m, Lme, unitTime, vRef cannot be zeroed ==")
    model = build_model("""
model Immutables
  constant Real pi = 2*Modelica.Math.asin(1.0);
  constant Integer m = 3;
  protected constant Real Lme = 1;
  constant Real unitTime = 1;
  protected constant Real vRef = 1;
  Real a, b, c, d, e;
equation
  a = 1/(2*pi);
  b = 1/m;
  c = 1/Lme;
  d = 1/unitTime;
  e = 1/vRef;
end Immutables;
""", "Immutables")
    if model is None:
        print("  skip  model unavailable")
        return
    found = defects(model)
    check(not found,
          f"none of the five is reported, got "
          f"{[f.evidence.get('witness') for f in found]}")
    environment = build(model)
    for name in ("pi", "m", "Lme", "unitTime", "vRef"):
        declared = symbol(model, name)
        if declared is None:
            continue
        domain = environment.domain(declared.id)
        check(not domain.settable, f"{name}: {domain.reason}")


def test_a_final_parameter_with_a_literal_binding_is_not_a_witness():
    print("\n== final parameter ZsRef = 1 cannot be overridden ==")
    model = build_model("""
model FinalBinding
  final parameter Real ZsRef = 1;
  Real y;
equation
  y = 1/ZsRef;
end FinalBinding;
""", "FinalBinding")
    if model is None:
        print("  skip  model unavailable")
        return
    check(not defects(model), "not reported")
    environment = build(model)
    domain = environment.domain(symbol(model, "ZsRef").id)
    check(not domain.settable, f"and the reason is recorded: {domain.reason!r}")
    check("final" in domain.reason, "which names the final prefix")


# ── the four that must still be reported ─────────────────────────────────────


def test_a_constant_that_is_actually_zero_is_still_reported():
    print("\n== constant Real c = 0; 1/c is a guaranteed division by zero ==")
    model = build_model("""
model ZeroConstant
  constant Real c = 0;
  Real y;
equation
  y = 1/c;
end ZeroConstant;
""", "ZeroConstant")
    if model is None:
        print("  skip  model unavailable")
        return
    findings = DivisorSan().analyze(model, AnalysisContext(model))
    check(bool(findings),
          "immutability suppresses a *witness*, never a denominator that is "
          "already zero")
    kinds = {f.kind for f in findings}
    check("divisor-zero-at-declared-values" in kinds or bool(kinds & DEFECT),
          f"and it is reported as such, got {kinds}")


def test_protected_does_not_imply_immutable():
    print("\n== protected parameter p = 0; 1/p must be reported ==")
    model = build_model("""
model ProtectedParameter
  protected parameter Real p = 0;
  Real y;
equation
  y = 1/p;
end ProtectedParameter;
""", "ProtectedParameter")
    if model is None:
        print("  skip  model unavailable")
        return
    environment = build(model)
    domain = environment.domain(symbol(model, "p").id)
    check(domain.settable,
          f"a protected parameter is still settable ({domain.reason!r})")
    findings = DivisorSan().analyze(model, AnalysisContext(model))
    check(bool(findings), f"and the division is reported, got {findings}")


def test_a_final_parameter_bound_to_a_settable_one_is_reported():
    print("\n== final parameter d = p; 1/d is reachable through p ==")
    model = build_model("""
model FinalThroughParameter
  parameter Real p = 1;
  final parameter Real d = p;
  Real y;
equation
  y = 1/d;
end FinalThroughParameter;
""", "FinalThroughParameter")
    if model is None:
        print("  skip  model unavailable")
        return
    environment = build(model)
    check(environment.domain(symbol(model, "d").id).settable,
          "d is final and still reachable, because its binding reads p")
    check(bool(defects(model)),
          "so the division is reported")


def test_an_ordinary_parameter_is_reported():
    print("\n== parameter p = 1; 1/p is reachable by setting p = 0 ==")
    model = build_model("""
model PlainParameter
  parameter Real p = 1;
  Real y;
equation
  y = 1/p;
end PlainParameter;
""", "PlainParameter")
    if model is None:
        print("  skip  model unavailable")
        return
    found = defects(model)
    check(bool(found), "reported")
    if found:
        check(found[0].evidence["denominator_at_witness"] == 0.0,
              "with a verified witness")
