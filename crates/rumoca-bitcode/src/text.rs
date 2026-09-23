//! A parseable textual form of Rumoca Bitcode — the `.ll` to the `.rbc`.
//!
//! `bitcode disasm` renders a *listing*: readable, lossy, one-way. JSON
//! round-trips but is a serialization nobody edits by hand. This is the third
//! thing, and the one a debugger actually wants: text you can read, edit, and
//! assemble back into a byte-identical artifact.
//!
//! ```text
//! rbc 1
//! producer "rumoca 0.10.0"
//! model "Modelica.Electrical.Analog.Examples.ChuaCircuit"
//!
//! $0 type real
//! %6 var "L.L" $0 parameter parameter scalars 1 unit "H" quantity "Inductance"
//!    binding ^24 @src 0 224 237 7 3
//! ^24 expr $0 lit real 18
//! ^83 expr $0 bin sub ^81 ^82 @src 5 224 237 7 3
//! eq 3 ^83 reads %0 %1 dreads %0 @src 5 224 237 7 3
//! ```
//!
//! **Every id is written explicitly.** Expressions form a flat table addressed
//! by index, exactly like a constant pool, and equations reference them by id.
//! Re-deriving indices on parse would renumber a model that contains duplicate
//! nodes — a real artifact has two separate `0` literals at ids 22 and 23 — so
//! the ids are data, not presentation, and the format states them.
//!
//! **Nothing is dropped silently.** Printing a construct this version cannot
//! represent is an error, not an omission. A textual IR that quietly loses a
//! section would assemble into a different model than the one it came from,
//! which is worse than refusing.
//!
//! The one deliberate exception is source *text*, which is omitted unless
//! asked for: it is most of the artifact's bytes and none of its semantics.
//! `print_text_with` takes the choice, and a round-trip through the form
//! without it preserves everything except that text.

use std::fmt::Write as _;

use crate::schema::*;

/// Errors from reading the textual form. A line number always accompanies the
/// message, because a parse failure the reader cannot locate is a bad error.
#[derive(Debug, thiserror::Error)]
#[error("line {line}: {message}")]
pub struct TextError {
    pub line: usize,
    pub message: String,
}

impl TextError {
    fn at(line: usize, message: impl Into<String>) -> Self {
        Self { line, message: message.into() }
    }
}

#[derive(Debug, Clone, Copy, Default)]
pub struct TextOptions {
    /// Include each source file's full text. Off by default: it is most of the
    /// bytes and none of the semantics.
    pub sources: bool,
}

// ── printing ─────────────────────────────────────────────────────────────────

fn quote(text: &str) -> String {
    let mut out = String::with_capacity(text.len() + 2);
    out.push('"');
    for character in text.chars() {
        match character {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            other => out.push(other),
        }
    }
    out.push('"');
    out
}

/// A real that reads back as the same bits.
///
/// `{}` renders `18.0` as `18`, which then parses as an integer literal and
/// changes the node's type. `{:?}` keeps the decimal point and round-trips.
fn real(value: f64) -> String {
    if value.is_finite() {
        format!("{value:?}")
    } else if value.is_nan() {
        "nan".to_string()
    } else if value > 0.0 {
        "inf".to_string()
    } else {
        "-inf".to_string()
    }
}

fn generation(value: RbcGeneration) -> &'static str {
    use RbcGeneration::*;
    match value {
        SyntheticResidual => "synthetic_residual",
        BindingEquation => "binding_equation",
        ConnectionEquation => "connection_equation",
        FlowBalanceEquation => "flow_balance_equation",
        AlgorithmEquation => "algorithm_equation",
        DiscreteUpdate => "discrete_update",
        ConditionLowering => "condition_lowering",
        PreValueLowering => "pre_value_lowering",
        ClockLowering => "clock_lowering",
        DelayLowering => "delay_lowering",
        SemiLinearLowering => "semi_linear_lowering",
        TerminalLowering => "terminal_lowering",
        EventActionLowering => "event_action_lowering",
        InitializationEquation => "initialization_equation",
        DefaultStart => "default_start",
        ArrayEquationProjection => "array_equation_projection",
        RecordEquationProjection => "record_equation_projection",
        FunctionLoopLowering => "function_loop_lowering",
        FunctionConditionLowering => "function_condition_lowering",
        FunctionAggregateLowering => "function_aggregate_lowering",
        DerivedParameterLowering => "derived_parameter_lowering",
        IndexReduction => "index_reduction",
        AliasElimination => "alias_elimination",
        RuntimeDiscontinuity => "runtime_discontinuity",
        Other => "other",
    }
}

fn parse_generation(word: &str) -> Option<RbcGeneration> {
    use RbcGeneration::*;
    Some(match word {
        "synthetic_residual" => SyntheticResidual,
        "binding_equation" => BindingEquation,
        "connection_equation" => ConnectionEquation,
        "flow_balance_equation" => FlowBalanceEquation,
        "algorithm_equation" => AlgorithmEquation,
        "discrete_update" => DiscreteUpdate,
        "condition_lowering" => ConditionLowering,
        "pre_value_lowering" => PreValueLowering,
        "clock_lowering" => ClockLowering,
        "delay_lowering" => DelayLowering,
        "semi_linear_lowering" => SemiLinearLowering,
        "terminal_lowering" => TerminalLowering,
        "event_action_lowering" => EventActionLowering,
        "initialization_equation" => InitializationEquation,
        "default_start" => DefaultStart,
        "array_equation_projection" => ArrayEquationProjection,
        "record_equation_projection" => RecordEquationProjection,
        "function_loop_lowering" => FunctionLoopLowering,
        "function_condition_lowering" => FunctionConditionLowering,
        "function_aggregate_lowering" => FunctionAggregateLowering,
        "derived_parameter_lowering" => DerivedParameterLowering,
        "index_reduction" => IndexReduction,
        "alias_elimination" => AliasElimination,
        "runtime_discontinuity" => RuntimeDiscontinuity,
        "other" => Other,
        _ => return None,
    })
}

fn provenance(value: &RbcProvenance) -> String {
    let span = &value.span;
    match value.origin {
        RbcOrigin::Source => format!(
            "@src {} {} {} {} {}",
            span.source.0, span.start, span.end, span.line, span.column
        ),
        RbcOrigin::Generated { generation: kind } => format!(
            "@gen {} {} {} {} {} {}",
            generation(kind),
            span.source.0,
            span.start,
            span.end,
            span.line,
            span.column
        ),
    }
}

fn scalar(value: RbcScalar) -> &'static str {
    match value {
        RbcScalar::Real => "real",
        RbcScalar::Integer => "integer",
        RbcScalar::Boolean => "boolean",
        RbcScalar::String => "string",
        RbcScalar::Enumeration => "enumeration",
        RbcScalar::Record => "record",
    }
}

fn role(value: RbcRole) -> &'static str {
    match value {
        RbcRole::Parameter => "parameter",
        RbcRole::Constant => "constant",
        RbcRole::Input => "input",
        RbcRole::State => "state",
        RbcRole::Algebraic => "algebraic",
        RbcRole::Output => "output",
        RbcRole::DiscreteReal => "discrete_real",
        RbcRole::DiscreteValue => "discrete_value",
    }
}

fn causality(value: RbcCausality) -> &'static str {
    match value {
        RbcCausality::Input => "input",
        RbcCausality::Output => "output",
        RbcCausality::Parameter => "parameter",
        RbcCausality::CalculatedParameter => "calculated_parameter",
        RbcCausality::Independent => "independent",
        RbcCausality::Local => "local",
    }
}

fn quantity_kind(value: RbcQuantityKind) -> &'static str {
    match value {
        RbcQuantityKind::Potential => "potential",
        RbcQuantityKind::Flow => "flow",
        RbcQuantityKind::Stream => "stream",
    }
}

fn unary(value: RbcUnaryOp) -> &'static str {
    match value {
        RbcUnaryOp::Negate => "negate",
        RbcUnaryOp::Not => "not",
        RbcUnaryOp::Plus => "plus",
    }
}

fn binary(value: RbcBinaryOp) -> &'static str {
    use RbcBinaryOp::*;
    match value {
        Add => "add", Subtract => "sub", Multiply => "mul", Divide => "div",
        Power => "pow", Equal => "eq", NotEqual => "ne", Less => "lt",
        LessEqual => "le", Greater => "gt", GreaterEqual => "ge",
        And => "and", Or => "or",
    }
}

