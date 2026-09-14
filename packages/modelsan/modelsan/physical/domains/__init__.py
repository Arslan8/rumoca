"""Domain rule packs. Each is independent; the engine imports none of them."""

from . import battery, electrical, fluid, mechanical, thermal

#: Packs loaded by default. Extending this list, or registering a pack from
#: outside the package, is the whole cost of adding a physical domain.
BUILTIN = (electrical.PACK, mechanical.PACK, thermal.PACK, fluid.PACK, battery.PACK)

__all__ = ["BUILTIN", "battery", "electrical", "fluid", "mechanical", "thermal"]
