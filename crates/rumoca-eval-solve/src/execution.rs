//! Ordered execution effects over canonical Solve scalar computation.
use rumoca_ir_solve as solve;
use solve::execution as ir;
use std::{
    collections::BTreeMap,
    fs::{File, OpenOptions},
    io::{BufWriter, Write},
    path::{Path, PathBuf},
};

#[derive(Clone)]
enum Value {
    Number(f64),
    Integer(u64),
    Text(String),
}
impl Value {
    fn number(&self) -> Result<f64, String> {
        match self {
            Self::Number(n) => Ok(*n),
            Self::Integer(n) => Ok(*n as f64),
            Self::Text(_) => Err("expected numeric value".into()),
        }
    }
    fn csv(&self) -> String {
        match self {
            Self::Number(n) => n.to_string(),
            Self::Integer(n) => n.to_string(),
            Self::Text(s) => quote(s),
        }
    }
}

pub struct CsvExecution {
    artifact: ir::ExecutionArtifact,
    root: PathBuf,
    files: BTreeMap<String, BufWriter<File>>,
    sequence: u64,
    finished: bool,
    time: f64,
    phase: String,
    y: Vec<f64>,
    p: Vec<f64>,
}

impl CsvExecution {
    pub fn start(artifact: ir::ExecutionArtifact, root: &Path) -> Result<Self, String> {
        ir::validate(&artifact)?;
        std::fs::create_dir(root)
            .map_err(|e| format!("trace directory must be new: {}: {e}", root.display()))?;
        let mut state = Self {
            artifact,
            root: root.into(),
            files: BTreeMap::new(),
            sequence: 0,
            finished: false,
            time: 0.0,
            phase: String::new(),
            y: vec![],
            p: vec![],
        };
        let count = state
            .artifact
            .numerical
            .storage
            .iter()
            .filter(|v| v.role == "parameter")
            .count();
        state.p.resize(count, 0.0);
        for v in &state.artifact.numerical.storage {
            if v.role == "parameter" {
                *state.p.get_mut(v.index).ok_or("invalid parameter index")? = v.start;
            }
        }
        let manifest = serde_json::json!({"schema_version": 1, "equation_digest": state.artifact.equation_digest, "execution_revision": state.artifact.revision, "sinks": state.artifact.sinks});
        let mut file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(root.join("manifest.json"))
            .map_err(|e| e.to_string())?;
        serde_json::to_writer_pretty(&mut file, &manifest).map_err(|e| e.to_string())?;
        state.function("run_start")?;
        Ok(state)
    }

    fn function(&mut self, name: &str) -> Result<(), String> {
        let body = self
            .artifact
            .functions
            .get(name)
            .ok_or("missing function")?
            .clone();
        self.body(&body, &mut BTreeMap::new())
    }

    fn body(
        &mut self,
        body: &[ir::Instruction],
        values: &mut BTreeMap<String, Value>,
    ) -> Result<(), String> {
        for op in body {
            if let Some((name, value)) = self.instruction(op, values)? {
                values.insert(name.clone(), value);
            }
        }
        Ok(())
    }

