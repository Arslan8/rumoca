"""Semantic binding: deciding what a model object *represents*.

PhysicalSan matches rules to variables. Matching on units and the declared
`quantity` recovers broad physical semantics cheaply and automatically, and
that remains the first level. It is not always enough:

    Ohm    -> resistance-like, but passive resistor or negative-impedance
              converter? Only the declaring class says.
    rad/s  -> angular velocity, but a wheel, a motor shaft or a fan? Usually
              nothing in the model says, and the user must.

So semantics are bound from several sources in priority order, every binding
records where it came from, and the result is a first-class artifact rather
than a detail of one sanitizer.

    RBC model
        |
        v
    SemanticBinder ── user > component type > connector > quantity > unit > heuristic
        |
        v
    SemanticMap ── bindings, conflicts, ambiguities
        |
        v
    PhysicalSan rules, written against roles
"""

from .binder import SemanticBinder
from .binding import (
    Ambiguity,
    BindingConflict,
    BindingSource,
    SemanticBinding,
    WEAK_SOURCES,
)
from .catalog import ClassCatalog, ClassSemantics, builtin_catalog
from .config import SemanticConfig
from .map import SemanticMap
from .providers import (
    ComponentTypeProvider,
    ConnectorProvider,
    NameHeuristicProvider,
    QuantityProvider,
    SemanticProvider,
    UserDeclarationProvider,
    UserProvider,
)
from .role import SemanticRole


def bind_semantics(model, *, config=None, user_mappings=None, catalog=None,
                   heuristics: bool = False, attach: bool = True) -> SemanticMap:
    """Bind `model` and, by default, attach the result as `model.semantics`.

    The map is a reusable artifact, not a private detail of PhysicalSan.
    Connector logging, differential analysis, fault injection, model slicing
    and runtime monitoring all need the same question answered — *what does
    this object represent* — and none of them should have to re-derive it:

        bind_semantics(model, config=SemanticConfig.load("semantics.toml"))
        model.semantics.get("automotive.vehicle_speed")

    Attaching is opt-out rather than mandatory so a caller comparing two
    bindings of the same model is not forced to mutate it.
    """
    mappings = dict(user_mappings or {})
    origin = "inline"
    if config is not None:
        mappings.update(config.mappings)
        origin = config.origin
    found = SemanticBinder(catalog=catalog, user_mappings=mappings,
                           origin=origin, heuristics=heuristics).bind(model)
    if attach:
        try:
            model.semantics = found
        except AttributeError:
            # A model type that forbids new attributes still gets the map back;
            # only the convenience spelling is unavailable.
            pass
    return found

__all__ = [
    "Ambiguity", "BindingConflict", "BindingSource", "ClassCatalog",
    "ClassSemantics", "ComponentTypeProvider", "ConnectorProvider",
    "NameHeuristicProvider", "QuantityProvider", "SemanticBinder",
    "SemanticBinding", "SemanticConfig", "SemanticMap", "SemanticProvider",
    "SemanticRole", "UserDeclarationProvider",
    "UserProvider", "WEAK_SOURCES", "bind_semantics",
    "builtin_catalog",
]
