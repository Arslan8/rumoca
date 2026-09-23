use super::{
    Result, compatible,
    linear::{Form, Proofs},
};
use crate::schema::*;
use std::collections::{BTreeMap, BTreeSet};

pub(super) fn check(
    model: &RbcModel,
    ports: &BTreeMap<&str, &RbcConnectorInstance>,
    membership: &BTreeMap<&str, usize>,
) -> Result<()> {
    let mut owned = BTreeMap::new();
    for (index, set) in model.connection_sets.iter().enumerate() {
        for equation in set
            .potential_equations
            .iter()
            .copied()
            .chain(set.balances.iter().filter_map(|b| b.equation))
        {
            if model.equations.get(equation.0 as usize).is_none() {
                return Err("missing connection equation".into());
            }
            if owned.insert(equation, index).is_some() {
                return Err("connection equation has duplicate ownership".into());
            }
        }
    }
    let proofs = Proofs::new(
        model,
        owned
            .keys()
            .map(|id| model.equations[id.0 as usize].residual),
    )?;
    for (index, set) in model.connection_sets.iter().enumerate() {
        check_set(model, set, ports, &proofs)
            .map_err(|e| format!("connection set {index}: {e}"))?;
    }
    check_edges(model, ports, membership, &owned, &proofs)?;
    for eq in &model.equations {
        if matches!(
            eq.provenance.origin,
            RbcOrigin::Generated {
                generation: RbcGeneration::ConnectionEquation | RbcGeneration::FlowBalanceEquation
            }
        ) && !owned.contains_key(&eq.id)
        {
            return Err(format!(
                "unowned generated boundary/connection equation {}",
                eq.id
            ));
        }
    }
    Ok(())
}

fn check_set(
    model: &RbcModel,
    set: &RbcConnectionSet,
    ports: &BTreeMap<&str, &RbcConnectorInstance>,
    proofs: &Proofs,
) -> Result<()> {
    if set.unconnected != (set.connectors.len() == 1) {
        return Err("unconnected flag disagrees with singleton boundary".into());
    }
    if model
        .sources
        .get(set.provenance.span.source.0 as usize)
        .is_none()
    {
        return Err("missing connection-set provenance source".into());
    }
    let members: Vec<_> = set
        .connectors
        .iter()
        .map(|path| {
            ports
                .get(path.as_str())
                .copied()
                .ok_or_else(|| format!("connector {path} lacks a complete port declaration"))
        })
        .collect::<Result<_>>()?;
    let prototype = &model.connector_types[members[0].type_id as usize];
    if members
        .iter()
        .any(|p| !compatible(prototype, &model.connector_types[p.type_id as usize]))
    {
        return Err("connection set types differ (member/type/unit/quantity/flow contract)".into());
    }
    let mut potentials = Vec::new();
    let mut flows = Vec::new();
    for (index, field) in prototype.members.iter().enumerate() {
        let ids: Vec<_> = members.iter().map(|p| p.members[index].variable).collect();
        match field.kind {
            RbcQuantityKind::Potential => potentials.push(ids),
            RbcQuantityKind::Flow => flows.push(
                members
                    .iter()
                    .zip(ids)
                    .map(|(p, id)| (id, if p.orientation == "inside" { -1 } else { 1 }))
                    .collect::<Form>(),
            ),
            RbcQuantityKind::Stream => return Err("unsupported stream connector".into()),
        }
    }
    check_potentials(model, set, &potentials, proofs)?;
    check_flows(model, set, &flows, proofs)
}

fn equation<'a>(model: &RbcModel, proofs: &'a Proofs, id: EquationId) -> Result<&'a Form> {
    let eq = model
        .equations
        .get(id.0 as usize)
        .ok_or("missing connection equation")?;
    proofs.get(eq.residual)
}

