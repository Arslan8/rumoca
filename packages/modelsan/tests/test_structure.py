"""StructureSan: matching over the equation-variable graph.

The array cases are the point of this file. `Real x[3]` is three unknowns and
`for i in 1:3 loop x[i] = i` is three rows, but both arrive as a single object
carrying a count. A matching that treats each as one node reports every array
model as under-constrained by its extent — which is exactly what happened, and
why the pass used to skip array models outright.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

from modelsan.analysis.structure import (                          # noqa: E402
    StructuralGraph, family_key, family_id_of, is_family, maximum_matching)


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def graph_of(rows: list[tuple[int, set[int], int]],
             scalars: dict[int, int] | None = None) -> StructuralGraph:
    """`rows` is (equation key, unknowns it reads, how many scalar rows)."""
    graph = StructuralGraph()
    for key, reads, count in rows:
        graph.incident[key] = set(reads)
        graph.equations.add(key)
        graph.equation_capacity[key] = count
        for variable in reads:
            graph.touching.setdefault(variable, set()).add(key)
            graph.unknowns.add(variable)
            graph.unknown_capacity[variable] = (scalars or {}).get(variable, 1)
    return graph


# ── the scalar case still behaves like an ordinary matching ──────────────────


def test_a_square_scalar_system_matches_completely():
    print("\n== three equations, three unknowns, nothing unmatched ==")
    graph = graph_of([(0, {0, 1}, 1), (1, {1, 2}, 1), (2, {0, 2}, 1)])
    matching = maximum_matching(graph)
    check(matching.size == 3, f"all three unknowns matched, got {matching.size}")
    check(not matching.unmatched_variables(graph), "no unknown left over")
    check(not matching.unmatched_equations(graph), "no equation left over")


def test_an_unknown_no_equation_touches_is_unmatched():
    print("\n== a genuinely under-determined scalar system still fires ==")
    graph = graph_of([(0, {0}, 1), (1, {0}, 1)], {0: 1})
    matching = maximum_matching(graph)
    check(matching.unmatched_equations(graph) == {1},
          "the second equation has nothing left to constrain")


# ── arrays: the capacity is the whole point ──────────────────────────────────


def test_a_family_of_three_rows_determines_an_unknown_of_three_scalars():
    print("\n== for i in 1:3 loop x[i] = i  is balanced, not 2 short ==")
    graph = graph_of([(family_key(0), {0}, 3)], {0: 3})
    matching = maximum_matching(graph)
    check(not matching.unmatched_variables(graph),
          "three rows determine three scalars, so nothing is unmatched")
    check(not matching.unmatched_equations(graph), "and no row is spare")


def test_a_family_one_row_short_reports_the_shortfall():
    print("\n== two rows for three scalars is short by exactly one ==")
    graph = graph_of([(family_key(0), {0}, 2)], {0: 3})
    matching = maximum_matching(graph)
    check(matching.unmatched_variables(graph) == {0}, "the unknown is short")
    check(matching.covered_variables.get(0) == 2,
          f"two of its three scalars are determined, got "
          f"{matching.covered_variables.get(0)}")


def test_a_family_with_a_spare_row_is_over_constrained():
    print("\n== four rows for three scalars leaves one row spare ==")
    graph = graph_of([(family_key(0), {0}, 4)], {0: 3})
    matching = maximum_matching(graph)
    check(matching.unmatched_equations(graph) == {family_key(0)},
          "the family has a row that determines nothing")
    check(matching.covered_equations.get(family_key(0)) == 3,
          "exactly three of its four rows were used")


def test_rows_are_shared_across_unknowns_by_flow_not_by_pairing():
    print("\n== one family of six rows covers two arrays of three ==")
    # A one-to-one matching cannot express this at all: it would pair the
    # family with one unknown and call the other undetermined.
    graph = graph_of([(family_key(0), {0, 1}, 6)], {0: 3, 1: 3})
    matching = maximum_matching(graph)
    check(not matching.unmatched_variables(graph), "both arrays are determined")
    check(matching.size == 6, f"all six scalars covered, got {matching.size}")


def test_family_keys_do_not_collide_with_equation_ids():
    print("\n== family 0 and equation 0 are different nodes ==")
    check(family_key(0) != 0, "family 0 must not be keyed as equation 0")
    check(is_family(family_key(7)) and family_id_of(family_key(7)) == 7,
          "a family key round-trips to its id")
    check(not is_family(0), "equation 0 is not a family")


# ── what counts as an incidence edge ─────────────────────────────────────────


def compile_model(source: str, name: str):
    """Compile one model and load its artifact, or None if rumoca is not built."""
    import rumoca_bitcode
    rumoca = ROOT / "target" / "debug" / "rumoca"
    if not rumoca.exists():
        return None
    with tempfile.TemporaryDirectory() as work:
        path = Path(work) / f"{name}.mo"
        path.write_text(source)
        artifact = Path(work) / f"{name}.rbc"
        result = subprocess.run(
            [str(rumoca), "compile", str(path), "--model", name,
             "--emit-bitcode", str(artifact)],
            capture_output=True, text=True)
        assert result.returncode == 0, result.stderr[-400:]
        return rumoca_bitcode.Model.load(artifact)


def matching_of(model):
    from modelsan.analysis import structure as structural
    from modelsan.analysis.dependencies import build as build_dependencies
    graph = structural.build(model, build_dependencies(model))
    return graph, maximum_matching(graph)


def test_a_state_is_matched_by_the_equation_holding_its_derivative():
    print("\n== der(x) is what determines x ==")
    # `der(x) = u` is the only equation mentioning `x`, and it mentions it only
    # under `der`. Excluding derivative reads drops `x` out of the graph, and
    # then nothing reports that the model has an undetermined state — or, worse,
    # the equation gets spent on `u` and something else comes up short.
    model = compile_model(
        "model Der1\n  Real x;\n  Real u;\nequation\n"
        "  der(x) = u;\n  u = time;\nend Der1;\n", "Der1")
    if model is None:
        print("  skip  rumoca is not built")
        return
    graph, matching = matching_of(model)
    check(not matching.unmatched_variables(graph),
          f"x and u are both determined, got {matching.unmatched_variables(graph)}")
    check(not matching.unmatched_equations(graph), "and no equation is spare")


def test_reading_pre_of_a_variable_does_not_determine_it():
    print("\n== pre(v) is a known, not a candidate ==")
    # `pre(v)` is the value `v` held at event entry. An equation reading it
    # depends on `v` but cannot determine it, and a matching that thinks
    # otherwise spends the equation there and reports something else unmatched.
    model = compile_model(
        "model Pre1\n  Real x(start = 0, fixed = true);\n"
        "  discrete Real held(start = 0, fixed = true);\n"
        "equation\n  der(x) = 1;\n"
        "  when sample(0, 1) then\n    held = pre(x) + 1;\n  end when;\n"
        "end Pre1;\n", "Pre1")
    if model is None:
        print("  skip  rumoca is not built")
        return
    equations = list(model.discrete_real_equations) + list(model.equations)
    previous = {v.name for e in equations for v in e.reads_previous}
    check("x" in previous, f"pre(x) is recorded as a previous-value read, got {previous}")
    for equation in equations:
        check("x" not in {v.name for v in equation.reads}
              or not any(v.name == "x" for v in equation.reads_previous),
              "a pre(x) read must not also appear as a current-value read")
    graph, matching = matching_of(model)
    check(not matching.unmatched_variables(graph),
          f"both unknowns are determined, got {matching.unmatched_variables(graph)}")


# ── end to end, through the compiler ─────────────────────────────────────────


def test_an_array_model_compiles_and_matches_through_the_real_pipeline():
    print("\n== Real x[3] with a for equation is balanced end to end ==")
    rumoca = ROOT / "target" / "debug" / "rumoca"
    if not rumoca.exists():
        print("  skip  rumoca is not built")
        return
    import rumoca_bitcode

    from modelsan.analysis import structure as structural
    from modelsan.analysis.dependencies import build as build_dependencies

    source = "model Arr\n  Real x[3];\nequation\n  for i in 1:3 loop\n" \
             "    x[i] = i;\n  end for;\nend Arr;\n"
    with tempfile.TemporaryDirectory() as work:
        path = Path(work) / "Arr.mo"
        path.write_text(source)
        artifact = Path(work) / "Arr.rbc"
        result = subprocess.run(
            [str(rumoca), "compile", str(path), "--model", "Arr",
             "--emit-bitcode", str(artifact)],
            capture_output=True, text=True)
        check(result.returncode == 0, f"the model compiles: {result.stderr[-200:]}")
        model = rumoca_bitcode.Model.load(artifact)

    check(len(model.equation_families) == 1,
          f"the for equation exports as one family, got "
          f"{len(model.equation_families)}")
    family = model.equation_families[0]
    check(family.scalar_rows == 3, f"standing for three rows, got {family.scalar_rows}")
    check([b.name for b in family.domain.binders] == ["i"],
          "over a binder named as the source wrote it")

    graph = structural.build(model, build_dependencies(model))
    matching = maximum_matching(graph)
    check(not matching.unmatched_variables(graph),
          f"x is fully determined, got {matching.unmatched_variables(graph)}")
    check(not matching.unmatched_equations(graph),
          f"and no row is spare, got {matching.unmatched_equations(graph)}")
