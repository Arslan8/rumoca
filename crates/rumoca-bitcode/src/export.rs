//! DAE → Rumoca Bitcode v1.
//!
//! The exporter reads the checked DAE through `Dae::inspect` and, optionally,
//! the Flat model for connector provenance the DAE does not retain. It writes
//! only public schema types: no internal identity, lifetime brand, or wire
//! record crosses this boundary.
//!
//! Dependency edges on each equation are computed here, using the compiler's
//! own scalar coordinate projection, so a consumer never has to re-derive them
//! by walking expressions.

use std::collections::BTreeMap;

use rumoca_core::{Span, text_position};
use rumoca_ir_dae as dae;
use rumoca_ir_flat as flat;

use crate::schema::*;

#[derive(Debug, thiserror::Error)]
pub enum ExportError {
    #[error("expression {0} references operand {1}, which is not yet defined")]
    ForwardOperand(u32, u32),
    #[error("dependency projection failed: {0}")]
    Projection(String),
}

/// What to include in the artifact.
///
/// Non-exhaustive: construct with `..ExportOptions::default()` so a future
/// option does not break callers.
#[derive(Debug, Clone)]
#[non_exhaustive]
pub struct ExportOptions {
    /// Embed full source text, making the artifact self-contained.
    pub embed_sources: bool,
    /// Emit `Unsupported` nodes for expression forms this schema version does
    /// not model, instead of failing. Off by default: a silent placeholder is
    /// worse than a refusal.
    pub tolerate_unsupported: bool,
    /// Compute per-equation dependency edges. Costs one projection pass.
    pub dependency_edges: bool,
}

impl Default for ExportOptions {
    fn default() -> Self {
        Self {
            embed_sources: true,
            tolerate_unsupported: true,
            dependency_edges: true,
        }
    }
}

/// Export a compiled model.
///
/// `flat` is optional. Without it the artifact has no `connections` and no
/// connector classification on variables, because the DAE does not retain them.
pub fn export(
    model: &dae::Dae,
    flat: Option<&flat::Model>,
    model_name: &str,
    options: &ExportOptions,
) -> Result<RbcFile, ExportError> {
    let rbc = model.inspect(|view| build(view, model, flat, model_name, options))?;
    Ok(RbcFile {
        magic: RBC_MAGIC.to_string(),
        bitcode_version: RBC_VERSION,
        producer: format!("rumoca {}", env!("CARGO_PKG_VERSION")),
        model: rbc,
    })
}

struct Ctx<'a> {
    /// Maps a `rumoca_core::SourceId` (a name-derived hash) to a dense RBC id.
    sources: BTreeMap<u64, SourceId>,
    /// Source text by RBC source id, for line/column resolution.
    texts: Vec<String>,
    names: Vec<String>,
    source_map: &'a rumoca_core::SourceMap,
}

impl Ctx<'_> {
    fn span(&mut self, span: Span) -> RbcSpan {
        let raw = span.source.0;
        let source = *self.sources.entry(raw).or_insert_with(|| {
            let id = SourceId(self.names.len() as u32);
            let (name, text) = self
                .source_map
                .get_source(span.source)
                .map(|(name, text)| (name.to_string(), text.to_string()))
                .unwrap_or_else(|| (format!("<unknown:{raw}>"), String::new()));
            self.names.push(name);
            self.texts.push(text);
            id
        });
        let start = span.start.0 as u32;
        let end = span.end.0 as u32;
        let text = &self.texts[source.0 as usize];
        let (line, column) = if text.is_empty() || start as usize > text.len() {
            (0, 0)
        } else {
            let position = text_position::byte_offset_to_position(text, start as usize);
            // RBC reports 1-based positions; TextPosition is 0-based.
            (position.line + 1, position.character + 1)
        };
        RbcSpan {
            source,
            start,
            end,
            line,
            column,
        }
    }

    fn provenance(&mut self, provenance: dae::DaeProvenance) -> RbcProvenance {
        RbcProvenance {
            origin: match provenance.origin() {
                dae::DaeProvenanceOrigin::Source => RbcOrigin::Source,
                dae::DaeProvenanceOrigin::Generated(generation) => RbcOrigin::Generated {
                    generation: generation_of(generation),
                },
            },
            span: self.span(provenance.span()),
        }
    }
}

