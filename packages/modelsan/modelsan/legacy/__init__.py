"""The pre-layering ModelSan, kept working while callers migrate.

These modules predate the layered architecture: they mix analysis, execution,
mutation and reporting in the same files, which is exactly what the new
structure separates. They are retained rather than deleted because the corpus
sweep tooling in `tools/sweep/` runs against them, and losing a reproducible
sweep to a refactor would be a bad trade.

Nothing new should import from here. The replacements are:

    legacy.analysis      -> analysis/ (shared services) + sanitizers/
    legacy.domains       -> sanitizers/domain.py
    legacy.mutate        -> fuzz/parameter.py
    legacy.runner        -> backends/rumoca.py
    legacy.omc_backend   -> backends/openmodelica.py
    legacy.differential  -> sanitizers/differential.py
    legacy.declcheck     -> sanitizers/declaration.py
"""
