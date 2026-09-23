within;
model LLM_FirstOrderZero
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Blocks.Continuous.FirstOrder dut(T=0, k=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_FirstOrderZero;

model LLM_FirstOrderNominal
  Modelica.Blocks.Sources.Constant source(k=1);
  Modelica.Blocks.Continuous.FirstOrder dut(T=1, k=1);
equation
  connect(source.y, dut.u);
  annotation(experiment(StopTime=0.1, Interval=0.01));
end LLM_FirstOrderNominal;
