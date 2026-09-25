//! Machine-readable command results, retaining compiler-owned diagnostics.
//!
//! Schema 1 uses one-based lines and UTF-16 columns, matching the human CLI's
//! source-location conversion. Byte offsets retain the original half-open span.
//! Absent source information stays absent; unstructured errors are tool errors
//! and never acquire a diagnostic code by interpreting their message.

#[cfg(test)]
mod tests;

use std::fs::File;
use std::io::Write;
use std::path::Path;

use anyhow::{Context, Result};
use rumoca_compile::compile::{FailedPhase, ModelFailureDiagnostic, source_span_location};
use rumoca_core::{Diagnostic, DiagnosticSeverity, Label, SourceMap, short_phase_error_code};
use serde::Serialize;

use crate::CompilerError;

#[derive(Serialize)]
struct Report<'a> {
    schema: u8,
    status: &'static str,
    diagnostics: Vec<ReportedDiagnostic<'a>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    tool_error: Option<String>,
}

#[derive(Serialize)]
struct ReportedDiagnostic<'a> {
    code: Option<&'a str>,
    message: &'a str,
    severity: &'static str,
    phase: Option<FailedPhase>,
    model: Option<&'a str>,
    labels: Vec<ReportedLabel<'a>>,
    notes: &'a [String],
}

#[derive(Serialize)]
struct ReportedLabel<'a> {
    file: Option<&'a str>,
    line: Option<u32>,
    column: Option<u32>,
    start: usize,
    end: usize,
    message: Option<&'a str>,
    primary: bool,
}

/// Invalidate prior evidence before executing, including on command failure.
/// Opening and writing the requested report are required parts of the command.
pub(super) fn run_with_report(
    path: Option<&Path>,
    action: impl FnOnce() -> Result<()>,
) -> Result<()> {
    let Some(path) = path else {
        return action();
    };
    let mut file = File::create(path)
        .with_context(|| format!("cannot create diagnostic report `{}`", path.display()))?;
    let result = action();
    let report = Report::from_result(&result);
    write_report(&mut file, &report)
        .with_context(|| format!("cannot write diagnostic report `{}`", path.display()))?;
    result
}

fn write_report(file: &mut File, report: &Report<'_>) -> Result<()> {
    serde_json::to_writer_pretty(&mut *file, report)?;
    file.write_all(b"\n")?;
    file.flush()?;
    Ok(())
}

impl<'a> Report<'a> {
    fn from_result(result: &'a Result<()>) -> Self {
        let mut report = Self {
            schema: 1,
            status: if result.is_ok() { "success" } else { "failed" },
            diagnostics: Vec::new(),
            tool_error: None,
        };
        let Err(error) = result else {
            return report;
        };
        report.diagnostics = match error.downcast_ref::<CompilerError>() {
            Some(CompilerError::CompileDiagnosticsError {
                failures,
                source_map,
                ..
            }) => failures
                .iter()
                .map(|failure| ReportedDiagnostic::compile(failure, source_map.as_deref()))
                .collect(),
            Some(CompilerError::SourceDiagnosticsError {
                diagnostics,
                source_map,
                ..
            }) => diagnostics
                .iter()
                .map(|diagnostic| ReportedDiagnostic::source(diagnostic, source_map))
                .collect(),
            _ => Vec::new(),
        };
        if report.diagnostics.is_empty() {
            report.tool_error = Some(format!("{error:#}"));
        }
        report
    }
}

impl<'a> ReportedDiagnostic<'a> {
    fn compile(failure: &'a ModelFailureDiagnostic, sources: Option<&'a SourceMap>) -> Self {
        Self {
            code: failure.error_code.as_deref().map(short_phase_error_code),
            message: &failure.error,
            severity: "error",
            phase: failure.phase,
            model: Some(&failure.model_name),
            labels: failure
                .primary_label
                .iter()
                .chain(failure.secondary_labels.iter())
                .map(|label| ReportedLabel::new(label, sources))
                .collect(),
            notes: &failure.notes,
        }
    }

    fn source(diagnostic: &'a Diagnostic, sources: &'a SourceMap) -> Self {
        Self {
            code: diagnostic.code.as_deref().map(short_phase_error_code),
            message: &diagnostic.message,
            severity: match diagnostic.severity {
                DiagnosticSeverity::Error => "error",
                DiagnosticSeverity::Warning => "warning",
                DiagnosticSeverity::Note => "note",
            },
            phase: None,
            model: None,
            labels: diagnostic
                .labels
                .iter()
                .map(|label| ReportedLabel::new(label, Some(sources)))
                .collect(),
            notes: &diagnostic.notes,
        }
    }
}

impl<'a> ReportedLabel<'a> {
    fn new(label: &'a Label, sources: Option<&'a SourceMap>) -> Self {
        let location = sources.and_then(|sources| source_span_location(sources, label.span));
        Self {
            file: sources.and_then(|sources| sources.name(label.span.source)),
            line: location.as_ref().map(|location| location.start.line + 1),
            column: location
                .as_ref()
                .map(|location| location.start.character + 1),
            start: label.span.start.0,
            end: label.span.end.0,
            message: label.message.as_deref(),
            primary: label.primary,
        }
    }
}
