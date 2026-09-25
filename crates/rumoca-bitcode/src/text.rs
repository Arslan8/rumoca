//! A parseable textual form of Rumoca Bitcode — the `.ll` to the `.rbc`.
//!
//! `bitcode disasm` renders a *listing*: readable, lossy, one-way. JSON
//! round-trips but is a serialization nobody edits by hand. This is the third
//! thing, and the one a debugger actually wants: text you can read, edit, and
//! assemble back into a byte-identical artifact.
//!
//! ```text
//! rbc 2
//! producer "rumoca 0.10.0"
//! model "Modelica.Electrical.Analog.Examples.ChuaCircuit"
//!
//! $0 type real
//! %6 var "L.L" $0 parameter parameter scalars 1 unit "H" quantity "Inductance"
//!    binding ^24 @src 0 224 237 7 3
//! ^24 expr $0 lit real 18
//! ^83 expr $0 bin sub ^81 ^82 @src 5 224 237 7 3
//! eq 3 ^83 reads %0 %1 dreads %0 @src 5 224 237 7 3
//! ```
//!
//! **Every id is written explicitly.** Expressions form a flat table addressed
//! by index, exactly like a constant pool, and equations reference them by id.
//! Re-deriving indices on parse would renumber a model that contains duplicate
//! nodes — a real artifact has two separate `0` literals at ids 22 and 23 — so
//! the ids are data, not presentation, and the format states them.
//!
//! **Nothing is dropped silently.** Printing a construct this version cannot
//! represent is an error, not an omission. A textual IR that quietly loses a
//! section would assemble into a different model than the one it came from,
//! which is worse than refusing.
//!
//! The one deliberate exception is source *text*, which is omitted unless
//! asked for: it is most of the artifact's bytes and none of its semantics.
//! `print_text_with` takes the choice, and a round-trip through the form
//! without it preserves everything except that text.

mod parser;
mod writer;

use crate::schema::*;
pub use parser::parse_text;
pub use writer::{print_text, print_text_with};

/// Errors from reading the textual form. A line number always accompanies the
/// message, because a parse failure the reader cannot locate is a bad error.
#[derive(Debug, thiserror::Error)]
#[error("line {line}: {message}")]
pub struct TextError {
    pub line: usize,
    pub message: String,
}

impl TextError {
    fn at(line: usize, message: impl Into<String>) -> Self {
        Self {
            line,
            message: message.into(),
        }
    }
}

#[derive(Debug, Clone, Copy, Default)]
pub struct TextOptions {
    /// Include each source file's full text. Off by default: it is most of the
    /// bytes and none of the semantics.
    pub sources: bool,
}
