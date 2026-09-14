//! Rumoca Bitcode v1 → checked DAE.
//!
//! Import is deliberately *not* a deserializer that fills in structs. It runs
//! [`crate::validate`] first, then rebuilds the model by issuing the DAE's own
//! checked construction operations. Every one of the DAE's construction
//! invariants therefore applies to imported bitcode exactly as it applies to a
//! freshly compiled model — an artifact that has been through an untrusted
//! external pass cannot produce an invalid DAE, only a rejection.
//!
//! # Source text
//!
//! DAE provenance is checked against the source map: a span must lie inside
//! its file and on character boundaries. An artifact exported with
//! `embed_sources` round-trips exactly. One exported without it is still
//! importable — filler of the required length is synthesised so spans stay
//! valid — but `source_text()` then returns filler rather than the original
//! program. Export embeds sources by default for this reason.

use rumoca_core::{SourceMap, Span};
use rumoca_ir_dae as dae;

use crate::schema::*;
use crate::validate::{ValidateOptions, ValidationError, validate};

#[derive(Debug, thiserror::Error)]
pub enum ImportError {
    #[error("bitcode failed validation:\n{}", .0.iter().map(|error| format!("  - {error}")).collect::<Vec<_>>().join("\n"))]
    Invalid(Vec<ValidationError>),
    /// The DAE's checked constructors refused this artifact.
    ///
    /// The message is rendered rather than typed: `DaeConstructionError` is an
    /// internal type, and exposing it here would make the compiler's error
    /// taxonomy part of this crate's public API.
    #[error("cannot rebuild a checked DAE from this bitcode: {0}")]
    Construction(String),
    #[error("{0}")]
    Unsupported(String),
}

/// Validate an artifact and rebuild a checked DAE from it.
pub fn import(file: &RbcFile) -> Result<dae::Dae, ImportError> {
    file.check_header().map_err(ImportError::Unsupported)?;
    let model = &file.model;

    validate(
        model,
        &ValidateOptions {
            // A model containing a node the schema could not represent cannot be
            // faithfully rebuilt, so import refuses it rather than silently
            // dropping behaviour.
            reject_unsupported: true,
        },
    )
    .map_err(ImportError::Invalid)?;

    let (source_map, sources) = rebuild_source_map(model);

    let detail = std::cell::RefCell::new(None);
    let dae = dae::Dae::construct(source_map, |construction| {
        rebuild(construction, model, &sources, &detail)
    })
    .map_err(|error| match detail.into_inner() {
        Some(message) => ImportError::Unsupported(message),
        None => ImportError::Construction(error.to_string()),
    })?;
    Ok(dae)
}

/// Rebuild a source map whose ids match what the spans will reference.
///
/// `SourceId` is derived from the file name, so re-adding by name reproduces
/// the original identity. Returns the map plus the RBC-index → `SourceId`
/// translation.
fn rebuild_source_map(model: &RbcModel) -> (SourceMap, Vec<rumoca_core::SourceId>) {
    // A span must fit inside its file, so a source without embedded text needs
    // filler at least as long as the furthest offset that references it.
    let mut needed = vec![0usize; model.sources.len()];
    let mut note = |span: RbcSpan| {
        let slot = span.source.0 as usize;
        if let Some(entry) = needed.get_mut(slot) {
            *entry = (*entry).max(span.end as usize);
        }
    };
    for variable in &model.variables {
        note(variable.declaration.span);
    }
    for expression in &model.expressions {
        note(expression.provenance.span);
    }
    for equation in model.equations.iter().chain(&model.initial_equations) {
        note(equation.provenance.span);
    }
    for relation in &model.relations {
        note(relation.provenance.span);
    }
    for condition in &model.conditions {
        note(condition.provenance.span);
    }
    for root in &model.roots {
        note(root.provenance.span);
    }
    for event in &model.events {
        note(event.provenance.span);
    }
    for event in &model.time_events {
        note(event.provenance.span);
    }
    for connection in &model.connections {
        note(connection.provenance.span);
    }

    let mut map = SourceMap::new();
    let mut ids = Vec::with_capacity(model.sources.len());
    for (index, source) in model.sources.iter().enumerate() {
        let text = match &source.text {
            Some(text) if text.len() >= needed[index] => text.clone(),
            // ASCII filler keeps every offset on a character boundary.
            _ => " ".repeat(needed[index]),
        };
        ids.push(map.add(&source.name, &text));
    }
    (map, ids)
}

