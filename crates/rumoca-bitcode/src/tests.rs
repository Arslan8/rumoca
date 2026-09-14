//! Round-trip, codec, and adversarial tests.
//!
//! The adversarial cases matter most: an external pass is untrusted, so every
//! way a malformed artifact could reach reconstruction must be a clean
//! rejection rather than a panic or an invalid model.

use crate::codec::{Encoding, decode, encode};
use crate::schema::*;
use crate::validate::{ValidateOptions, ValidationError, recompute_summary, validate};

// ── Fixtures ─────────────────────────────────────────────────────────────────

fn span() -> RbcSpan {
    RbcSpan {
        source: SourceId(0),
        start: 0,
        end: 4,
        line: 1,
        column: 1,
    }
}

fn source_provenance() -> RbcProvenance {
    RbcProvenance {
        origin: RbcOrigin::Source,
        span: span(),
    }
}

/// `der(x) = -k*x` in bitcode form: two variables, one residual.
fn decay_model() -> RbcModel {
    let mut model = RbcModel {
        name: "Decay".into(),
        sources: vec![RbcSource {
            id: SourceId(0),
            name: "Decay.mo".into(),
            text: Some("model Decay end Decay;".into()),
        }],
        types: vec![RbcType {
            id: TypeId(0),
            scalar: RbcScalar::Real,
            dimensions: Vec::new(),
        }],
        variables: vec![
            variable(0, "x", RbcRole::State),
            variable(1, "k", RbcRole::Parameter),
        ],
        expressions: vec![
            expression(
                0,
                RbcExprNode::Coordinate {
                    coordinate: RbcCoordinate::Derivative {
                        variable: VariableId(0),
                    },
                },
            ),
            expression(
                1,
                RbcExprNode::Coordinate {
                    coordinate: RbcCoordinate::Parameter {
                        variable: VariableId(1),
                    },
                },
            ),
            expression(
                2,
                RbcExprNode::Coordinate {
                    coordinate: RbcCoordinate::State {
                        variable: VariableId(0),
                    },
                },
            ),
            expression(
                3,
                RbcExprNode::Binary {
                    op: RbcBinaryOp::Multiply,
                    lhs: ExprId(1),
                    rhs: ExprId(2),
                },
            ),
            expression(
                4,
                RbcExprNode::Unary {
                    op: RbcUnaryOp::Negate,
                    operand: ExprId(3),
                },
            ),
            expression(
                5,
                RbcExprNode::Binary {
                    op: RbcBinaryOp::Subtract,
                    lhs: ExprId(0),
                    rhs: ExprId(4),
                },
            ),
        ],
        equations: vec![RbcEquation {
            id: EquationId(0),
            residual: ExprId(5),
            provenance: source_provenance(),
            reads: vec![VariableId(0), VariableId(1)],
            reads_derivative: vec![VariableId(0)],
        }],
        initial_equations: Vec::new(),
        relations: Vec::new(),
        conditions: Vec::new(),
        roots: Vec::new(),
        events: Vec::new(),
        time_events: Vec::new(),
        connections: Vec::new(),
        components: Vec::new(),
        trace_points: Vec::new(),
        discrete_definitions: Vec::new(),
        summary: RbcSummary::default(),
    };
    recompute_summary(&mut model);
    model
}

fn variable(id: u32, name: &str, role: RbcRole) -> RbcVariable {
    RbcVariable {
        id: VariableId(id),
        name: name.into(),
        role,
        causality: RbcCausality::Local,
        value_type: TypeId(0),
        scalar_count: 1,
        declaration: source_provenance(),
        component: None,
        unit: None,
        description: None,
        binding: None,
        start: None,
        min: None,
        max: None,
        nominal: None,
        fixed: None,
        tunable: false,
        from_source: true,
        connector: None,
    }
}

fn expression(id: u32, node: RbcExprNode) -> RbcExpr {
    RbcExpr {
        id: ExprId(id),
        value_type: TypeId(0),
        node,
        provenance: source_provenance(),
    }
}

fn file(model: RbcModel) -> RbcFile {
    RbcFile {
        magic: RBC_MAGIC.into(),
        bitcode_version: RBC_VERSION,
        producer: "test".into(),
        model,
    }
}

fn errors(model: &RbcModel) -> Vec<ValidationError> {
    validate(model, &ValidateOptions::default()).unwrap_err()
}

