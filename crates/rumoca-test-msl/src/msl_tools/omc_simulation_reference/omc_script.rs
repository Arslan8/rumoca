//! Explicit socket-free OMC transport. Same simulate call and trace comparator.
use super::{
    SessionModelOutcome, SessionWorkerCtx, build_session_model_result, session_error_result,
};
use anyhow::{Context, Result};
use std::process::{Command, Stdio};
use std::time::Instant;

pub(super) fn run(ctx: &SessionWorkerCtx<'_>, idx: usize, model: &str) -> SessionModelOutcome {
    let start = Instant::now();
    let (result, timed_out) = match execute(ctx, idx, model) {
        Ok((Some(outcome), false)) => (
            build_session_model_result(&outcome, start.elapsed().as_secs_f64()),
            false,
        ),
        Ok(_) => (
            super::session_timeout_result(start.elapsed().as_secs_f64(), ctx.sim_timeout),
            true,
        ),
        Err(error) => (
            session_error_result(format!("OMC script failed: {error:#}")),
            false,
        ),
    };
    SessionModelOutcome {
        idx,
        model: model.into(),
        result,
        elapsed_seconds: start.elapsed().as_secs_f64(),
        timed_out,
    }
}

fn execute(
    ctx: &SessionWorkerCtx<'_>,
    idx: usize,
    model: &str,
) -> Result<(Option<super::OmcSimOutcome>, bool)> {
    std::fs::create_dir_all(ctx.work_dir)?;
    let script = ctx.work_dir.join(format!("reference-{idx}.mos"));
    let log = ctx.work_dir.join(format!("reference-{idx}.log"));
    let mut lines = ctx.msl_exprs.to_vec();
    let stop = if ctx.use_experiment {
        String::new()
    } else {
        format!("stopTime={}, ", ctx.stop_time)
    };
    lines.push(format!(
        "simulate({model}, {stop}outputFormat=\"csv\", fileNamePrefix=\"{model}\");"
    ));
    lines.push("getErrorString();".into());
    std::fs::write(&script, lines.join("\n"))?;
    let output = std::fs::File::create(&log)?;
    let mut command = Command::new("omc");
    command
        .arg(&script)
        .arg("--locale=C")
        .current_dir(ctx.work_dir)
        .stdin(Stdio::null())
        .stdout(output.try_clone()?)
        .stderr(output);
    super::super::common::apply_omc_thread_env(&mut command, ctx.omc_threads);
    #[cfg(unix)]
    std::os::unix::process::CommandExt::process_group(&mut command, 0);
    let mut child = command.spawn().context("start omc")?;
    let started = Instant::now();
    let status = loop {
        if let Some(status) = child.try_wait()? {
            break status;
        }
        if started.elapsed() >= ctx.sim_timeout {
            #[cfg(unix)]
            if let Ok(pid) = i32::try_from(child.id()) {
                let _ = nix::sys::signal::killpg(
                    nix::unistd::Pid::from_raw(pid),
                    nix::sys::signal::Signal::SIGKILL,
                );
            }
            let _ = child.kill();
            let _ = child.wait();
            return Ok((None, true));
        }
        std::thread::sleep(std::time::Duration::from_millis(20));
    };
    let text = std::fs::read_to_string(log)?;
    anyhow::ensure!(status.success(), "omc exited {status}: {text}");
    let outcome = super::omc_session::parse_sim_record(&text, text.clone());
    anyhow::ensure!(
        outcome.result_file.is_some(),
        "no simulation result: {text}"
    );
    Ok((Some(outcome), false))
}
