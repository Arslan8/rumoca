use super::*;

// The public StringConversion tag identifies the predefined MLS operation.
// Import gives that one declaration a fresh local slot; no source-name lookup
// or source compiler DefId crosses the public interchange boundary.
pub(super) const DECLARATION: rumoca_core::DefId = rumoca_core::DefId(0);

pub(super) fn format<'dae>(
    format: &RbcStringConversionFormat,
    expressions: &[dae::ExprId<'dae>],
    ctx: &Rebuild<'_>,
) -> Result<dae::StringConversionFormatInput<'dae>, dae::DaeConstructionError> {
    let expression = |id: ExprId| resolve(expressions, id.0, "expression", ctx);
    Ok(match format {
        RbcStringConversionFormat::Options {
            minimum_length,
            left_justified,
            significant_digits,
        } => dae::StringConversionFormatInput::Options {
            minimum_length: minimum_length.map(expression).transpose()?,
            left_justified: left_justified.map(expression).transpose()?,
            significant_digits: significant_digits.map(expression).transpose()?,
        },
        RbcStringConversionFormat::Format { value } => dae::StringConversionFormatInput::Format {
            value: expression(*value)?,
        },
    })
}