fn span_of(span: RbcSpan, sources: &[rumoca_core::SourceId]) -> Span {
    let source = sources
        .get(span.source.0 as usize)
        .copied()
        .unwrap_or_default();
    Span {
        source,
        start: rumoca_core::BytePos(span.start as usize),
        end: rumoca_core::BytePos(span.end as usize),
    }
}

fn provenance_of(
    provenance: RbcProvenance,
    sources: &[rumoca_core::SourceId],
) -> Result<dae::DaeProvenance, ImportError> {
    let span = span_of(provenance.span, sources);
    let result = match provenance.origin {
        RbcOrigin::Source => dae::DaeProvenance::source(span),
        RbcOrigin::Generated { generation } => {
            dae::DaeProvenance::generated(generation_of(generation)?, span)
        }
    };
    result.map_err(|error| ImportError::Construction(error.to_string()))
}

fn generation_of(generation: RbcGeneration) -> Result<dae::DaeGeneration, ImportError> {
    use RbcGeneration as R;
    Ok(match generation {
        R::SyntheticResidual => dae::DaeGeneration::SyntheticResidual,
        R::BindingEquation => dae::DaeGeneration::BindingEquation,
        R::ConnectionEquation => dae::DaeGeneration::ConnectionEquation,
        R::FlowBalanceEquation => dae::DaeGeneration::FlowBalanceEquation,
        R::AlgorithmEquation => dae::DaeGeneration::AlgorithmEquation,
        R::DiscreteUpdate => dae::DaeGeneration::DiscreteUpdate,
        R::ConditionLowering => dae::DaeGeneration::ConditionLowering,
        R::PreValueLowering => dae::DaeGeneration::PreValueLowering,
        R::ClockLowering => dae::DaeGeneration::ClockLowering,
        R::DelayLowering => dae::DaeGeneration::DelayLowering,
        R::SemiLinearLowering => dae::DaeGeneration::SemiLinearLowering,
        R::TerminalLowering => dae::DaeGeneration::TerminalLowering,
        R::EventActionLowering => dae::DaeGeneration::EventActionLowering,
        R::InitializationEquation => dae::DaeGeneration::InitializationEquation,
        R::DefaultStart => dae::DaeGeneration::DefaultStart,
        R::ArrayEquationProjection => dae::DaeGeneration::ArrayEquationProjection,
        R::RecordEquationProjection => dae::DaeGeneration::RecordEquationProjection,
        R::FunctionLoopLowering => dae::DaeGeneration::FunctionLoopLowering,
        R::FunctionConditionLowering => dae::DaeGeneration::FunctionConditionLowering,
        R::FunctionAggregateLowering => dae::DaeGeneration::FunctionAggregateLowering,
        R::DerivedParameterLowering => dae::DaeGeneration::DerivedParameterLowering,
        R::IndexReduction => dae::DaeGeneration::IndexReduction,
        R::AliasElimination => dae::DaeGeneration::AliasElimination,
        R::RuntimeDiscontinuity => dae::DaeGeneration::RuntimeDiscontinuity,
        R::Other => {
            return Err(ImportError::Unsupported(
                "bitcode names a lowering kind this build does not know".to_string(),
            ));
        }
    })
}

/// Issue the construction operations that rebuild the model.
///
/// Order matters and is forced by the IR: variables are *reserved* before
/// expressions (so a coordinate can name one), then *defined* afterwards (so an
/// attribute can name an expression). This mirrors how the compiler's own
/// lowering resolves the same circularity.
/// Shared inputs every rebuild stage needs.
struct Rebuild<'a> {
    model: &'a RbcModel,
    sources: &'a [rumoca_core::SourceId],
    /// The construction closure may only return `DaeConstructionError`, whose
    /// `MalformedWire` carries a `&'static str`. Richer messages are recorded
    /// here so `import` can surface them instead of the bare variant.
    detail: &'a std::cell::RefCell<Option<String>>,
}

