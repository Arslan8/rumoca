//! Rumoca Bitcode v1 — the public wire schema.
//!
//! This module is the contract external tools depend on. It is deliberately
//! **not** a mirror of any internal Rumoca type: no field here is required to
//! correspond to a Rust struct field in `rumoca-ir-dae`, and the internal
//! `DAE_SCHEMA_VERSION` may change without changing [`RBC_VERSION`].
//!
//! Rules for changing this file:
//!
//! * Adding an optional field, a new enum variant with an explicit tag, or a
//!   new collection is a **compatible** change and does not bump
//!   [`RBC_VERSION`].
//! * Removing a field, renaming a tag, or changing a field's meaning is an
//!   **incompatible** change and bumps [`RBC_VERSION`].
//! * Every enum is externally tagged by an explicit `kind` string, never by
//!   declaration order, so appending or reordering variants cannot silently
//!   change how an older file decodes.

use serde::{Deserialize, Serialize};

/// Container magic. Present so a reader can reject a non-RBC file before
/// attempting to decode it as one.
pub const RBC_MAGIC: &str = "RUMOCA-RBC";

/// Public bitcode contract version. Independent of `DAE_SCHEMA_VERSION`.
pub const RBC_VERSION: u32 = 1;

// ── Identities ───────────────────────────────────────────────────────────────
//
// Every ID is unique within one artifact. IDs are carried as explicit `id`
// fields on each record rather than implied by array position, so a consumer
// never has to assume an index is an identity. They are NOT stable across two
// separate compilations; cross-artifact matching uses names, roles, and types.

macro_rules! rbc_id {
    ($($(#[$doc:meta])* $name:ident),+ $(,)?) => {$(
        $(#[$doc])*
        #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
        #[serde(transparent)]
        pub struct $name(pub u32);

        impl std::fmt::Display for $name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.0)
            }
        }
    )+};
}

rbc_id! {
    /// Identifies a source file within this artifact.
    SourceId,
    /// Identifies a value type within this artifact.
    TypeId,
    /// Identifies a variable within this artifact.
    VariableId,
    /// Identifies an expression node within this artifact.
    ExprId,
    /// Identifies an equation within this artifact.
    EquationId,
    /// Identifies a relation (a primitive comparison) within this artifact.
    RelationId,
    /// Identifies a boolean condition within this artifact.
    ConditionId,
    /// Identifies a zero-crossing root within this artifact.
    RootId,
    /// Identifies an event action within this artifact.
    EventId,
    /// Identifies a connection within this artifact.
    ConnectionId,
    /// Identifies a component instance within this artifact.
    ComponentId,
    /// Identifies a trace point within this artifact.
    TracePointId,
}

// ── Container ────────────────────────────────────────────────────────────────

/// One `.rbc` artifact.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcFile {
    /// Always [`RBC_MAGIC`].
    pub magic: String,
    /// Public contract version. See [`RBC_VERSION`].
    pub bitcode_version: u32,
    /// Free-form producer identification, e.g. `"rumoca 0.10.0"`. Informational
    /// only: a consumer must not change behaviour based on it.
    pub producer: String,
    /// The compiled model.
    pub model: RbcModel,
}

