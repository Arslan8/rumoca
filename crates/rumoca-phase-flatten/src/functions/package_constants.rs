//! Bind enclosing package constants in an inherited callable's exposure.
//!
//! MLS §5.3 and §7.2: the declaration identity of an inherited constant stays
//! the same, while each package exposure has its own effective modification.
//! Substitute against that exact exposure before declaration-only constant
//! folding can discard it. No rendered path participates in value selection.

use indexmap::IndexMap;
use rumoca_core::{
    ClassType, DefId, Expression, FallibleExpressionRewriter, FallibleStatementRewriter, Function,
    Literal, Reference, Span, Subscript, Variability,
};
use rumoca_ir_ast as ast;
use rustc_hash::FxHashSet;

use super::FunctionRequest;
use crate::{FlattenError, ast_lower};

pub(super) fn specialize_package_constants(
    tree: &ast::ClassTree,
    index: &ast::ClassDefIndex<'_>,
    request: &FunctionRequest,
    function: &mut Function,
) -> Result<(), FlattenError> {
    let owner = request
        .component_ref
        .as_ref()
        .and_then(|reference| reference.parts().iter().rev().nth(1))
        .map(|part| part.def_id)
        .or_else(|| function.def_id.and_then(|id| index.parent_def_id(id)));
    let Some(package) = owner.and_then(|id| index.get(id)) else {
        return Ok(());
    };
    if package.class_type != ClassType::Package {
        return Ok(());
    }
    let mut bindings = IndexMap::new();
    collect_bindings(index, package, &mut bindings, &mut FxHashSet::default());
    let mut rewriter = PackageConstants {
        owner: package.def_id,
        bindings,
        intrinsics: ast_lower::PredefinedIntrinsicIds::from_tree(tree),
        expanding: Vec::new(),
    };
    for parameter in function
        .inputs
        .iter_mut()
        .chain(&mut function.outputs)
        .chain(&mut function.locals)
    {
        if let Some(default) = &mut parameter.default {
            *default = rewriter.rewrite_expression(default)?;
        }
        parameter.shape_expr = rewriter.rewrite_subscripts(&parameter.shape_expr)?;
        crate::postprocess::materialize_literal_parameter_shape(parameter)?;
    }
    function.body = rewriter.rewrite_statements(&function.body)?;
    Ok(())
}

fn collect_bindings<'tree>(
    index: &ast::ClassDefIndex<'tree>,
    package: &'tree ast::ClassDef,
    bindings: &mut IndexMap<DefId, &'tree ast::Expression>,
    visiting: &mut FxHashSet<DefId>,
) {
    let Some(package_id) = package.def_id.filter(|id| visiting.insert(*id)) else {
        return;
    };
    for extend in &package.extends {
        if let Some(base) = extend.base_def_id.and_then(|id| index.get(id)) {
            collect_bindings(index, base, bindings, visiting);
        }
        for modification in extend.modifications.iter().filter(|m| !m.redeclare) {
            if let ast::Expression::Modification { target, value, .. } = &modification.expr
                && let Some(id) = target.target_def_id()
            {
                bindings.insert(id, value);
            }
        }
    }
    for component in package.components.values() {
        if matches!(component.variability, Variability::Constant(_))
            && let Some(id) = component.def_id
            && let Some(binding) = &component.binding
        {
            bindings.insert(id, binding);
        }
    }
    visiting.remove(&package_id);
}

struct PackageConstants<'tree> {
    owner: Option<DefId>,
    bindings: IndexMap<DefId, &'tree ast::Expression>,
    intrinsics: ast_lower::PredefinedIntrinsicIds,
    expanding: Vec<DefId>,
}

impl FallibleExpressionRewriter for PackageConstants<'_> {
    type Error = FlattenError;

    fn rewrite_var_ref_expression(
        &mut self,
        name: &Reference,
        subscripts: &[Subscript],
        span: Span,
    ) -> Result<Expression, Self::Error> {
        // An explicitly qualified reference to a different package keeps that
        // package's value even when both packages inherit the same declaration.
        if name
            .component_ref()
            .and_then(|reference| reference.parts().iter().rev().nth(1))
            .is_some_and(|part| Some(part.def_id) != self.owner)
        {
            return self.walk_var_ref_expression(name, subscripts, span);
        }
        let Some((id, binding)) = name
            .target_def_id()
            .and_then(|id| self.bindings.get(&id).map(|binding| (id, *binding)))
        else {
            return self.walk_var_ref_expression(name, subscripts, span);
        };
        if self.expanding.contains(&id) {
            return Err(FlattenError::cyclic_constant_binding(
                name.as_str(),
                format!("package constant declaration {id:?} depends on itself"),
                span,
            ));
        }
        let lowered = ast_lower::expression_from_ast_with_intrinsics(binding, self.intrinsics)?;
        self.expanding.push(id);
        let result = self.rewrite_expression(&lowered);
        self.expanding.pop();
        let value = fold_scalar_constant(result?.with_span(span), span);
        let subscripts = self.rewrite_subscripts(subscripts)?;
        if subscripts.is_empty() {
            Ok(value)
        } else {
            Ok(Expression::Index {
                base: Box::new(value),
                subscripts,
                span,
            })
        }
    }
}

impl FallibleStatementRewriter for PackageConstants<'_> {}

fn fold_scalar_constant(expression: Expression, span: Span) -> Expression {
    use rumoca_eval_flat::constant::{EvalContext, Value, eval_expr};
    // In particular, dimensions such as size(substanceNames, 1) must become
    // literal integers before a constant fill/zeros reaches checked DAE.
    let value = match eval_expr(&expression, &EvalContext::new()) {
        Ok(Value::Integer(value)) => Literal::Integer(value),
        Ok(Value::Real(value)) if value.is_finite() => Literal::Real(value),
        Ok(Value::Bool(value)) => Literal::Boolean(value),
        Ok(Value::String(value)) => Literal::String(value),
        _ => return expression,
    };
    Expression::Literal { value, span }
}