impl Rebuild<'_> {
    fn unsupported(&self, message: impl Into<String>) -> dae::DaeConstructionError {
        self.detail.borrow_mut().get_or_insert(message.into());
        dae::DaeConstructionError::MalformedWire {
            column: "rumoca bitcode",
        }
    }

    fn provenance(
        &self,
        provenance: RbcProvenance,
    ) -> Result<dae::DaeProvenance, dae::DaeConstructionError> {
        provenance_of(provenance, self.sources).map_err(|error| self.unsupported(error.to_string()))
    }
}

/// Resolve an id against a table built by an earlier stage.
fn resolve<T: Copy>(
    table: &[T],
    index: u32,
    what: &'static str,
    ctx: &Rebuild<'_>,
) -> Result<T, dae::DaeConstructionError> {
    table
        .get(index as usize)
        .copied()
        .ok_or_else(|| ctx.unsupported(format!("{what} {index} is not defined")))
}

/// Issue the construction operations that rebuild the model.
///
/// Order is forced by the IR: variables are *reserved* before expressions (so a
/// coordinate can name one), then *defined* afterwards (so an attribute can name
/// an expression). This mirrors how the compiler's own lowering resolves the
/// same circularity.
fn rebuild(
    construction: &mut dae::DaeConstruction<'_>,
    model: &RbcModel,
    sources: &[rumoca_core::SourceId],
    detail: &std::cell::RefCell<Option<String>>,
) -> Result<(), dae::DaeConstructionError> {
    let ctx = Rebuild {
        model,
        sources,
        detail,
    };
    let types = rebuild_types(construction, &ctx)?;
    let (variables, reservations) = reserve_variables(construction, &ctx, &types)?;
    let expressions = rebuild_expressions(construction, &ctx, &variables)?;
    define_variables(construction, &ctx, &expressions, reservations)?;
    let conditions = rebuild_conditions(construction, &ctx, &expressions)?;
    rebuild_equations(construction, &ctx, &expressions)?;
    rebuild_events(construction, &ctx, &expressions, &variables, &conditions)
}

fn rebuild_types<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
) -> Result<Vec<dae::ValueTypeId<'dae>>, dae::DaeConstructionError> {
    // Every checked object needs source-backed provenance, including a value
    // type. Any object in the artifact anchors it equally well.
    let anchor = ctx
        .model
        .variables
        .first()
        .map(|variable| variable.declaration)
        .or_else(|| ctx.model.expressions.first().map(|e| e.provenance))
        .ok_or_else(|| ctx.unsupported("bitcode has no object to anchor type provenance"))?;
    let anchor = ctx.provenance(anchor)?;

    let mut types = Vec::with_capacity(ctx.model.types.len());
    construction.types(|owner| {
        for ty in &ctx.model.types {
            let scalar = scalar_of(ty.scalar);
            let value_type = if ty.dimensions.is_empty() {
                dae::ValueType::scalar(scalar)
            } else {
                dae::ValueType::array(scalar, ty.dimensions.clone())
            };
            types.push(owner.derived(value_type, anchor)?);
        }
        Ok(())
    })?;
    Ok(types)
}

type Reservations<'dae> = Vec<dae::VariableReservation<'dae>>;

fn reserve_variables<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    types: &[dae::ValueTypeId<'dae>],
) -> Result<(Vec<VariableSlot<'dae>>, Reservations<'dae>), dae::DaeConstructionError> {
    let mut slots = Vec::with_capacity(ctx.model.variables.len());
    let mut reservations = Vec::with_capacity(ctx.model.variables.len());
    construction.variables(|owner| {
        for variable in &ctx.model.variables {
            let name = rumoca_core::VarName::intern(&variable.name);
            let ty = resolve(types, variable.value_type.0, "type", ctx)?;
            let at = ctx.provenance(variable.declaration)?;
            let (slot, reservation) = match variable.role {
                RbcRole::Parameter => {
                    let (id, r) = owner.reserve_parameter(name, ty, at)?;
                    (VariableSlot::Parameter(id), r)
                }
                RbcRole::Constant => {
                    let (id, r) = owner.reserve_constant(name, ty, at)?;
                    (VariableSlot::Parameter(id), r)
                }
                RbcRole::Input => {
                    let (id, r) =
                        owner.reserve_input(name, ty, dae::InputVariability::Continuous, at)?;
                    (VariableSlot::Input(id), r)
                }
                RbcRole::State => {
                    let (id, r) = owner.reserve_state(name, ty, at)?;
                    (VariableSlot::State(id), r)
                }
                RbcRole::Algebraic => {
                    let (id, r) = owner.reserve_algebraic(name, ty, at)?;
                    (VariableSlot::Algebraic(id), r)
                }
                RbcRole::Output => {
                    let (id, r) = owner.reserve_output(name, ty, at)?;
                    (VariableSlot::Algebraic(id), r)
                }
                RbcRole::DiscreteReal => {
                    let (id, r) = owner.reserve_discrete_real(name, ty, at)?;
                    (VariableSlot::DiscreteReal(id), r)
                }
                RbcRole::DiscreteValue => {
                    let (id, r) = owner.reserve_discrete_value(name, ty, at)?;
                    (VariableSlot::DiscreteValue(id), r)
                }
            };
            slots.push(slot);
            reservations.push(reservation);
        }
        Ok(())
    })?;
    Ok((slots, reservations))
}

