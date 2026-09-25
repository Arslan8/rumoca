//! MLS §12.4.2.1: static function arguments become exact executable callables.
//! Captures remain call-time values, and independent closure occurrences do not alias.

use rumoca_core::{ClassType, Expression, FunctionInstanceId, VarName};
use rumoca_eval_flat::constant::{EvalContext, Value, eval_expr};
use rumoca_ir_ast as ast;

const LIBRARY: &str = r#"
package Closures
  partial function Unary
    input Real x;
    output Real y;
  end Unary;
  function twice
    extends Unary;
  algorithm
    y := 2*x;
  end twice;
  function triple
    extends Unary;
  algorithm
    y := 3*x;
  end triple;
  function scaled
    extends Unary;
    input Real p;
  algorithm
    y := p*x;
  end scaled;
  function weighted
    extends Unary;
    input Real p[:];
  algorithm
    y := sum(p)*x;
  end weighted;
  function sized
    extends Unary;
    input Integer n;
    input Real data[n];
  algorithm
    y := sum(data)*x;
  end sized;
  function apply
    input Unary f;
    input Real x;
    output Real y;
  algorithm
    y := f(x);
  end apply;
  function forward
    input Unary g;
    input Real x;
    output Real y;
  algorithm
    y := apply(g,x);
  end forward;
  function namedApply
    input Unary f;
    input Real x;
    output Real y;
  algorithm
    y := f(x=x);
  end namedApply;
  function applyWithLocal
    input Unary f;
    input Real x;
    output Real y;
  protected
    Real p;
  algorithm
    p := 5;
    y := f(x)+p;
  end applyWithLocal;
  function applyTwo
    input Unary f;
    input Unary g;
    input Real x;
    output Real y;
  algorithm
    y := f(x)+g(x);
  end applyTwo;
"#;

fn flatten(body: &str) -> (rumoca_ir_flat::Model, rumoca_core::SourceMap) {
    let source = format!("{LIBRARY}\n model Subject\n{body}\n end Subject;\nend Closures;\n");
    let filename = "<functional_input_specialization>";
    let parsed = rumoca_phase_parse::parse_to_ast(&source, filename).expect("parse source");
    let mut tree = ast::ClassTree::from_parsed(parsed);
    tree.source_map.add(filename, &source);
    let resolved = rumoca_phase_resolve::resolve(ast::ParsedTree::new(tree)).expect("resolve");
    let instanced = rumoca_phase_instantiate::instantiate(resolved, "Closures.Subject")
        .expect("instantiate source");
    let ast::InstancedTree { tree, mut overlay } = instanced;
    rumoca_phase_typecheck::typecheck_instanced(&tree, &mut overlay, "Closures.Subject")
        .expect("typecheck source");
    let flat = rumoca_phase_flatten::flatten_ref(&tree, &overlay, "Closures.Subject")
        .expect("specialize function inputs during Flatten");
    for function in flat.functions.values() {
        assert!(
            function
                .inputs
                .iter()
                .all(|input| input.type_class != Some(ClassType::Function)),
            "reachable function {} retains a functional input",
            function.name
        );
    }
    (flat, tree.source_map)
}

fn binding<'a>(flat: &'a rumoca_ir_flat::Model, name: &str) -> &'a Expression {
    flat.variables[&VarName::new(name)]
        .binding
        .as_ref()
        .expect("binding")
}

fn evaluate(flat: &rumoca_ir_flat::Model, name: &str, time: f64) -> f64 {
    let mut context = EvalContext::new();
    context.add_parameter("time", Value::Real(time));
    for function in flat.functions.values() {
        context
            .functions
            .insert(function.name.to_string(), function.clone());
    }
    eval_expr(binding(flat, name), &context)
        .expect("specialized Flat call is executable")
        .to_real()
        .expect("real result")
}

