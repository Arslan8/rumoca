//! Reissue checked clock construction; never infer schedules from source text.
use super::*;
use rumoca_core::{ClockLattice, ClockRational, PeriodicClockSchedule};

fn rational(
    value: &RbcClockRational,
    ctx: &Rebuild<'_>,
) -> Result<ClockRational, dae::DaeConstructionError> {
    let parse = |text: &str| {
        text.parse::<i128>()
            .map_err(|_| ctx.unsupported("clock rational requires a decimal 128-bit integer"))
    };
    ClockRational::new(parse(&value.numerator)?, parse(&value.denominator)?)
        .map_err(|error| ctx.unsupported(error.to_string()))
}

pub(super) fn rebuild<'dae>(
    construction: &mut dae::DaeConstruction<'dae>,
    ctx: &Rebuild<'_>,
    variables: &[VariableSlot<'dae>],
    conditions: &[dae::ConditionId<'dae>],
) -> Result<Vec<dae::ClockId<'dae>>, dae::DaeConstructionError> {
    let mut ids = Vec::with_capacity(ctx.model.clocks.len());
    for clock in &ctx.model.clocks {
        let at = ctx.provenance(clock.provenance)?;
        let id = construction.clocks(|owner| match &clock.node {
            RbcClockNode::Periodic {
                period,
                phase,
                anchor,
            } => {
                let lattice = ClockLattice::new(rational(period, ctx)?, rational(phase, ctx)?)
                    .map_err(|error| ctx.unsupported(error.to_string()))?;
                let schedule = match anchor {
                    RbcClockAnchor::Absolute => PeriodicClockSchedule::absolute(lattice),
                    RbcClockAnchor::SimulationStart => {
                        PeriodicClockSchedule::simulation_start_relative(lattice)
                    }
                }
                .map_err(|error| ctx.unsupported(error.to_string()))?;
                owner.scheduled(schedule, at).map(Into::into)
            }
            RbcClockNode::Triggered { condition } => {
                owner.triggered(resolve(conditions, condition.0, "condition", ctx)?, at)
            }
        })?;
        ids.push(id);
    }
    for ownership in &ctx.model.clock_ownerships {
        let at = ctx.provenance(ownership.provenance)?;
        let clock = resolve(&ids, ownership.clock.0, "clock", ctx)?;
        let variable = resolve(variables, ownership.variable.0, "variable", ctx)?;
        construction.clocks(|owner| match (variable, ownership.sampled) {
            (VariableSlot::DiscreteReal(id), false) => owner.own_discrete_real(clock, id, at),
            (VariableSlot::DiscreteReal(id), true) => {
                owner.own_sampled_discrete_real(clock, id, at)
            }
            (VariableSlot::DiscreteValue(id), false) => owner.own_discrete_value(clock, id, at),
            (VariableSlot::DiscreteValue(id), true) => {
                owner.own_sampled_discrete_value(clock, id, at)
            }
            _ => Err(ctx.unsupported("clock ownership requires a discrete variable")),
        })?;
    }
    Ok(ids)
}