fn generation_of(generation: dae::DaeGeneration) -> RbcGeneration {
    use dae::DaeGeneration as G;
    match generation {
        G::SyntheticResidual => RbcGeneration::SyntheticResidual,
        G::BindingEquation => RbcGeneration::BindingEquation,
        G::ConnectionEquation => RbcGeneration::ConnectionEquation,
        G::FlowBalanceEquation => RbcGeneration::FlowBalanceEquation,
        G::AlgorithmEquation => RbcGeneration::AlgorithmEquation,
        G::DiscreteUpdate => RbcGeneration::DiscreteUpdate,
        G::ConditionLowering => RbcGeneration::ConditionLowering,
        G::PreValueLowering => RbcGeneration::PreValueLowering,
        G::ClockLowering => RbcGeneration::ClockLowering,
        G::DelayLowering => RbcGeneration::DelayLowering,
        G::SemiLinearLowering => RbcGeneration::SemiLinearLowering,
        G::TerminalLowering => RbcGeneration::TerminalLowering,
        G::EventActionLowering => RbcGeneration::EventActionLowering,
        G::InitializationEquation => RbcGeneration::InitializationEquation,
        G::DefaultStart => RbcGeneration::DefaultStart,
        G::ArrayEquationProjection => RbcGeneration::ArrayEquationProjection,
        G::RecordEquationProjection => RbcGeneration::RecordEquationProjection,
        G::FunctionLoopLowering => RbcGeneration::FunctionLoopLowering,
        G::FunctionConditionLowering => RbcGeneration::FunctionConditionLowering,
        G::FunctionAggregateLowering => RbcGeneration::FunctionAggregateLowering,
        G::DerivedParameterLowering => RbcGeneration::DerivedParameterLowering,
        G::IndexReduction => RbcGeneration::IndexReduction,
        G::AliasElimination => RbcGeneration::AliasElimination,
        G::RuntimeDiscontinuity => RbcGeneration::RuntimeDiscontinuity,
    }
}

fn build(
    view: dae::DaeView<'_>,
    model: &dae::Dae,
    flat: Option<&flat::Model>,
    model_name: &str,
    options: &ExportOptions,
) -> Result<RbcModel, ExportError> {
    let mut ctx = Ctx {
        sources: BTreeMap::new(),
        texts: Vec::new(),
        names: Vec::new(),
        source_map: model.source_map(),
    };

    let types = export_types(view, &mut ctx);
    let expressions = export_expressions(view, &mut ctx, options)?;
    let (components, component_of) = export_components(view);
    let variables = export_variables(view, &mut ctx, flat, &component_of);
    let equations = export_equations(view, &mut ctx, options, EquationKind::Continuous)?;
    let initial_equations = export_equations(view, &mut ctx, options, EquationKind::Initial)?;
    let relations = export_relations(view, &mut ctx);
    let conditions = export_conditions(view, &mut ctx);
    let roots = export_roots(view, &mut ctx);
    let events = export_events(view, &mut ctx);
    let discrete_definitions = export_discrete_definitions(view, &mut ctx);
    let time_events = export_time_events(view, &mut ctx)?;
    let connections = export_connections(flat, &variables, &equations, &mut ctx);

    let sources = ctx
        .names
        .iter()
        .enumerate()
        .map(|(index, name)| RbcSource {
            id: SourceId(index as u32),
            name: name.clone(),
            text: options
                .embed_sources
                .then(|| ctx.texts[index].clone())
                .filter(|text| !text.is_empty()),
        })
        .collect();

    let summary = summarize(
        &variables,
        &expressions,
        &equations,
        &initial_equations,
        &relations,
        &conditions,
        &roots,
        &events,
        &time_events,
        &discrete_definitions,
        &connections,
        &components,
    );

    Ok(RbcModel {
        name: model_name.to_string(),
        sources,
        types,
        variables,
        expressions,
        equations,
        initial_equations,
        relations,
        conditions,
        roots,
        events,
        time_events,
        discrete_definitions,
        connections,
        components,
        trace_points: Vec::new(),
        summary,
    })
}

fn export_types(view: dae::DaeView<'_>, ctx: &mut Ctx<'_>) -> Vec<RbcType> {
    (0..view.value_type_count())
        .filter_map(|index| {
            let id = view.value_type_id(index)?;
            let ty = view.value_type(id)?;
            let _ = ctx;
            Some(RbcType {
                id: TypeId(index as u32),
                scalar: scalar_of(ty),
                dimensions: ty.dimensions().to_vec(),
            })
        })
        .collect()
}

fn scalar_of(ty: &dae::ValueType) -> RbcScalar {
    if ty.is_record() {
        // v1 has no record type; report the field-free shape rather than lie
        // about the scalar kind.
        return RbcScalar::String;
    }
    match ty.scalar_type() {
        dae::ScalarType::Real => RbcScalar::Real,
        dae::ScalarType::Integer => RbcScalar::Integer,
        dae::ScalarType::Boolean => RbcScalar::Boolean,
        dae::ScalarType::String => RbcScalar::String,
        dae::ScalarType::Enumeration => RbcScalar::Enumeration,
        dae::ScalarType::Record => RbcScalar::String,
    }
}

