//! Namespaced, disjoint linking of public equation artifacts.
//!
//! This is an interchange operation, not DAE structural lowering (SPEC_0007).
//! It preserves equations, boundaries and provenance; it never guesses wiring.

mod expressions;
mod records;
#[cfg(test)]
mod tests;

use std::collections::BTreeSet;

use crate::schema::*;
use crate::validate::{ValidateOptions, recompute_summary, validate};

/// One module instance. The same artifact may be linked under different names.
pub struct LinkInput<'a> {
    pub namespace: &'a str,
    pub file: &'a RbcFile,
}

#[derive(Debug, thiserror::Error)]
#[error("bitcode link: {0}")]
pub struct LinkError(pub String);

type Result<T> = std::result::Result<T, LinkError>;

/// Link independent modules without mutating inputs or inferring connections.
///
/// Namespaces must be distinct simple identifiers. Execution projections are
/// rejected unless `discard_execution` explicitly authorizes their removal,
/// including numerical edits and instrumentation. The result must be lowered
/// again before execution. A successful link proves structural consistency,
/// not solvability or runtime support.
pub fn link(name: &str, inputs: &[LinkInput<'_>], discard_execution: bool) -> Result<RbcFile> {
    if name.trim().is_empty() || inputs.is_empty() {
        return Err(LinkError(
            "a model name and at least one input are required".into(),
        ));
    }
    let mut names = BTreeSet::new();
    let mut model = crate::build::Builder::new(name).finish();
    // Builder seeds a source and types; a link uses only the input tables.
    model.sources.clear();
    model.types.clear();
    for input in inputs {
        check_input(input, discard_execution, &mut names)?;
        let map = Map::new(&model, &input.file.model, input.namespace)?;
        let mut part = input.file.model.clone();
        map.relocate(&mut part)?;
        append(&mut model, part);
    }
    // Structured rows may vastly outnumber their compact table entries.
    model
        .equation_families
        .iter()
        .try_fold(0u32, |total, family| {
            total
                .checked_add(family.scalar_rows)
                .ok_or_else(|| LinkError("family scalar-row count overflow".into()))
        })?;
    recompute_summary(&mut model);
    check_model(&model)?;
    Ok(RbcFile {
        magic: RBC_MAGIC.into(),
        bitcode_version: RBC_VERSION,
        producer: format!("rumoca-bitcode-link {}", env!("CARGO_PKG_VERSION")),
        execution: None,
        model,
    })
}

fn check_model(model: &RbcModel) -> Result<()> {
    let options = ValidateOptions {
        reject_unsupported: true,
    };
    validate(model, &options).map_err(|errors| {
        LinkError(
            errors
                .iter()
                .map(ToString::to_string)
                .collect::<Vec<_>>()
                .join("; "),
        )
    })
}

fn check_input(input: &LinkInput<'_>, discard: bool, names: &mut BTreeSet<String>) -> Result<()> {
    let ns = input.namespace;
    let valid = !ns.is_empty()
        && ns
            .bytes()
            .enumerate()
            .all(|(i, c)| c == b'_' || c.is_ascii_alphabetic() || (i > 0 && c.is_ascii_digit()));
    if !valid || !names.insert(ns.to_owned()) {
        return Err(LinkError(format!(
            "namespace {ns:?} must be a unique simple identifier"
        )));
    }
    input.file.check_header().map_err(LinkError)?;
    if input.file.execution.is_some() && !discard {
        return Err(LinkError(format!(
            "{ns}: executable input; explicitly discard execution to link its equations (numerical edits and instrumentation will be lost)"
        )));
    }
    check_model(&input.file.model).map_err(|e| LinkError(format!("{ns}: {e}")))
}

#[derive(Clone, Copy)]
struct Range {
    start: u32,
    len: u32,
    table: &'static str,
}

impl Range {
    fn new(start: usize, len: usize, table: &'static str) -> Result<Self> {
        let start = u32::try_from(start).map_err(|_| LinkError(format!("{table}: ID overflow")))?;
        let len = u32::try_from(len).map_err(|_| LinkError(format!("{table}: ID overflow")))?;
        start
            .checked_add(len)
            .ok_or_else(|| LinkError(format!("{table}: ID overflow")))?;
        Ok(Self { start, len, table })
    }

    fn shift(self, id: &mut u32) -> Result<()> {
        if *id >= self.len {
            return Err(LinkError(format!(
                "{} reference {} out of bounds ({})",
                self.table, id, self.len
            )));
        }
        *id += self.start;
        Ok(())
    }
}

// A single table catalog supplies relocation ranges and concatenation. IDs in
// initial/discrete equations, time events and initial families have their own
// spaces even though the schema reuses their Rust newtype.
macro_rules! tables {
    ($($field:ident),+ $(,)?) => {
        struct Map<'a> { namespace: &'a str, $($field: Range,)+ }
        impl<'a> Map<'a> {
            fn new(out: &RbcModel, input: &RbcModel, namespace: &'a str) -> Result<Self> {
                Ok(Self { namespace, $($field: Range::new(out.$field.len(), input.$field.len(), stringify!($field))?,)+ })
            }
        }
        fn append(out: &mut RbcModel, input: RbcModel) {
            // Exhaustive destructuring makes adding a table a linker review.
            let RbcModel { name: _, summary: _, $($field,)+ } = input;
            $(out.$field.extend($field);)+
        }
    }
}
tables!(
    sources,
    types,
    variables,
    expressions,
    equations,
    initial_equations,
    domains,
    discrete_real_equations,
    initial_discrete_values,
    functions,
    equation_families,
    initial_equation_families,
    relations,
    conditions,
    roots,
    events,
    time_events,
    connections,
    connection_sets,
    components,
    trace_points,
    discrete_definitions,
    connector_types,
    connectors
);