fn coordinate(value: RbcCoordinate) -> String {
    use RbcCoordinate::*;
    match value {
        Time => "time".to_string(),
        Parameter { variable } => format!("param %{}", variable.0),
        Input { variable } => format!("input %{}", variable.0),
        State { variable } => format!("state %{}", variable.0),
        Derivative { variable } => format!("der %{}", variable.0),
        Algebraic { variable } => format!("alg %{}", variable.0),
        DiscreteReal { variable } => format!("dreal %{}", variable.0),
        DiscreteValue { variable } => format!("dval %{}", variable.0),
        PreState { variable } => format!("pre_state %{}", variable.0),
        PreAlgebraic { variable } => format!("pre_alg %{}", variable.0),
        PreDiscreteReal { variable } => format!("pre_dreal %{}", variable.0),
        PreDiscreteValue { variable } => format!("pre_dval %{}", variable.0),
        Binder { domain, ordinal } => format!("binder &{} {ordinal}", domain.0),
        Condition { condition } => format!("cond ?{}", condition.0),
        FunctionParameter { function, ordinal } =>
            format!("fnparam ~{} {ordinal}", function.0),
    }
}

fn subscript(value: &RbcSubscript) -> String {
    match value {
        RbcSubscript::Index { expression } => format!("at ^{}", expression.0),
        RbcSubscript::Whole => "all".to_string(),
        RbcSubscript::Slice { expression } => format!("slice ^{}", expression.0),
    }
}

fn literal(value: &RbcLiteral) -> String {
    match value {
        RbcLiteral::Real { value } => format!("lit real {}", real(*value)),
        RbcLiteral::Integer { value } => format!("lit integer {value}"),
        RbcLiteral::Enumeration { ordinal } => format!("lit enum {ordinal}"),
        RbcLiteral::Boolean { value } => format!("lit boolean {value}"),
        RbcLiteral::String { value } => format!("lit string {}", quote(value)),
    }
}

/// Render `file` as the textual IR.
pub fn print_text(file: &RbcFile) -> Result<String, TextError> {
    print_text_with(file, TextOptions::default())
}

