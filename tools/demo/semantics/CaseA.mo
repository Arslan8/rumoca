model CaseA "a resistance-valued parameter whose declaring class nothing knows"
  parameter Modelica.Units.SI.Resistance Rload = -47 "not a catalogued class";
  Real v, i;
equation
  v = Rload * i;
  i = 1 - v;
end CaseA;