/// A compiled Modelica model in public form.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcModel {
    /// Top-level model name as compiled, e.g. `"Circuit.Test"`.
    pub name: String,
    /// Source files referenced by provenance in this artifact.
    pub sources: Vec<RbcSource>,
    /// Value types referenced by variables and expressions.
    pub types: Vec<RbcType>,
    /// Every variable in the model, in every role.
    pub variables: Vec<RbcVariable>,
    /// Flat expression arena. Operands reference earlier entries by [`ExprId`].
    pub expressions: Vec<RbcExpr>,
    /// Continuous residual equations: each asserts `residual == 0`.
    pub equations: Vec<RbcEquation>,
    /// Initialization residual equations.
    pub initial_equations: Vec<RbcEquation>,
    /// Primitive comparisons that can generate events.
    pub relations: Vec<RbcRelation>,
    /// Boolean activation conditions over relations, clocks and discretes.
    pub conditions: Vec<RbcCondition>,
    /// Zero-crossing surfaces the solver must monitor.
    pub roots: Vec<RbcRoot>,
    /// Actions performed when an event fires.
    pub events: Vec<RbcEventAction>,
    /// Scheduled (time-triggered) events.
    pub time_events: Vec<RbcTimeEvent>,
    /// Connector-level provenance recovered from flattening.
    pub connections: Vec<RbcConnection>,
    /// Component instances referenced by connections and variables.
    pub components: Vec<RbcComponent>,
    /// Observation requests. Empty on export; a transformation pass adds these.
    #[serde(default)]
    pub trace_points: Vec<RbcTracePoint>,
    /// MLS Appendix B.1c definitions: what each discrete-valued variable
    /// (Boolean, Integer, enumeration) is equal to, and under what activation.
    ///
    /// Separate from `equations`, which carries only continuous residuals, and
    /// from `events`, which carries reinit/assert/terminate actions. Without
    /// this a `discrete_value` variable is declared and never defined, and
    /// reconstruction rejects the artifact.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub discrete_definitions: Vec<RbcDiscreteDefinition>,
    /// Counts a consumer can check against the collections above. Present so a
    /// truncated or partially-written artifact fails loudly.
    pub summary: RbcSummary,
}

/// Denormalised counts, for cheap validation and for `bitcode inspect`.
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcSummary {
    pub variables: u32,
    pub states: u32,
    pub parameters: u32,
    pub constants: u32,
    pub inputs: u32,
    pub outputs: u32,
    pub algebraics: u32,
    pub discrete_reals: u32,
    pub discrete_values: u32,
    pub equations: u32,
    pub initial_equations: u32,
    pub expressions: u32,
    pub relations: u32,
    pub conditions: u32,
    pub roots: u32,
    pub events: u32,
    pub time_events: u32,
    pub connections: u32,
    pub components: u32,
    pub trace_points: u32,
    #[serde(default)]
    pub discrete_definitions: u32,
}

// ── Provenance ───────────────────────────────────────────────────────────────

/// One source file.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcSource {
    pub id: SourceId,
    /// Path or logical name as Rumoca saw it.
    pub name: String,
    /// Full source text, when the producer was asked to embed it. Absent keeps
    /// artifacts small; present makes them self-contained.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub text: Option<String>,
}

/// A resolved source location. Byte offsets are authoritative; line and column
/// are precomputed at export time so consumers never need the source text to
/// report `Model.mo:52`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcSpan {
    pub source: SourceId,
    pub start: u32,
    pub end: u32,
    /// 1-based line of `start`.
    pub line: u32,
    /// 1-based column of `start`.
    pub column: u32,
}

/// Why a model object exists and where it came from.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcProvenance {
    pub origin: RbcOrigin,
    pub span: RbcSpan,
}

/// Whether an object was written by the author or produced by lowering.
///
/// `Generated` carries the lowering kind so a consumer can distinguish a
/// connection equation from a flow balance without guessing from shape.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcOrigin {
    /// Written in the source at `span`.
    Source,
    /// Produced by the compiler; `span` names the nearest responsible source.
    Generated { generation: RbcGeneration },
}

/// Lowering kinds a consumer may care about. Mirrors the compiler's own
/// classification; `Other` keeps a v1 reader working against a producer that
/// learns a new kind.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcGeneration {
    SyntheticResidual,
    BindingEquation,
    ConnectionEquation,
    FlowBalanceEquation,
    AlgorithmEquation,
    DiscreteUpdate,
    ConditionLowering,
    PreValueLowering,
    ClockLowering,
    DelayLowering,
    SemiLinearLowering,
    TerminalLowering,
    EventActionLowering,
    InitializationEquation,
    DefaultStart,
    ArrayEquationProjection,
    RecordEquationProjection,
    FunctionLoopLowering,
    FunctionConditionLowering,
    FunctionAggregateLowering,
    DerivedParameterLowering,
    IndexReduction,
    AliasElimination,
    RuntimeDiscontinuity,
    /// A lowering kind this schema version does not name.
    Other,
}

