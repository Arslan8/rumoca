model CaseB "a rigid rotating body given zero moment of inertia"
  // Rotational.Components.Inertia declares `J(min=0)`, which permits exactly
  // the value that degenerates `J*a = tau`. Unlike the electrical Basic
  // elements, MSL grants no documented latitude here, so the physical claim
  // `J > 0` is the component's to keep. Execution-confirmed as BUG-018.
  Modelica.Mechanics.Rotational.Components.Inertia load(J = 0);
  Modelica.Mechanics.Rotational.Sources.ConstantTorque src(tau_constant = 1);
equation
  connect(src.flange, load.flange_a);
end CaseB;
