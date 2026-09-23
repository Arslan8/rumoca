model LinkDecay
  parameter Real k = 1;
  Real x(start = 2, fixed = true);
equation
  der(x) = -k*x;
end LinkDecay;