fn rebuild_expressions<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    variables: &[VariableSlot<'dae>],
) -> Result<Vec<dae::ExprId<'dae>>, dae::DaeConstructionError> {
    let mut built: Vec<dae::ExprId<'dae>> = Vec::with_capacity(ctx.model.expressions.len());
    construction.expressions(|owner| {
        for expression in &ctx.model.expressions {
            // Validation already proved operands reference strictly earlier
            // nodes, so one forward pass suffices.
            let at = ctx.provenance(expression.provenance)?;
            let node = build_expression(owner, ctx, expression, &built, variables, at)?;
            built.push(node);
        }
        Ok(())
    })?;
    Ok(built)
}

fn build_expression<'dae>(
    owner: &mut dae::Expressions<'_, 'dae>,
    ctx: &Rebuild<'_>,
    expression: &RbcExpr,
    built: &[dae::ExprId<'dae>],
    variables: &[VariableSlot<'dae>],
    at: dae::DaeProvenance,
) -> Result<dae::ExprId<'dae>, dae::DaeConstructionError> {
    Ok(match &expression.node {
        RbcExprNode::Literal { value } => owner.at(at).literal(literal_of(value))?,
        RbcExprNode::Coordinate { coordinate } => {
            let input = coordinate_of(*coordinate, variables)
                .ok_or_else(|| ctx.unsupported("coordinate names an unknown variable"))?;
            owner.at(at).coordinate(input)?
        }
        RbcExprNode::Unary { op, operand } => {
            let operand = resolve(built, operand.0, "expression", ctx)?;
            owner.at(at).unary(unary_of(*op), operand)?
        }
        RbcExprNode::Binary { op, lhs, rhs } => {
            let lhs = resolve(built, lhs.0, "expression", ctx)?;
            let rhs = resolve(built, rhs.0, "expression", ctx)?;
            owner.at(at).binary(binary_of(*op), lhs, rhs)?
        }
        RbcExprNode::Conditional { branches, fallback } => {
            let mut arms = Vec::with_capacity(branches.len());
            for branch in branches {
                let condition = resolve(built, branch.condition.0, "expression", ctx)?;
                let value = resolve(built, branch.value.0, "expression", ctx)?;
                arms.push((condition, value));
            }
            let fallback = resolve(built, fallback.0, "expression", ctx)?;
            owner.at(at).conditional(arms, fallback)?
        }
        RbcExprNode::Unsupported { detail } => {
            return Err(ctx.unsupported(format!(
                "expression {} is unsupported: {detail}",
                expression.id
            )));
        }
    })
}

fn define_variables<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    expressions: &[dae::ExprId<'dae>],
    reservations: Reservations<'dae>,
) -> Result<(), dae::DaeConstructionError> {
    construction.variables(|owner| {
        for (variable, reservation) in ctx.model.variables.iter().zip(reservations) {
            let at = ctx.provenance(variable.declaration)?;
            let attribute = |id: Option<ExprId>| match id {
                Some(id) => resolve(expressions, id.0, "expression", ctx).map(Some),
                None => Ok(None),
            };
            let attributes = dae::VariableAttributes {
                causality: causality_of(variable.causality),
                unit: variable.unit.clone(),
                description: variable.description.clone(),
                fixed: variable.fixed,
                is_tunable: variable.tunable,
                origin: if variable.from_source {
                    dae::VariableOrigin::Source
                } else {
                    dae::VariableOrigin::Generated
                },
                binding: attribute(variable.binding)?,
                start: attribute(variable.start)?,
                min: attribute(variable.min)?,
                max: attribute(variable.max)?,
                nominal: attribute(variable.nominal)?,
                ..Default::default()
            };
            owner.define(reservation, attributes, at)?;
        }
        Ok(())
    })
}

