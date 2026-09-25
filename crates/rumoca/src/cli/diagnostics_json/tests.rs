use std::cell::Cell;
use std::fs;

use clap::Parser;
use rumoca_core::{PrimaryLabel, SourceId, Span};
use serde_json::{Value, json};
use tempfile::tempdir;

use super::*;
use crate::cli::{Cli, run};

fn read_report(path: &Path) -> Value {
    serde_json::from_slice(&fs::read(path).expect("read report")).expect("valid JSON report")
}

#[test]
fn global_option_writes_success_with_no_diagnostics() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("diagnostics.json");
    let cli = Cli::try_parse_from([
        "rumoca",
        "build-info",
        "--diagnostics-json",
        path.to_str().unwrap(),
    ])
    .unwrap();

    run(cli).expect("successful command");
    assert_eq!(
        read_report(&path),
        json!({"schema": 1, "status": "success", "diagnostics": []})
    );
}

#[test]
fn compile_failure_preserves_both_labels_and_notes() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("diagnostics.json");
    let file = dir.path().join("Bad.mo");
    fs::write(
        &file,
        "connector C\n  Real e;\n  flow Real f;\nend C;\n\nmodel Bad\n  C a;\n  C b;\nequation\n  connect(a[1], b);\nend Bad;\n",
    )
    .unwrap();
    let cli = Cli::try_parse_from([
        "rumoca",
        "--diagnostics-json",
        path.to_str().unwrap(),
        "compile",
        file.to_str().unwrap(),
        "--model",
        "Bad",
    ])
    .unwrap();

    let error = run(cli).expect_err("scalar connector cannot be indexed");
    assert!(matches!(
        error.downcast_ref::<CompilerError>(),
        Some(CompilerError::CompileDiagnosticsError { .. })
    ));
    let report = read_report(&path);
    assert_eq!(report["status"], "failed");
    let diagnostic = &report["diagnostics"][0];
    assert_eq!(diagnostic["code"], "EF026");
    assert_eq!(diagnostic["phase"], "Flatten");
    assert_eq!(diagnostic["model"], "Bad");
    assert_eq!(diagnostic["labels"].as_array().unwrap().len(), 2);
    assert_eq!(diagnostic["labels"][0]["file"], file.to_str().unwrap());
    assert_eq!(diagnostic["labels"][0]["line"], 10);
    assert_eq!(diagnostic["labels"][0]["column"], 11);
    assert_eq!(diagnostic["labels"][1]["line"], 7);
    assert_eq!(diagnostic["labels"][1]["column"], 3);
    assert!(diagnostic["notes"].to_string().contains("MLS §10.5"));
    assert!(report.get("tool_error").is_none());
}

#[test]
fn source_diagnostics_resolve_each_file_and_preserve_severity() {
    let mut sources = SourceMap::new();
    let first = sources.add("Pkg/A.mo", "// first\nmodel A end A;");
    let second = sources.add("Pkg/B.mo", "model B end B;");
    let diagnostic = Diagnostic::warning(
        "rumoca::typecheck::WT003",
        "source warning",
        PrimaryLabel::new(Span::from_offsets(first, 15, 16)).with_message("primary"),
    )
    .with_label(Label::secondary(Span::from_offsets(second, 6, 7)).with_message("related"))
    .with_note("preserved note");
    let result = Err(CompilerError::SourceDiagnosticsError {
        summary: "source diagnostics".into(),
        diagnostics: vec![diagnostic],
        source_map: Box::new(sources),
    }
    .into());

    let report = serde_json::to_value(Report::from_result(&result)).unwrap();
    let diagnostic = &report["diagnostics"][0];
    assert_eq!(diagnostic["code"], "WT003");
    assert_eq!(diagnostic["severity"], "warning");
    assert!(diagnostic["phase"].is_null());
    assert_eq!(diagnostic["labels"][0]["file"], "Pkg/A.mo");
    assert_eq!(diagnostic["labels"][0]["line"], 2);
    assert_eq!(diagnostic["labels"][0]["column"], 7);
    assert_eq!(diagnostic["labels"][1]["file"], "Pkg/B.mo");
    assert_eq!(diagnostic["labels"][1]["line"], 1);
    assert_eq!(diagnostic["notes"], json!(["preserved note"]));
}

#[test]
fn unresolvable_labels_never_invent_locations() {
    let missing = SourceId::from_source_name("missing.mo");
    let mut sources = SourceMap::new();
    let real = sources.add("present.mo", "model Present end Present;");
    let missing_span = Label::primary(Span::from_offsets(missing, 6, 7));
    let missing_label = ReportedLabel::new(&missing_span, Some(&sources));
    let missing = serde_json::to_value(missing_label).unwrap();
    assert!(missing["file"].is_null());
    assert!(missing["line"].is_null());
    assert!(missing["column"].is_null());
    assert_eq!(missing["start"], 6);
    assert_eq!(missing["end"], 7);

    let invalid_span = Label::primary(Span::from_offsets(real, 50, 99));
    let invalid = serde_json::to_value(ReportedLabel::new(&invalid_span, Some(&sources))).unwrap();
    assert_eq!(invalid["file"], "present.mo");
    assert!(invalid["line"].is_null());
    assert!(invalid["column"].is_null());
}

#[test]
fn unknown_failure_replaces_stale_success_without_message_classification() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("diagnostics.json");
    fs::write(
        &path,
        "{\"schema\":1,\"status\":\"success\",\"diagnostics\":[]}",
    )
    .unwrap();
    let result = run_with_report(Some(&path), || {
        assert_eq!(
            fs::read(&path).unwrap(),
            b"",
            "prior report already invalidated"
        );
        anyhow::bail!("EF032 array index out of bounds (untyped external text)");
    });
    assert!(result.is_err());
    let report = read_report(&path);
    assert_eq!(report["status"], "failed");
    assert_eq!(report["diagnostics"], json!([]));
    assert!(report["tool_error"].as_str().unwrap().contains("EF032"));
}

#[test]
fn ordinary_io_error_remains_untyped() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("diagnostics.json");
    let missing = dir.path().join("missing.mo");
    let cli = Cli::try_parse_from([
        "rumoca",
        "compile",
        missing.to_str().unwrap(),
        "--diagnostics-json",
        path.to_str().unwrap(),
    ])
    .unwrap();
    assert!(run(cli).is_err());
    let report = read_report(&path);
    assert_eq!(report["status"], "failed");
    assert_eq!(report["diagnostics"], json!([]));
    assert!(report["tool_error"].is_string());
}

#[test]
fn report_creation_failure_prevents_command_execution() {
    let dir = tempdir().unwrap();
    let ran = Cell::new(false);
    let error = run_with_report(Some(dir.path()), || {
        ran.set(true);
        Ok(())
    })
    .expect_err("a directory cannot receive a report");
    assert!(!ran.get());
    assert!(
        error
            .to_string()
            .contains("cannot create diagnostic report")
    );
}

#[test]
#[cfg(target_os = "linux")]
fn report_write_failure_cannot_return_success() {
    let ran = Cell::new(false);
    let error = run_with_report(Some(Path::new("/dev/full")), || {
        ran.set(true);
        Ok(())
    })
    .expect_err("a full device cannot receive a report");
    assert!(ran.get());
    assert!(error.to_string().contains("cannot write diagnostic report"));
}