// ── Types ────────────────────────────────────────────────────────────────────

/// A value type: a scalar, or a rectangular array of one.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcType {
    pub id: TypeId,
    pub scalar: RbcScalar,
    /// Empty for a scalar; otherwise the array extents in row-major order.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub dimensions: Vec<u32>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcScalar {
    Real,
    Integer,
    Boolean,
    String,
    Enumeration,
}

// ── Variables ────────────────────────────────────────────────────────────────

/// Appendix-B partition a variable belongs to.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcRole {
    Parameter,
    Constant,
    Input,
    State,
    Algebraic,
    Output,
    DiscreteReal,
    DiscreteValue,
}

/// Interface causality, orthogonal to [`RbcRole`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcCausality {
    Input,
    Output,
    Parameter,
    CalculatedParameter,
    Independent,
    Local,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcVariable {
    pub id: VariableId,
    /// Fully-qualified flattened name, e.g. `"motor.flange.tau"`.
    pub name: String,
    pub role: RbcRole,
    pub causality: RbcCausality,
    pub value_type: TypeId,
    /// Number of scalars this variable expands to (1 for a scalar).
    pub scalar_count: u32,
    pub declaration: RbcProvenance,
    /// Component instance this variable belongs to, when it is inside one.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub component: Option<ComponentId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub unit: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    /// Declaration binding expression, when the source gave one.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub binding: Option<ExprId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub start: Option<ExprId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub min: Option<ExprId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub max: Option<ExprId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub nominal: Option<ExprId>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub fixed: Option<bool>,
    #[serde(default)]
    pub tunable: bool,
    /// True when the variable was written in the source rather than generated.
    #[serde(default)]
    pub from_source: bool,
    /// Connector semantics recovered from flattening, when this variable is a
    /// connector member.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub connector: Option<RbcConnectorMember>,
}

/// Modelica connector semantics for one variable.
///
/// A `flow` member obeys a sum-to-zero conservation law; a `potential` member
/// is equated across a connection. Preserving this distinction is why
/// connections are not modelled as directional messages.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcConnectorMember {
    pub quantity: RbcQuantityKind,
    /// True when this member participates in at least one `connect(...)`.
    pub connected: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcQuantityKind {
    /// Equated across a connection (voltage, angle, temperature).
    Potential,
    /// Conserved across a connection; signed sum is zero (current, torque).
    Flow,
    /// Stream variable (MLS §15).
    Stream,
}

// ── Components and connections ───────────────────────────────────────────────

/// One component instance, identified by its flattened path prefix.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcComponent {
    pub id: ComponentId,
    /// Dotted instance path, e.g. `"motor"` or `"drive.motor"`. Empty for the
    /// top-level model itself.
    pub path: String,
}

/// One `connect(...)` relationship recovered from flattening.
///
/// A connection is an equality between two connector endpoints, plus the
/// conservation law over the flow members of the connection set. It is **not**
/// a directional message: `left` and `right` are symmetric.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcConnection {
    pub id: ConnectionId,
    /// Endpoint variable on one side.
    pub left: VariableId,
    /// Endpoint variable on the other side.
    pub right: VariableId,
    /// Physical role of the quantity being connected.
    pub quantity: RbcQuantityKind,
    /// Connector instance paths, e.g. `("battery.pin", "motor.pin")`.
    pub left_connector: String,
    pub right_connector: String,
    /// Equation this connection produced, when one was generated.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub equation: Option<EquationId>,
    pub provenance: RbcProvenance,
}

// ── Expressions ──────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcExpr {
    pub id: ExprId,
    pub value_type: TypeId,
    pub node: RbcExprNode,
    pub provenance: RbcProvenance,
}