// ── Header ───────────────────────────────────────────────────────────────────

#[test]
fn header_rejects_foreign_magic() {
    let mut file = file(decay_model());
    file.magic = "NOT-RBC".into();
    assert!(file.check_header().is_err());
}

#[test]
fn header_rejects_another_version() {
    let mut file = file(decay_model());
    file.bitcode_version = RBC_VERSION + 1;
    assert!(file.check_header().is_err());
}

// ── Discrete value definitions (MLS Appendix B.1c) ───────────────────────────

/// A `discrete_value` variable must arrive with a definition.
///
/// Bitcode v1 originally had no field for B.1c definitions at all, so
/// `Boolean b; b = x < 0.5;` exported a variable nothing defined and
/// reconstruction refused it with "missing B.1c topology definition". The
/// artifact was internally consistent and passed validation, which is what
/// made it hard to see — so validation now states the invariant too.
#[test]
fn a_discrete_value_variable_carries_its_definition() {
    let mut model = decay_model();
    model.types.push(RbcType {
        id: TypeId(1),
        scalar: RbcScalar::Boolean,
        dimensions: Vec::new(),
    });
    let target = VariableId(model.variables.len() as u32);
    let mut flag = variable(target.0, "b", RbcRole::DiscreteValue);
    flag.value_type = TypeId(1);
    model.variables.push(flag);

    let value = ExprId(model.expressions.len() as u32);
    model.expressions.push(RbcExpr {
        id: value,
        value_type: TypeId(1),
        node: RbcExprNode::Literal {
            value: RbcLiteral::Boolean { value: true },
        },
        provenance: source_provenance(),
    });
    model.discrete_definitions.push(RbcDiscreteDefinition {
        targets: vec![target],
        branches: vec![RbcDiscreteBranch {
            activation: RbcDiscreteActivation::Always,
            values: vec![value],
            provenance: source_provenance(),
        }],
        provenance: source_provenance(),
    });
    recompute_summary(&mut model);

    assert_eq!(model.summary.discrete_definitions, 1);
    assert!(
        validate(&model, &ValidateOptions::default()).is_ok(),
        "a defined discrete variable must validate: {:?}",
        errors(&model)
    );

    // And it must survive both encodings with its activation intact.
    for encoding in [Encoding::Cbor, Encoding::Json] {
        let bytes = encode(&file(model.clone()), encoding).expect("encode");
        let (decoded, _) = decode(&bytes).expect("decode");
        let definition = &decoded.model.discrete_definitions[0];
        assert_eq!(definition.targets, vec![target]);
        assert_eq!(definition.branches[0].values, vec![value]);
        assert!(matches!(
            definition.branches[0].activation,
            RbcDiscreteActivation::Always
        ));
    }
}

/// A `when` branch carries its trigger and guard, which is what distinguishes
/// it from a plain equation on the same target.
#[test]
fn a_when_branch_keeps_its_trigger_and_guard() {
    let branch = RbcDiscreteBranch {
        activation: RbcDiscreteActivation::When {
            trigger: ConditionId(2),
            guard: ConditionId(5),
        },
        values: vec![ExprId(7)],
        provenance: source_provenance(),
    };
    let bytes = serde_json::to_vec(&branch).expect("encode");
    let back: RbcDiscreteBranch = serde_json::from_slice(&bytes).expect("decode");
    assert_eq!(back, branch);
}

/// The invariant that would have caught BUG-009 at the producer.
#[test]
fn a_discrete_value_variable_with_no_definition_is_rejected() {
    let mut model = decay_model();
    model.types.push(RbcType {
        id: TypeId(1),
        scalar: RbcScalar::Boolean,
        dimensions: Vec::new(),
    });
    let id = model.variables.len() as u32;
    let mut flag = variable(id, "b", RbcRole::DiscreteValue);
    flag.value_type = TypeId(1);
    model.variables.push(flag);
    recompute_summary(&mut model);

    assert!(
        errors(&model).iter().any(|error| matches!(
            error,
            ValidationError::UndefinedDiscreteValue { id: reported, .. } if *reported == id
        )),
        "an undefined discrete variable must be a validation error, got {:?}",
        errors(&model)
    );
}

