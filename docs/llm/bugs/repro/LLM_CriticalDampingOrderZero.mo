within;
model LLM_CriticalDampingOrderZero
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.CriticalDamping dut(n=0, f=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_CriticalDampingOrderZero;

model LLM_CriticalDampingOrderTwo
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.CriticalDamping dut(n=2, f=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_CriticalDampingOrderTwo;
