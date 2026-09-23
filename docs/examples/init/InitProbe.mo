model InitProbe "exercises every initialization construct at once"
  parameter Real p = 10                      "parameter value";
  parameter Real pDerived = p * 2            "derived parameter";
  Real xFixed(start = 5, fixed = true)       "fixed start";
  Real xGuess(start = 7, fixed = false)      "guess only";
  Real xBounded(min = 0, max = 10, start = 3, fixed = true) "bounded + fixed";
  Real xFromInitEq                           "set by an initial equation";
  Real yAlg                                  "algebraic";
  discrete Real d(start = 2, fixed = true)   "discrete state";
  Boolean b(start = true, fixed = true)      "discrete boolean";
  Real usesInitial                           "reads initial()";
initial equation
  xFromInitEq = -1;
  yAlg = xFromInitEq + p;
equation
  der(xFixed) = -xFixed;
  der(xGuess) = -xGuess;
  der(xBounded) = 0;
  der(xFromInitEq) = 0;
  yAlg = xFromInitEq + p;
  when time > 1 then
    d = pre(d) + 1;
    b = not pre(b);
  end when;
  usesInitial = if initial() then 1.0 else 0.0;
end InitProbe;
