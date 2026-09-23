//! CLI transport for the public bitcode linker. Semantics live in bitcode.
use std::io::Write;
use std::path::PathBuf;

use anyhow::{Context, Result, bail};
use clap::Args;
use rumoca_bitcode::link::{LinkInput, link};

use crate::bitcode_cli::BitcodeFormat;

#[derive(Args, Debug)]
pub struct LinkArgs {
    /// Input instances, e.g. motor=motor.rbc load=load.rbc.
    #[arg(required = true, num_args = 1.., value_name = "NAMESPACE=FILE")]
    pub inputs: Vec<String>,
    /// New artifact path. Must not already exist (inputs are never overwritten).
    #[arg(short, long)]
    pub output: PathBuf,
    /// Name of the combined model.
    #[arg(long, default_value = "LinkedModel")]
    pub name: String,
    #[arg(long, value_enum, default_value_t = BitcodeFormat::Cbor)]
    pub format: BitcodeFormat,
    /// Discard input execution programs, numerical edits and instrumentation.
    /// The result contains equations only and must be lowered again.
    #[arg(long)]
    pub discard_execution: bool,
}

pub fn run(args: LinkArgs) -> Result<()> {
    let mut files = Vec::new();
    for input in &args.inputs {
        let Some((namespace, path)) = input.split_once('=') else {
            bail!("input {input:?}: expected NAMESPACE=FILE");
        };
        let (file, _) = rumoca_bitcode::read_file(std::path::Path::new(path))
            .with_context(|| format!("read module {namespace:?} from {path}"))?;
        files.push((namespace, file));
    }
    let inputs: Vec<_> = files
        .iter()
        .map(|(namespace, file)| LinkInput { namespace, file })
        .collect();
    let output = link(&args.name, &inputs, args.discard_execution)?;
    let bytes = rumoca_bitcode::encode(&output, args.format.into())?;
    // Only create a file after every input and the complete result validated.
    let mut file = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&args.output)
        .with_context(|| format!("create new output {}", args.output.display()))?;
    file.write_all(&bytes).context("write linked bitcode")?;
    eprintln!(
        "linked {} modules into {} (equations only; no new connections)",
        inputs.len(),
        args.output.display()
    );
    Ok(())
}
