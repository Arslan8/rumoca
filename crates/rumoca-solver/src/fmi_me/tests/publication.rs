//! A real ME event/periodic coincidence, in addition to recorder unit tests.
use super::*;
use crate::fmi_me::{
    PublicationObserver,
    driver::{batch_output_cursor, batch_session_options},
};
use std::{cell::RefCell, rc::Rc};

#[test]
fn executable_publication_deduplicates_a_real_scheduled_event() {
    struct Observer(
        Rc<RefCell<Vec<(f64, String)>>>,
        rumoca_eval_solve::execution::CsvExecution,
    );
    impl PublicationObserver for Observer {
        fn publish(
            &mut self,
            t: f64,
            phase: &str,
            names: &[String],
            values: &[f64],
        ) -> Result<(), String> {
            self.0.borrow_mut().push((t, phase.into()));
            self.1.publish(t, phase, names, values)
        }
        fn finish(&mut self) -> Result<(), String> {
            self.1.finish()
        }
    }
    let rows = Rc::new(RefCell::new(Vec::new()));
    let directory = tempfile::tempdir().unwrap();
    let root = directory.path().join("trace");
    let effects =
        rumoca_eval_solve::execution::CsvExecution::start(publication_program(), &root).unwrap();
    let mut model = solve::SolveModel::default();
    model.problem.events.scheduled_time_events = vec![0.5];
    let model = refresh_owned(model);
    let retained = MeRetainedComponent::instantiate(
        MeModelSource::fixture(&model),
        &fixture_instance_config(),
        None,
    )
    .unwrap();
    let options = batch_session_options(0.0, 1.0, 1e-9, 1e-11, 0.1, None).unwrap();
    let mut cursor = batch_output_cursor(&options).unwrap();
    let host = retained
        .into_lease_with_observer(options, Some(Box::new(Observer(rows.clone(), effects))))
        .unwrap();
    let mut session = host.into_session(None).unwrap();
    session.run_to_stop(&mut cursor).unwrap();
    session.finish_publication().unwrap();
    let rows = rows.borrow();
    assert_eq!(rows.len(), 11);
    assert_eq!(rows[0], (0.0, "initial".into()));
    let event: Vec<_> = rows
        .iter()
        .filter(|(t, _)| (*t - 0.5).abs() < 1e-12)
        .collect();
    assert_eq!(event.len(), 1);
    assert_eq!(event[0].1, "settled");
    let csv = std::fs::read_to_string(root.join("event.csv")).unwrap();
    assert_eq!(csv.lines().count(), 12);
    assert_eq!(csv.lines().nth(6).unwrap(), "0.5,5,settled");
}

fn publication_program() -> solve::execution::ExecutionArtifact {
    serde_json::from_value(serde_json::json!({
        "version": 1, "equation_digest": "test-event-host", "lowering": "solve-scalar-v1", "revision": 1, "passes": [],
        "numerical": {"source_name": "event-publication-test", "storage": [], "residual": [], "derivatives": [], "initialization": [], "algebraic_blocks": [], "initial_blocks": [], "observations": []},
        "sinks": [{"key": "event", "filename": "event.csv", "columns": ["time", "id", "phase"], "column_types": ["real", "integer", "string"], "metadata": {}}],
        "functions": {
            "run_start": [{"op": "csv.open", "sink": "event"}],
            "publish": [{"op": "snapshot.time", "result": "t"}, {"op": "snapshot.sequence", "result": "id"}, {"op": "snapshot.phase", "result": "phase"}, {"op": "csv.write_row", "sink": "event", "values": ["t", "id", "phase"]}],
            "run_finish": [{"op": "csv.close", "sink": "event"}]
        }
    })).unwrap()
}