fn check_flows(
    model: &RbcModel,
    set: &RbcConnectionSet,
    expected: &[Form],
    proofs: &Proofs,
) -> Result<()> {
    if set.balances.len() != expected.len() {
        return Err("missing/extra flow balance".into());
    }
    let mut matched = BTreeSet::new();
    for balance in &set.balances {
        let terms: Form = balance
            .terms
            .iter()
            .map(|t| (t.variable, if t.negated { -1 } else { 1 }))
            .collect();
        if terms.len() != balance.terms.len() {
            return Err("duplicate flow member".into());
        }
        let index = expected
            .iter()
            .position(|e| *e == terms)
            .ok_or("flow members/signs disagree with port orientation")?;
        if !matched.insert(index) {
            return Err("duplicate flow field balance".into());
        }
        let id = balance.equation.ok_or("flow balance lacks an equation")?;
        if !super::linear::same_law(equation(model, proofs, id)?, &terms) {
            return Err(format!(
                "flow equation {id} does not implement declared conservation law"
            ));
        }
    }
    Ok(())
}

fn check_potentials(
    model: &RbcModel,
    set: &RbcConnectionSet,
    groups: &[Vec<VariableId>],
    proofs: &Proofs,
) -> Result<()> {
    let all: BTreeSet<_> = groups.iter().flatten().copied().collect();
    if all != set.potentials.iter().copied().collect() || all.len() != set.potentials.len() {
        return Err("potential members differ from declared ports".into());
    }
    let count: usize = groups.iter().map(|g| g.len() - 1).sum();
    if set.potential_equations.len() != count {
        return Err("missing/extra potential equality equation".into());
    }
    let mut adjacency: BTreeMap<VariableId, Vec<VariableId>> = BTreeMap::new();
    for id in &set.potential_equations {
        let law = equation(model, proofs, *id)?;
        let pair: Vec<_> = law.iter().collect();
        if pair.len() != 2 || !matches!((*pair[0].1, *pair[1].1), (1, -1) | (-1, 1)) {
            return Err(format!("potential equation {id} is not a member equality"));
        }
        let (a, b) = (*pair[0].0, *pair[1].0);
        if !groups.iter().any(|g| g.contains(&a) && g.contains(&b)) {
            return Err("potential equality joins different fields or undeclared members".into());
        }
        adjacency.entry(a).or_default().push(b);
        adjacency.entry(b).or_default().push(a);
    }
    for group in groups {
        let mut seen = BTreeSet::new();
        let mut stack = vec![group[0]];
        while let Some(v) = stack.pop() {
            if seen.insert(v) {
                stack.extend(adjacency.get(&v).into_iter().flatten().copied());
            }
        }
        if seen.len() != group.len() {
            return Err(
                "potential equalities do not span every port (duplicate/cyclic/missing edge)"
                    .into(),
            );
        }
    }
    Ok(())
}

fn check_edges(
    model: &RbcModel,
    ports: &BTreeMap<&str, &RbcConnectorInstance>,
    membership: &BTreeMap<&str, usize>,
    owned: &BTreeMap<EquationId, usize>,
    proofs: &Proofs,
) -> Result<()> {
    for edge in &model.connections {
        let left = ports
            .get(edge.left_connector.as_str())
            .ok_or("connection edge lacks left port declaration")?;
        let right = ports
            .get(edge.right_connector.as_str())
            .ok_or("connection edge lacks right port declaration")?;
        let a = left
            .members
            .iter()
            .position(|m| m.variable == edge.left && m.kind == edge.quantity);
        let b = right
            .members
            .iter()
            .position(|m| m.variable == edge.right && m.kind == edge.quantity);
        let set = membership.get(left.path.as_str());
        if a.is_none() || a != b || set.is_none() || set != membership.get(right.path.as_str()) {
            return Err("connection edge disagrees with declared members/set membership".into());
        }
        if let Some(id) = edge.equation {
            if edge.left == edge.right {
                return Err("connection self-edge cannot claim a nontrivial set equation".into());
            }
            if owned.get(&id) != set {
                return Err("connection edge equation is not owned by its set".into());
            }
            let law = equation(model, proofs, id)?;
            if !law.contains_key(&edge.left) || !law.contains_key(&edge.right) {
                return Err("connection edge equation does not connect its endpoints".into());
            }
        }
    }
    Ok(())
}
