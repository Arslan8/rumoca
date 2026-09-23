# Found by the parameter probe + SolverSan

Implemented in `packages/modelsan/modelsan/sanitizers/solver.py`.

the parameter probe + SolverSan sets one parameter to a suspect value, runs the model, and reports a solver or initialization failure that the declared values do not produce.

**1 instances.**

| ID | Tier | Kind | Target | Model or file |
|---|---|---|---|---|
| [BUG-026](../BUG-elasticbearing-idealgear-ratio.md) | confirmed | `solver-failure` | `idealGear.ratio` | `Modelica.Mechanics.Rotational.Examples.ElasticBearing` |