/// Derive component instances from flattened variable paths.
///
/// Name segmentation at a serialization boundary is explicitly permitted;
/// compiler-internal identity elsewhere uses `DefId`/`VarName`.
fn export_components(view: dae::DaeView<'_>) -> (Vec<RbcComponent>, BTreeMap<String, ComponentId>) {
    let mut paths = BTreeMap::new();
    for index in 0..view.variable_count() {
        let Some(id) = view.variable_id(index) else {
            continue;
        };
        let Some(variable) = view.variable(id) else {
            continue;
        };
        let name = variable.name().to_string();
        if let Some((component, _)) = name.split_once('.') {
            let next = ComponentId(paths.len() as u32);
            paths.entry(component.to_string()).or_insert(next);
        }
    }
    // Re-index densely in sorted order so output is deterministic.
    let mut components = Vec::new();
    let mut map = BTreeMap::new();
    for (index, path) in paths.keys().enumerate() {
        let id = ComponentId(index as u32);
        map.insert(path.clone(), id);
        components.push(RbcComponent {
            id,
            path: path.clone(),
        });
    }
    (components, map)
}

fn export_variables(
    view: dae::DaeView<'_>,
    ctx: &mut Ctx<'_>,
    flat: Option<&flat::Model>,
    component_of: &BTreeMap<String, ComponentId>,
) -> Vec<RbcVariable> {
    (0..view.variable_count())
        .filter_map(|index| {
            let id = view.variable_id(index)?;
            let variable = view.variable(id)?;
            let name = variable.name().to_string();
            let connector = flat.and_then(|flat| connector_member(flat, &name));
            let component = name
                .split_once('.')
                .and_then(|(prefix, _)| component_of.get(prefix).copied());
            Some(RbcVariable {
                id: VariableId(index as u32),
                role: role_of(variable.role()),
                causality: causality_of(variable.causality()),
                value_type: TypeId(variable.value_type_id().index()),
                scalar_count: variable.scalar_count() as u32,
                declaration: ctx.provenance(variable.declaration()),
                component,
                unit: variable.unit().map(str::to_string),
                physical_quantity: flat.and_then(|flat| physical_quantity(flat, &name)),
                description: variable.description().map(str::to_string),
                binding: variable.binding().map(|e| ExprId(e.index())),
                start: variable.start().map(|e| ExprId(e.index())),
                min: variable.minimum().map(|e| ExprId(e.index())),
                max: variable.maximum().map(|e| ExprId(e.index())),
                nominal: variable.nominal().map(|e| ExprId(e.index())),
                fixed: variable.fixed(),
                tunable: variable.is_tunable(),
                from_source: matches!(variable.origin(), dae::VariableOrigin::Source),
                connector,
                name,
            })
        })
        .collect()
}

/// Recover connector semantics for one flattened variable from the Flat model.
/// The declared `quantity` attribute, which the DAE does not carry but Flat does.
fn physical_quantity(flat: &flat::Model, name: &str) -> Option<String> {
    let interned = rumoca_core::VarName::intern(name);
    flat.variables.get(&interned)?.quantity.clone()
}

fn connector_member(flat: &flat::Model, name: &str) -> Option<RbcConnectorMember> {
    let interned = rumoca_core::VarName::intern(name);
    let variable = flat.variables.get(&interned)?;
    let quantity = if variable.stream {
        RbcQuantityKind::Stream
    } else if variable.flow {
        RbcQuantityKind::Flow
    } else if variable.connected {
        RbcQuantityKind::Potential
    } else {
        return None;
    };
    Some(RbcConnectorMember {
        quantity,
        connected: variable.connected,
    })
}

fn role_of(role: dae::VariableRole) -> RbcRole {
    match role {
        dae::VariableRole::Parameter => RbcRole::Parameter,
        dae::VariableRole::Constant => RbcRole::Constant,
        dae::VariableRole::Input => RbcRole::Input,
        dae::VariableRole::State => RbcRole::State,
        dae::VariableRole::Algebraic => RbcRole::Algebraic,
        dae::VariableRole::Output => RbcRole::Output,
        dae::VariableRole::DiscreteReal => RbcRole::DiscreteReal,
        dae::VariableRole::DiscreteValue => RbcRole::DiscreteValue,
    }
}