/// A branch must give exactly one value per target.
#[test]
fn a_discrete_branch_must_match_its_target_count() {
    let mut model = decay_model();
    model.types.push(RbcType {
        id: TypeId(1),
        scalar: RbcScalar::Boolean,
        dimensions: Vec::new(),
    });
    let target = VariableId(model.variables.len() as u32);
    let mut flag = variable(target.0, "b", RbcRole::DiscreteValue);
    flag.value_type = TypeId(1);
    model.variables.push(flag);
    model.discrete_definitions.push(RbcDiscreteDefinition {
        targets: vec![target],
        branches: vec![RbcDiscreteBranch {
            activation: RbcDiscreteActivation::Always,
            values: Vec::new(), // one target, no value
            provenance: source_provenance(),
        }],
        provenance: source_provenance(),
    });
    recompute_summary(&mut model);

    assert!(
        errors(&model)
            .iter()
            .any(|error| matches!(error, ValidationError::DiscreteBranchArity { .. })),
        "arity mismatch must be reported, got {:?}",
        errors(&model)
    );
}

// ── Enumerations ─────────────────────────────────────────────────────────────

/// An enumeration value must not be carried as an `Integer`.
///
/// It was, until a real MSL model (`OpAmpCircuits.Der`, whose
/// `opAmp.homotopyType` is an enumeration parameter) exported cleanly and then
/// failed to import with `expression type mismatch: expected Enumeration,
/// found Integer`. Export and import disagreeing is the one thing an
/// interchange format cannot do, so both directions are pinned here.
#[test]
fn enumeration_literal_keeps_its_type_through_the_codec() {
    let mut model = decay_model();
    model.types.push(RbcType {
        id: TypeId(1),
        scalar: RbcScalar::Enumeration,
        dimensions: Vec::new(),
    });
    let id = ExprId(model.expressions.len() as u32);
    model.expressions.push(RbcExpr {
        id,
        value_type: TypeId(1),
        node: RbcExprNode::Literal {
            value: RbcLiteral::Enumeration { ordinal: 3 },
        },
        provenance: source_provenance(),
    });
    recompute_summary(&mut model);

    for encoding in [Encoding::Cbor, Encoding::Json] {
        let bytes = encode(&file(model.clone()), encoding).expect("encode");
        let (decoded, _) = decode(&bytes).expect("decode");
        let node = &decoded.model.expressions[id.0 as usize].node;
        assert!(
            matches!(
                node,
                RbcExprNode::Literal {
                    value: RbcLiteral::Enumeration { ordinal: 3 }
                }
            ),
            "{encoding:?} degraded an enumeration literal to {node:?}",
        );
    }
}

/// MLS §4.9.5 ordinals are one-based, and `enumeration_literal` is the only
/// DAE constructor that proves it. A zero ordinal must survive the codec so
/// reconstruction is the thing that rejects it, with a span.
#[test]
fn enumeration_ordinal_is_carried_verbatim_for_reconstruction_to_judge() {
    let value = RbcLiteral::Enumeration { ordinal: 0 };
    let bytes = serde_json::to_vec(&value).expect("encode");
    let back: RbcLiteral = serde_json::from_slice(&bytes).expect("decode");
    assert_eq!(back, value);
}

// ── Codec ────────────────────────────────────────────────────────────────────

#[test]
fn both_encodings_carry_the_same_document() {
    let original = file(decay_model());
    for encoding in [Encoding::Cbor, Encoding::Json] {
        let bytes = encode(&original, encoding).expect("encode");
        let (decoded, detected) = decode(&bytes).expect("decode");
        assert_eq!(detected, encoding, "encoding must be detected from bytes");
        assert_eq!(decoded.model.name, original.model.name);
        assert_eq!(
            decoded.model.expressions.len(),
            original.model.expressions.len()
        );
    }
}

#[test]
fn re_encoding_a_decoded_document_is_byte_identical() {
    // The cheap determinism property: whatever a consumer decodes, it can
    // re-encode without drift. Milestone 2 requires deterministic export, and
    // this is the same obligation observed from the other side.
    let original = file(decay_model());
    for encoding in [Encoding::Cbor, Encoding::Json] {
        let first = encode(&original, encoding).expect("encode");
        let (decoded, _) = decode(&first).expect("decode");
        let second = encode(&decoded, encoding).expect("re-encode");
        assert_eq!(first, second, "{encoding:?} round trip must be stable");
    }
}

#[test]
fn garbage_is_rejected_not_guessed() {
    assert!(decode(b"not bitcode at all").is_err());
    assert!(decode(b"{\"magic\": \"RUMOCA-RBC\"").is_err());
}