fn rebuild_conditions<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    expressions: &[dae::ExprId<'dae>],
) -> Result<Vec<dae::ConditionId<'dae>>, dae::DaeConstructionError> {
    let mut relations = Vec::with_capacity(ctx.model.relations.len());
    let mut conditions = Vec::with_capacity(ctx.model.conditions.len());
    construction.conditions(|owner| {
        for relation in &ctx.model.relations {
            let at = ctx.provenance(relation.provenance)?;
            let expression = resolve(expressions, relation.expression.0, "expression", ctx)?;
            relations.push(owner.relation(expression, at)?);
        }
        // Reserve every condition first: the boolean algebra is a DAG over
        // earlier conditions, and reservation lets the second pass name them.
        for condition in &ctx.model.conditions {
            let at = ctx.provenance(condition.provenance)?;
            conditions.push(owner.reserve(at)?);
        }
        for (condition, id) in ctx.model.conditions.iter().zip(&conditions) {
            let at = ctx.provenance(condition.provenance)?;
            let input = condition_input(ctx, condition, &relations, &conditions, expressions)?;
            owner.define(*id, input, at)?;
        }
        for root in &ctx.model.roots {
            let at = ctx.provenance(root.provenance)?;
            let relation = resolve(&relations, root.relation.0, "relation", ctx)?;
            let activation = resolve(&conditions, root.activation.0, "condition", ctx)?;
            owner.root(relation, activation, at)?;
        }
        Ok(())
    })?;
    Ok(conditions)
}

