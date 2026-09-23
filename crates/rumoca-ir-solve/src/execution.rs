//! Public RBC execution v1: a deliberately bounded scalar Solve projection.
//! This is not the private Solve wire. Certificates, caches, byte offsets and
//! differentiated programs are reconstructed by the lowering owner.
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
mod validate;
pub use validate::validate;

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExecutionArtifact {
    pub version: u32,
    pub equation_digest: String,
    pub lowering: String,
    pub revision: u64,
    pub passes: Vec<serde_json::Value>,
    pub numerical: NumericalProgram,
    pub functions: BTreeMap<String, Vec<Instruction>>,
    pub sinks: Vec<CsvSink>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct NumericalProgram {
    /// Virtual source owner for generated executable instructions.
    pub source_name: String,
    pub storage: Vec<Storage>,
    pub residual: Vec<Row>,
    pub derivatives: Vec<Row>,
    pub initialization: Vec<Row>,
    pub algebraic_blocks: Vec<Projection>,
    pub initial_blocks: Vec<Projection>,
    pub observations: Vec<Observation>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Storage {
    pub name: String,
    pub role: String,
    pub causality: String,
    pub index: usize,
    pub start: f64,
    pub nominal: f64,
    pub unit: Option<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Row {
    pub output: usize,
    pub target: Option<usize>,
    pub instructions: Vec<ScalarOp>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Projection {
    pub rows: Vec<usize>,
    pub unknowns: Vec<usize>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Observation {
    pub variable_id: u32,
    pub name: String,
    pub instructions: Vec<ScalarOp>,
}

/// Operand/register semantics are exactly those of canonical Solve LinearOp.
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case", deny_unknown_fields)]
pub enum ScalarOp {
    Const {
        dst: u32,
        value: f64,
    },
    LoadTime {
        dst: u32,
    },
    LoadY {
        dst: u32,
        index: usize,
    },
    LoadP {
        dst: u32,
        index: usize,
    },
    Unary {
        dst: u32,
        operator: String,
        src: u32,
    },
    Binary {
        dst: u32,
        operator: String,
        lhs: u32,
        rhs: u32,
    },
    Compare {
        dst: u32,
        operator: String,
        lhs: u32,
        rhs: u32,
    },
    Select {
        dst: u32,
        cond: u32,
        if_true: u32,
        if_false: u32,
    },
    StoreOutput {
        src: u32,
    },
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CsvSink {
    pub key: String,
    pub filename: String,
    pub columns: Vec<String>,
    pub column_types: Vec<String>,
    pub metadata: serde_json::Value,
}

/// All effects are sequential. Branch regions and calls preserve that order;
/// none of these operations may be treated as an unused pure expression.
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(tag = "op", deny_unknown_fields)]
pub enum Instruction {
    #[serde(rename = "snapshot.time")]
    Time { result: String },
    #[serde(rename = "snapshot.sequence")]
    Sequence { result: String },
    #[serde(rename = "snapshot.phase")]
    Phase { result: String },
    #[serde(rename = "snapshot.value")]
    Value { result: String, variable_id: u32 },
    /// Existing Solve evaluator; LoadY reads the explicit numeric arguments.
    #[serde(rename = "compute")]
    Compute {
        result: String,
        arguments: Vec<String>,
        instructions: Vec<ScalarOp>,
    },
    #[serde(rename = "csv.open")]
    Open { sink: String },
    #[serde(rename = "csv.write_row")]
    Write { sink: String, values: Vec<String> },
    #[serde(rename = "csv.close")]
    Close { sink: String },
    #[serde(rename = "if")]
    If {
        condition: String,
        then_body: Vec<Instruction>,
        else_body: Vec<Instruction>,
    },
    #[serde(rename = "call")]
    Call { function: String },
    #[serde(rename = "assert")]
    Assert { condition: String, message: String },
}

impl ScalarOp {
    pub fn from_solve(op: &crate::LinearOp) -> Result<Self, String> {
        use crate::LinearOp as L;
        Ok(match op {
            L::Const { dst, value } => Self::Const {
                dst: *dst,
                value: *value,
            },
            L::LoadTime { dst } => Self::LoadTime { dst: *dst },
            L::LoadY { dst, index } => Self::LoadY {
                dst: *dst,
                index: *index,
            },
            L::LoadP { dst, index } => Self::LoadP {
                dst: *dst,
                index: *index,
            },
            L::Unary { dst, op, arg } => Self::Unary {
                dst: *dst,
                operator: op.kind_name().into(),
                src: *arg,
            },
            L::Binary { dst, op, lhs, rhs } => Self::Binary {
                dst: *dst,
                operator: op.kind_name().into(),
                lhs: *lhs,
                rhs: *rhs,
            },
            L::Compare { dst, op, lhs, rhs } => Self::Compare {
                dst: *dst,
                operator: op.kind_name().into(),
                lhs: *lhs,
                rhs: *rhs,
            },
            L::Select {
                dst,
                cond,
                if_true,
                if_false,
            } => Self::Select {
                dst: *dst,
                cond: *cond,
                if_true: *if_true,
                if_false: *if_false,
            },
            L::StoreOutput { src } => Self::StoreOutput { src: *src },
            other => {
                return Err(format!(
                    "execution v1 unsupported Solve operation: {}",
                    other.kind_name()
                ));
            }
        })
    }

    pub fn to_solve(&self) -> Result<crate::LinearOp, String> {
        use crate::LinearOp as L;
        fn operator<T: serde::de::DeserializeOwned>(name: &str) -> Result<T, String> {
            serde_json::from_value(serde_json::Value::String(name.into()))
                .map_err(|e| e.to_string())
        }
        Ok(match self {
            Self::Const { dst, value } => L::Const {
                dst: *dst,
                value: *value,
            },
            Self::LoadTime { dst } => L::LoadTime { dst: *dst },
            Self::LoadY { dst, index } => L::LoadY {
                dst: *dst,
                index: *index,
            },
            Self::LoadP { dst, index } => L::LoadP {
                dst: *dst,
                index: *index,
            },
            Self::Unary {
                dst,
                operator: op,
                src,
            } => L::Unary {
                dst: *dst,
                op: operator(op)?,
                arg: *src,
            },
            Self::Binary {
                dst,
                operator: op,
                lhs,
                rhs,
            } => L::Binary {
                dst: *dst,
                op: operator(op)?,
                lhs: *lhs,
                rhs: *rhs,
            },
            Self::Compare {
                dst,
                operator: op,
                lhs,
                rhs,
            } => L::Compare {
                dst: *dst,
                op: operator(op)?,
                lhs: *lhs,
                rhs: *rhs,
            },
            Self::Select {
                dst,
                cond,
                if_true,
                if_false,
            } => L::Select {
                dst: *dst,
                cond: *cond,
                if_true: *if_true,
                if_false: *if_false,
            },
            Self::StoreOutput { src } => L::StoreOutput { src: *src },
        })
    }
}

pub fn checked_scalar(
    ops: &[ScalarOp],
    y: usize,
    p: usize,
) -> Result<Vec<crate::LinearOp>, String> {
    if ops
        .iter()
        .filter(|o| matches!(o, ScalarOp::StoreOutput { .. }))
        .count()
        != 1
    {
        return Err("scalar program must store exactly one output".into());
    }
    if !matches!(ops.last(), Some(ScalarOp::StoreOutput { .. })) {
        return Err("scalar program must end with its output store".into());
    }
    for op in ops {
        let dst = match op {
            ScalarOp::Const { dst, .. }
            | ScalarOp::LoadTime { dst }
            | ScalarOp::LoadY { dst, .. }
            | ScalarOp::LoadP { dst, .. }
            | ScalarOp::Unary { dst, .. }
            | ScalarOp::Binary { dst, .. }
            | ScalarOp::Compare { dst, .. }
            | ScalarOp::Select { dst, .. } => Some(*dst),
            ScalarOp::StoreOutput { .. } => None,
        };
        if dst.is_some_and(|d| d as usize >= ops.len()) {
            return Err("register exceeds scalar program size".into());
        }
        match op {
            ScalarOp::LoadY { index, .. } if *index >= y => {
                return Err("LoadY outside storage".into());
            }
            ScalarOp::LoadP { index, .. } if *index >= p => {
                return Err("LoadP outside storage".into());
            }
            ScalarOp::Const { value, .. } if !value.is_finite() => {
                return Err("non-finite constant".into());
            }
            _ => {}
        }
    }
    let row = ops
        .iter()
        .map(ScalarOp::to_solve)
        .collect::<Result<Vec<_>, _>>()?;
    let span = rumoca_core::Span::from_offsets(
        rumoca_core::SourceId::from_source_name("rbc:execution/scalar-check"),
        0,
        0,
    );
    crate::ScalarProgramBlock::with_program_spans(vec![row.clone()], vec![span])
        .map_err(|e| e.to_string())?;
    Ok(row)
}
