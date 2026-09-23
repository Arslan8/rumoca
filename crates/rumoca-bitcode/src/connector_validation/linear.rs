//! Bounded, exact proof of additive connection laws, never numeric sampling.
//! Only scalar Real coordinates, zero, add/subtract and unary negate are
//! admitted. Other forms fail closed for connection-owned equations. This is
//! not a general simplifier and does not evaluate parameter-dependent factors.
use super::Result;
use crate::schema::*;
use std::collections::{BTreeMap, BTreeSet};

pub(super) type Form = BTreeMap<VariableId, i64>;

pub(super) struct Proofs(BTreeMap<ExprId, Option<Form>>);

impl Proofs {
    pub(super) fn new(model: &RbcModel, roots: impl Iterator<Item = ExprId>) -> Result<Self> {
        let mut required = BTreeSet::new();
        let mut stack: Vec<_> = roots.collect();
        while let Some(id) = stack.pop() {
            if !required.insert(id) {
                continue;
            }
            if required.len() > 100_000 {
                return Err("connection law proof exceeds 100000 nodes".into());
            }
            let expr = model
                .expressions
                .get(id.0 as usize)
                .ok_or("connection law references missing expression")?;
            let children = operands(&expr.node);
            if children.iter().any(|operand| operand.0 >= id.0) {
                return Err("connection law expression is cyclic/non-topological".into());
            }
            stack.extend(children);
        }
        let mut proofs = Self(BTreeMap::new());
        let mut entries = 0usize;
        for id in required {
            let form = proofs.compute(model, &model.expressions[id.0 as usize]);
            entries += form.as_ref().map_or(0, BTreeMap::len);
            if entries > 1_000_000 {
                return Err("connection law proof exceeds 1000000 coefficients".into());
            }
            proofs.0.insert(id, form);
        }
        Ok(proofs)
    }

    pub(super) fn get(&self, id: ExprId) -> Result<&Form> {
        self.0
            .get(&id)
            .and_then(Option::as_ref)
            .ok_or_else(|| "connection law requires a provable scalar additive equation".into())
    }

    fn compute(&self, model: &RbcModel, expr: &RbcExpr) -> Option<Form> {
        let ty = model.types.get(expr.value_type.0 as usize)?;
        if ty.scalar != RbcScalar::Real || !ty.dimensions.is_empty() {
            return None;
        }
        let get = |id| self.0.get(&id).and_then(Option::as_ref).cloned();
        match &expr.node {
            RbcExprNode::Literal {
                value: RbcLiteral::Real { value },
            } if *value == 0.0 => Some(Form::new()),
            RbcExprNode::Coordinate { coordinate } => {
                let variable = coordinate.variable()?;
                let role = model.variables.get(variable.0 as usize)?.role;
                let correct_role = match coordinate {
                    RbcCoordinate::Algebraic { .. } => {
                        matches!(role, RbcRole::Algebraic | RbcRole::Output)
                    }
                    RbcCoordinate::State { .. } => role == RbcRole::State,
                    _ => false,
                };
                correct_role.then(|| BTreeMap::from([(variable, 1)]))
            }
            RbcExprNode::Unary {
                op: RbcUnaryOp::Negate,
                operand,
            } => combine(Form::new(), get(*operand)?, -1),
            RbcExprNode::Binary {
                op: RbcBinaryOp::Add,
                lhs,
                rhs,
            } => combine(get(*lhs)?, get(*rhs)?, 1),
            RbcExprNode::Binary {
                op: RbcBinaryOp::Subtract,
                lhs,
                rhs,
            } => combine(get(*lhs)?, get(*rhs)?, -1),
            _ => None,
        }
    }
}

fn operands(node: &RbcExprNode) -> Vec<ExprId> {
    match node {
        RbcExprNode::Unary {
            op: RbcUnaryOp::Negate,
            operand,
        } => vec![*operand],
        RbcExprNode::Binary {
            op: RbcBinaryOp::Add | RbcBinaryOp::Subtract,
            lhs,
            rhs,
        } => vec![*lhs, *rhs],
        _ => vec![],
    }
}

fn combine(mut a: Form, b: Form, sign: i64) -> Option<Form> {
    for (variable, coefficient) in b {
        let entry = a.entry(variable).or_default();
        *entry = entry.checked_add(coefficient.checked_mul(sign)?)?;
    }
    a.retain(|_, value| *value != 0);
    (a.len() <= 4096).then_some(a)
}

pub(super) fn same_law(actual: &Form, expected: &Form) -> bool {
    actual == expected
        || (actual.len() == expected.len()
            && actual.iter().all(|(v, c)| {
                c.checked_neg()
                    .is_some_and(|neg| expected.get(v) == Some(&neg))
            }))
}