#[test]
fn transcoding_preserves_fields_this_build_does_not_know() {
    // Forward compatibility: a newer producer may add fields. Changing how an
    // artifact is *stored* must not change what it *contains*, or `convert`
    // becomes a silent downgrade. The typed path deliberately drops them —
    // that is correct when rebuilding a model — so the two paths are asserted
    // against each other here.
    let original = file(decay_model());
    let json = encode(&original, Encoding::Json).expect("encode");
    let mut document: serde_json::Value = serde_json::from_slice(&json).expect("parse");
    document["model"]["variables"][0]["future_field"] = serde_json::json!("v2-data");
    document["model"]["future_collection"] = serde_json::json!([{"id": 0}]);
    let injected = serde_json::to_vec(&document).expect("re-encode");

    for encoding in [Encoding::Cbor, Encoding::Json] {
        let converted = crate::codec::transcode(&injected, encoding).expect("transcode");
        let back = crate::codec::dump_json(&converted).expect("dump");
        let seen: serde_json::Value = serde_json::from_str(&back).expect("parse");
        assert_eq!(
            seen["model"]["variables"][0]["future_field"],
            serde_json::json!("v2-data"),
            "{encoding:?} transcode dropped an unknown field"
        );
        assert!(
            seen["model"]["future_collection"].is_array(),
            "{encoding:?} transcode dropped an unknown collection"
        );
    }

    // The typed path is the contrast: it rebuilds only what it understands.
    let (typed, _) = decode(&injected).expect("decode");
    let typed_json = crate::codec::to_json(&typed).expect("render");
    assert!(
        !typed_json.contains("future_field"),
        "the typed view must not invent fields it cannot interpret"
    );
}

#[test]
fn transcoding_still_refuses_something_that_is_not_bitcode() {
    assert!(crate::codec::transcode(b"not bitcode", Encoding::Json).is_err());
}

// ── Validation: the artifact we produce is valid ─────────────────────────────

#[test]
fn a_well_formed_model_validates() {
    assert!(validate(&decay_model(), &ValidateOptions::default()).is_ok());
}

// ── Adversarial: every case from the project brief's mutation list ───────────

#[test]
fn rejects_reference_to_nonexistent_variable() {
    let mut model = decay_model();
    model.expressions[2].node = RbcExprNode::Coordinate {
        coordinate: RbcCoordinate::State {
            variable: VariableId(92831),
        },
    };
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::DanglingReference {
            target: "variable",
            id: 92831,
            ..
        }
    )));
}

#[test]
fn rejects_duplicate_id() {
    let mut model = decay_model();
    model.variables[1].id = VariableId(0);
    assert!(
        errors(&model)
            .iter()
            .any(|error| matches!(error, ValidationError::NonDenseId { .. }))
    );
}

#[test]
fn rejects_duplicate_variable_name() {
    let mut model = decay_model();
    model.variables[1].name = "x".into();
    assert!(
        errors(&model)
            .iter()
            .any(|error| matches!(error, ValidationError::DuplicateVariableName { .. }))
    );
}

#[test]
fn rejects_invalid_equation_reference() {
    let mut model = decay_model();
    model.equations[0].residual = ExprId(999);
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::DanglingReference {
            target: "expression",
            id: 999,
            ..
        }
    )));
}

#[test]
fn rejects_an_expression_cycle() {
    // Operands must be strictly earlier, which makes a cycle unrepresentable
    // rather than something to detect after the fact.
    let mut model = decay_model();
    model.expressions[3].node = RbcExprNode::Binary {
        op: RbcBinaryOp::Multiply,
        lhs: ExprId(3),
        rhs: ExprId(2),
    };
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::NonTopologicalOperand {
            expression: 3,
            operand: 3
        }
    )));
}

#[test]
fn rejects_forward_operand_reference() {
    let mut model = decay_model();
    model.expressions[0].node = RbcExprNode::Unary {
        op: RbcUnaryOp::Negate,
        operand: ExprId(5),
    };
    assert!(
        errors(&model)
            .iter()
            .any(|error| matches!(error, ValidationError::NonTopologicalOperand { .. }))
    );
}

#[test]
fn rejects_malformed_event() {
    let mut model = decay_model();
    model.events.push(RbcEventAction {
        id: EventId(0),
        trigger: ConditionId(7),
        guard: ConditionId(7),
        action: RbcAction::Reinitialize {
            state: VariableId(0),
            value: ExprId(0),
        },
        provenance: source_provenance(),
    });
    recompute_summary(&mut model);
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::DanglingReference {
            target: "condition",
            ..
        }
    )));
}

