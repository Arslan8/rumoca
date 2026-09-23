use crate::schema::*;
use std::collections::BTreeSet;

pub(crate) fn validate(model: &RbcModel) -> Result<(), String> {
    for (i, t) in model.connector_types.iter().enumerate() {
        if t.id as usize != i || t.flow_convention != "positive_into_owner" || t.members.is_empty()
        {
            return Err(format!(
                "connector type {i}: ID, flow convention or members invalid"
            ));
        }
        let mut names = BTreeSet::new();
        for member in &t.members {
            if !names.insert(&member.name)
                || member.scalar_type != "real"
                || member.kind == RbcQuantityKind::Stream
            {
                return Err(format!("connector type {i}: unsupported/duplicate member"));
            }
        }
    }
    let mut paths = BTreeSet::new();
    let mut variables = BTreeSet::new();
    for (i, c) in model.connectors.iter().enumerate() {
        let ty = model
            .connector_types
            .get(c.type_id as usize)
            .ok_or("missing connector type")?;
        let owner = model
            .components
            .get(c.owner.0 as usize)
            .ok_or("missing connector owner")?;
        if c.id as usize != i
            || !paths.insert(&c.path)
            || !c.path.starts_with(&format!("{}.", owner.path))
            || !matches!(c.orientation.as_str(), "inside" | "outside")
            || c.members.len() != ty.members.len()
            || model
                .sources
                .get(c.provenance.span.source.0 as usize)
                .is_none()
        {
            return Err(format!(
                "connector {i}: identity/ownership/orientation/provenance invalid"
            ));
        }
        for (field, binding) in ty.members.iter().zip(&c.members) {
            let v = model
                .variables
                .get(binding.variable.0 as usize)
                .ok_or("missing connector member variable")?;
            let vt = model
                .types
                .get(v.value_type.0 as usize)
                .ok_or("missing member type")?;
            if field.name != binding.name
                || field.kind != binding.kind
                || !variables.insert(binding.variable.0)
                || v.component != Some(c.owner)
                || vt.scalar != RbcScalar::Real
                || !vt.dimensions.is_empty()
                || v.unit.as_deref().unwrap_or("") != field.unit
                || v.connector.as_ref().map(|c| c.quantity) != Some(field.kind)
            {
                return Err(format!(
                    "connector {i}: member {} disagrees with declaration",
                    field.name
                ));
            }
        }
    }
    Ok(())
}
