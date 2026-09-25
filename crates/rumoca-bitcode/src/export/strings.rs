use super::*;

pub(super) fn format<'dae>(
    format: dae::StringConversionFormatView<'dae>,
    check: impl Fn(dae::ExprId<'dae>) -> Result<ExprId, ExportError>,
) -> Result<RbcStringConversionFormat, ExportError> {
    Ok(match format {
        dae::StringConversionFormatView::Options {
            minimum_length,
            left_justified,
            significant_digits,
        } => RbcStringConversionFormat::Options {
            minimum_length: minimum_length.map(&check).transpose()?,
            left_justified: left_justified.map(&check).transpose()?,
            significant_digits: significant_digits.map(&check).transpose()?,
        },
        dae::StringConversionFormatView::Format { value } => RbcStringConversionFormat::Format {
            value: check(value)?,
        },
    })
}
