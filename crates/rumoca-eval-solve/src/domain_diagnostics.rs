//! Scoped evidence from executed scalar instructions, not sampled reconstruction.
//! Internal trial coordinates are diagnostics, never published physical traces.
#[cfg(test)]
mod tests;

use rumoca_ir_solve as solve;
use serde_json::{Value, json};
use sha1::{Digest, Sha1};
use std::{cell::RefCell, collections::BTreeSet, marker::PhantomData, rc::Rc};

const MAX_FAULTS: usize = 64;

#[derive(Default)]
struct Evidence {
    faults: Vec<Value>,
    seen: BTreeSet<(String, usize)>,
    unobserved_evaluations: u64,
    truncated: bool,
}

thread_local! {
    static EVIDENCE: RefCell<Option<Evidence>> = const { RefCell::new(None) };
}

/// One synchronous interpreter run. Thread-affine, bounded, and reset on unwind.
pub struct Scope(PhantomData<Rc<()>>);

impl Scope {
    pub fn start() -> Result<Self, String> {
        EVIDENCE.with(|slot| {
            let mut slot = slot.borrow_mut();
            if slot.is_some() {
                return Err("nested domain diagnostic scope".into());
            }
            *slot = Some(Evidence::default());
            Ok(Self(PhantomData))
        })
    }

    pub fn finish(self) -> Value {
        // Not `unwrap_or_default()`: an empty record here would report "no
        // faults observed" for a run whose evidence went missing, which is the
        // false clean result this diagnostic exists to prevent. `start()` fills
        // the slot and only `finish` or `Drop` clears it, and `finish` consumes
        // the live `Scope`, so the slot is present whenever this runs.
        let evidence = EVIDENCE.with(|slot| {
            slot.borrow_mut()
                .take()
                .expect("a live Scope holds its evidence until finish takes it")
        });
        json!({"schema_version": 1, "kind": "solve-domain-diagnostics",
            "coordinates": "internal-evaluation", "execution_policy": "interpreter",
            "coverage": "scalar-output-rows", "faults": evidence.faults,
            "unobserved_evaluations": evidence.unobserved_evaluations,
            "truncated": evidence.truncated})
    }
}

impl Drop for Scope {
    fn drop(&mut self) {
        EVIDENCE.with(|slot| *slot.borrow_mut() = None);
    }
}

pub(crate) fn active() -> bool {
    EVIDENCE.with(|slot| slot.borrow().is_some())
}

pub(crate) fn supported(row: &[solve::LinearOp]) -> bool {
    use solve::LinearOp as L;
    let mut definitions = BTreeSet::new();
    row.iter().any(|op| matches!(op, L::StoreOutput { .. }))
        && row
            .iter()
            .filter_map(L::dst_register)
            .all(|dst| definitions.insert(dst))
        && row.iter().all(|op| {
            matches!(
                op,
                L::Const { .. }
                    | L::LoadTime { .. }
                    | L::LoadY { .. }
                    | L::LoadP { .. }
                    | L::Unary { .. }
                    | L::Binary { .. }
                    | L::Compare { .. }
                    | L::Select { .. }
                    | L::StoreOutput { .. }
            )
        })
}

pub(crate) fn checked_flow(row: &[solve::LinearOp], span: Option<rumoca_core::Span>) -> bool {
    let span = span.unwrap_or_else(|| {
        rumoca_core::Span::from_offsets(
            rumoca_core::SourceId::from_source_name("runtime:domain-diagnostics"),
            0,
            0,
        )
    });
    solve::ScalarProgramBlock::with_program_spans(vec![row.to_vec()], vec![span]).is_ok()
}

pub(crate) fn unobserved() {
    EVIDENCE.with(|slot| {
        if let Some(evidence) = slot.borrow_mut().as_mut() {
            evidence.unobserved_evaluations = evidence.unobserved_evaluations.saturating_add(1);
        }
    });
}

pub(crate) fn observe(row: &[solve::LinearOp], op: &solve::LinearOp, regs: &[f64], time: f64) {
    if !active() {
        return;
    }
    let Some((operation, requirement, value)) = violation(op, regs) else {
        return;
    };
    if !supported(row) {
        return;
    }
    EVIDENCE.with(|slot| {
        let mut slot = slot.borrow_mut();
        let Some(evidence) = slot.as_mut() else {
            return;
        };
        if evidence.faults.len() >= MAX_FAULTS {
            evidence.truncated = true;
            return;
        }
        let Ok(bytes) = serde_json::to_vec(row) else {
            return;
        };
        let fingerprint = format!("{:x}", Sha1::digest(bytes));
        let index = row
            .iter()
            .position(|item| item.dst_register() == op.dst_register())
            .unwrap_or(0);
        if !evidence.seen.insert((fingerprint.clone(), index)) {
            return;
        }
        evidence.faults.push(json!({"program_sha1": fingerprint,
            "instruction_index": index, "operation": operation, "requirement": requirement,
            "operand_value": value, "time": time}));
    });
}

fn violation(op: &solve::LinearOp, regs: &[f64]) -> Option<(&'static str, &'static str, f64)> {
    use solve::{BinaryOp as B, LinearOp as L, UnaryOp as U};
    let (operation, requirement, value, violated) = match *op {
        L::Binary {
            op: B::Div, rhs, ..
        } => (
            "division",
            "nonzero",
            regs[rhs as usize],
            regs[rhs as usize] == 0.0,
        ),
        L::Unary {
            op: U::Sqrt, arg, ..
        } => (
            "sqrt",
            "non-negative",
            regs[arg as usize],
            regs[arg as usize] < 0.0,
        ),
        L::Unary {
            op: U::Log | U::Log10,
            arg,
            ..
        } => (
            "log",
            "positive",
            regs[arg as usize],
            regs[arg as usize] <= 0.0,
        ),
        L::Unary {
            op: U::Asin | U::Acos,
            arg,
            ..
        } => (
            "inverse-trig",
            "unit-interval",
            regs[arg as usize],
            regs[arg as usize].abs() > 1.0,
        ),
        _ => return None,
    };
    (violated && value.is_finite()).then_some((operation, requirement, value))
}