fn causality_of(causality: dae::VariableCausality) -> RbcCausality {
    match causality {
        dae::VariableCausality::Input => RbcCausality::Input,
        dae::VariableCausality::Output => RbcCausality::Output,
        dae::VariableCausality::Parameter => RbcCausality::Parameter,
        dae::VariableCausality::CalculatedParameter => RbcCausality::CalculatedParameter,
        dae::VariableCausality::Independent => RbcCausality::Independent,
        dae::VariableCausality::Local => RbcCausality::Local,
    }
}

fn export_expressions(
    view: dae::DaeView<'_>,
    ctx: &mut Ctx<'_>,
    options: &ExportOptions,
) -> Result<Vec<RbcExpr>, ExportError> {
    let mut out = Vec::with_capacity(view.expression_count());
    for index in 0..view.expression_count() {
        let Some(id) = view.expression_id(index) else {
            continue;
        };
        let Some(expression) = view.expression(id) else {
            continue;
        };
        let node = expression_node(expression, index as u32, options)?;
        out.push(RbcExpr {
            id: ExprId(index as u32),
            value_type: TypeId(expression.value_type_id().index()),
            node,
            provenance: ctx.provenance(expression.provenance()),
        });
    }
    Ok(out)
}

fn expression_node(
    expression: dae::ExpressionView<'_>,
    index: u32,
    options: &ExportOptions,
) -> Result<RbcExprNode, ExportError> {
    let check = |operand: dae::ExprId<'_>| -> Result<ExprId, ExportError> {
        if operand.index() >= index {
            return Err(ExportError::ForwardOperand(index, operand.index()));
        }
        Ok(ExprId(operand.index()))
    };
    let node = match expression.operation() {
        dae::ExpressionOperation::Literal(literal) => RbcExprNode::Literal {
            value: literal_of(literal),
        },
        dae::ExpressionOperation::Coordinate(coordinate) => match coordinate_of(coordinate) {
            Some(coordinate) => RbcExprNode::Coordinate { coordinate },
            None => unsupported("coordinate kind not in bitcode v1", options)?,
        },
        dae::ExpressionOperation::Unary { operator, operand } => match unary_of(operator) {
            Some(op) => RbcExprNode::Unary {
                op,
                operand: check(operand)?,
            },
            None => unsupported("unary operator not in bitcode v1", options)?,
        },
        dae::ExpressionOperation::Binary { operator, lhs, rhs } => match binary_of(operator) {
            Some(op) => RbcExprNode::Binary {
                op,
                lhs: check(lhs)?,
                rhs: check(rhs)?,
            },
            None => unsupported("binary operator not in bitcode v1", options)?,
        },
        dae::ExpressionOperation::Conditional(operands) => {
            // Packed as [cond, value, cond, value, ..., fallback]: an even
            // number of branch operands followed by the required fallback.
            let count = operands.len();
            if count == 0 || count % 2 == 0 {
                unsupported("malformed conditional operand packing", options)?
            } else {
                let mut branches = Vec::with_capacity(count / 2);
                for pair in 0..count / 2 {
                    let condition = operands
                        .get(pair * 2)
                        .ok_or_else(|| ExportError::Projection("conditional operand".into()))?;
                    let value = operands
                        .get(pair * 2 + 1)
                        .ok_or_else(|| ExportError::Projection("conditional operand".into()))?;
                    branches.push(RbcBranch {
                        condition: check(condition)?,
                        value: check(value)?,
                    });
                }
                let fallback = operands
                    .get(count - 1)
                    .ok_or_else(|| ExportError::Projection("conditional fallback".into()))?;
                RbcExprNode::Conditional {
                    branches,
                    fallback: check(fallback)?,
                }
            }
        }
        dae::ExpressionOperation::Builtin { builtin, arguments } => {
            let mut operands = Vec::with_capacity(arguments.len());
            for position in 0..arguments.len() {
                let argument = arguments
                    .get(position)
                    .ok_or_else(|| ExportError::Projection("builtin argument".into()))?;
                operands.push(check(argument)?);
            }
            RbcExprNode::Builtin {
                name: builtin_name(builtin).to_string(),
                arguments: operands,
            }
        }
        _ => unsupported("expression form not in bitcode v1", options)?,
    };
    Ok(node)
}

fn unsupported(detail: &str, options: &ExportOptions) -> Result<RbcExprNode, ExportError> {
    if options.tolerate_unsupported {
        Ok(RbcExprNode::Unsupported {
            detail: detail.to_string(),
        })
    } else {
        Err(ExportError::Projection(detail.to_string()))
    }
}

