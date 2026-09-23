"""Producing an artifact, from an SDK that until now could only read one.

Rumoca Bitcode calls itself "a public, versioned interchange format" and its
spec promises a consumer needs no linkage against Rumoca's crates. The SDK's
whole write surface was `add_trace_point` and `save`: you could ask to observe
a variable and nothing else, and the only program that could *produce* an
artifact was the Rumoca compiler.

These tests are the demonstration that it is writable now: build a model from
nothing, validate it with the real validator, simulate it, and check the answer
against the closed form.
"""
from __future__ import annotations

import csv
import math
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "packages" / "rumoca-bitcode"),
                str(ROOT / "packages" / "modelsan")]

import rumoca_bitcode as rb                                       # noqa: E402

RUMOCA = ROOT / "target" / "debug" / "rumoca"


def check(condition: bool, label: str) -> None:
    print(f"  {'ok  ' if condition else 'FAIL'} {label}")
    assert condition, label


def decay(k: float = 2.0, start: float = 1.0):
    """`der(x) = -k*x`, written by something that is not the compiler."""
    model = rb.Model.empty("Decay")
    builder = model.builder("test")
    parameter = builder.add_parameter("k", k)
    state = builder.add_state("x", start=start)
    builder.add_derivative_equation(
        state,
        builder.unary("negate", builder.multiply(builder.coordinate(parameter),
                                                 builder.coordinate(state))))
    builder.add_trace_point(state, "x")
    builder.finish()
    return model


def test_an_empty_model_is_valid_on_its_own():
    print("\n== a producer starts from something already accepted ==")
    model = rb.Model.empty("Nothing")
    check(model.name == "Nothing", "it has a name")
    check(len(model.variables) == 0, "and nothing else")
    if not RUMOCA.exists():
        print("  skip: rumoca not built")
        return
    work = Path(tempfile.mkdtemp()) / "empty.rbc"
    model.save(work)
    finished = subprocess.run(
        [str(RUMOCA), "bitcode", "check", str(work), "--strict"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          f"and the validator accepts it ({finished.stdout.strip()[-70:]})")


def test_a_model_built_from_nothing_validates():
    print("\n== variables, expressions and an equation, from scratch ==")
    model = decay()
    check(len(model.variables) == 2, "two variables")
    check(len(model.equations) == 1, "one equation")
    if not RUMOCA.exists():
        print("  skip: rumoca not built")
        return
    work = Path(tempfile.mkdtemp()) / "decay.rbc"
    model.save(work)
    finished = subprocess.run(
        [str(RUMOCA), "bitcode", "check", str(work), "--strict"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          f"strictly valid ({finished.stdout.strip()[-70:]})")


def test_the_built_model_simulates_to_the_closed_form():
    print("\n== and it is the model we meant ==")
    if not RUMOCA.exists():
        print("  skip: rumoca not built")
        return
    work = Path(tempfile.mkdtemp())
    artifact, trace = work / "decay.rbc", work / "decay.csv"
    decay(k=2.0, start=1.0).save(artifact)
    subprocess.run([str(RUMOCA), "compile-bitcode", str(artifact), "--simulate",
                    "--trace-out", str(trace)], capture_output=True, cwd=ROOT)
    check(trace.exists(), "a trajectory came back")
    rows = list(csv.DictReader(trace.open()))
    final = float(rows[-1]["value"])
    check(abs(final - math.exp(-2.0)) < 1e-4,
          f"x(1) = {final:.6f} against exp(-2) = {math.exp(-2):.6f}")


def test_the_derivative_form_the_runtime_requires_is_in_the_api():
    print("\n== der(x) - rhs, not der(x) + rhs ==")
    if not RUMOCA.exists():
        print("  skip: rumoca not built")
        return
    # The runtime rejects a state equation that is not a *subtractive*
    # derivative residual. The algebraically identical additive form fails at
    # simulation with a message about a constraint nothing else states, so the
    # builder offers the canonical form and this pins why.
    model = rb.Model.empty("Additive")
    builder = model.builder("test")
    state = builder.add_state("x", start=1.0)
    builder.add_equation(builder.add(builder.derivative(state),
                                     builder.coordinate(state)))
    builder.finish()
    work = Path(tempfile.mkdtemp()) / "additive.rbc"
    model.save(work)
    finished = subprocess.run(
        [str(RUMOCA), "compile-bitcode", str(work), "--simulate"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode != 0 or "not a subtractive" in finished.stderr
          or "not a subtractive" in finished.stdout,
          "the additive form is refused by the runtime")

    good = rb.Model.empty("Subtractive")
    builder = good.builder("test")
    state = builder.add_state("x", start=1.0)
    builder.add_derivative_equation(
        state, builder.unary("negate", builder.coordinate(state)))
    # A trace point, because the runtime refuses to simulate an artifact with
    # nothing to observe — correctly, and it says so.
    builder.add_trace_point(state, "x")
    builder.finish()
    work = Path(tempfile.mkdtemp()) / "subtractive.rbc"
    good.save(work)
    finished = subprocess.run(
        [str(RUMOCA), "compile-bitcode", str(work), "--simulate"],
        capture_output=True, text=True, cwd=ROOT)
    check(finished.returncode == 0,
          "and `add_derivative_equation` produces the form that works")


def test_the_builder_refuses_a_forward_operand():
    print("\n== the topological rule, at the call that breaks it ==")
    model = rb.Model.empty("Forward")
    builder = model.builder("test")
    try:
        builder.add_expression({"kind": "unary", "op": "negate", "operand": 99})
        check(False, "a forward operand was accepted")
    except ValueError as error:
        check("not strictly earlier" in str(error), f"refused ({error})")


def test_every_variable_role_can_be_built():
    print("\n== the builder covers the roles, not a convenient subset ==")
    model = rb.Model.empty("Roles")
    builder = model.builder("test")
    for role in rb.builder.ROLES:
        builder.add_variable(f"v_{role}", role)
    builder.finish()
    check(len(model.variables) == len(rb.builder.ROLES),
          f"all {len(rb.builder.ROLES)} roles ({[v.role for v in model.variables]})")


def test_events_and_discrete_definitions_are_reachable():
    print("\n== a pass can add a trap, not only a probe ==")
    model = rb.Model.empty("Trap")
    builder = model.builder("test")
    state = builder.add_state("x", start=1.0)
    builder.add_derivative_equation(state, builder.real(-1.0))
    relation = builder.add_relation(
        builder.binary("less", builder.coordinate(state), builder.real(0.0)))
    trigger = builder.when_relation(relation)
    builder.add_root(relation, builder.always())
    builder.add_event(trigger,
                      builder.assert_action(builder.boolean(False),
                                            "x went negative"))
    builder.finish()
    check(len(model.raw_model["relations"]) == 1, "a relation")
    check(len(model.raw_model["roots"]) == 1, "a zero crossing to locate")
    check(len(model.raw_model["events"]) == 1, "and an action at the event")


def test_the_builder_is_the_sdk_not_the_sanitizer():
    print("\n== writing an artifact is part of the format's contract ==")
    check(hasattr(rb, "Builder"), "rumoca_bitcode.Builder exists")
    from modelsan.passes import Builder as reexported
    check(reexported is rb.Builder,
          "and modelsan re-exports it rather than keeping its own")