    fn instruction<'a>(
        &mut self,
        op: &'a ir::Instruction,
        values: &mut BTreeMap<String, Value>,
    ) -> Result<Option<(&'a String, Value)>, String> {
        use ir::Instruction::*;
        let result = match op {
            Time { result } => Some((result, self::Value::Number(self.time))),
            Sequence { result } => Some((result, self::Value::Integer(self.sequence))),
            Phase { result } => Some((result, self::Value::Text(self.phase.clone()))),
            Value {
                result,
                variable_id,
            } => {
                let obs = self
                    .artifact
                    .numerical
                    .observations
                    .iter()
                    .find(|o| o.variable_id == *variable_id)
                    .ok_or("missing observation")?;
                let ops = ir::checked_scalar(&obs.instructions, self.y.len(), self.p.len())?;
                let value = crate::eval_row(&ops, &self.y, &self.p, self.time, None)
                    .map_err(|e| e.to_string())?;
                Some((result, self.finite(value)?))
            }
            Compute {
                result,
                arguments,
                instructions,
            } => {
                let args = arguments
                    .iter()
                    .map(|n| get(values, n)?.number())
                    .collect::<Result<Vec<_>, _>>()?;
                let ops = ir::checked_scalar(instructions, args.len(), 0)?;
                let value =
                    crate::eval_row(&ops, &args, &[], 0.0, None).map_err(|e| e.to_string())?;
                Some((result, self.finite(value)?))
            }
            Open { sink } => {
                self.open_sink(sink)?;
                None
            }
            Write { sink, values: args } => {
                let row = args
                    .iter()
                    .map(|n| Ok(get(values, n)?.csv()))
                    .collect::<Result<Vec<_>, String>>()?
                    .join(",");
                let file = self.files.get_mut(sink).ok_or("CSV sink is not open")?;
                writeln!(file, "{row}").map_err(|e| e.to_string())?;
                None
            }
            Close { sink } => {
                // Also used by controlled-failure cleanup after partial setup.
                if let Some(mut file) = self.files.remove(sink) {
                    file.flush().map_err(|e| e.to_string())?;
                }
                None
            }
            If {
                condition,
                then_body,
                else_body,
            } => {
                let selected = if get(values, condition)?.number()? != 0.0 {
                    then_body
                } else {
                    else_body
                };
                self.body(selected, &mut values.clone())?;
                None
            }
            Call { function } => {
                self.function(function)?;
                None
            }
            Assert { condition, message } => {
                if get(values, condition)?.number()? == 0.0 {
                    return Err(format!("execution assertion: {message}"));
                }
                None
            }
        };
        Ok(result)
    }

    fn open_sink(&mut self, sink: &String) -> Result<(), String> {
        let decl = self
            .artifact
            .sinks
            .iter()
            .find(|s| &s.key == sink)
            .ok_or("missing sink")?;
        let file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(self.root.join(&decl.filename))
            .map_err(|e| e.to_string())?;
        let mut out = BufWriter::new(file);
        writeln!(
            out,
            "{}",
            decl.columns
                .iter()
                .map(|s| quote(s))
                .collect::<Vec<_>>()
                .join(",")
        )
        .map_err(|e| e.to_string())?;
        self.files.insert(sink.clone(), out);
        Ok(())
    }

    fn finite(&self, value: f64) -> Result<Value, String> {
        if value.is_finite() {
            Ok(Value::Number(value))
        } else {
            Err("non-finite executable observation/computation".into())
        }
    }
}

impl CsvExecution {
    pub fn publish(
        &mut self,
        time: f64,
        phase: &str,
        names: &[String],
        values: &[f64],
    ) -> Result<(), String> {
        self.time = time;
        self.phase = phase.into();
        self.y
            .resize(self.artifact.numerical.storage.len() - self.p.len(), 0.0);
        for v in &self.artifact.numerical.storage {
            if v.role == "parameter" {
                continue;
            }
            let i = names
                .iter()
                .position(|n| n == &v.name)
                .ok_or_else(|| format!("host did not reconstruct {}", v.name))?;
            *self
                .y
                .get_mut(v.index)
                .ok_or("invalid snapshot storage index")? =
                *values.get(i).ok_or("invalid snapshot width")?;
        }
        self.function("publish")?;
        self.sequence += 1;
        Ok(())
    }

    pub fn finish(&mut self) -> Result<(), String> {
        if self.finished {
            return Ok(());
        }
        self.finished = true;
        let result = self.function("run_finish");
        // Even a failing finish instruction cannot keep later resources open.
        let mut cleanup = Ok(());
        for (_, mut file) in std::mem::take(&mut self.files) {
            if let Err(e) = file.flush() {
                cleanup = Err(e.to_string());
            }
        }
        result.and(cleanup)
    }
}

impl Drop for CsvExecution {
    fn drop(&mut self) {
        if let Err(error) = self.finish() {
            eprintln!("execution cleanup failed: {error}");
        }
    }
}

fn get<'a>(values: &'a BTreeMap<String, Value>, name: &str) -> Result<&'a Value, String> {
    values
        .get(name)
        .ok_or_else(|| format!("undefined value {name}"))
}

fn quote(s: &str) -> String {
    if s.contains([',', '"', '\n', '\r']) {
        format!("\"{}\"", s.replace('"', "\"\""))
    } else {
        s.into()
    }
}