fn literal_of(literal: &dae::DaeLiteral) -> RbcLiteral {
    match literal {
        dae::DaeLiteral::Real(value) => RbcLiteral::Real { value: *value },
        dae::DaeLiteral::Integer(value) => RbcLiteral::Integer { value: *value },
        dae::DaeLiteral::Boolean(value) => RbcLiteral::Boolean { value: *value },
        dae::DaeLiteral::String(value) => RbcLiteral::String {
            value: value.to_string(),
        },
        dae::DaeLiteral::Enumeration(ordinal) => RbcLiteral::Enumeration { ordinal: *ordinal },
    }
}

fn coordinate_of(coordinate: dae::CoordinateView<'_>) -> Option<RbcCoordinate> {
    use dae::CoordinateView as C;
    let variable = |index: u32| VariableId(index);
    Some(match coordinate {
        C::Parameter(id) => RbcCoordinate::Parameter {
            variable: variable(id.index()),
        },
        C::Input(id) => RbcCoordinate::Input {
            variable: variable(id.index()),
        },
        C::State(id) => RbcCoordinate::State {
            variable: variable(id.index()),
        },
        C::Derivative(id) => RbcCoordinate::Derivative {
            variable: variable(id.index()),
        },
        C::Algebraic(id) => RbcCoordinate::Algebraic {
            variable: variable(id.index()),
        },
        C::DiscreteReal(id) => RbcCoordinate::DiscreteReal {
            variable: variable(id.index()),
        },
        C::DiscreteValue(id) => RbcCoordinate::DiscreteValue {
            variable: variable(id.index()),
        },
        C::PreState(id) => RbcCoordinate::PreState {
            variable: variable(id.index()),
        },
        C::PreAlgebraic(id) => RbcCoordinate::PreAlgebraic {
            variable: variable(id.index()),
        },
        C::PreDiscreteReal(id) => RbcCoordinate::PreDiscreteReal {
            variable: variable(id.index()),
        },
        C::PreDiscreteValue(id) => RbcCoordinate::PreDiscreteValue {
            variable: variable(id.index()),
        },
        C::Time => RbcCoordinate::Time,
        _ => return None,
    })
}

/// Modelica spelling of a pure built-in.
///
/// Names are the contract, not enum ordinals: a consumer matches `"sqrt"`, and
/// appending a variant upstream cannot silently change what an existing
/// artifact means.
fn builtin_name(builtin: dae::PureBuiltin) -> &'static str {
    use dae::PureBuiltin as B;
    match builtin {
        B::Abs => "abs",
        B::Sign => "sign",
        B::Sqrt => "sqrt",
        B::Div => "div",
        B::Mod => "mod",
        B::Rem => "rem",
        B::Floor => "floor",
        B::Ceil => "ceil",
        B::Integer => "integer",
        B::Sin => "sin",
        B::Cos => "cos",
        B::Tan => "tan",
        B::Asin => "asin",
        B::Acos => "acos",
        B::Atan => "atan",
        B::Atan2 => "atan2",
        B::Sinh => "sinh",
        B::Cosh => "cosh",
        B::Tanh => "tanh",
        B::Exp => "exp",
        B::Log => "log",
        B::Log10 => "log10",
        B::Smooth => "smooth",
        B::NoEvent => "noEvent",
        B::Homotopy => "homotopy",
        B::Min => "min",
        B::Max => "max",
        B::Sum => "sum",
        B::Product => "product",
        B::Size => "size",
        B::Zeros => "zeros",
        B::Ones => "ones",
        B::Fill => "fill",
        B::Linspace => "linspace",
        B::Cross => "cross",
        B::Identity => "identity",
        B::Vector => "vector",
        B::Transpose => "transpose",
        B::Diagonal => "diagonal",
        B::OuterProduct => "outerProduct",
        B::Skew => "skew",
        B::PromotedCat1 => "cat1",
        B::PromotedCat2 => "cat2",
    }
}

fn unary_of(operator: dae::UnaryOperator) -> Option<RbcUnaryOp> {
    match operator {
        dae::UnaryOperator::Negate => Some(RbcUnaryOp::Negate),
        dae::UnaryOperator::Not => Some(RbcUnaryOp::Not),
        _ => None,
    }
}

