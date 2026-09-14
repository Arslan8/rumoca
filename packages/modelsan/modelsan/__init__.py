"""ModelSan — a bug finder for Modelica models.

ModelSan is not a linter. It does not care whether a model is syntactically
valid; the compiler settles that. It looks for parameter values, initial
states and execution conditions under which a *valid* model becomes
mathematically invalid or exposes a latent structural problem.

    modelsan Tank.mo

It works on Rumoca's DAE, exported as bitcode, so analyses live outside the
compiler and can be written in Python.
"""

from .analysis import Site, find_domain_sites, incomplete, search_knobs
from .domains import Domain
from .mutate import Candidate, candidates, minimize
from .runner import Outcome, export, find_rumoca, run

__all__ = [
    "Site",
    "Domain",
    "Candidate",
    "Outcome",
    "find_domain_sites",
    "incomplete",
    "search_knobs",
    "candidates",
    "minimize",
    "run",
    "export",
    "find_rumoca",
]
