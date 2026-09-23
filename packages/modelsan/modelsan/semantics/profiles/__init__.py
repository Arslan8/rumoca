"""Application profiles: rules written against semantic roles.

A profile is not a domain. `physical/domains/` holds what physics says about a
quantity, which the model's own metadata can usually establish. A profile holds
what an *application* says about an object — a wheel radius, a state of charge,
a supply air temperature — which the metadata usually cannot, and which the
binder therefore resolves from the declaring class or from the user.

Selecting a profile says only that these rules are relevant. It does not say
which variable is the vehicle speed; that still needs a binding.
"""

from .automotive import PACK as AUTOMOTIVE_PACK

#: Profiles are opt-in by name, unlike `physical/domains/` which is always on.
BUILTIN_PROFILES = {"automotive": AUTOMOTIVE_PACK}


def profile_packs(names) -> list:
    """Packs for the named profiles, ignoring names nobody registered."""
    return [BUILTIN_PROFILES[n] for n in (names or ()) if n in BUILTIN_PROFILES]


__all__ = ["AUTOMOTIVE_PACK", "BUILTIN_PROFILES", "profile_packs"]