fn binary_of(operator: dae::BinaryOperator) -> Option<RbcBinaryOp> {
    use dae::BinaryOperator as B;
    Some(match operator {
        B::Add => RbcBinaryOp::Add,
        B::Subtract => RbcBinaryOp::Subtract,
        B::Multiply => RbcBinaryOp::Multiply,
        B::Divide => RbcBinaryOp::Divide,
        B::Power => RbcBinaryOp::Power,
        B::Equal => RbcBinaryOp::Equal,
        B::NotEqual => RbcBinaryOp::NotEqual,
        B::Less => RbcBinaryOp::Less,
        B::LessEqual => RbcBinaryOp::LessEqual,
        B::Greater => RbcBinaryOp::Greater,
        B::GreaterEqual => RbcBinaryOp::GreaterEqual,
        B::And => RbcBinaryOp::And,
        B::Or => RbcBinaryOp::Or,
        _ => return None,
    })
}

#[derive(Clone, Copy)]
enum EquationKind {
    Continuous,
    Initial,
}

fn export_equations(
    view: dae::DaeView<'_>,
    ctx: &mut Ctx<'_>,
    options: &ExportOptions,
    kind: EquationKind,
) -> Result<Vec<RbcEquation>, ExportError> {
    let count = match kind {
        EquationKind::Continuous => view.continuous_equation_count(),
        EquationKind::Initial => view.initialization_equation_count(),
    };
    let mut out = Vec::with_capacity(count);
    for index in 0..count {
        let equation = match kind {
            EquationKind::Continuous => view.continuous_equation(index),
            EquationKind::Initial => view.initialization_equation(index),
        };
        let Some(equation) = equation else { continue };
        let residual = equation.residual();
        let (reads, reads_derivative) = if options.dependency_edges {
            dependencies(view, residual)?
        } else {
            (Vec::new(), Vec::new())
        };
        out.push(RbcEquation {
            id: EquationId(index as u32),
            residual: ExprId(residual.index()),
            provenance: ctx.provenance(equation.provenance()),
            reads,
            reads_derivative,
        });
    }
    Ok(out)
}

/// Compute the variables one equation reads, using the compiler's own scalar
/// coordinate projection rather than a private expression walk.
fn dependencies<'dae>(
    view: dae::DaeView<'dae>,
    residual: dae::ExprId<'dae>,
) -> Result<(Vec<VariableId>, Vec<VariableId>), ExportError> {
    use std::collections::BTreeSet;
    let mut reads = BTreeSet::new();
    let mut derivatives = BTreeSet::new();
    rumoca_eval_dae::for_each_scalar_coordinate(view, residual, 0, None, |coordinate, _| {
        use dae::CoordinateView as C;
        match coordinate {
            C::Derivative(id) => {
                derivatives.insert(id.index());
            }
            other => {
                if let Some(variable) = coordinate_of(other).and_then(RbcCoordinate::variable) {
                    reads.insert(variable.0);
                }
            }
        }
    })
    .map_err(|error| ExportError::Projection(error.to_string()))?;
    Ok((
        reads.into_iter().map(VariableId).collect(),
        derivatives.into_iter().map(VariableId).collect(),
    ))
}

fn export_relations(view: dae::DaeView<'_>, ctx: &mut Ctx<'_>) -> Vec<RbcRelation> {
    (0..view.relation_count())
        .filter_map(|index| {
            let id = view.relation_id(index)?;
            let relation = view.relation(id)?;
            Some(RbcRelation {
                id: RelationId(index as u32),
                expression: ExprId(relation.expression().index()),
                provenance: ctx.provenance(relation.provenance()),
            })
        })
        .collect()
}

fn export_conditions(view: dae::DaeView<'_>, ctx: &mut Ctx<'_>) -> Vec<RbcCondition> {
    use dae::ConditionOperation as Op;
    (0..view.condition_count())
        .filter_map(|index| {
            let id = view.condition_id(index)?;
            let condition = view.condition(id)?;
            let node = match condition.operation() {
                Op::Initial => RbcConditionNode::Initial,
                Op::Always => RbcConditionNode::Always,
                Op::Relation(relation) => RbcConditionNode::Relation {
                    relation: RelationId(relation.index()),
                },
                Op::Discrete(expression) => RbcConditionNode::Discrete {
                    expression: ExprId(expression.index()),
                },
                Op::Clock(_) => RbcConditionNode::Clock,
                Op::Not(operand) => RbcConditionNode::Not {
                    operand: ConditionId(operand.index()),
                },
                Op::And(lhs, rhs) => RbcConditionNode::And {
                    lhs: ConditionId(lhs.index()),
                    rhs: ConditionId(rhs.index()),
                },
                Op::Or(lhs, rhs) => RbcConditionNode::Or {
                    lhs: ConditionId(lhs.index()),
                    rhs: ConditionId(rhs.index()),
                },
                Op::AnyRise(lhs, rhs) => RbcConditionNode::AnyRise {
                    lhs: ConditionId(lhs.index()),
                    rhs: ConditionId(rhs.index()),
                },
            };
            Some(RbcCondition {
                id: ConditionId(index as u32),
                node,
                provenance: ctx.provenance(condition.provenance()),
            })
        })
        .collect()
}