trait Shift {
    fn shift(&mut self, map: &Map<'_>) -> Result<()>;
}
impl<T: Shift> Shift for Vec<T> {
    fn shift(&mut self, map: &Map<'_>) -> Result<()> {
        self.iter_mut().try_for_each(|v| v.shift(map))
    }
}
impl<T: Shift> Shift for Option<T> {
    fn shift(&mut self, map: &Map<'_>) -> Result<()> {
        if let Some(v) = self {
            v.shift(map)?;
        }
        Ok(())
    }
}
macro_rules! ids {
    ($($ty:ident => $table:ident),+ $(,)?) => {$(
        impl Shift for $ty {
            fn shift(&mut self, map: &Map<'_>) -> Result<()> { map.$table.shift(&mut self.0) }
        }
    )+}
}
ids!(SourceId=>sources, TypeId=>types, VariableId=>variables, ExprId=>expressions,
    EquationId=>equations, RelationId=>relations, ConditionId=>conditions,
    RootId=>roots, EventId=>events, ConnectionId=>connections,
    ConnectionSetId=>connection_sets, ComponentId=>components,
    TracePointId=>trace_points, DomainId=>domains, FunctionId=>functions,
    FamilyId=>equation_families);

macro_rules! fields {
    ($value:ident, $map:ident, $($field:ident),+ $(,)?) => { $( $value.$field.shift($map)?; )+ }
}
use fields;

impl Map<'_> {
    fn qualify(&self, value: &mut String) {
        *value = if value.is_empty() {
            self.namespace.to_owned()
        } else {
            format!("{}.{}", self.namespace, value)
        };
    }

    fn relocate(&self, m: &mut RbcModel) -> Result<()> {
        m.sources.shift(self)?;
        m.types.shift(self)?;
        m.variables.shift(self)?;
        m.expressions.shift(self)?;
        m.equations.shift(self)?;
        for eq in &mut m.initial_equations {
            self.initial_equations.shift(&mut eq.id.0)?;
            self.equation_body(eq)?;
        }
        m.domains.shift(self)?;
        m.functions.shift(self)?;
        m.equation_families.shift(self)?;
        for family in &mut m.initial_equation_families {
            self.initial_equation_families.shift(&mut family.id.0)?;
            self.family_body(family)?;
        }
        m.discrete_real_equations.shift(self)?;
        m.initial_discrete_values.shift(self)?;
        m.discrete_definitions.shift(self)?;
        m.relations.shift(self)?;
        m.conditions.shift(self)?;
        m.roots.shift(self)?;
        m.events.shift(self)?;
        m.time_events.shift(self)?;
        m.components.shift(self)?;
        m.connections.shift(self)?;
        m.connection_sets.shift(self)?;
        m.trace_points.shift(self)?;
        m.connector_types.shift(self)?;
        m.connectors.shift(self)?;
        // These tables have no entry IDs, but are still concatenated/count-checked.
        let _ = (self.initial_discrete_values, self.discrete_definitions);
        Ok(())
    }
}
