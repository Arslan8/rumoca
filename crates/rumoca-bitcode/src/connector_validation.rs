//! Public scalar-port contracts. SPEC_0022 CONN-001/002/003/005/008/026
//! (MLS 9.2) require compatible members, potential equality and signed flow
//! conservation. These checks belong at the untrusted artifact boundary, not
//! only in an authoring helper. They do not infer physical intent from names.
mod laws;
mod linear;

use crate::schema::*;
use std::collections::{BTreeMap, BTreeSet};

type Result<T> = std::result::Result<T, String>;

pub(crate) fn validate(model: &RbcModel) -> Result<()> {
    check_types(model)?;
    let mut ports = BTreeMap::new();
    let mut variables = BTreeSet::new();
    for (index, port) in model.connectors.iter().enumerate() {
        check_port(model, index, port, &mut variables)?;
        if ports.insert(port.path.as_str(), port).is_some() {
            return Err(format!("duplicate connector path {}", port.path));
        }
    }
    if !model.connectors.is_empty() || !model.connector_types.is_empty() {
        let membership = check_membership(model)?;
        check_coverage(model, &variables, &membership)?;
        laws::check(model, &ports, &membership)?;
    }
    Ok(())
}

fn check_types(model: &RbcModel) -> Result<()> {
    for (index, ty) in model.connector_types.iter().enumerate() {
        if ty.id as usize != index
            || ty.flow_convention != "positive_into_owner"
            || ty.members.is_empty()
        {
            return Err(format!(
                "connector type {index}: ID, flow convention or members invalid"
            ));
        }
        let mut names = BTreeSet::new();
        for member in &ty.members {
            if member.name.is_empty()
                || !names.insert(&member.name)
                || member.scalar_type != "real"
                || member.kind == RbcQuantityKind::Stream
            {
                return Err(format!(
                    "connector type {index}: unsupported/duplicate member"
                ));
            }
        }
    }
    Ok(())
}

fn check_port(
    model: &RbcModel,
    index: usize,
    port: &RbcConnectorInstance,
    variables: &mut BTreeSet<VariableId>,
) -> Result<()> {
    let ty = model
        .connector_types
        .get(port.type_id as usize)
        .ok_or("missing connector type")?;
    let owner = model
        .components
        .get(port.owner.0 as usize)
        .ok_or("missing connector owner")?;
    if port.id as usize != index
        || !port.path.starts_with(&format!("{}.", owner.path))
        || !matches!(port.orientation.as_str(), "inside" | "outside")
        || port.members.len() != ty.members.len()
        || model
            .sources
            .get(port.provenance.span.source.0 as usize)
            .is_none()
    {
        return Err(format!(
            "connector {index}: identity/ownership/orientation/provenance invalid"
        ));
    }
    for (field, binding) in ty.members.iter().zip(&port.members) {
        check_member(model, port, field, binding, variables)?;
    }
    Ok(())
}

fn check_member(
    model: &RbcModel,
    port: &RbcConnectorInstance,
    field: &RbcConnectorField,
    binding: &RbcConnectorFieldBinding,
    variables: &mut BTreeSet<VariableId>,
) -> Result<()> {
    let v = model
        .variables
        .get(binding.variable.0 as usize)
        .ok_or("missing connector member variable")?;
    let ty = model
        .types
        .get(v.value_type.0 as usize)
        .ok_or("missing member type")?;
    if field.name != binding.name
        || field.kind != binding.kind
        || !variables.insert(binding.variable)
        || v.component != Some(port.owner)
        || ty.scalar != RbcScalar::Real
        || !ty.dimensions.is_empty()
        || v.scalar_count != 1
        || !matches!(
            v.role,
            RbcRole::Algebraic | RbcRole::State | RbcRole::Output
        )
        || !matches!(v.causality, RbcCausality::Local | RbcCausality::Output)
        || v.unit.as_deref().unwrap_or("") != field.unit
        || v.physical_quantity.as_deref().unwrap_or("") != field.quantity
        || v.connector.as_ref().map(|c| c.quantity) != Some(field.kind)
    {
        return Err(format!(
            "connector {}: member {} disagrees with declaration",
            port.id, field.name
        ));
    }
    Ok(())
}

fn check_membership(model: &RbcModel) -> Result<BTreeMap<&str, usize>> {
    let mut membership = BTreeMap::new();
    for (index, set) in model.connection_sets.iter().enumerate() {
        if set.connectors.is_empty() {
            return Err(format!("connection set {index}: empty membership"));
        }
        for path in &set.connectors {
            if membership.insert(path.as_str(), index).is_some() {
                return Err(format!(
                    "connector {path}: duplicate or overlapping finalized connection sets"
                ));
            }
        }
    }
    Ok(membership)
}

fn check_coverage(
    model: &RbcModel,
    variables: &BTreeSet<VariableId>,
    membership: &BTreeMap<&str, usize>,
) -> Result<()> {
    for v in &model.variables {
        if v.connector.is_some() && !variables.contains(&v.id) {
            return Err(format!(
                "connector variable {} has no complete port declaration",
                v.id
            ));
        }
    }
    for port in &model.connectors {
        let connected = membership.contains_key(port.path.as_str());
        for member in &port.members {
            let flags = model.variables[member.variable.0 as usize]
                .connector
                .as_ref();
            if flags.is_none_or(|flags| flags.connected != connected) {
                return Err(format!(
                    "connector {}: connected flag disagrees with set membership",
                    port.path
                ));
            }
        }
    }
    Ok(())
}

fn compatible(a: &RbcConnectorType, b: &RbcConnectorType) -> bool {
    a.flow_convention == b.flow_convention
        && a.members.len() == b.members.len()
        && a.members.iter().zip(&b.members).all(|(a, b)| {
            a.name == b.name
                && a.kind == b.kind
                && a.scalar_type == b.scalar_type
                && a.unit == b.unit
                && a.quantity == b.quantity
        })
}