fn export_roots(view: dae::DaeView<'_>, ctx: &mut Ctx<'_>) -> Vec<RbcRoot> {
    (0..view.root_count())
        .filter_map(|index| {
            let id = view.root_id(index)?;
            let root = view.root(id)?;
            Some(RbcRoot {
                id: RootId(index as u32),
                relation: RelationId(root.relation().index()),
                activation: ConditionId(root.activation().index()),
                provenance: ctx.provenance(root.provenance()),
            })
        })
        .collect()
}

fn export_events(view: dae::DaeView<'_>, ctx: &mut Ctx<'_>) -> Vec<RbcEventAction> {
    use dae::EventActionOperation as Op;
    (0..view.event_action_count())
        .filter_map(|index| {
            let id = view.event_action_id(index)?;
            let action = view.event_action(id)?;
            let operation = match action.operation() {
                Op::Reinitialize { state, value } => RbcAction::Reinitialize {
                    state: VariableId(state.index()),
                    value: ExprId(value.index()),
                },
                Op::Assert { message, level } => RbcAction::Assert {
                    message: ExprId(message.index()),
                    level: level.map(|level| ExprId(level.index())),
                },
                Op::Terminate { message } => RbcAction::Terminate {
                    message: ExprId(message.index()),
                },
            };
            Some(RbcEventAction {
                id: EventId(index as u32),
                trigger: ConditionId(action.trigger().index()),
                guard: ConditionId(action.guard().index()),
                action: operation,
                provenance: ctx.provenance(action.provenance()),
            })
        })
        .collect()
}

/// MLS Appendix B.1c: what each discrete-valued variable equals.
///
/// This is a separate arena from the residual equations, and omitting it
/// produced an artifact that declared `discrete_value` variables and never
/// defined them — see docs/bugs/BUG-009.
fn export_discrete_definitions(
    view: dae::DaeView<'_>,
    ctx: &mut Ctx<'_>,
) -> Vec<RbcDiscreteDefinition> {
    (0..view.discrete_value_owner_count())
        .filter_map(|index| {
            let id = view.discrete_value_owner_id(index)?;
            let owner = view.discrete_value_owner(id)?;
            let targets = owner
                .targets()
                .iter()
                .map(|target| VariableId(dae::VariableId::from(target).index()))
                .collect();
            let branches = owner
                .branches()
                .iter()
                .map(|branch| RbcDiscreteBranch {
                    activation: match branch.activation() {
                        dae::DiscreteBranchActivation::Always => RbcDiscreteActivation::Always,
                        dae::DiscreteBranchActivation::When { trigger, guard } => {
                            RbcDiscreteActivation::When {
                                trigger: ConditionId(trigger.index()),
                                guard: ConditionId(guard.index()),
                            }
                        }
                    },
                    values: branch
                        .values()
                        .iter()
                        .map(|(value, _)| ExprId(value.index()))
                        .collect(),
                    provenance: ctx.provenance(branch.provenance()),
                })
                .collect();
            Some(RbcDiscreteDefinition {
                targets,
                branches,
                provenance: ctx.provenance(owner.provenance()),
            })
        })
        .collect()
}

fn export_time_events(
    view: dae::DaeView<'_>,
    ctx: &mut Ctx<'_>,
) -> Result<Vec<RbcTimeEvent>, ExportError> {
    use dae::TimeEventOperation as Op;
    let mut out = Vec::with_capacity(view.time_event_count());
    for index in 0..view.time_event_count() {
        let Some(id) = view.time_event_id(index) else {
            continue;
        };
        let Some(event) = view.time_event(id) else {
            continue;
        };
        let schedule = match event.operation() {
            Op::Static(instant) => {
                // The DAE carries an exact i128 rational. Bitcode v1 declares
                // i64; refuse rather than silently truncate an instant.
                let numerator = i64::try_from(instant.numerator()).map_err(|_| {
                    ExportError::Projection(
                        "time-event instant does not fit bitcode v1's i64 rational".into(),
                    )
                })?;
                let denominator = i64::try_from(instant.denominator()).map_err(|_| {
                    ExportError::Projection(
                        "time-event instant does not fit bitcode v1's i64 rational".into(),
                    )
                })?;
                RbcSchedule::Static {
                    numerator,
                    denominator,
                }
            }
            Op::Dynamic(deadline) => RbcSchedule::Dynamic {
                deadline: ExprId(deadline.index()),
            },
        };
        out.push(RbcTimeEvent {
            id: EventId(index as u32),
            schedule,
            provenance: ctx.provenance(event.provenance()),
        });
    }
    Ok(out)
}

