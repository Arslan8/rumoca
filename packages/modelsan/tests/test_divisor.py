#!/usr/bin/env python3
"""DivisorSan: reaching a denominator, and knowing when we cannot see the path.

Run: python3 packages/modelsan/tests/test_divisor.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages/rumoca-bitcode"), str(ROOT / "packages/modelsan")]

from modelsan.analysis import AnalysisContext          # noqa: E402
from modelsan.dae import load                          # noqa: E402
from modelsan.findings.signature import attach         # noqa: E402
from modelsan.sanitizers import DivisorSan             # noqa: E402

FAILURES: list[str] = []

SOURCE = '''package D
  model Direct
    parameter Real p = 4;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / p;
  end Direct;

  model Product
    parameter Real a = 2;
    parameter Real b = 3;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / (a * b);
  end Product;

  model Propagated
    parameter Real k;
    parameter Real d = k * 10;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / d;
  end Propagated;

  model Relational
    parameter Real hi = 15;
    parameter Real lo = -15;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / (hi - lo);
  end Relational;

  model Guarded
    parameter Real p(min = 1e-9) = 4;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / p;
  end Guarded;

  model NamedBound
    // The bound is a named constant, not a literal. Reading only literals made
    // this read as *unbounded*, and the sanitizer proposed zero for a parameter
    // whose declaration already forbids it — which is how ElastoGap.s_ref and
    // Blocks.Continuous.PI.T reached the confirmed set as false positives.
    constant Real tiny = 1e-60;
    parameter Real p(min = tiny) = 4;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / p;
  end NamedBound;

  model DerivedBound
    constant Real tiny = 1e-60;
    parameter Real scale = 2;
    parameter Real p(min = scale * tiny) = 4;
    Real x(start = 1, fixed = true);
  equation
    der(x) = -x / p;
  end DerivedBound;

  model NoDivision
    parameter Real m = 2;
    Real v(start = 1, fixed = true);
  equation
    m * der(v) = -v;
  end NoDivision;
end D;
'''


def check(condition: bool, label: str) -> None:
    print(f"{'PASS' if condition else 'FAIL'}  {label}")
    if not condition:
        FAILURES.append(label)


def analyze(work: Path, model: str):
    source = work / "D.mo"
    source.write_text(SOURCE)
    artifact = work / f"{model}.rbc"
    subprocess.run([str(ROOT / "target/debug/rumoca"), "compile", str(source),
                    "--model", f"D.{model}", "--emit-bitcode", str(artifact)],
                   capture_output=True, cwd=ROOT, timeout=120)
    if not artifact.exists():
        return None, []
    dae = load(artifact)
    context = AnalysisContext(dae)
    return dae, attach(DivisorSan().analyze(dae, context))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)

        for model, shape, parameter in (("Direct", "direct", "p"),
                                        ("Relational", "relational", "hi")):
            _, findings = analyze(work, model)
            check(len(findings) == 1, f"{model}: one finding")
            if findings:
                evidence = findings[0].evidence
                check(evidence["shape"] == shape, f"{model}: shape is {shape}")
                check(evidence["parameter"] == parameter,
                      f"{model}: blames {parameter}")

        _, findings = analyze(work, "Product")
        check({f.evidence["parameter"] for f in findings} == {"a", "b"},
              "Product: every factor of the denominator is reported")

        # The propagated case needs a parameter that resists constant folding;
        # `k` has no default, so `d = k * 10` survives into the DAE.
        _, findings = analyze(work, "Propagated")
        check(len(findings) == 1, "Propagated: one finding")
        if findings:
            evidence = findings[0].evidence
            check(evidence["parameter"] == "k",
                  "Propagated: blames the settable parameter, not the derived one")
            check(evidence["path"] == "k -> d", "Propagated: the path is recorded")
            check(evidence["shape"] == "propagated", "Propagated: shape is propagated")

        _, findings = analyze(work, "Guarded")
        check(findings == [], "Guarded: a declared min excludes zero, so nothing "
                              "is reported")

        # TOOLBUG-010. A bound written as a named constant is still a bound.
        # Reading only bare literals made these read as unbounded, and produced
        # findings against models that are correct — `ElastoGap.s_ref` declares
        # `min=Modelica.Constants.eps` and `Blocks.Continuous.PI.T` declares
        # `min=Modelica.Constants.small`, and both reached the confirmed set.
        _, findings = analyze(work, "NamedBound")
        check(findings == [], "NamedBound: `min = tiny` excludes zero as surely "
                              "as `min = 1e-60` would")

        _, findings = analyze(work, "DerivedBound")
        check(findings == [], "DerivedBound: a bound computed from constants is "
                              "still a bound")

        _, findings = analyze(work, "NoDivision")
        check(findings == [], "NoDivision: a vanishing coefficient is not a "
                              "divisor and belongs to SingularitySan")

        # The relational hint must aim at equality, not at zero: `hi = 0` leaves
        # `hi - lo = 15`, which is perfectly fine.
        dae, _ = analyze(work, "Relational")
        if dae is not None:
            hints = DivisorSan().hints(dae, AnalysisContext(dae))
            values = [v for h in hints for v in h.values]
            check(-15.0 in values,
                  f"Relational hint targets equality with the partner ({values})")
            check(0.0 not in values, "and not zero, which would not zero the divisor")

    print(f"\n{'ALL PASS' if not FAILURES else str(len(FAILURES)) + ' FAILED'}")
    for failure in FAILURES:
        print(f"  - {failure}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
