//! CLI boundaries for public, writable execution artifacts.
mod overrides;
use anyhow::{Context, Result, bail};
use clap::Args;
use rumoca_bitcode::{Encoding, RbcFile};
use rumoca_ir_solve as solve;
use sha1::{Digest, Sha1};
use std::path::{Path, PathBuf};

#[derive(Debug, Args)]
pub struct LowerArgs {
    pub input: PathBuf,
    #[arg(short, long)]
    pub output: PathBuf,
    /// Semantic RBC variable IDs to preserve. Repeated; absent selects all.
    #[arg(long)]
    pub observe: Vec<u32>,
}

#[derive(Debug, Args)]
pub struct RunArgs {
    pub input: PathBuf,
    #[arg(long, default_value = "require")]
    pub execution: String,
    #[arg(long, default_value = "rk45")]
    pub backend: String,
    #[arg(long, default_value_t = 0.0)]
    pub start: f64,
    #[arg(long, default_value_t = 5.0)]
    pub stop: f64,
    #[arg(long, default_value_t = 0.1)]
    pub publish_interval: f64,
    #[arg(long, default_value_t = 1e-9)]
    pub rtol: f64,
    #[arg(long, default_value_t = 1e-11)]
    pub atol: f64,
    #[arg(long)]
    pub trace_root: PathBuf,
    /// Optional ordinary simulation result, for independent neutrality tests.
    #[arg(long)]
    pub result: Option<PathBuf>,
    /// Set a retained tunable scalar parameter without re-lowering.
    #[arg(long = "param")]
    pub parameters: Vec<String>,
    /// Override a scalar state start (refuses explicit initialization owners).
    #[arg(long = "initial")]
    pub initial_values: Vec<String>,
    /// Capture reached scalar domain violations with the native interpreter.
    #[arg(long)]
    pub domain_diagnostics: bool,
}

pub fn digest(file: &RbcFile) -> Result<String> {
    Ok(format!(
        "sha1:{:x}",
        Sha1::digest(serde_json::to_vec(&file.model)?)
    ))
}

pub fn check(file: &RbcFile) -> Result<()> {
    let execution = file
        .execution
        .as_ref()
        .context("artifact has no execution program; explicitly lower first")?;
    if execution.equation_digest != digest(file)? {
        bail!(
            "stale execution: equation artifact changed; explicitly re-lower and replay compatible execution passes"
        );
    }
    let mut options = rumoca_bitcode::validate::ValidateOptions::default();
    options.reject_unsupported = true;
    rumoca_bitcode::validate(&file.model, &options).map_err(|errors| {
        anyhow::anyhow!(
            "invalid equation artifact: {}",
            errors
                .iter()
                .map(ToString::to_string)
                .collect::<Vec<_>>()
                .join("; ")
        )
    })?;
    rumoca_sim::execution::check(execution).map_err(anyhow::Error::msg)
}

pub fn lower(args: LowerArgs) -> Result<()> {
    let (mut file, _) = rumoca_bitcode::read_file(&args.input)?;
    if file.execution.is_some() {
        bail!(
            "lower-execution requires an equation-only artifact; retain recipes and explicitly replay passes"
        );
    }
    let dae = rumoca_bitcode::import(&file)?;
    let model = rumoca_sim::lower_dae_for_simulation(&dae, &Default::default())?;
    let ids = if args.observe.is_empty() {
        file.model.variables.iter().map(|v| v.id.0).collect()
    } else {
        args.observe
    };
    let requested = ids
        .iter()
        .map(|id| {
            let v = file
                .model
                .variables
                .iter()
                .find(|v| v.id.0 == *id)
                .with_context(|| format!("unknown observation variable {id}"))?;
            Ok((*id, v.name.clone()))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut numerical =
        rumoca_sim::execution::lower(&model, &requested).map_err(anyhow::Error::msg)?;
    for storage in &mut numerical.storage {
        if let Some(variable) = file.model.variables.iter().find(|v| v.name == storage.name) {
            storage.causality = serde_json::to_value(variable.causality)?
                .as_str()
                .context("invalid causality")?
                .into();
            storage.unit = variable.unit.clone();
        }
    }
    file.execution = Some(solve::execution::ExecutionArtifact {
        version: 1,
        equation_digest: digest(&file)?,
        lowering: "solve-scalar-v1".into(),
        revision: 0,
        passes: vec![],
        numerical,
        functions: ["run_start", "publish", "run_finish"]
            .into_iter()
            .map(|s| (s.into(), vec![]))
            .collect(),
        sinks: vec![],
    });
    check(&file)?;
    rumoca_bitcode::write_file(&args.output, &file, Encoding::Json)?;
    Ok(())
}

pub fn check_path(path: &Path) -> Result<()> {
    let (file, _) = rumoca_bitcode::read_file(path)?;
    check(&file)?;
    println!("valid execution v1; fresh derivation; native RK45 capable");
    Ok(())
}

pub fn run(args: RunArgs) -> Result<()> {
    if args.execution != "require" || args.backend != "rk45" {
        bail!(
            "unsupported execution mode/backend: public execution v1 requires --execution=require --backend=rk45"
        );
    }
    if !args.start.is_finite()
        || !args.stop.is_finite()
        || args.stop < args.start
        || !args.publish_interval.is_finite()
        || args.publish_interval <= 0.0
        || !args.rtol.is_finite()
        || args.rtol <= 0.0
        || !args.atol.is_finite()
        || args.atol <= 0.0
    {
        bail!("invalid simulation interval/tolerances");
    }
    let (mut file, _) = rumoca_bitcode::read_file(&args.input)?;
    check(&file)?;
    overrides::apply(&mut file, &args.parameters, &args.initial_values)?;
    check(&file)?;
    let options = rumoca_sim::SimOptions {
        t_start: args.start,
        t_end: args.stop,
        dt: Some(args.publish_interval),
        rtol: args.rtol,
        atol: args.atol,
        solver_mode: rumoca_sim::SimSolverMode::RkLike,
        ..Default::default()
    };
    let runner = if args.domain_diagnostics {
        rumoca_sim::execution::run_with_domain_diagnostics
    } else {
        rumoca_sim::execution::run
    };
    let result = runner(
        file.execution.as_ref().context("missing executable")?,
        &options,
        &args.trace_root,
    )
    .map_err(|message| {
        anyhow::anyhow!(serde_json::json!({"kind": "execution-failure", "detail": message}))
    })?;
    if let Some(path) = args.result {
        std::fs::write(
            path,
            serde_json::to_vec(
                &serde_json::json!({"times": result.times, "names": result.names, "data": result.data}),
            )?,
        )?;
    }
    println!(
        "executed saved program; {} published times",
        result.times.len()
    );
    Ok(())
}
