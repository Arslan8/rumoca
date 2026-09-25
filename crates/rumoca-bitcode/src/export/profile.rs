//! Reject semantic owners the public schema cannot faithfully transport.
use super::*;

pub(super) fn check(view: dae::DaeView<'_>) -> Result<(), ExportError> {
    let owners = [
        (
            "model_event_transactions",
            view.model_event_transaction_count(),
        ),
        ("structured_roots", view.structured_root_count()),
        ("previous_values", view.previous_value_count()),
        ("terminals", view.terminal_count()),
        ("delays", view.delay_count()),
    ];
    if let Some((name, _)) = owners.into_iter().find(|(_, count)| *count != 0) {
        return Err(ExportError::UnsupportedOwner(name));
    }
    Ok(())
}
