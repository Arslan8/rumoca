"""Native solver telemetry; projection coordinates are never physical samples."""
import math

from ..runtime.anchors import BackendAnchor, EntityKind
from ..runtime.failures import ExecutionPhase
from ..runtime.observations import (
    EquationResidual, EventTriggered, EventIteration, JacobianObservation, SolverStep,
)


def read_solver(evidence, stream):
    if (not isinstance(evidence, dict) or evidence.get("schema_version") != 1
            or evidence.get("coordinates") != "native-internal"
            or evidence.get("coverage") != "me-accepted-proposals-events-projection-blocks"
            or type(evidence.get("omitted")) is not int or evidence["omitted"] < 0
            or not isinstance(evidence.get("records"), list)):
        raise ValueError("malformed native solver diagnostics")
    for record in evidence["records"]:
        time = float(record["time"])
        if not math.isfinite(time):
            raise ValueError("nonfinite solver diagnostic time")
        kind = record["kind"]
        if kind == "accepted-proposal":
            size, start = float(record["step_size"]), float(record["start"])
            if not math.isfinite(size) or size <= 0 or not math.isfinite(start) or time - start != size:
                raise ValueError("invalid accepted proposal")
            stream.add(SolverStep(time=time, step_size=size, coordinates="accepted-proposal"))
        elif kind == "event":
            stream.add(EventTriggered(time=time))
        elif kind == "event-iterations":
            if type(record["iterations"]) is not int or record["iterations"] < 1 or type(record["converged"]) is not bool:
                raise ValueError("invalid event iteration diagnostic")
            stream.add(EventIteration(time=time, iterations=record["iterations"], converged=record["converged"]))
        elif kind == "projection":
            _projection(record, stream, time)
        else:
            raise ValueError("unknown solver diagnostic record")


def _projection(record, stream, time):
    phase = record["phase"]
    if phase not in {"initialization", "projection", "manifold", "torn-projection"}:
        raise ValueError("unknown projection owner")
    nr, nc = record["row_count"], record["column_count"]
    if type(nr) is not int or type(nc) is not int or min(nr, nc) < 0 or type(record["values_omitted"]) is not bool:
        raise ValueError("invalid projection dimensions")
    if record["values_omitted"]:
        return
    rows, columns = record["rows"], record["columns"]
    residual, matrix = record["residual"], record["jacobian_column_major"]
    if (len(rows) != nr or len(columns) != nc or len(residual) != nr or len(matrix) != nr * nc
            or any(type(i) is not int or i < 0 for i in rows + columns)
            or any(v is not None and (type(v) not in {float, int} or not math.isfinite(v)) for v in residual + matrix)):
        raise ValueError("invalid projection payload")
    execution_phase = ExecutionPhase.INITIALIZATION if phase == "initialization" else ExecutionPhase.SIMULATION
    # Null is native nonfinite numerical evidence, not a missing sample fabricated
    # by the transport. Keep it in the matrix; do not turn it into a finite value.
    stream.add(JacobianObservation(time=time, phase=execution_phase, rows=rows, columns=columns,
        dimension=nr, values_column_major=matrix, coordinates=f"internal-{phase}"))
    for row, value in zip(rows, residual):
        if value is not None:
            stream.add(EquationResidual(time=time, phase=execution_phase, residual=value,
                backend=BackendAnchor("rumoca", f"{phase}:row:{row}", EntityKind.EQUATION),
                coordinates=f"internal-{phase}"))
