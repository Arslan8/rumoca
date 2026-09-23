model Decay "the smallest thing with a state, a parameter and a divisor"
  parameter Real k = 2.5;
  parameter Real tau = 1 / k;
  Real x(start = 1, fixed = true);
equation
  der(x) = -x / tau;
end Decay;
