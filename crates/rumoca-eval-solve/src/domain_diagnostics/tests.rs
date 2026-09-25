use super::*;
use solve::{BinaryOp as B, CompareOp as C, LinearOp as L};

fn guarded() -> Vec<L> {
    vec![
        L::Const { dst: 0, value: 1.0 },
        L::LoadP { dst: 1, index: 0 },
        L::Binary {
            dst: 2,
            op: B::Div,
            lhs: 0,
            rhs: 1,
        },
        L::Const { dst: 3, value: 0.0 },
        L::Compare {
            dst: 4,
            op: C::Ne,
            lhs: 1,
            rhs: 3,
        },
        L::Select {
            dst: 5,
            cond: 4,
            if_true: 2,
            if_false: 3,
        },
        L::StoreOutput { src: 5 },
    ]
}

#[test]
fn inactive_short_select_does_not_report_a_zero() {
    let scope = Scope::start().unwrap();
    let row = guarded();
    for p in [0.0, 2.0, 0.0] {
        let result = crate::eval_row(&row, &[], &[p], 0.0, None).unwrap();
        assert_eq!(result, if p == 0.0 { 0.0 } else { 0.5 });
    }
    assert_eq!(scope.finish()["faults"], json!([]));
}

#[test]
fn an_active_zero_is_recorded_without_changing_arithmetic() {
    let scope = Scope::start().unwrap();
    let mut row = guarded()[..3].to_vec();
    row.push(L::StoreOutput { src: 2 });
    assert!(
        crate::eval_row(&row, &[], &[0.0], 0.125, None)
            .unwrap()
            .is_infinite()
    );
    let evidence = scope.finish();
    assert_eq!(evidence["faults"][0]["operand_value"], 0.0);
    assert_eq!(evidence["faults"][0]["time"], 0.125);
    assert_eq!(evidence["faults"][0]["instruction_index"], 2);
    assert!(!active());
}

#[test]
fn a_reassigned_register_retains_sequential_semantics_and_reports_gap() {
    let scope = Scope::start().unwrap();
    let row = [
        L::Const { dst: 0, value: 1.0 },
        L::Const { dst: 1, value: 2.0 },
        L::Binary {
            dst: 0,
            op: B::Add,
            lhs: 0,
            rhs: 1,
        },
        L::StoreOutput { src: 0 },
    ];
    assert_eq!(crate::eval_row(&row, &[], &[], 0.0, None).unwrap(), 3.0);
    assert_eq!(scope.finish()["unobserved_evaluations"], 1);
}

#[test]
fn scope_is_thread_local_and_resets_on_drop() {
    let scope = Scope::start().unwrap();
    assert!(Scope::start().is_err());
    assert!(!std::thread::spawn(active).join().unwrap());
    drop(scope);
    assert!(!active());
}

#[test]
fn bad_register_flow_keeps_the_checked_evaluator_error() {
    let scope = Scope::start().unwrap();
    assert!(crate::eval_row(&[L::StoreOutput { src: 0 }], &[], &[], 0.0, None).is_err());
    assert!(scope.finish()["faults"].as_array().unwrap().is_empty());
}