/// Recover `connect(...)` relationships from the Flat model.
///
/// The DAE keeps only a `ConnectionEquation` / `FlowBalanceEquation` tag, so
/// endpoints come from Flat's per-equation `EquationOrigin`. Where the number
/// of Flat connection equations matches the number of DAE connection equations,
/// they are paired in order; otherwise the link is left unset rather than
/// guessed.
fn export_connections(
    flat: Option<&flat::Model>,
    variables: &[RbcVariable],
    equations: &[RbcEquation],
    ctx: &mut Ctx<'_>,
) -> Vec<RbcConnection> {
    let Some(flat) = flat else {
        return Vec::new();
    };
    let by_name: BTreeMap<&str, VariableId> = variables
        .iter()
        .map(|variable| (variable.name.as_str(), variable.id))
        .collect();

    let dae_connection_equations: Vec<EquationId> = equations
        .iter()
        .filter(|equation| {
            matches!(
                equation.provenance.origin,
                RbcOrigin::Generated {
                    generation: RbcGeneration::ConnectionEquation
                }
            )
        })
        .map(|equation| equation.id)
        .collect();

    let flat_connections: Vec<(&str, &str, Span)> = flat
        .equations
        .iter()
        .filter_map(|equation| match &equation.origin {
            flat::EquationOrigin::Connection { lhs, rhs } => {
                Some((lhs.as_str(), rhs.as_str(), equation.span))
            }
            _ => None,
        })
        .collect();

    let pairable = flat_connections.len() == dae_connection_equations.len();

    flat_connections
        .into_iter()
        .enumerate()
        .filter_map(|(index, (lhs, rhs, span))| {
            let left = *by_name.get(lhs)?;
            let right = *by_name.get(rhs)?;
            let quantity = variables
                .get(left.0 as usize)
                .and_then(|variable| variable.connector)
                .map(|connector| connector.quantity)
                .unwrap_or(RbcQuantityKind::Potential);
            Some(RbcConnection {
                id: ConnectionId(index as u32),
                left,
                right,
                quantity,
                left_connector: connector_path(lhs).to_string(),
                right_connector: connector_path(rhs).to_string(),
                equation: pairable
                    .then(|| dae_connection_equations.get(index).copied())
                    .flatten(),
                provenance: RbcProvenance {
                    origin: RbcOrigin::Generated {
                        generation: RbcGeneration::ConnectionEquation,
                    },
                    span: ctx.span(span),
                },
            })
        })
        .collect()
}

/// `"battery.pin.v"` → `"battery.pin"`. A serialization-boundary operation.
fn connector_path(member: &str) -> &str {
    member.rsplit_once('.').map_or(member, |(path, _)| path)
}

#[allow(clippy::too_many_arguments)]
fn summarize(
    variables: &[RbcVariable],
    expressions: &[RbcExpr],
    equations: &[RbcEquation],
    initial_equations: &[RbcEquation],
    relations: &[RbcRelation],
    conditions: &[RbcCondition],
    roots: &[RbcRoot],
    events: &[RbcEventAction],
    time_events: &[RbcTimeEvent],
    discrete_definitions: &[RbcDiscreteDefinition],
    connections: &[RbcConnection],
    components: &[RbcComponent],
) -> RbcSummary {
    let count = |role: RbcRole| {
        variables
            .iter()
            .filter(|variable| variable.role == role)
            .count() as u32
    };
    RbcSummary {
        discrete_definitions: discrete_definitions.len() as u32,
        variables: variables.len() as u32,
        states: count(RbcRole::State),
        parameters: count(RbcRole::Parameter),
        constants: count(RbcRole::Constant),
        inputs: count(RbcRole::Input),
        outputs: count(RbcRole::Output),
        algebraics: count(RbcRole::Algebraic),
        discrete_reals: count(RbcRole::DiscreteReal),
        discrete_values: count(RbcRole::DiscreteValue),
        equations: equations.len() as u32,
        initial_equations: initial_equations.len() as u32,
        expressions: expressions.len() as u32,
        relations: relations.len() as u32,
        conditions: conditions.len() as u32,
        roots: roots.len() as u32,
        events: events.len() as u32,
        time_events: time_events.len() as u32,
        connections: connections.len() as u32,
        components: components.len() as u32,
        trace_points: 0,
    }
}
