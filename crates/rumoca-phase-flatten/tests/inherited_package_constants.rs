//! MLS §5.3 / §7.2: one inherited declaration, distinct package bindings.

use rumoca_eval_flat::constant::{EvalContext, EvalLimits, Value, eval_function};
use rumoca_ir_ast as ast;

const SOURCE: &str = r#"
package Packages
  package Base
    constant Real cp = 2;
    constant Real twice = 2*cp;
    function f
      input Real x;
      output Real y;
    algorithm
      y := twice*x;
    end f;
  end Base;
  package Three
    extends Base(cp=3);
  end Three;
  package Seven
    extends Base(cp=7);
  end Seven;
  model Both
    package Local = Three;
    Real a=Local.f(time);
    Real b=Seven.f(time);
    Real c=Base.f(time);
  end Both;
end Packages;
"#;

fn flatten(source: &str) -> (rumoca_ir_flat::Model, rumoca_core::SourceMap) {
    let filename = "<inherited_package_constants>";
    let parsed = rumoca_phase_parse::parse_to_ast(source, filename).expect("parse");
    let mut tree = ast::ClassTree::from_parsed(parsed);
    tree.source_map.add(filename, source);
    let resolved = rumoca_phase_resolve::resolve(ast::ParsedTree::new(tree)).expect("resolve");
    let instanced =
        rumoca_phase_instantiate::instantiate(resolved, "Packages.Both").expect("instantiate");
    let ast::InstancedTree { tree, mut overlay } = instanced;
    rumoca_phase_typecheck::typecheck_instanced(&tree, &mut overlay, "Packages.Both")
        .expect("typecheck");
    let flat =
        rumoca_phase_flatten::flatten_ref(&tree, &overlay, "Packages.Both").expect("flatten");
    (flat, tree.source_map)
}

fn values(flat: &rumoca_ir_flat::Model) -> Vec<f64> {
    let context = EvalContext::new();
    let mut values = flat
        .functions
        .values()
        .map(|function| {
            eval_function(
                function,
                vec![Value::Real(1.0)],
                &context,
                &EvalLimits::default(),
                0,
                function.span,
            )
            .expect("each function's package constants are bound")
            .to_real()
            .expect("real result")
        })
        .collect::<Vec<_>>();
    values.sort_by(f64::total_cmp);
    values
}

#[test]
fn package_aliases_keep_distinct_modified_and_default_bindings() {
    let (flat, sources) = flatten(SOURCE);
    assert_eq!(values(&flat), vec![4.0, 6.0, 14.0]);
    rumoca_phase_dae::to_dae(&flat, sources).expect("all package constants resolve at DAE");
}

#[test]
fn an_unbound_base_constant_is_bound_in_each_concrete_exposure() {
    let source = SOURCE
        .replace("constant Real cp = 2;", "constant Real cp;")
        .replace("Real c=Base.f(time);", "");
    let (flat, sources) = flatten(&source);
    assert_eq!(values(&flat), vec![6.0, 14.0]);
    rumoca_phase_dae::to_dae(&flat, sources)
        .expect("concrete modifications bind abstract constants");
}

#[test]
fn function_local_shadows_package_constant_by_declaration_identity() {
    let source = SOURCE
        .replace("input Real x;", "input Real cp;")
        .replace("twice*x", "cp");
    let (flat, sources) = flatten(&source);
    assert_eq!(values(&flat), vec![1.0, 1.0, 1.0]);
    rumoca_phase_dae::to_dae(&flat, sources).expect("function inputs remain function locals");
}

#[test]
fn explicitly_qualified_base_constant_keeps_the_base_binding() {
    let source = SOURCE.replace("twice*x", "Base.cp*x");
    let (flat, sources) = flatten(&source);
    assert_eq!(values(&flat), vec![2.0, 2.0, 2.0]);
    rumoca_phase_dae::to_dae(&flat, sources).expect("explicit package qualification is preserved");
}

#[test]
fn inherited_array_dimensions_are_materialized_per_package() {
    let source = SOURCE
        .replace("constant Real cp = 2;", "constant Integer cp = 2;")
        .replace("output Real y;", "output Real y[cp];")
        .replace("Real a=", "Real a[3]=")
        .replace("Real b=", "Real b[7]=")
        .replace("Real c=", "Real c[2]=")
        .replace("y := twice*x;", "y := fill(x, cp);");
    let (flat, sources) = flatten(&source);
    let mut dimensions = flat
        .functions
        .values()
        .map(|function| function.outputs[0].dimensions().to_vec())
        .collect::<Vec<_>>();
    dimensions.sort();
    assert_eq!(dimensions, vec![vec![2], vec![3], vec![7]]);
    rumoca_phase_dae::to_dae(&flat, sources).expect("concrete function shapes reach DAE");
}

#[test]
fn inherited_default_arguments_keep_their_concrete_package_binding() {
    let source = SOURCE
        .replace("input Real x;", "input Real x=cp;")
        .replace("f(time)", "f()");
    let (flat, sources) = flatten(&source);
    let mut results = flat
        .functions
        .values()
        .map(|function| {
            eval_function(
                function,
                Vec::new(),
                &EvalContext::new(),
                &EvalLimits::default(),
                0,
                function.span,
            )
            .expect("modified defaults remain evaluable")
            .to_real()
            .expect("real result")
        })
        .collect::<Vec<_>>();
    results.sort_by(f64::total_cmp);
    assert_eq!(results, vec![8.0, 18.0, 98.0]);
    rumoca_phase_dae::to_dae(&flat, sources)
        .expect("materialized default call arguments reach DAE");
}

#[test]
fn inherited_record_constructor_keeps_materialized_field_shape() {
    let source = r#"package Packages
  package Base
    constant Integer n=1;
    replaceable record State
      Real x[n];
    end State;
  end Base;
  package Medium
    extends Base(n=2);
    redeclare record extends State end State;
    function read
      input State state;
      output Real y;
    algorithm
      y := state.x[1];
    end read;
    function make
      input Real x[n];
      output State state;
    algorithm
      state := State(x);
    end make;
  end Medium;
  model Both
    Real y=Medium.read(Medium.make({time,time}));
  end Both;
end Packages;
"#;
    let (flat, sources) = flatten(source);
    let record = flat
        .record_types
        .values()
        .find(|record| record.name.ends_with("State"))
        .expect("retained record layout");
    assert_eq!(record.fields.len(), 1);
    assert_eq!(record.fields[0].name, "x");
    assert_eq!(record.fields[0].dims, vec![2]);
    rumoca_phase_dae::to_dae(&flat, sources)
        .expect("record layout is consistent with its materialized constructor");
}