fn condition_input<'dae>(
    ctx: &Rebuild<'_>,
    condition: &RbcCondition,
    relations: &[dae::RelationId<'dae>],
    conditions: &[dae::ConditionId<'dae>],
    expressions: &[dae::ExprId<'dae>],
) -> Result<dae::ConditionInput<'dae>, dae::DaeConstructionError> {
    let inner = |id: ConditionId| resolve(conditions, id.0, "condition", ctx);
    Ok(match &condition.node {
        RbcConditionNode::Initial => dae::ConditionInput::Initial,
        RbcConditionNode::Always => dae::ConditionInput::Always,
        RbcConditionNode::Relation { relation } => {
            dae::ConditionInput::Relation(resolve(relations, relation.0, "relation", ctx)?)
        }
        RbcConditionNode::Discrete { expression } => {
            dae::ConditionInput::Discrete(resolve(expressions, expression.0, "expression", ctx)?)
        }
        RbcConditionNode::Not { operand } => dae::ConditionInput::Not(inner(*operand)?),
        RbcConditionNode::And { lhs, rhs } => dae::ConditionInput::And(inner(*lhs)?, inner(*rhs)?),
        RbcConditionNode::Or { lhs, rhs } => dae::ConditionInput::Or(inner(*lhs)?, inner(*rhs)?),
        RbcConditionNode::AnyRise { lhs, rhs } => {
            dae::ConditionInput::AnyRise(inner(*lhs)?, inner(*rhs)?)
        }
        RbcConditionNode::Clock => {
            return Err(ctx.unsupported("clocked conditions are not supported by bitcode v1"));
        }
        RbcConditionNode::Unsupported { detail } => {
            return Err(ctx.unsupported(format!("unsupported condition: {detail}")));
        }
    })
}

fn rebuild_equations<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    expressions: &[dae::ExprId<'dae>],
) -> Result<(), dae::DaeConstructionError> {
    construction.continuous(|owner| {
        for equation in &ctx.model.equations {
            let at = ctx.provenance(equation.provenance)?;
            let residual = resolve(expressions, equation.residual.0, "expression", ctx)?;
            owner.equation(at, |body| body.residual(residual))?;
        }
        Ok(())
    })?;
    construction.initialization(|owner| {
        for equation in &ctx.model.initial_equations {
            let at = ctx.provenance(equation.provenance)?;
            let residual = resolve(expressions, equation.residual.0, "expression", ctx)?;
            owner.equation(at, |body| body.residual(residual))?;
        }
        Ok(())
    })
}

fn rebuild_events<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    expressions: &[dae::ExprId<'dae>],
    variables: &[VariableSlot<'dae>],
    conditions: &[dae::ConditionId<'dae>],
) -> Result<(), dae::DaeConstructionError> {
    construction.events(|owner| {
        for event in &ctx.model.events {
            let at = ctx.provenance(event.provenance)?;
            let trigger = resolve(conditions, event.trigger.0, "condition", ctx)?;
            let guard = resolve(conditions, event.guard.0, "condition", ctx)?;
            rebuild_action(
                owner,
                ctx,
                event,
                expressions,
                variables,
                trigger,
                guard,
                at,
            )?;
        }
        Ok(())
    })
}

#[allow(clippy::too_many_arguments)]
fn rebuild_action<'dae>(
    owner: &mut dae::Events<'_, 'dae>,
    ctx: &Rebuild<'_>,
    event: &RbcEventAction,
    expressions: &[dae::ExprId<'dae>],
    variables: &[VariableSlot<'dae>],
    trigger: dae::ConditionId<'dae>,
    guard: dae::ConditionId<'dae>,
    at: dae::DaeProvenance,
) -> Result<(), dae::DaeConstructionError> {
    let expression = |id: ExprId| resolve(expressions, id.0, "expression", ctx);
    match &event.action {
        RbcAction::Reinitialize { state, value } => {
            let state = reinit_state(ctx, variables, *state)?;
            owner.reinitialize(trigger, guard, state, expression(*value)?, at)?;
        }
        RbcAction::Assert { message, level } => {
            let message = expression(*message)?;
            let level = match level {
                Some(level) => Some(expression(*level)?),
                None => None,
            };
            owner.assert_with_level(trigger, guard, message, level, at)?;
        }
        RbcAction::Terminate { message } => {
            owner.terminate(trigger, guard, expression(*message)?, at)?;
        }
    }
    Ok(())
}

/// `reinit` may only target a continuous state; anything else is a rejection,
/// not a coercion.
fn reinit_state<'dae>(
    ctx: &Rebuild<'_>,
    variables: &[VariableSlot<'dae>],
    state: VariableId,
) -> Result<dae::StateId<'dae>, dae::DaeConstructionError> {
    match resolve(variables, state.0, "variable", ctx)? {
        VariableSlot::State(state) => Ok(state),
        _ => Err(ctx.unsupported("reinit target is not a state")),
    }
}

/// Which typed id a variable slot holds. RBC uses one variable id space; the
/// DAE uses role-specific ids over the same index, so this keeps the mapping
/// explicit rather than casting between them.
#[derive(Clone, Copy)]
enum VariableSlot<'dae> {
    Parameter(dae::ParameterId<'dae>),
    Input(dae::InputId<'dae>),
    State(dae::StateId<'dae>),
    Algebraic(dae::AlgebraicId<'dae>),
    DiscreteReal(dae::DiscreteRealId<'dae>),
    DiscreteValue(dae::DiscreteValueId<'dae>),
}

fn coordinate_of<'dae>(
    coordinate: RbcCoordinate,
    variables: &[VariableSlot<'dae>],
) -> Option<dae::CoordinateInput<'dae>> {
    let slot = |id: VariableId| variables.get(id.0 as usize).copied();
    Some(match coordinate {
        RbcCoordinate::Time => dae::CoordinateInput::Time,
        RbcCoordinate::Parameter { variable } => match slot(variable)? {
            VariableSlot::Parameter(id) => dae::CoordinateInput::Parameter(id),
            _ => return None,
        },
        RbcCoordinate::Input { variable } => match slot(variable)? {
            VariableSlot::Input(id) => dae::CoordinateInput::Input(id),
            _ => return None,
        },
        RbcCoordinate::State { variable } => match slot(variable)? {
            VariableSlot::State(id) => dae::CoordinateInput::State(id),
            _ => return None,
        },
        RbcCoordinate::Derivative { variable } => match slot(variable)? {
            VariableSlot::State(id) => dae::CoordinateInput::Derivative(id),
            _ => return None,
        },
        RbcCoordinate::PreState { variable } => match slot(variable)? {
            VariableSlot::State(id) => dae::CoordinateInput::PreState(id),
            _ => return None,
        },
        RbcCoordinate::Algebraic { variable } => match slot(variable)? {
            VariableSlot::Algebraic(id) => dae::CoordinateInput::Algebraic(id),
            _ => return None,
        },
        RbcCoordinate::PreAlgebraic { variable } => match slot(variable)? {
            VariableSlot::Algebraic(id) => dae::CoordinateInput::PreAlgebraic(id),
            _ => return None,
        },
        RbcCoordinate::DiscreteReal { variable } => match slot(variable)? {
            VariableSlot::DiscreteReal(id) => dae::CoordinateInput::DiscreteReal(id),
            _ => return None,
        },
        RbcCoordinate::PreDiscreteReal { variable } => match slot(variable)? {
            VariableSlot::DiscreteReal(id) => dae::CoordinateInput::PreDiscreteReal(id),
            _ => return None,
        },
        RbcCoordinate::DiscreteValue { variable } => match slot(variable)? {
            VariableSlot::DiscreteValue(id) => dae::CoordinateInput::DiscreteValue(id),
            _ => return None,
        },
        RbcCoordinate::PreDiscreteValue { variable } => match slot(variable)? {
            VariableSlot::DiscreteValue(id) => dae::CoordinateInput::PreDiscreteValue(id),
            _ => return None,
        },
    })
}

fn scalar_of(scalar: RbcScalar) -> dae::ScalarType {
    match scalar {
        RbcScalar::Real => dae::ScalarType::Real,
        RbcScalar::Integer => dae::ScalarType::Integer,
        RbcScalar::Boolean => dae::ScalarType::Boolean,
        RbcScalar::String => dae::ScalarType::String,
        RbcScalar::Enumeration => dae::ScalarType::Enumeration,
    }
}

fn literal_of(literal: &RbcLiteral) -> dae::DaeLiteral {
    match literal {
        RbcLiteral::Real { value } => dae::DaeLiteral::Real(*value),
        RbcLiteral::Integer { value } => dae::DaeLiteral::Integer(*value),
        RbcLiteral::Boolean { value } => dae::DaeLiteral::Boolean(*value),
        RbcLiteral::String { value } => dae::DaeLiteral::String(value.clone()),
    }
}

fn unary_of(op: RbcUnaryOp) -> dae::UnaryOperator {
    match op {
        RbcUnaryOp::Negate => dae::UnaryOperator::Negate,
        RbcUnaryOp::Not => dae::UnaryOperator::Not,
    }
}

fn binary_of(op: RbcBinaryOp) -> dae::BinaryOperator {
    match op {
        RbcBinaryOp::Add => dae::BinaryOperator::Add,
        RbcBinaryOp::Subtract => dae::BinaryOperator::Subtract,
        RbcBinaryOp::Multiply => dae::BinaryOperator::Multiply,
        RbcBinaryOp::Divide => dae::BinaryOperator::Divide,
        RbcBinaryOp::Power => dae::BinaryOperator::Power,
        RbcBinaryOp::Equal => dae::BinaryOperator::Equal,
        RbcBinaryOp::NotEqual => dae::BinaryOperator::NotEqual,
        RbcBinaryOp::Less => dae::BinaryOperator::Less,
        RbcBinaryOp::LessEqual => dae::BinaryOperator::LessEqual,
        RbcBinaryOp::Greater => dae::BinaryOperator::Greater,
        RbcBinaryOp::GreaterEqual => dae::BinaryOperator::GreaterEqual,
        RbcBinaryOp::And => dae::BinaryOperator::And,
        RbcBinaryOp::Or => dae::BinaryOperator::Or,
    }
}

fn causality_of(causality: RbcCausality) -> dae::VariableCausality {
    match causality {
        RbcCausality::Input => dae::VariableCausality::Input,
        RbcCausality::Output => dae::VariableCausality::Output,
        RbcCausality::Parameter => dae::VariableCausality::Parameter,
        RbcCausality::CalculatedParameter => dae::VariableCausality::CalculatedParameter,
        RbcCausality::Independent => dae::VariableCausality::Independent,
        RbcCausality::Local => dae::VariableCausality::Local,
    }
}