/// Expression node. Operands always reference nodes with a **lower** [`ExprId`],
/// so the arena is a DAG in topological order and can be evaluated in one pass.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcExprNode {
    Literal {
        value: RbcLiteral,
    },
    Coordinate {
        coordinate: RbcCoordinate,
    },
    Unary {
        op: RbcUnaryOp,
        operand: ExprId,
    },
    Binary {
        op: RbcBinaryOp,
        lhs: ExprId,
        rhs: ExprId,
    },
    /// `if c1 then v1 elseif c2 then v2 else fallback`. Branches are evaluated
    /// in order; `fallback` is required, so the node is total.
    Conditional {
        branches: Vec<RbcBranch>,
        fallback: ExprId,
    },
    /// A pure built-in call: `sqrt(x)`, `log(x)`, `abs(x)`, `min(a, b)`, ...
    ///
    /// `name` is the Modelica spelling in lower case, so a consumer matches on
    /// `"sqrt"` rather than on an enum ordinal that could shift.
    Builtin {
        name: String,
        arguments: Vec<ExprId>,
    },
    /// A node this schema version cannot represent. A consumer must treat the
    /// containing model as not fully understood rather than assume a default.
    /// Producers only emit this when explicitly asked to tolerate gaps.
    Unsupported {
        detail: String,
    },
}

/// One `condition -> value` arm of a conditional expression.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct RbcBranch {
    pub condition: ExprId,
    pub value: ExprId,
}

/// One MLS Appendix B.1c definition owner: a set of discrete-valued targets
/// defined together, and the branches that give them values.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RbcDiscreteDefinition {
    /// The discrete-valued variables this owner defines, in the order the
    /// branches' `values` follow.
    pub targets: Vec<VariableId>,
    pub branches: Vec<RbcDiscreteBranch>,
    pub provenance: RbcProvenance,
}

