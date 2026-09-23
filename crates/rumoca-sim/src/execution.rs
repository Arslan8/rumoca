//! Native execution of checked public RBC programs on the existing ME/RK45 host.
use rumoca_ir_solve as solve;
#[cfg(feature = "solver-rk45")]
use rumoca_solver::fmi_me::{MeModelArtifact, PublicationObserver, session::MeRetainedComponent};
use solve::execution as ir;
#[cfg(feature = "solver-rk45")]
use std::path::Path;

pub fn lower(
    model: &rumoca_ir_solve::SolveModel,
    observed: &[(u32, String)],
) -> Result<ir::NumericalProgram, String> {
    rumoca_phase_solve::execution::export(model, observed)
}

pub fn check(artifact: &ir::ExecutionArtifact) -> Result<(), String> {
    ir::validate(artifact)?;
    rumoca_phase_solve::execution::reconstruct(&artifact.numerical)?;
    Ok(())
}

/// Executes saved numerical instructions, never lowers their equation source.
#[cfg(feature = "solver-rk45")]
pub fn run(
    artifact: &ir::ExecutionArtifact,
    options: &crate::SimOptions,
    root: &Path,
) -> Result<crate::SimResult, String> {
    check(artifact)?;
    let component = rumoca_phase_solve::execution::reconstruct(&artifact.numerical)?;
    let observer = NativePublication(rumoca_eval_solve::execution::CsvExecution::start(
        artifact.clone(),
        root,
    )?);
    let artifact = MeModelArtifact::new(component);
    let options_host = crate::me_backend::batch_options(options).map_err(|e| e.to_string())?;
    let mut cursor = rumoca_solver::fmi_me::driver::batch_output_cursor(&options_host)
        .map_err(|e| e.to_string())?;
    let retained = MeRetainedComponent::instantiate(
        artifact.source(),
        &crate::me_backend::instance_config("rbc-execution", options).map_err(|e| e.to_string())?,
        None,
    )
    .map_err(|e| e.to_string())?;
    let mut host = retained
        .into_lease_with_observer(options_host, Some(Box::new(observer)))
        .map_err(|e| e.to_string())?;
    if host.is_terminated() {
        host.finish_publication().map_err(|e| e.to_string())?;
        return Ok(host.finish());
    }
    let plugin = crate::me_backend::plugin_for_host(
        &host,
        options,
        rumoca_solver_rk45::model_exchange_integrator,
    )
    .map_err(|e| e.to_string())?;
    let mut session = host.into_session(plugin).map_err(|e| e.to_string())?;
    session
        .run_to_stop(&mut cursor)
        .map_err(|e| e.to_string())?;
    session.finish_publication().map_err(|e| e.to_string())?;
    Ok(session.finish())
}

#[cfg(feature = "solver-rk45")]
struct NativePublication(rumoca_eval_solve::execution::CsvExecution);
#[cfg(feature = "solver-rk45")]
impl PublicationObserver for NativePublication {
    fn publish(
        &mut self,
        time: f64,
        phase: &str,
        names: &[String],
        values: &[f64],
    ) -> Result<(), String> {
        self.0.publish(time, phase, names, values)
    }
    fn finish(&mut self) -> Result<(), String> {
        self.0.finish()
    }
}
