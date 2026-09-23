within;
model LLM_BlocksCriticalDampingOrderZero
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Blocks.Continuous.CriticalDamping dut(n=0, f=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_BlocksCriticalDampingOrderZero;

model LLM_BlocksCriticalDampingOrderTwo
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Blocks.Continuous.CriticalDamping dut(n=2, f=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_BlocksCriticalDampingOrderTwo;