pub fn print_text_with(file: &RbcFile, options: TextOptions) -> Result<String, TextError> {
    if file.execution.is_some() || !file.model.connectors.is_empty() || !file.model.connector_types.is_empty() {
        return Err(TextError::at(0, "text profile cannot represent executable/connector declarations; use JSON or CBOR"));
    }
    let model = &file.model;
    let mut out = String::new();
    let _ = writeln!(out, "; rumoca bitcode, textual form");
    let _ = writeln!(out, "rbc {}", file.bitcode_version);
    let _ = writeln!(out, "producer {}", quote(&file.producer));
    let _ = writeln!(out, "model {}", quote(&model.name));

    if !model.sources.is_empty() {
        let _ = writeln!(out, "\n; sources");
        for source in &model.sources {
            match (&source.text, options.sources) {
                (Some(text), true) => {
                    let _ = writeln!(out, "!{} source {} text {}",
                                     source.id.0, quote(&source.name), quote(text));
                }
                _ => {
                    let _ = writeln!(out, "!{} source {}", source.id.0, quote(&source.name));
                }
            }
        }
    }

    if !model.types.is_empty() {
        let _ = writeln!(out, "\n; types");
        for entry in &model.types {
            let dims = if entry.dimensions.is_empty() {
                String::new()
            } else {
                format!(" dims {}", entry.dimensions.iter()
                        .map(u32::to_string).collect::<Vec<_>>().join(","))
            };
            let record = match &entry.record {
                Some(record) => format!(
                    " record {} {} {}", quote(&record.name), record.fields.len(),
                    record.fields.iter()
                        .map(|f| format!("{} ${}", quote(&f.name), f.value_type.0))
                        .collect::<Vec<_>>().join(" ")),
                None => String::new(),
            };
            let _ = writeln!(out, "${} type {}{dims}{record}",
                             entry.id.0, scalar(entry.scalar));
        }
    }

    if !model.functions.is_empty() {
        let _ = writeln!(out, "\n; functions");
        for function in &model.functions {
            let parameters = function.parameters.iter()
                .map(|p| format!("{} ${}", quote(&p.name), p.value_type.0))
                .collect::<Vec<_>>().join(" ");
            let results = function.results.iter()
                .map(|t| format!("${}", t.0)).collect::<Vec<_>>().join(" ");
            let body = match &function.body {
                RbcFunctionBody::ElidedModelica => "body elided".to_string(),
                RbcFunctionBody::External { language, symbol } =>
                    format!("body external {} {}", quote(language), quote(symbol)),
            };
            let inline = match function.inline {
                RbcInline::Unstated => "",
                RbcInline::Requested => " inline",
                RbcInline::Never => " noinline",
            };
            let _ = writeln!(out, "~{} fn {} params {} {parameters} results {} {results} \
{body}{inline} {}",
                             function.id.0, quote(&function.name),
                             function.parameters.len(), function.results.len(),
                             provenance(&function.declaration));
        }
    }

    if !model.components.is_empty() {
        let _ = writeln!(out, "\n; components");
        for component in &model.components {
            let class = component
                .class_name
                .as_deref()
                .map(|name| format!(" of {}", quote(name)))
                .unwrap_or_default();
            let _ = writeln!(out, "#{} comp {}{class}",
                             component.id.0, quote(&component.path));
        }
    }

    if !model.variables.is_empty() {
        let _ = writeln!(out, "\n; variables");
        for variable in &model.variables {
            let mut line = format!(
                "%{} var {} ${} {} {} scalars {}",
                variable.id.0, quote(&variable.name), variable.value_type.0,
                role(variable.role), causality(variable.causality), variable.scalar_count
            );
            if variable.discrete_input {
                let _ = write!(line, " discrete");
            }
            if let Some(contract) = &variable.contract {
                let _ = write!(line, " contract {}", match contract.variability {
                    RbcVariability::Constant => "constant",
                    RbcVariability::Parameter => "parameter",
                    RbcVariability::Discrete => "discrete",
                    RbcVariability::Continuous => "continuous",
                });
                for (flag, set) in [("final", contract.is_final),
                                    ("protected", contract.is_protected),
                                    ("evaluate", contract.evaluate),
                                    ("structural", contract.structural),
                                    ("frommod", contract.binding_from_modification)] {
                    if set {
                        let _ = write!(line, " {flag}");
                    }
                }
                if let Some(value) = contract.effective_value {
                    let _ = write!(line, " value {}", real(value));
                }
                if !contract.binding_depends_on.is_empty() {
                    let _ = write!(line, " uses {}", contract.binding_depends_on.iter()
                        .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
                }
                if let Some(declared) = &contract.declared_in {
                    let _ = write!(line, " declaredin {}", quote(declared));
                }
            }
            if let Some(component) = variable.component {
                let _ = write!(line, " comp #{}", component.0);
            }
            for (key, slot) in [("unit", &variable.unit),
                                ("quantity", &variable.physical_quantity),
                                ("class", &variable.declaring_class),
                                ("desc", &variable.description)] {
                if let Some(value) = slot {
                    let _ = write!(line, " {key} {}", quote(value));
                }
            }
            if let Some(fixed) = variable.fixed {
                let _ = write!(line, " fixed {fixed}");
            }
            if variable.tunable {
                let _ = write!(line, " tunable");
            }
            if variable.from_source {
                let _ = write!(line, " from_source");
            }
            for (key, slot) in [("start", variable.start), ("min", variable.min),
                                ("max", variable.max), ("nominal", variable.nominal),
                                ("binding", variable.binding)] {
                if let Some(expression) = slot {
                    let _ = write!(line, " {key} ^{}", expression.0);
                }
            }
            if let Some(connector) = &variable.connector {
                let _ = write!(line, " connector {}{}", quantity_kind(connector.quantity),
                               if connector.connected { " connected" } else { "" });
            }
            let _ = writeln!(out, "{line} {}", provenance(&variable.declaration));
        }
    }

    if !model.expressions.is_empty() {
        let _ = writeln!(out, "\n; expressions");
        for expression in &model.expressions {
            let body = match &expression.node {
                RbcExprNode::Literal { value } => literal(value),
                RbcExprNode::Coordinate { coordinate: c } => format!("coord {}", coordinate(*c)),
                RbcExprNode::Unary { op, operand } =>
                    format!("un {} ^{}", unary(*op), operand.0),
                RbcExprNode::Binary { op, lhs, rhs } =>
                    format!("bin {} ^{} ^{}", binary(*op), lhs.0, rhs.0),
                RbcExprNode::Conditional { branches, fallback } => {
                    let arms: Vec<String> = branches.iter()
                        .map(|b| format!("^{} ^{}", b.condition.0, b.value.0)).collect();
                    format!("cond {} {} else ^{}", arms.len(), arms.join(" "), fallback.0)
                }
                RbcExprNode::Builtin { name, arguments } => format!(
                    "call {} {} {}", quote(name), arguments.len(),
                    arguments.iter().map(|a| format!("^{}", a.0))
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::Array { elements, empty_type } => format!(
                    "array {}{} {}", elements.len(),
                    match empty_type {
                        Some(ty) => format!(" of ${}", ty.0),
                        None => String::new(),
                    },
                    elements.iter().map(|e| format!("^{}", e.0))
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::Record { ty, fields } => format!(
                    "record ${} {} {}", ty.0, fields.len(),
                    fields.iter().map(|f| format!("^{}", f.0))
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::Field { base, field } =>
                    format!("field ^{} {field}", base.0),
                RbcExprNode::Range { start, step, stop } => format!(
                    "range ^{} {} ^{}", start.0,
                    match step {
                        Some(step) => format!("step ^{}", step.0),
                        None => "nostep".to_string(),
                    },
                    stop.0),
                RbcExprNode::Comprehension { domain, body } =>
                    format!("comp &{} ^{}", domain.0, body.0),
                RbcExprNode::Index { base, subscripts } => format!(
                    "index ^{} {} {}", base.0, subscripts.len(),
                    subscripts.iter().map(subscript)
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::ArrayUpdate { base, value, subscripts } => format!(
                    "update ^{} ^{} {} {}", base.0, value.0, subscripts.len(),
                    subscripts.iter().map(subscript)
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::Call { owner, function, output, arguments } => format!(
                    "invoke ~{} out {output} owner ^{} {} {}", function.0, owner.0,
                    arguments.len(),
                    arguments.iter().map(|a| format!("^{}", a.0))
                        .collect::<Vec<_>>().join(" ")),
                RbcExprNode::Unsupported { detail } => format!("unsupported {}", quote(detail)),
            };
            let _ = writeln!(out, "^{} expr ${} {body} {}", expression.id.0,
                             expression.value_type.0, provenance(&expression.provenance));
        }
    }

    for (keyword, equations) in [("eq", &model.equations), ("ieq", &model.initial_equations)] {
        if equations.is_empty() {
            continue;
        }
        let _ = writeln!(out, "\n; {keyword}");
        for equation in equations {
            let mut line = format!("{keyword} {} ^{}", equation.id.0, equation.residual.0);
            if !equation.reads.is_empty() {
                let _ = write!(line, " reads {}", equation.reads.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !equation.reads_derivative.is_empty() {
                let _ = write!(line, " dreads {}", equation.reads_derivative.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !equation.reads_previous.is_empty() {
                let _ = write!(line, " preads {}", equation.reads_previous.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            let _ = writeln!(out, "{line} {}", provenance(&equation.provenance));
        }
    }

    if !model.domains.is_empty() {
        let _ = writeln!(out, "\n; domains");
        for domain in &model.domains {
            let binders = domain
                .binders
                .iter()
                .map(|b| format!("{} {} {} {} {}", b.id, quote(&b.display_name),
                                 b.lower, b.upper, b.step))
                .collect::<Vec<_>>()
                .join(" ");
            let parent = domain
                .parent
                .map(|p| format!(" parent &{}", p.0))
                .unwrap_or_default();
            let extents = if domain.extents.is_empty() {
                "-".to_string()
            } else {
                domain.extents.iter().map(u32::to_string).collect::<Vec<_>>().join(",")
            };
            let _ = writeln!(out, "&{} domain scalars {} extents {extents}{parent} \
binders {} {binders} {}",
                             domain.id.0, domain.scalar_count,
                             domain.binders.len(), provenance(&domain.provenance));
        }
    }

    for (keyword, families) in [("family", &model.equation_families),
                                ("ifamily", &model.initial_equation_families)] {
        if families.is_empty() {
            continue;
        }
        let _ = writeln!(out, "\n; {keyword}");
        for family in families {
            let view = match family.scalar_view {
                RbcScalarView::BinderSubstitution => "binder".to_string(),
                RbcScalarView::RowMajorProjection => "rowmajor".to_string(),
                RbcScalarView::BinderPrefixProjection { binder_count } =>
                    format!("prefix {binder_count}"),
            };
            let extents = if family.extents.is_empty() {
                "-".to_string()
            } else {
                family.extents.iter().map(u32::to_string)
                    .collect::<Vec<_>>().join(",")
            };
            let bodies = family.bodies.iter()
                .map(|b| format!("^{}", b.0)).collect::<Vec<_>>().join(" ");
            let mut line = format!("{keyword} {} domain &{} rows {} extents {extents} \
view {view} bodies {} {bodies}",
                                   family.id.0, family.domain.0, family.scalar_rows,
                                   family.bodies.len());
            if !family.reads.is_empty() {
                let _ = write!(line, " reads {}", family.reads.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !family.reads_derivative.is_empty() {
                let _ = write!(line, " dreads {}", family.reads_derivative.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !family.reads_previous.is_empty() {
                let _ = write!(line, " preads {}", family.reads_previous.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            let _ = writeln!(out, "{line} {}", provenance(&family.provenance));
        }
    }

    if !model.discrete_real_equations.is_empty() {
        let _ = writeln!(out, "\n; discrete real equations (MLS B.1b)");
        for equation in &model.discrete_real_equations {
            let activation = match equation.activation {
                RbcDiscreteRealActivation::Always => "always".to_string(),
                RbcDiscreteRealActivation::When { trigger, guard } =>
                    format!("when ?{} guard ?{}", trigger.0, guard.0),
            };
            let mut line = format!("dreq {} ^{} {activation}",
                                   equation.id.0, equation.residual.0);
            if !equation.reads.is_empty() {
                let _ = write!(line, " reads {}", equation.reads.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !equation.reads_derivative.is_empty() {
                let _ = write!(line, " dreads {}", equation.reads_derivative.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            if !equation.reads_previous.is_empty() {
                let _ = write!(line, " preads {}", equation.reads_previous.iter()
                    .map(|v| format!("%{}", v.0)).collect::<Vec<_>>().join(" "));
            }
            let _ = writeln!(out, "{line} {}", provenance(&equation.provenance));
        }
    }

    if !model.initial_discrete_values.is_empty() {
        let _ = writeln!(out, "\n; initial discrete values");
        for entry in &model.initial_discrete_values {
            let _ = writeln!(out, "idval %{} ^{} {}", entry.target.0, entry.value.0,
                             provenance(&entry.provenance));
        }
    }

    if !model.relations.is_empty() {
        let _ = writeln!(out, "\n; relations");
        for relation in &model.relations {
            let _ = writeln!(out, "rel {} ^{} {}", relation.id.0, relation.expression.0,
                             provenance(&relation.provenance));
        }
    }

    if !model.conditions.is_empty() {
        let _ = writeln!(out, "\n; conditions");
        for condition in &model.conditions {
            use RbcConditionNode::*;
            let body = match &condition.node {
                Initial => "initial".to_string(),
                Always => "always".to_string(),
                Clock => "clock".to_string(),
                Relation { relation } => format!("rel {}", relation.0),
                Discrete { expression } => format!("discrete ^{}", expression.0),
                Not { operand } => format!("not {}", operand.0),
                And { lhs, rhs } => format!("and {} {}", lhs.0, rhs.0),
                Or { lhs, rhs } => format!("or {} {}", lhs.0, rhs.0),
                AnyRise { lhs, rhs } => format!("any_rise {} {}", lhs.0, rhs.0),
                Unsupported { detail } => format!("unsupported {}", quote(detail)),
            };
            let _ = writeln!(out, "cond {} {body} {}", condition.id.0,
                             provenance(&condition.provenance));
        }
    }

    if !model.roots.is_empty() {
        let _ = writeln!(out, "\n; roots");
        for root in &model.roots {
            let _ = writeln!(out, "root {} rel {} act {} {}", root.id.0, root.relation.0,
                             root.activation.0, provenance(&root.provenance));
        }
    }

    if !model.events.is_empty() {
        let _ = writeln!(out, "\n; events");
        for event in &model.events {
            let action = match &event.action {
                RbcAction::Reinitialize { state, value } =>
                    format!("reinit %{} ^{}", state.0, value.0),
                RbcAction::Assert { message, level } => match level {
                    Some(level) => format!("assert ^{} level ^{}", message.0, level.0),
                    None => format!("assert ^{}", message.0),
                },
                RbcAction::Terminate { message } => format!("terminate ^{}", message.0),
            };
            let _ = writeln!(out, "event {} trig {} guard {} {action} {}", event.id.0,
                             event.trigger.0, event.guard.0, provenance(&event.provenance));
        }
    }

    if !model.time_events.is_empty() {
        let _ = writeln!(out, "\n; time events");
        for event in &model.time_events {
            let schedule = match event.schedule {
                RbcSchedule::Static { numerator, denominator } =>
                    format!("static {numerator} {denominator}"),
                RbcSchedule::Dynamic { deadline } => format!("dynamic ^{}", deadline.0),
            };
            let _ = writeln!(out, "tevent {} {schedule} {}", event.id.0,
                             provenance(&event.provenance));
        }
    }

    if !model.connections.is_empty() {
        let _ = writeln!(out, "\n; connections");
        for connection in &model.connections {
            let equation = connection.equation
                .map(|e| format!(" eq {}", e.0)).unwrap_or_default();
            let _ = writeln!(out, "conn {} %{} %{} {} {} {}{equation} {}",
                             connection.id.0, connection.left.0, connection.right.0,
                             quantity_kind(connection.quantity),
                             quote(&connection.left_connector),
                             quote(&connection.right_connector),
                             provenance(&connection.provenance));
        }
    }

    if !model.connection_sets.is_empty() {
        let _ = writeln!(out, "\n; connection sets");
        for set in &model.connection_sets {
            let mut line = format!("connset {}", set.id.0);
            for connector in &set.connectors {
                let _ = write!(line, " at {}", quote(connector));
            }
            for potential in &set.potentials {
                let _ = write!(line, " pot %{}", potential.0);
            }
            for balance in &set.balances {
                let _ = write!(line, " balance");
                if let Some(equation) = balance.equation {
                    let _ = write!(line, " eq {}", equation.0);
                }
                for term in &balance.terms {
                    let _ = write!(line, " {}%{}",
                                   if term.negated { "-" } else { "+" },
                                   term.variable.0);
                }
                let _ = write!(line, " end");
            }
            for equation in &set.potential_equations {
                let _ = write!(line, " poteq {}", equation.0);
            }
            if set.unconnected {
                let _ = write!(line, " unconnected");
            }
            let _ = writeln!(out, "{line} {}", provenance(&set.provenance));
        }
    }

    if !model.discrete_definitions.is_empty() {
        let _ = writeln!(out, "\n; discrete definitions");
        for definition in &model.discrete_definitions {
            let targets = definition.targets.iter()
                .map(|t| format!("%{}", t.0)).collect::<Vec<_>>().join(" ");
            let _ = writeln!(out, "disc {} targets {}", definition.targets.len(), targets);
            for branch in &definition.branches {
                let activation = match branch.activation {
                    RbcDiscreteActivation::Always => "always".to_string(),
                    RbcDiscreteActivation::When { trigger, guard } =>
                        format!("when {} {}", trigger.0, guard.0),
                };
                let values = branch.values.iter()
                    .map(|v| format!("^{}", v.0)).collect::<Vec<_>>().join(" ");
                let _ = writeln!(out, "  branch {activation} values {} {values} {}",
                                 branch.values.len(), provenance(&branch.provenance));
            }
            let _ = writeln!(out, "  end {}", provenance(&definition.provenance));
        }
    }

    if !model.trace_points.is_empty() {
        let _ = writeln!(out, "\n; trace points");
        for point in &model.trace_points {
            let mut line = format!("trace {} %{} {}", point.id.0, point.variable.0,
                                   quote(&point.label));
            if let Some(connection) = point.connection {
                let _ = write!(line, " conn {}", connection.0);
            }
            if let Some(set) = point.connection_set {
                let _ = write!(line, " connset {}", set.0);
            }
            if let Some(kind) = point.quantity {
                let _ = write!(line, " kind {}", quantity_kind(kind));
            }
            if let Some(unit) = &point.unit {
                let _ = write!(line, " unit {}", quote(unit));
            }
            if let Some(added_by) = &point.added_by {
                let _ = write!(line, " added_by {}", quote(added_by));
            }
            let _ = writeln!(out, "{line}");
        }
    }

    Ok(out)
}

// ── parsing ──────────────────────────────────────────────────────────────────

/// A line split into tokens, with quoted strings kept whole.
///
/// Hand-rolled rather than a lexer crate: the grammar is one statement per
/// line over a fixed keyword set, and the only subtlety is that a quoted
/// string may contain spaces and escapes.
fn tokenize(line: &str, number: usize) -> Result<Vec<String>, TextError> {
    let mut tokens = Vec::new();
    let mut chars = line.chars().peekable();
    while let Some(&character) = chars.peek() {
        if character.is_whitespace() {
            chars.next();
            continue;
        }
        if character == ';' {
            break; // comment to end of line
        }
        if character == '"' {
            chars.next();
            let mut value = String::new();
            loop {
                match chars.next() {
                    None => return Err(TextError::at(number, "unterminated string")),
                    Some('"') => break,
                    Some('\\') => match chars.next() {
                        Some('n') => value.push('\n'),
                        Some('r') => value.push('\r'),
                        Some('t') => value.push('\t'),
                        Some('\\') => value.push('\\'),
                        Some('"') => value.push('"'),
                        Some(other) => value.push(other),
                        None => return Err(TextError::at(number, "trailing escape")),
                    },
                    Some(other) => value.push(other),
                }
            }
            tokens.push(format!("\u{0}{value}")); // marked as a string literal
            continue;
        }
        let mut word = String::new();
        while let Some(&next) = chars.peek() {
            if next.is_whitespace() || next == ';' {
                break;
            }
            word.push(next);
            chars.next();
        }
        tokens.push(word);
    }
    Ok(tokens)
}

/// Cursor over one line's tokens. Every accessor reports the line on failure.
struct Cursor<'a> {
    tokens: &'a [String],
    at: usize,
    line: usize,
}

impl<'a> Cursor<'a> {
    fn new(tokens: &'a [String], line: usize) -> Self {
        Self { tokens, at: 0, line }
    }

    fn done(&self) -> bool {
        self.at >= self.tokens.len()
    }

    fn peek(&self) -> Option<&str> {
        self.tokens.get(self.at).map(String::as_str)
    }

    fn next_raw(&mut self) -> Result<&'a str, TextError> {
        let token = self.tokens.get(self.at)
            .ok_or_else(|| TextError::at(self.line, "unexpected end of line"))?;
        self.at += 1;
        Ok(token.as_str())
    }

    fn word(&mut self) -> Result<&'a str, TextError> {
        let token = self.next_raw()?;
        if let Some(text) = token.strip_prefix('\u{0}') {
            return Err(TextError::at(self.line, format!("expected a word, got string {text:?}")));
        }
        Ok(token)
    }

    fn string(&mut self) -> Result<String, TextError> {
        let token = self.next_raw()?;
        token.strip_prefix('\u{0}').map(str::to_string)
            .ok_or_else(|| TextError::at(self.line, format!("expected a quoted string, got `{token}`")))
    }

    /// A sigil-prefixed id: `%3`, `^12`, `$0`, `#1`, `!2`.
    fn id(&mut self, sigil: char) -> Result<u32, TextError> {
        let token = self.word()?;
        let rest = token.strip_prefix(sigil).ok_or_else(|| {
            TextError::at(self.line, format!("expected `{sigil}<id>`, got `{token}`"))
        })?;
        rest.parse().map_err(|_| {
            TextError::at(self.line, format!("`{rest}` is not an id"))
        })
    }

    fn number<T: std::str::FromStr>(&mut self) -> Result<T, TextError> {
        let token = self.word()?;
        token.parse().map_err(|_| {
            TextError::at(self.line, format!("`{token}` is not a number"))
        })
    }

    fn expect(&mut self, keyword: &str) -> Result<(), TextError> {
        let token = self.word()?;
        if token != keyword {
            return Err(TextError::at(self.line,
                format!("expected `{keyword}`, got `{token}`")));
        }
        Ok(())
    }

    /// Consume `keyword` if it is next. Used for optional clauses.
    fn eat(&mut self, keyword: &str) -> bool {
        if self.peek() == Some(keyword) {
            self.at += 1;
            return true;
        }
        false
    }

    fn provenance(&mut self) -> Result<RbcProvenance, TextError> {
        let marker = self.word()?;
        let origin = match marker {
            "@src" => RbcOrigin::Source,
            "@gen" => {
                let word = self.word()?;
                let generation = parse_generation(word).ok_or_else(|| {
                    TextError::at(self.line, format!("unknown generation `{word}`"))
                })?;
                RbcOrigin::Generated { generation }
            }
            other => return Err(TextError::at(self.line,
                format!("expected `@src` or `@gen`, got `{other}`"))),
        };
        Ok(RbcProvenance {
            origin,
            span: RbcSpan {
                source: SourceId(self.number()?),
                start: self.number()?,
                end: self.number()?,
                line: self.number()?,
                column: self.number()?,
            },
        })
    }
}

fn parse_scalar(word: &str, line: usize) -> Result<RbcScalar, TextError> {
    Ok(match word {
        "real" => RbcScalar::Real,
        "integer" => RbcScalar::Integer,
        "boolean" => RbcScalar::Boolean,
        "string" => RbcScalar::String,
        "enumeration" => RbcScalar::Enumeration,
        "record" => RbcScalar::Record,
        other => return Err(TextError::at(line, format!("unknown scalar `{other}`"))),
    })
}

fn parse_role(word: &str, line: usize) -> Result<RbcRole, TextError> {
    Ok(match word {
        "parameter" => RbcRole::Parameter,
        "constant" => RbcRole::Constant,
        "input" => RbcRole::Input,
        "state" => RbcRole::State,
        "algebraic" => RbcRole::Algebraic,
        "output" => RbcRole::Output,
        "discrete_real" => RbcRole::DiscreteReal,
        "discrete_value" => RbcRole::DiscreteValue,
        other => return Err(TextError::at(line, format!("unknown role `{other}`"))),
    })
}

fn parse_causality(word: &str, line: usize) -> Result<RbcCausality, TextError> {
    Ok(match word {
        "input" => RbcCausality::Input,
        "output" => RbcCausality::Output,
        "parameter" => RbcCausality::Parameter,
        "calculated_parameter" => RbcCausality::CalculatedParameter,
        "independent" => RbcCausality::Independent,
        "local" => RbcCausality::Local,
        other => return Err(TextError::at(line, format!("unknown causality `{other}`"))),
    })
}

fn parse_quantity(word: &str, line: usize) -> Result<RbcQuantityKind, TextError> {
    Ok(match word {
        "potential" => RbcQuantityKind::Potential,
        "flow" => RbcQuantityKind::Flow,
        "stream" => RbcQuantityKind::Stream,
        other => return Err(TextError::at(line, format!("unknown quantity kind `{other}`"))),
    })
}

fn parse_unary(word: &str, line: usize) -> Result<RbcUnaryOp, TextError> {
    Ok(match word {
        "negate" => RbcUnaryOp::Negate,
        "not" => RbcUnaryOp::Not,
        "plus" => RbcUnaryOp::Plus,
        other => return Err(TextError::at(line, format!("unknown unary op `{other}`"))),
    })
}

fn parse_binary(word: &str, line: usize) -> Result<RbcBinaryOp, TextError> {
    use RbcBinaryOp::*;
    Ok(match word {
        "add" => Add, "sub" => Subtract, "mul" => Multiply, "div" => Divide,
        "pow" => Power, "eq" => Equal, "ne" => NotEqual, "lt" => Less,
        "le" => LessEqual, "gt" => Greater, "ge" => GreaterEqual,
        "and" => And, "or" => Or,
        other => return Err(TextError::at(line, format!("unknown binary op `{other}`"))),
    })
}

fn parse_real(word: &str, line: usize) -> Result<f64, TextError> {
    match word {
        "nan" => Ok(f64::NAN),
        "inf" => Ok(f64::INFINITY),
        "-inf" => Ok(f64::NEG_INFINITY),
        other => other.parse().map_err(|_| {
            TextError::at(line, format!("`{other}` is not a real"))
        }),
    }
}

fn parse_subscripts(cursor: &mut Cursor<'_>) -> Result<Vec<RbcSubscript>, TextError> {
    let count: usize = cursor.number()?;
    let mut subscripts = Vec::with_capacity(count);
    for _ in 0..count {
        let kind = cursor.word()?;
        subscripts.push(match &*kind {
            "at" => RbcSubscript::Index { expression: ExprId(cursor.id('^')?) },
            "all" => RbcSubscript::Whole,
            "slice" => RbcSubscript::Slice { expression: ExprId(cursor.id('^')?) },
            other => return Err(TextError::at(cursor.line,
                format!("unknown subscript kind `{other}`"))),
        });
    }
    Ok(subscripts)
}

fn parse_coordinate(cursor: &mut Cursor<'_>) -> Result<RbcCoordinate, TextError> {
    use RbcCoordinate::*;
    let kind = cursor.word()?;
    if kind == "time" {
        return Ok(Time);
    }
    if kind == "binder" {
        let domain = DomainId(cursor.id('&')?);
        return Ok(Binder { domain, ordinal: cursor.number()? });
    }
    if kind == "cond" {
        return Ok(Condition { condition: ConditionId(cursor.id('?')?) });
    }
    if kind == "fnparam" {
        let function = FunctionId(cursor.id('~')?);
        return Ok(FunctionParameter { function, ordinal: cursor.number()? });
    }
    let variable = VariableId(cursor.id('%')?);
    Ok(match kind {
        "param" => Parameter { variable },
        "input" => Input { variable },
        "state" => State { variable },
        "der" => Derivative { variable },
        "alg" => Algebraic { variable },
        "dreal" => DiscreteReal { variable },
        "dval" => DiscreteValue { variable },
        "pre_state" => PreState { variable },
        "pre_alg" => PreAlgebraic { variable },
        "pre_dreal" => PreDiscreteReal { variable },
        "pre_dval" => PreDiscreteValue { variable },
        other => return Err(TextError::at(cursor.line,
            format!("unknown coordinate `{other}`"))),
    })
}

fn parse_equation(cursor: &mut Cursor<'_>) -> Result<RbcEquation, TextError> {
    let id = EquationId(cursor.number()?);
    let residual = ExprId(cursor.id('^')?);
    let mut reads = Vec::new();
    let mut reads_derivative = Vec::new();
    let mut reads_previous = Vec::new();
    for (keyword, sink) in [("reads", &mut reads),
                            ("dreads", &mut reads_derivative),
                            ("preads", &mut reads_previous)] {
        if cursor.eat(keyword) {
            while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                sink.push(VariableId(cursor.id('%')?));
            }
        }
    }
    Ok(RbcEquation { id, residual, provenance: cursor.provenance()?,
                     reads, reads_derivative, reads_previous })
}

/// A provenance for an item whose own line has not been read yet.
///
/// Every item that carries one overwrites this before it is stored; it exists
/// because a partially built record has to hold *something*, not because an
/// unknown origin is meaningful.
fn placeholder_provenance() -> RbcProvenance {
    RbcProvenance {
        origin: RbcOrigin::Source,
        span: RbcSpan {
            source: SourceId::PLACEHOLDER,
            start: 0,
            end: 0,
            line: 0,
            column: 0,
        },
    }
}

fn empty_model() -> RbcModel {
    RbcModel {
        connector_types: Vec::new(),
        connectors: Vec::new(),
        connection_sets: Vec::new(),
        functions: Vec::new(),
        discrete_real_equations: Vec::new(),
        initial_discrete_values: Vec::new(),
        name: String::new(),
        domains: Vec::new(),
        equation_families: Vec::new(), initial_equation_families: Vec::new(),
        sources: Vec::new(), types: Vec::new(), variables: Vec::new(),
        expressions: Vec::new(), equations: Vec::new(),
        initial_equations: Vec::new(), relations: Vec::new(),
        conditions: Vec::new(), roots: Vec::new(), events: Vec::new(),
        time_events: Vec::new(), connections: Vec::new(),
        components: Vec::new(), trace_points: Vec::new(),
        discrete_definitions: Vec::new(),
        summary: RbcSummary::default(),
    }
}

/// Read the textual IR back into an artifact.
pub fn parse_text(text: &str) -> Result<RbcFile, TextError> {
    let mut file = RbcFile {
        execution: None,
        magic: RBC_MAGIC.to_string(),
        bitcode_version: RBC_VERSION,
        producer: String::new(),
        model: empty_model(),
    };
    let model = &mut file.model;
    // A discrete definition spans several lines, so it is assembled across
    // iterations and closed by its `end` line.
    let mut open_discrete: Option<RbcDiscreteDefinition> = None;

    for (index, raw) in text.lines().enumerate() {
        let number = index + 1;
        let tokens = tokenize(raw, number)?;
        if tokens.is_empty() {
            continue;
        }
        let mut cursor = Cursor::new(&tokens, number);
        let head = cursor.next_raw()?.to_string();

        // Sigil-led lines declare a numbered item; keyword-led lines do not.
        if let Some(rest) = head.strip_prefix('!') {
            let id = SourceId(rest.parse().map_err(|_|
                TextError::at(number, "bad source id"))?);
            cursor.expect("source")?;
            let name = cursor.string()?;
            let text = if cursor.eat("text") { Some(cursor.string()?) } else { None };
            model.sources.push(RbcSource { id, name, text });
        } else if let Some(rest) = head.strip_prefix('$') {
            let id = TypeId(rest.parse().map_err(|_| TextError::at(number, "bad type id"))?);
            cursor.expect("type")?;
            let scalar = parse_scalar(cursor.word()?, number)?;
            let mut dimensions = Vec::new();
            if cursor.eat("dims") {
                for part in cursor.word()?.split(',') {
                    dimensions.push(part.parse().map_err(|_|
                        TextError::at(number, format!("bad dimension `{part}`")))?);
                }
            }
            let record = if cursor.eat("record") {
                let name = cursor.string()?;
                let count: usize = cursor.number()?;
                let mut fields = Vec::with_capacity(count);
                for _ in 0..count {
                    fields.push(RbcRecordField {
                        name: cursor.string()?,
                        value_type: TypeId(cursor.id('$')?),
                    });
                }
                Some(RbcRecord { name, fields })
            } else {
                None
            };
            model.types.push(RbcType { id, scalar, dimensions, record });
        } else if let Some(rest) = head.strip_prefix('~') {
            let id = FunctionId(rest.parse().map_err(|_|
                TextError::at(number, "bad function id"))?);
            cursor.expect("fn")?;
            let name = cursor.string()?;
            cursor.expect("params")?;
            let count: usize = cursor.number()?;
            let mut parameters = Vec::with_capacity(count);
            for _ in 0..count {
                parameters.push(RbcFunctionParameter {
                    name: cursor.string()?,
                    value_type: TypeId(cursor.id('$')?),
                });
            }
            cursor.expect("results")?;
            let count: usize = cursor.number()?;
            let mut results = Vec::with_capacity(count);
            for _ in 0..count {
                results.push(TypeId(cursor.id('$')?));
            }
            cursor.expect("body")?;
            let body = match &*cursor.word()? {
                "elided" => RbcFunctionBody::ElidedModelica,
                "external" => RbcFunctionBody::External {
                    language: cursor.string()?,
                    symbol: cursor.string()?,
                },
                other => return Err(TextError::at(number,
                    format!("unknown function body `{other}`"))),
            };
            let inline = if cursor.eat("inline") {
                RbcInline::Requested
            } else if cursor.eat("noinline") {
                RbcInline::Never
            } else {
                RbcInline::Unstated
            };
            model.functions.push(RbcFunction {
                id, name, parameters, results, inline, body,
                declaration: cursor.provenance()?,
            });
        } else if let Some(rest) = head.strip_prefix('#') {
            let id = ComponentId(rest.parse().map_err(|_|
                TextError::at(number, "bad component id"))?);
            cursor.expect("comp")?;
            let path = cursor.string()?;
            let class_name = if cursor.eat("of") {
                Some(cursor.string()?)
            } else {
                None
            };
            model.components.push(RbcComponent { id, path, class_name });
        } else if let Some(rest) = head.strip_prefix('%') {
            let id = VariableId(rest.parse().map_err(|_|
                TextError::at(number, "bad variable id"))?);
            cursor.expect("var")?;
            let name = cursor.string()?;
            let value_type = TypeId(cursor.id('$')?);
            let role = parse_role(cursor.word()?, number)?;
            let causality = parse_causality(cursor.word()?, number)?;
            cursor.expect("scalars")?;
            let scalar_count = cursor.number()?;
            let mut variable = RbcVariable {
                id, name, role, causality, value_type, scalar_count,
                declaration: placeholder_provenance(),
                component: None, unit: None, description: None, fixed: None,
                start: None, min: None, max: None, nominal: None, binding: None,
                connector: None, tunable: false, from_source: false,
                physical_quantity: None, declaring_class: None,
                discrete_input: false,
                contract: None,
            };
            loop {
                let Some(keyword) = cursor.peek() else { break };
                if keyword.starts_with('@') {
                    break;
                }
                let keyword = cursor.word()?;
                match keyword {
                    "comp" => variable.component = Some(ComponentId(cursor.id('#')?)),
                    "unit" => variable.unit = Some(cursor.string()?),
                    "quantity" => variable.physical_quantity = Some(cursor.string()?),
                    "class" => variable.declaring_class = Some(cursor.string()?),
                    "desc" => variable.description = Some(cursor.string()?),
                    "fixed" => variable.fixed = Some(cursor.word()? == "true"),
                    "tunable" => variable.tunable = true,
                    "discrete" => variable.discrete_input = true,
                    "contract" => {
                        let variability = match &*cursor.word()? {
                            "constant" => RbcVariability::Constant,
                            "parameter" => RbcVariability::Parameter,
                            "discrete" => RbcVariability::Discrete,
                            "continuous" => RbcVariability::Continuous,
                            other => return Err(TextError::at(number,
                                format!("unknown variability `{other}`"))),
                        };
                        let mut contract = RbcSymbolContract {
                            variability, is_final: false, is_protected: false,
                            evaluate: false, structural: false,
                            effective_value: None,
                            binding_depends_on: Vec::new(),
                            binding_from_modification: false,
                            declared_in: None,
                        };
                        loop {
                            match cursor.peek().map(|t| t.to_string()) {
                                Some(t) if t == "final" => {
                                    cursor.word()?; contract.is_final = true }
                                Some(t) if t == "protected" => {
                                    cursor.word()?; contract.is_protected = true }
                                Some(t) if t == "evaluate" => {
                                    cursor.word()?; contract.evaluate = true }
                                Some(t) if t == "structural" => {
                                    cursor.word()?; contract.structural = true }
                                Some(t) if t == "frommod" => {
                                    cursor.word()?;
                                    contract.binding_from_modification = true }
                                Some(t) if t == "value" => {
                                    cursor.word()?;
                                    let raw = cursor.word()?;
                                    contract.effective_value =
                                        Some(parse_real(raw, number)?) }
                                Some(t) if t == "uses" => {
                                    cursor.word()?;
                                    while cursor.peek()
                                        .is_some_and(|t| t.starts_with('%')) {
                                        contract.binding_depends_on
                                            .push(VariableId(cursor.id('%')?));
                                    } }
                                Some(t) if t == "declaredin" => {
                                    cursor.word()?;
                                    contract.declared_in = Some(cursor.string()?) }
                                _ => break,
                            }
                        }
                        variable.contract = Some(contract);
                    }
                    "from_source" => variable.from_source = true,
                    "start" => variable.start = Some(ExprId(cursor.id('^')?)),
                    "min" => variable.min = Some(ExprId(cursor.id('^')?)),
                    "max" => variable.max = Some(ExprId(cursor.id('^')?)),
                    "nominal" => variable.nominal = Some(ExprId(cursor.id('^')?)),
                    "binding" => variable.binding = Some(ExprId(cursor.id('^')?)),
                    "connector" => {
                        let quantity = parse_quantity(cursor.word()?, number)?;
                        variable.connector = Some(RbcConnectorMember {
                            quantity, connected: cursor.eat("connected") });
                    }
                    other => return Err(TextError::at(number,
                        format!("unknown variable attribute `{other}`"))),
                }
            }
            variable.declaration = cursor.provenance()?;
            model.variables.push(variable);
        } else if let Some(rest) = head.strip_prefix('&') {
            let id = DomainId(rest.parse().map_err(|_|
                TextError::at(number, "bad domain id"))?);
            cursor.expect("domain")?;
            cursor.expect("scalars")?;
            let scalar_count = cursor.number()?;
            cursor.expect("extents")?;
            let raw = cursor.word()?;
            let extents = if raw == "-" {
                Vec::new()
            } else {
                raw.split(',')
                    .map(|p| p.parse().map_err(|_| TextError::at(
                        number, format!("bad extent `{p}`"))))
                    .collect::<Result<Vec<u32>, _>>()?
            };
            let parent = cursor.eat("parent").then(|| cursor.id('&')).transpose()?
                .map(DomainId);
            cursor.expect("binders")?;
            let count: usize = cursor.number()?;
            let mut binders = Vec::with_capacity(count);
            for _ in 0..count {
                binders.push(RbcBinder {
                    id: cursor.number()?,
                    display_name: cursor.string()?,
                    lower: cursor.number()?,
                    upper: cursor.number()?,
                    step: cursor.number()?,
                });
            }
            model.domains.push(RbcDomain {
                id, binders, parent, extents, scalar_count,
                provenance: cursor.provenance()?,
            });
        } else if let Some(rest) = head.strip_prefix('^') {
            let id = ExprId(rest.parse().map_err(|_|
                TextError::at(number, "bad expression id"))?);
            cursor.expect("expr")?;
            let value_type = TypeId(cursor.id('$')?);
            let kind = cursor.word()?;
            let node = match kind {
                "lit" => {
                    let which = cursor.word()?;
                    RbcExprNode::Literal {
                        value: match which {
                            "real" => RbcLiteral::Real {
                                value: parse_real(cursor.word()?, number)? },
                            "integer" => RbcLiteral::Integer { value: cursor.number()? },
                            "enum" => RbcLiteral::Enumeration { ordinal: cursor.number()? },
                            "boolean" => RbcLiteral::Boolean {
                                value: cursor.word()? == "true" },
                            "string" => RbcLiteral::String { value: cursor.string()? },
                            other => return Err(TextError::at(number,
                                format!("unknown literal kind `{other}`"))),
                        },
                    }
                }
                "coord" => RbcExprNode::Coordinate {
                    coordinate: parse_coordinate(&mut cursor)? },
                "un" => RbcExprNode::Unary {
                    op: parse_unary(cursor.word()?, number)?,
                    operand: ExprId(cursor.id('^')?) },
                "bin" => RbcExprNode::Binary {
                    op: parse_binary(cursor.word()?, number)?,
                    lhs: ExprId(cursor.id('^')?), rhs: ExprId(cursor.id('^')?) },
                "cond" => {
                    let count: usize = cursor.number()?;
                    let mut branches = Vec::with_capacity(count);
                    for _ in 0..count {
                        branches.push(RbcBranch {
                            condition: ExprId(cursor.id('^')?),
                            value: ExprId(cursor.id('^')?),
                        });
                    }
                    cursor.expect("else")?;
                    RbcExprNode::Conditional { branches, fallback: ExprId(cursor.id('^')?) }
                }
                "call" => {
                    let name = cursor.string()?;
                    let count: usize = cursor.number()?;
                    let mut arguments = Vec::with_capacity(count);
                    for _ in 0..count {
                        arguments.push(ExprId(cursor.id('^')?));
                    }
                    RbcExprNode::Builtin { name, arguments }
                }
                "array" => {
                    let count: usize = cursor.number()?;
                    let empty_type = cursor.eat("of").then(|| cursor.id('$')).transpose()?
                        .map(TypeId);
                    let mut elements = Vec::with_capacity(count);
                    for _ in 0..count {
                        elements.push(ExprId(cursor.id('^')?));
                    }
                    RbcExprNode::Array { elements, empty_type }
                }
                "record" => {
                    let ty = TypeId(cursor.id('$')?);
                    let count: usize = cursor.number()?;
                    let mut fields = Vec::with_capacity(count);
                    for _ in 0..count {
                        fields.push(ExprId(cursor.id('^')?));
                    }
                    RbcExprNode::Record { ty, fields }
                }
                "field" => RbcExprNode::Field {
                    base: ExprId(cursor.id('^')?), field: cursor.number()? },
                "range" => {
                    let start = ExprId(cursor.id('^')?);
                    let step = if cursor.eat("step") {
                        Some(ExprId(cursor.id('^')?))
                    } else {
                        cursor.expect("nostep")?;
                        None
                    };
                    RbcExprNode::Range { start, step, stop: ExprId(cursor.id('^')?) }
                }
                "comp" => RbcExprNode::Comprehension {
                    domain: DomainId(cursor.id('&')?), body: ExprId(cursor.id('^')?) },
                "index" => {
                    let base = ExprId(cursor.id('^')?);
                    RbcExprNode::Index { base, subscripts: parse_subscripts(&mut cursor)? }
                }
                "update" => {
                    let base = ExprId(cursor.id('^')?);
                    let value = ExprId(cursor.id('^')?);
                    RbcExprNode::ArrayUpdate {
                        base, value, subscripts: parse_subscripts(&mut cursor)? }
                }
                "invoke" => {
                    let function = FunctionId(cursor.id('~')?);
                    cursor.expect("out")?;
                    let output = cursor.number()?;
                    cursor.expect("owner")?;
                    let owner = ExprId(cursor.id('^')?);
                    let count: usize = cursor.number()?;
                    let mut arguments = Vec::with_capacity(count);
                    for _ in 0..count {
                        arguments.push(ExprId(cursor.id('^')?));
                    }
                    RbcExprNode::Call { owner, function, output, arguments }
                }
                "unsupported" => RbcExprNode::Unsupported { detail: cursor.string()? },
                other => return Err(TextError::at(number,
                    format!("unknown expression kind `{other}`"))),
            };
            model.expressions.push(RbcExpr {
                id, value_type, node, provenance: cursor.provenance()? });
        } else {
            match head.as_str() {
                "rbc" => file.bitcode_version = cursor.number()?,
                "producer" => file.producer = cursor.string()?,
                "model" => model.name = cursor.string()?,
                "eq" => model.equations.push(parse_equation(&mut cursor)?),
                "ieq" => model.initial_equations.push(parse_equation(&mut cursor)?),
                "family" | "ifamily" => {
                    let id = FamilyId(cursor.number()?);
                    cursor.expect("domain")?;
                    let domain = DomainId(cursor.id('&')?);
                    cursor.expect("rows")?;
                    let scalar_rows = cursor.number()?;
                    cursor.expect("extents")?;
                    let raw = cursor.word()?;
                    let extents = if raw == "-" {
                        Vec::new()
                    } else {
                        raw.split(',')
                            .map(|p| p.parse().map_err(|_| TextError::at(
                                number, format!("bad extent `{p}`"))))
                            .collect::<Result<Vec<u32>, _>>()?
                    };
                    cursor.expect("view")?;
                    let scalar_view = match cursor.word()? {
                        "binder" => RbcScalarView::BinderSubstitution,
                        "rowmajor" => RbcScalarView::RowMajorProjection,
                        "prefix" => RbcScalarView::BinderPrefixProjection {
                            binder_count: cursor.number()?,
                        },
                        other => return Err(TextError::at(number,
                            format!("unknown scalar view `{other}`"))),
                    };
                    cursor.expect("bodies")?;
                    let count: usize = cursor.number()?;
                    let mut bodies = Vec::with_capacity(count);
                    for _ in 0..count {
                        bodies.push(ExprId(cursor.id('^')?));
                    }
                    let mut reads = Vec::new();
                    let mut reads_derivative = Vec::new();
                    if cursor.eat("reads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads.push(VariableId(cursor.id('%')?));
                        }
                    }
                    if cursor.eat("dreads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads_derivative.push(VariableId(cursor.id('%')?));
                        }
                    }
                    let mut reads_previous = Vec::new();
                    if cursor.eat("preads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads_previous.push(VariableId(cursor.id('%')?));
                        }
                    }
                    let family = RbcEquationFamily {
                        id, domain, bodies, scalar_rows, extents, scalar_view,
                        reads, reads_derivative, reads_previous,
                        provenance: cursor.provenance()?,
                    };
                    if head == "family" {
                        model.equation_families.push(family);
                    } else {
                        model.initial_equation_families.push(family);
                    }
                }
                "dreq" => {
                    let id = EquationId(cursor.number()?);
                    let residual = ExprId(cursor.id('^')?);
                    let activation = if cursor.eat("always") {
                        RbcDiscreteRealActivation::Always
                    } else {
                        cursor.expect("when")?;
                        let trigger = ConditionId(cursor.id('?')?);
                        cursor.expect("guard")?;
                        RbcDiscreteRealActivation::When {
                            trigger, guard: ConditionId(cursor.id('?')?) }
                    };
                    let mut reads = Vec::new();
                    let mut reads_derivative = Vec::new();
                    if cursor.eat("reads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads.push(VariableId(cursor.id('%')?));
                        }
                    }
                    if cursor.eat("dreads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads_derivative.push(VariableId(cursor.id('%')?));
                        }
                    }
                    let mut reads_previous = Vec::new();
                    if cursor.eat("preads") {
                        while cursor.peek().is_some_and(|t| t.starts_with('%')) {
                            reads_previous.push(VariableId(cursor.id('%')?));
                        }
                    }
                    model.discrete_real_equations.push(RbcDiscreteRealEquation {
                        id, residual, activation, reads, reads_derivative,
                        reads_previous,
                        provenance: cursor.provenance()?,
                    });
                }
                "idval" => model.initial_discrete_values.push(RbcInitialDiscreteValue {
                    target: VariableId(cursor.id('%')?),
                    value: ExprId(cursor.id('^')?),
                    provenance: cursor.provenance()?,
                }),
                "rel" => model.relations.push(RbcRelation {
                    id: RelationId(cursor.number()?),
                    expression: ExprId(cursor.id('^')?),
                    provenance: cursor.provenance()?,
                }),
                "cond" => {
                    let id = ConditionId(cursor.number()?);
                    let kind = cursor.word()?;
                    use RbcConditionNode::*;
                    let node = match kind {
                        "initial" => Initial,
                        "always" => Always,
                        "clock" => Clock,
                        "rel" => Relation { relation: RelationId(cursor.number()?) },
                        "discrete" => Discrete { expression: ExprId(cursor.id('^')?) },
                        "not" => Not { operand: ConditionId(cursor.number()?) },
                        "and" => And { lhs: ConditionId(cursor.number()?),
                                       rhs: ConditionId(cursor.number()?) },
                        "or" => Or { lhs: ConditionId(cursor.number()?),
                                     rhs: ConditionId(cursor.number()?) },
                        "any_rise" => AnyRise { lhs: ConditionId(cursor.number()?),
                                                rhs: ConditionId(cursor.number()?) },
                        "unsupported" => Unsupported { detail: cursor.string()? },
                        other => return Err(TextError::at(number,
                            format!("unknown condition `{other}`"))),
                    };
                    model.conditions.push(RbcCondition {
                        id, node, provenance: cursor.provenance()? });
                }
                "root" => {
                    let id = RootId(cursor.number()?);
                    cursor.expect("rel")?;
                    let relation = RelationId(cursor.number()?);
                    cursor.expect("act")?;
                    let activation = ConditionId(cursor.number()?);
                    model.roots.push(RbcRoot {
                        id, relation, activation, provenance: cursor.provenance()? });
                }
                "event" => {
                    let id = EventId(cursor.number()?);
                    cursor.expect("trig")?;
                    let trigger = ConditionId(cursor.number()?);
                    cursor.expect("guard")?;
                    let guard = ConditionId(cursor.number()?);
                    let action = match cursor.word()? {
                        "reinit" => RbcAction::Reinitialize {
                            state: VariableId(cursor.id('%')?),
                            value: ExprId(cursor.id('^')?) },
                        "assert" => {
                            let message = ExprId(cursor.id('^')?);
                            let level = if cursor.eat("level") {
                                Some(ExprId(cursor.id('^')?))
                            } else { None };
                            RbcAction::Assert { message, level }
                        }
                        "terminate" => RbcAction::Terminate {
                            message: ExprId(cursor.id('^')?) },
                        other => return Err(TextError::at(number,
                            format!("unknown action `{other}`"))),
                    };
                    model.events.push(RbcEventAction {
                        id, trigger, guard, action, provenance: cursor.provenance()? });
                }
                "tevent" => {
                    let id = EventId(cursor.number()?);
                    let schedule = match cursor.word()? {
                        "static" => RbcSchedule::Static {
                            numerator: cursor.number()?, denominator: cursor.number()? },
                        "dynamic" => RbcSchedule::Dynamic {
                            deadline: ExprId(cursor.id('^')?) },
                        other => return Err(TextError::at(number,
                            format!("unknown schedule `{other}`"))),
                    };
                    model.time_events.push(RbcTimeEvent {
                        id, schedule, provenance: cursor.provenance()? });
                }
                "conn" => {
                    let id = ConnectionId(cursor.number()?);
                    let left = VariableId(cursor.id('%')?);
                    let right = VariableId(cursor.id('%')?);
                    let quantity = parse_quantity(cursor.word()?, number)?;
                    let left_connector = cursor.string()?;
                    let right_connector = cursor.string()?;
                    let equation = if cursor.eat("eq") {
                        Some(EquationId(cursor.number()?))
                    } else { None };
                    model.connections.push(RbcConnection {
                        id, left, right, quantity, left_connector, right_connector,
                        equation, provenance: cursor.provenance()? });
                }
                "connset" => {
                    let id = ConnectionSetId(cursor.number()?);
                    let mut connectors = Vec::new();
                    let mut potentials = Vec::new();
                    let mut balances: Vec<RbcFlowBalance> = Vec::new();
                    let mut potential_equations = Vec::new();
                    let mut unconnected = false;
                    // Clauses first, provenance last: it is the one token that
                    // starts with `@`, so the loop stops there rather than
                    // needing to put anything back.
                    while !cursor.peek().is_some_and(|word| word.starts_with('@')) {
                        match cursor.word()? {
                            "at" => connectors.push(cursor.string()?),
                            "pot" => potentials.push(VariableId(cursor.id('%')?)),
                            "balance" => {
                                let equation = if cursor.eat("eq") {
                                    Some(EquationId(cursor.number()?))
                                } else {
                                    None
                                };
                                let mut terms = Vec::new();
                                while !cursor.eat("end") {
                                    let token = cursor.word()?;
                                    let negated = token.starts_with('-');
                                    let digits = token
                                        .trim_start_matches(['+', '-'])
                                        .trim_start_matches('%');
                                    terms.push(RbcFlowTerm {
                                        variable: VariableId(
                                            digits.parse().map_err(|_| {
                                                TextError::at(number,
                                                              "bad flow member")
                                            })?,
                                        ),
                                        negated,
                                    });
                                }
                                balances.push(RbcFlowBalance { equation, terms });
                            }
                            "poteq" => potential_equations
                                .push(EquationId(cursor.number()?)),
                            "unconnected" => unconnected = true,
                            other => {
                                return Err(TextError::at(
                                    number,
                                    format!("unknown connset clause `{other}`"),
                                ))
                            }
                        }
                    }
                    model.connection_sets.push(RbcConnectionSet {
                        id, connectors, potentials, balances,
                        potential_equations, unconnected,
                        provenance: cursor.provenance()? });
                }
                "disc" => {
                    let count: usize = cursor.number()?;
                    cursor.expect("targets")?;
                    let mut targets = Vec::with_capacity(count);
                    for _ in 0..count {
                        targets.push(VariableId(cursor.id('%')?));
                    }
                    open_discrete = Some(RbcDiscreteDefinition {
                        targets, branches: Vec::new(),
                        provenance: placeholder_provenance() });
                }
                "branch" => {
                    let definition = open_discrete.as_mut().ok_or_else(||
                        TextError::at(number, "`branch` outside a `disc` block"))?;
                    let activation = match cursor.word()? {
                        "always" => RbcDiscreteActivation::Always,
                        "when" => RbcDiscreteActivation::When {
                            trigger: ConditionId(cursor.number()?),
                            guard: ConditionId(cursor.number()?) },
                        other => return Err(TextError::at(number,
                            format!("unknown activation `{other}`"))),
                    };
                    cursor.expect("values")?;
                    let count: usize = cursor.number()?;
                    let mut values = Vec::with_capacity(count);
                    for _ in 0..count {
                        values.push(ExprId(cursor.id('^')?));
                    }
                    definition.branches.push(RbcDiscreteBranch {
                        activation, values, provenance: cursor.provenance()? });
                }
                "end" => {
                    let mut definition = open_discrete.take().ok_or_else(||
                        TextError::at(number, "`end` outside a `disc` block"))?;
                    definition.provenance = cursor.provenance()?;
                    model.discrete_definitions.push(definition);
                }
                "trace" => {
                    let id = TracePointId(cursor.number()?);
                    let variable = VariableId(cursor.id('%')?);
                    let label = cursor.string()?;
                    let mut point = RbcTracePoint {
                        id, variable, label, connection: None,
                        connection_set: None, quantity: None,
                        unit: None, added_by: None };
                    while !cursor.done() {
                        match cursor.word()? {
                            "conn" => point.connection =
                                Some(ConnectionId(cursor.number()?)),
                            "connset" => point.connection_set =
                                Some(ConnectionSetId(cursor.number()?)),
                            "kind" => point.quantity =
                                Some(parse_quantity(cursor.word()?, number)?),
                            "unit" => point.unit = Some(cursor.string()?),
                            "added_by" => point.added_by = Some(cursor.string()?),
                            other => return Err(TextError::at(number,
                                format!("unknown trace attribute `{other}`"))),
                        }
                    }
                    model.trace_points.push(point);
                }
                other => return Err(TextError::at(number,
                    format!("unknown statement `{other}`"))),
            }
        }
    }

    if open_discrete.is_some() {
        return Err(TextError::at(text.lines().count(),
            "a `disc` block was never closed by `end`"));
    }

    // The summary is derived, never written: two sources of truth for a count
    // is one source of truth and one way to be wrong.
    crate::validate::recompute_summary(&mut file.model);
    Ok(file)
}