/// One activation branch of a B.1c definition. `values` has exactly one entry
/// per target of the owning definition, in the same order.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RbcDiscreteBranch {
    pub activation: RbcDiscreteActivation,
    pub values: Vec<ExprId>,
    pub provenance: RbcProvenance,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcDiscreteActivation {
    /// A plain equation, active whenever the model is: `b = x < 0.5`.
    Always,
    /// A `when` branch, active on its trigger under its guard.
    When {
        trigger: ConditionId,
        guard: ConditionId,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcLiteral {
    Real { value: f64 },
    Integer { value: i64 },
    /// An enumeration value, carried as its 1-based ordinal (MLS §4.9.5).
    ///
    /// This is distinct from `Integer` even though both hold an integer: the
    /// DAE's type checker demands an `Enumeration` where the declaration says
    /// enumeration, and rebuilding one from an `Integer` literal is rejected
    /// with `expected Enumeration, found Integer`.
    Enumeration { ordinal: i64 },
    Boolean { value: bool },
    String { value: String },
}

/// A leaf referencing a model quantity. This is how expressions name
/// variables — never by string.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcCoordinate {
    Parameter {
        variable: VariableId,
    },
    Input {
        variable: VariableId,
    },
    State {
        variable: VariableId,
    },
    /// `der(x)` for state `variable`.
    Derivative {
        variable: VariableId,
    },
    Algebraic {
        variable: VariableId,
    },
    DiscreteReal {
        variable: VariableId,
    },
    DiscreteValue {
        variable: VariableId,
    },
    PreState {
        variable: VariableId,
    },
    PreAlgebraic {
        variable: VariableId,
    },
    PreDiscreteReal {
        variable: VariableId,
    },
    PreDiscreteValue {
        variable: VariableId,
    },
    /// Simulation time.
    Time,
}

impl RbcCoordinate {
    /// The variable this coordinate reads, if any. `Time` reads none.
    pub fn variable(self) -> Option<VariableId> {
        match self {
            Self::Parameter { variable }
            | Self::Input { variable }
            | Self::State { variable }
            | Self::Derivative { variable }
            | Self::Algebraic { variable }
            | Self::DiscreteReal { variable }
            | Self::DiscreteValue { variable }
            | Self::PreState { variable }
            | Self::PreAlgebraic { variable }
            | Self::PreDiscreteReal { variable }
            | Self::PreDiscreteValue { variable } => Some(variable),
            Self::Time => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcUnaryOp {
    Negate,
    Not,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RbcBinaryOp {
    Add,
    Subtract,
    Multiply,
    Divide,
    Power,
    Equal,
    NotEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    And,
    Or,
}

// ── Equations ────────────────────────────────────────────────────────────────

/// A residual equation: the model asserts `residual == 0`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcEquation {
    pub id: EquationId,
    pub residual: ExprId,
    pub provenance: RbcProvenance,
    /// Variables this equation reads, precomputed by the compiler's own
    /// dependency projection. A consumer must not have to re-derive these by
    /// walking expressions.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reads: Vec<VariableId>,
    /// States whose derivative this equation reads, i.e. `der(x)` occurrences.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub reads_derivative: Vec<VariableId>,
}

// ── Events ───────────────────────────────────────────────────────────────────

/// A primitive comparison that can generate an event.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcRelation {
    pub id: RelationId,
    pub expression: ExprId,
    pub provenance: RbcProvenance,
}

/// Boolean activation condition.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcCondition {
    pub id: ConditionId,
    pub node: RbcConditionNode,
    pub provenance: RbcProvenance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcConditionNode {
    /// True during initialization only.
    Initial,
    /// Always active; the section is not a `when` at all.
    Always,
    Relation {
        relation: RelationId,
    },
    Discrete {
        expression: ExprId,
    },
    Not {
        operand: ConditionId,
    },
    And {
        lhs: ConditionId,
        rhs: ConditionId,
    },
    Or {
        lhs: ConditionId,
        rhs: ConditionId,
    },
    /// MLS §8.3.5 vector activation: fires when any element rises.
    AnyRise {
        lhs: ConditionId,
        rhs: ConditionId,
    },
    /// Clocked activation this schema version does not detail.
    Clock,
    Unsupported {
        detail: String,
    },
}

/// A zero-crossing surface the solver monitors.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcRoot {
    pub id: RootId,
    pub relation: RelationId,
    pub activation: ConditionId,
    pub provenance: RbcProvenance,
}

/// Something the model does when an event fires.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcEventAction {
    pub id: EventId,
    pub trigger: ConditionId,
    pub guard: ConditionId,
    pub action: RbcAction,
    pub provenance: RbcProvenance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcAction {
    /// `reinit(state, value)`.
    Reinitialize {
        state: VariableId,
        value: ExprId,
    },
    Assert {
        message: ExprId,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        level: Option<ExprId>,
    },
    Terminate {
        message: ExprId,
    },
}

/// A scheduled event.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcTimeEvent {
    pub id: EventId,
    pub schedule: RbcSchedule,
    pub provenance: RbcProvenance,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum RbcSchedule {
    /// Fires at a fixed instant, as an exact rational `numerator/denominator`.
    Static { numerator: i64, denominator: i64 },
    /// Fires at a time computed by an expression.
    Dynamic { deadline: ExprId },
}

// ── Instrumentation ──────────────────────────────────────────────────────────

/// A request to observe a value at runtime.
///
/// Trace points are **observation metadata**, deliberately separate from the
/// physical equations. Adding one does not change model semantics, which is why
/// an instrumentation pass does not need to rewrite equations.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RbcTracePoint {
    pub id: TracePointId,
    /// The variable to observe.
    pub variable: VariableId,
    /// Human-readable label for the trace output.
    pub label: String,
    /// Connection this observation belongs to, when it came from connector
    /// instrumentation.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub connection: Option<ConnectionId>,
    /// Physical role of the observed quantity, when known.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub quantity: Option<RbcQuantityKind>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub unit: Option<String>,
    /// Tool that added this trace point, for provenance of the instrumentation
    /// itself.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub added_by: Option<String>,
}

impl RbcFile {
    /// Reject a file that is not RBC, or is a version this build cannot read.
    pub fn check_header(&self) -> Result<(), String> {
        if self.magic != RBC_MAGIC {
            return Err(format!(
                "not a Rumoca Bitcode file: magic is {:?}, expected {RBC_MAGIC:?}",
                self.magic
            ));
        }
        if self.bitcode_version != RBC_VERSION {
            return Err(format!(
                "unsupported bitcode version {}: this build reads version {RBC_VERSION}",
                self.bitcode_version
            ));
        }
        Ok(())
    }
}
