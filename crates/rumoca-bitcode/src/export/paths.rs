//! Recovering instance structure from flattened variable paths.
//!
//! Flattening reduces a component to a prefix on a name, so the only way back
//! to "which class declared this" is the declaring-class map plus a split of
//! the path. Both live here rather than in `export.rs`: this is the boundary
//! where flat text becomes structure again, and it should have one owner.

use std::collections::BTreeMap;

use rumoca_ir_flat as flat;

/// The class each top-level instance is of, from Flat's declaring-class map.
///
/// Taken from a variable the instance declares *directly*: `L.L` is declared
/// by `Analog.Basic.Inductor`, where `L.n.v` is declared by `NegativePin`. A
/// connector's own class is recovered the same way one level down.
pub(super) fn component_classes(flat: Option<&flat::Model>) -> BTreeMap<String, String> {
    let mut found: BTreeMap<String, BTreeMap<String, usize>> = BTreeMap::new();
    let Some(flat) = flat else {
        return BTreeMap::new();
    };
    for (name, class) in flat.variable_declaring_classes.iter() {
        let text = name.as_str();
        let Some((owner, leaf)) = split_owner(text) else {
            continue;
        };
        if leaf.is_empty() || owner.is_empty() {
            continue;
        }
        *found
            .entry(owner.to_string())
            .or_default()
            .entry(class.clone())
            .or_default() += 1;
    }
    found
        .into_iter()
        .filter_map(|(owner, classes)| {
            // An instance's variables agree on their declaring class except
            // where one is inherited from a base; the commonest wins, and ties
            // break on the name so the artifact stays deterministic.
            let best = classes
                .into_iter()
                .max_by(|left, right| left.1.cmp(&right.1).then(right.0.cmp(&left.0)))?;
            Some((owner, best.0))
        })
        .collect()
}

pub(super) fn connector_path(member: &str) -> &str {
    split_owner(member).map_or(member, |(path, _)| path)
}

/// `"battery.pin.v"` → `("battery.pin", "v")`. The one place this file takes a
/// flattened path apart, so the boundary operation has a named owner rather
/// than being open-coded wherever a prefix is wanted.
///
/// Delegates to the shared splitter rather than calling `rsplit_once`: a raw
/// split also cuts at a dot inside a subscript, so `a[i.j].v` came apart in
/// the wrong place. `split_last_top_level` only cuts at bracket depth zero.
pub(super) fn split_owner(path: &str) -> Option<(&str, &str)> {
    rumoca_core::split_last_top_level(path)
}
