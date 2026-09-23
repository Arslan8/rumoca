//! Single authoritative lifecycle operation/type/effect checker.
use super::*;
use std::collections::BTreeSet;

pub fn validate(a: &ExecutionArtifact) -> Result<(), String> {
    if a.version != 1 || a.lowering != "solve-scalar-v1" {
        return Err("unsupported execution version/lowering configuration".into());
    }
    let mut keys = BTreeSet::new();
    let mut files = BTreeSet::new();
    for s in &a.sinks {
        if !keys.insert(s.key.clone()) || !files.insert(s.filename.clone()) {
            return Err("duplicate CSV sink key or filename".into());
        }
        if s.filename.is_empty()
            || s.filename.contains(['/', '\\'])
            || s.filename == "."
            || s.filename == ".."
            || s.filename == "manifest.json"
        {
            return Err("CSV filename must be one relative, non-reserved path component".into());
        }
        if s.columns.len() != s.column_types.len() || s.columns.is_empty() {
            return Err("CSV sink requires one type per column".into());
        }
        for t in &s.column_types {
            if !matches!(t.as_str(), "real" | "integer" | "string") {
                return Err(format!("unsupported CSV column type {t}"));
            }
        }
    }
    for phase in ["run_start", "publish", "run_finish"] {
        let mut resources = if phase == "run_start" {
            BTreeSet::new()
        } else {
            keys.clone()
        };
        function(a, phase, phase, &mut resources, &mut Vec::new())?;
        let expected = if phase == "run_finish" {
            BTreeSet::new()
        } else {
            keys.clone()
        };
        if resources != expected {
            return Err(format!(
                "{phase} does not establish the required CSV resource state"
            ));
        }
    }
    // Even unused functions must be well-formed, under their declared lifecycle.
    for name in a
        .functions
        .keys()
        .filter(|n| !matches!(n.as_str(), "run_start" | "publish" | "run_finish"))
    {
        let phase = name
            .split_once(':')
            .map(|p| p.0)
            .ok_or("helper function names require a lifecycle prefix, e.g. publish:check")?;
        if !matches!(phase, "run_start" | "publish" | "run_finish") {
            return Err("unknown helper lifecycle".into());
        }
        let mut resources = if phase == "run_start" {
            BTreeSet::new()
        } else {
            keys.clone()
        };
        function(a, name, phase, &mut resources, &mut Vec::new())?;
    }
    Ok(())
}

fn function(
    a: &ExecutionArtifact,
    name: &str,
    phase: &str,
    resources: &mut BTreeSet<String>,
    stack: &mut Vec<String>,
) -> Result<(), String> {
    if stack.iter().any(|n| n == name) || stack.len() >= 64 {
        return Err("recursive/deep execution call graph".into());
    }
    if name != phase && !name.starts_with(&format!("{phase}:")) {
        return Err("call crosses lifecycle boundary".into());
    }
    let body = a
        .functions
        .get(name)
        .ok_or_else(|| format!("undefined execution function {name}"))?;
    stack.push(name.into());
    body_check(a, body, phase, &mut BTreeMap::new(), resources, stack)?;
    stack.pop();
    Ok(())
}

fn body_check(
    a: &ExecutionArtifact,
    body: &[Instruction],
    phase: &str,
    values: &mut BTreeMap<String, String>,
    resources: &mut BTreeSet<String>,
    stack: &mut Vec<String>,
) -> Result<(), String> {
    use Instruction::*;
    for op in body {
        let produced = match op {
            Time { result } | Sequence { result } | Phase { result } | Value { result, .. } => {
                if phase != "publish" {
                    return Err("snapshot operation outside publish lifecycle".into());
                }
                if let Value { variable_id, .. } = op
                    && !a
                        .numerical
                        .observations
                        .iter()
                        .any(|o| o.variable_id == *variable_id)
                {
                    return Err(format!(
                        "missing checked observation for variable {variable_id}"
                    ));
                }
                Some((
                    result,
                    match op {
                        Phase { .. } => "string",
                        Sequence { .. } => "integer",
                        _ => "real",
                    },
                ))
            }
            Compute {
                result,
                arguments,
                instructions,
            } => {
                for arg in arguments {
                    numeric(values, arg)?;
                }
                checked_scalar(instructions, arguments.len(), 0)?;
                // Lifecycle time is explicit snapshot.time, never an ambient RHS time.
                if instructions
                    .iter()
                    .any(|i| matches!(i, ScalarOp::LoadTime { .. }))
                {
                    return Err("compute must receive time as an explicit argument".into());
                }
                Some((result, "real"))
            }
            Open { .. } | Close { .. } | Write { .. } => {
                effect_check(a, op, phase, values, resources)?;
                None
            }
            If {
                condition,
                then_body,
                else_body,
            } => {
                numeric(values, condition)?;
                let mut left = resources.clone();
                let mut right = resources.clone();
                body_check(a, then_body, phase, &mut values.clone(), &mut left, stack)?;
                body_check(a, else_body, phase, &mut values.clone(), &mut right, stack)?;
                if left != right {
                    return Err("branch resource states disagree".into());
                }
                *resources = left;
                None
            }
            Call { function: name } => {
                function(a, name, phase, resources, stack)?;
                None
            }
            Assert { condition, .. } => {
                numeric(values, condition)?;
                None
            }
        };
        if let Some((name, ty)) = produced
            && (name.is_empty() || values.insert(name.clone(), ty.into()).is_some())
        {
            return Err("empty or multiply-defined execution value".into());
        }
    }
    Ok(())
}

fn numeric(values: &BTreeMap<String, String>, name: &str) -> Result<(), String> {
    match values.get(name).map(String::as_str) {
        Some("real" | "integer") => Ok(()),
        _ => Err(format!("{name} is undefined or not numeric")),
    }
}

fn effect_check(
    a: &ExecutionArtifact,
    op: &Instruction,
    phase: &str,
    values: &BTreeMap<String, String>,
    resources: &mut BTreeSet<String>,
) -> Result<(), String> {
    use Instruction::*;
    let sink = match op {
        Open { sink } | Close { sink } | Write { sink, .. } => sink,
        _ => unreachable!(),
    };
    let decl = a
        .sinks
        .iter()
        .find(|s| &s.key == sink)
        .ok_or("undefined CSV resource")?;
    match op {
        Open { .. } => {
            if phase != "run_start" || !resources.insert(sink.clone()) {
                return Err("csv.open must establish a unique run_start resource".into());
            }
        }
        Close { .. } => {
            if phase != "run_finish" || !resources.remove(sink) {
                return Err("csv.close must consume an open run_finish resource".into());
            }
        }
        Write { values: args, .. } => {
            if phase != "publish" || !resources.contains(sink) || args.len() != decl.columns.len() {
                return Err("invalid csv.write_row lifecycle/resource/width".into());
            }
            for (arg, expected) in args.iter().zip(&decl.column_types) {
                let actual = values
                    .get(arg)
                    .ok_or_else(|| format!("undefined value {arg}"))?;
                if actual != expected {
                    return Err(format!(
                        "CSV type mismatch: {arg} is {actual}, expected {expected}"
                    ));
                }
            }
        }
        _ => unreachable!(),
    }

    Ok(())
}
