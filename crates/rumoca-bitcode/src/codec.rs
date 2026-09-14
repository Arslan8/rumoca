//! Encoding and decoding of `.rbc` artifacts.
//!
//! Two encodings carry the same schema:
//!
//! * [`Encoding::Cbor`] — the production binary encoding. Self-describing and
//!   map-keyed, so a field a reader does not know is skipped rather than
//!   shifting every field after it. Contrast with an ordinal-tagged codec,
//!   where inserting an enum variant silently changes how old payloads decode.
//! * [`Encoding::Json`] — the debugging encoding, byte-for-byte the same data.
//!
//! The encoding is detected on read, so a consumer never has to be told which
//! one it was handed.

use std::path::Path;

use crate::schema::{RBC_MAGIC, RbcFile};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Encoding {
    /// Compact binary. The default for `.rbc`.
    Cbor,
    /// Human-readable. Same schema, larger.
    Json,
}

impl Encoding {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Cbor => "cbor",
            Self::Json => "json",
        }
    }
}

#[derive(Debug, thiserror::Error)]
pub enum CodecError {
    #[error("cannot read {path}: {source}")]
    Read {
        path: String,
        #[source]
        source: std::io::Error,
    },
    #[error("cannot write {path}: {source}")]
    Write {
        path: String,
        #[source]
        source: std::io::Error,
    },
    #[error("malformed bitcode: {0}")]
    Malformed(String),
    #[error("{0}")]
    Header(String),
}

/// Encode an artifact.
pub fn encode(file: &RbcFile, encoding: Encoding) -> Result<Vec<u8>, CodecError> {
    match encoding {
        Encoding::Json => serde_json::to_vec_pretty(file)
            .map(|mut bytes| {
                bytes.push(b'\n');
                bytes
            })
            .map_err(|error| CodecError::Malformed(error.to_string())),
        Encoding::Cbor => {
            let mut bytes = Vec::new();
            ciborium::into_writer(file, &mut bytes)
                .map_err(|error| CodecError::Malformed(error.to_string()))?;
            Ok(bytes)
        }
    }
}

/// Decode an artifact, detecting the encoding, then check its header.
///
/// Header checking happens here rather than in the caller so that no code path
/// can obtain an `RbcFile` of an unsupported version.
pub fn decode(bytes: &[u8]) -> Result<(RbcFile, Encoding), CodecError> {
    let encoding = detect(bytes);
    let file: RbcFile = match encoding {
        Encoding::Json => serde_json::from_slice(bytes)
            .map_err(|error| CodecError::Malformed(format!("invalid JSON bitcode: {error}")))?,
        Encoding::Cbor => ciborium::from_reader(bytes)
            .map_err(|error| CodecError::Malformed(format!("invalid CBOR bitcode: {error}")))?,
    };
    file.check_header().map_err(CodecError::Header)?;
    Ok((file, encoding))
}

/// Guess the encoding from the leading bytes.
///
/// JSON always starts with `{` after optional whitespace; CBOR's first byte is
/// a major-type header that is never `{`.
fn detect(bytes: &[u8]) -> Encoding {
    let first = bytes.iter().find(|byte| !byte.is_ascii_whitespace());
    match first {
        Some(b'{') => Encoding::Json,
        _ => Encoding::Cbor,
    }
}

pub fn write_file(path: &Path, file: &RbcFile, encoding: Encoding) -> Result<(), CodecError> {
    let bytes = encode(file, encoding)?;
    if let Some(parent) = path
        .parent()
        .filter(|parent| !parent.as_os_str().is_empty())
    {
        std::fs::create_dir_all(parent).map_err(|source| CodecError::Write {
            path: parent.display().to_string(),
            source,
        })?;
    }
    std::fs::write(path, bytes).map_err(|source| CodecError::Write {
        path: path.display().to_string(),
        source,
    })
}

pub fn read_file(path: &Path) -> Result<(RbcFile, Encoding), CodecError> {
    let bytes = std::fs::read(path).map_err(|source| CodecError::Read {
        path: path.display().to_string(),
        source,
    })?;
    if bytes.is_empty() {
        return Err(CodecError::Malformed(format!(
            "{} is empty; expected a {RBC_MAGIC} artifact",
            path.display()
        )));
    }
    decode(&bytes)
}

/// Re-encode a decoded artifact as pretty JSON, for `rumoca bitcode dump`.
///
/// This renders the *typed* view, so a field this build does not know is not
/// shown. Use [`transcode`] when the goal is to preserve an artifact exactly.
pub fn to_json(file: &RbcFile) -> Result<String, CodecError> {
    serde_json::to_string_pretty(file).map_err(|error| CodecError::Malformed(error.to_string()))
}

/// Re-encode raw bytes into another encoding without going through the typed
/// schema.
///
/// Converting between encodings must not be a lossy operation. Decoding into
/// [`RbcFile`] would silently drop any field this build does not know — which
/// is correct when *rebuilding a model*, and wrong when the user asked only to
/// change how the same artifact is stored. A producer newer than this reader
/// must survive `convert` and `dump` intact.
///
/// The header is still checked first: transcoding something that is not
/// bitcode, or is a version this build cannot interpret, would be a silent
/// pass-through of garbage.
pub fn transcode(bytes: &[u8], to: Encoding) -> Result<Vec<u8>, CodecError> {
    let (_checked, from) = decode(bytes)?;
    let document: serde_json::Value = match from {
        Encoding::Json => serde_json::from_slice(bytes)
            .map_err(|error| CodecError::Malformed(error.to_string()))?,
        Encoding::Cbor => ciborium::from_reader(bytes)
            .map_err(|error| CodecError::Malformed(error.to_string()))?,
    };
    match to {
        Encoding::Json => serde_json::to_vec_pretty(&document)
            .map(|mut bytes| {
                bytes.push(b'\n');
                bytes
            })
            .map_err(|error| CodecError::Malformed(error.to_string())),
        Encoding::Cbor => {
            let mut out = Vec::new();
            ciborium::into_writer(&document, &mut out)
                .map_err(|error| CodecError::Malformed(error.to_string()))?;
            Ok(out)
        }
    }
}

/// Render raw bytes as pretty JSON, preserving unknown fields.
pub fn dump_json(bytes: &[u8]) -> Result<String, CodecError> {
    let json = transcode(bytes, Encoding::Json)?;
    String::from_utf8(json).map_err(|error| CodecError::Malformed(error.to_string()))
}