#[test]
fn rejects_invalid_connector_reference() {
    let mut model = decay_model();
    model.connections.push(RbcConnection {
        id: ConnectionId(0),
        left: VariableId(0),
        right: VariableId(404),
        quantity: RbcQuantityKind::Potential,
        left_connector: "a.p".into(),
        right_connector: "b.p".into(),
        equation: None,
        provenance: source_provenance(),
    });
    recompute_summary(&mut model);
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::DanglingReference {
            target: "variable",
            id: 404,
            ..
        }
    )));
}

#[test]
fn rejects_trace_point_naming_a_missing_variable() {
    let mut model = decay_model();
    model.trace_points.push(RbcTracePoint {
        id: TracePointId(0),
        variable: VariableId(77),
        label: "ghost".into(),
        connection: None,
        quantity: None,
        unit: None,
        added_by: Some("test".into()),
    });
    recompute_summary(&mut model);
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::DanglingReference {
            target: "variable",
            id: 77,
            ..
        }
    )));
}

#[test]
fn rejects_a_summary_that_disagrees_with_the_contents() {
    // Catches a truncated or hand-edited artifact whose counts no longer match.
    let mut model = decay_model();
    model.summary.variables = 99;
    assert!(errors(&model).iter().any(|error| matches!(
        error,
        ValidationError::SummaryMismatch {
            field: "variables",
            declared: 99,
            ..
        }
    )));
}

#[test]
fn import_rejects_an_unsupported_node() {
    // Export may record an expression form the schema cannot carry. Import must
    // refuse it: a model it cannot faithfully rebuild is not a model.
    let mut model = decay_model();
    model.expressions[4].node = RbcExprNode::Unsupported {
        detail: "array comprehension".into(),
    };
    let strict = ValidateOptions {
        reject_unsupported: true,
    };
    let found = validate(&model, &strict).unwrap_err();
    assert!(found.iter().any(|error| matches!(
        error,
        ValidationError::UnsupportedNode { expression: 4, .. }
    )));
    // The same artifact passes the permissive gate an analysis pass would use.
    assert!(validate(&model, &ValidateOptions::default()).is_ok());
}

#[test]
fn validation_reports_every_problem_not_only_the_first() {
    // A pass author should fix one round of errors, not play whack-a-mole.
    let mut model = decay_model();
    model.equations[0].residual = ExprId(900);
    model.variables[1].value_type = TypeId(900);
    let found = errors(&model);
    assert!(found.len() >= 2, "expected several errors, got {found:?}");
}

// ── Import ───────────────────────────────────────────────────────────────────

#[test]
fn import_rebuilds_a_checked_dae() {
    let file = file(decay_model());
    let dae = crate::import(&file).expect("import a well-formed artifact");
    let (variables, equations) =
        dae.inspect(|view| (view.variable_count(), view.continuous_equation_count()));
    assert_eq!(variables, 2);
    assert_eq!(equations, 1);
}

#[test]
fn import_refuses_a_dangling_reference() {
    let mut model = decay_model();
    model.equations[0].residual = ExprId(999);
    let error = crate::import(&file(model)).expect_err("must refuse");
    assert!(
        matches!(error, crate::ImportError::Invalid(_)),
        "expected a validation failure, got {error}"
    );
}

#[test]
fn export_import_export_is_stable() {
    // The Milestone 3 obligation, stated as a property: reconstructing a DAE
    // and re-exporting it reproduces the artifact it came from.
    let original = file(decay_model());
    let dae = crate::import(&original).expect("import");
    let again =
        crate::export(&dae, None, &original.model.name, &Default::default()).expect("re-export");
    assert_eq!(original.model.variables.len(), again.model.variables.len());
    assert_eq!(
        original.model.expressions.len(),
        again.model.expressions.len()
    );
    for (before, after) in original.model.variables.iter().zip(&again.model.variables) {
        assert_eq!(before.name, after.name);
        assert_eq!(before.role, after.role);
    }
    for (before, after) in original
        .model
        .expressions
        .iter()
        .zip(&again.model.expressions)
    {
        assert_eq!(format!("{:?}", before.node), format!("{:?}", after.node));
    }
}