fn call_instance(flat: &rumoca_ir_flat::Model, variable: &str) -> FunctionInstanceId {
    let Expression::FunctionCall { name, .. } = binding(flat, variable) else {
        panic!("expected specialized call")
    };
    name.resolved_function()
        .expect("exact callable identity")
        .instance_id
}

#[test]
fn empty_partial_application_is_a_function_value_not_a_zero_argument_call() {
    let (flat, sources) = flatten("Real y=apply(function twice(),time);");
    assert_eq!(evaluate(&flat, "y", 3.0), 6.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("first-order calls reach DAE");
}

#[test]
fn capture_values_are_runtime_arguments_of_one_specialization() {
    let (flat, sources) = flatten(
        "Real a=apply(function scaled(p=2),time);\nReal b=apply(function scaled(p=3),time);",
    );
    assert_eq!(evaluate(&flat, "a", 3.0), 6.0);
    assert_eq!(evaluate(&flat, "b", 3.0), 9.0);
    assert_eq!(call_instance(&flat, "a"), call_instance(&flat, "b"));
    rumoca_phase_dae::to_dae(&flat, sources).expect("capture values need no separate callable");
}

#[test]
fn same_named_callback_formals_keep_their_exact_callable_instances() {
    let (flat, sources) =
        flatten("Real a=apply(function twice(),time);\nReal b=apply(function triple(),time);");
    assert_eq!(evaluate(&flat, "a", 3.0), 6.0);
    assert_eq!(evaluate(&flat, "b", 3.0), 9.0);
    assert_ne!(call_instance(&flat, "a"), call_instance(&flat, "b"));
    rumoca_phase_dae::to_dae(&flat, sources).expect("distinct callback identities reach DAE");
}

#[test]
fn capture_formal_does_not_alias_an_outer_local_with_the_same_name() {
    let (flat, sources) = flatten("Real y=applyWithLocal(function scaled(p=time),3);");
    assert_eq!(evaluate(&flat, "y", 2.0), 11.0);
    assert_eq!(evaluate(&flat, "y", 4.0), 17.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("captured value and outer local are distinct");
}

#[test]
fn two_occurrences_of_one_callback_keep_independent_captures() {
    let (flat, sources) =
        flatten("Real y=applyTwo(function scaled(p=2),function scaled(p=3),time);");
    assert_eq!(evaluate(&flat, "y", 3.0), 15.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("closure occurrences do not alias");
}

#[test]
fn array_captures_keep_runtime_values_and_concrete_call_shapes() {
    let (flat, sources) = flatten(
        "Real a=apply(function weighted(p={time,2*time}),3);\n\
         Real b=apply(function weighted(p={time,2*time,3*time}),3);",
    );
    assert_eq!(evaluate(&flat, "a", 2.0), 18.0);
    assert_eq!(evaluate(&flat, "b", 2.0), 36.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("capture array shapes specialize at DAE");
}

#[test]
fn captured_array_extent_refers_to_the_corresponding_captured_integer() {
    let (flat, sources) = flatten(
        "Real a=apply(function sized(n=2,data={time,2*time}),3);\n\
         Real b=apply(function sized(n=3,data={time,2*time,3*time}),3);",
    );
    assert_eq!(evaluate(&flat, "a", 2.0), 18.0);
    assert_eq!(evaluate(&flat, "b", 2.0), 36.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("capture extent identity remains bound");
}

#[test]
fn closure_can_be_forwarded_through_another_functional_input() {
    let (flat, sources) = flatten("Real y=forward(function scaled(p=2),time);");
    assert_eq!(evaluate(&flat, "y", 3.0), 6.0);
    rumoca_phase_dae::to_dae(&flat, sources).expect("forwarded closure becomes first-order calls");
}

#[test]
fn callback_named_actuals_bind_to_unbound_callback_formals() {
    let (flat, sources) = flatten("Real y=namedApply(function scaled(p=2),time);");
    assert_eq!(evaluate(&flat, "y", 3.0), 6.0);
    rumoca_phase_dae::to_dae(&flat, sources)
        .expect("named callback argument becomes a positional slot");
}
