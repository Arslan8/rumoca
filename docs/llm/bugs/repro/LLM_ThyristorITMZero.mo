within;
model LLM_ThyristorITMZero
  Modelica.Electrical.Analog.Semiconductors.Thyristor dut(ITM=0);
  Modelica.Electrical.Analog.Basic.Ground ground;
equation
  connect(dut.Anode, ground.p);
  connect(dut.Cathode, ground.p);
  connect(dut.Gate, ground.p);
  annotation(experiment(StopTime=0.001, Interval=0.0001));
end LLM_ThyristorITMZero;

model LLM_ThyristorITMNominal
  Modelica.Electrical.Analog.Semiconductors.Thyristor dut(ITM=25);
  Modelica.Electrical.Analog.Basic.Ground ground;
equation
  connect(dut.Anode, ground.p);
  connect(dut.Cathode, ground.p);
  connect(dut.Gate, ground.p);
  annotation(experiment(StopTime=0.001, Interval=0.0001));
end LLM_ThyristorITMNominal;

model LLM_ThyristorIHZero
  Modelica.Electrical.Analog.Semiconductors.Thyristor dut(IH=0);
  Modelica.Electrical.Analog.Basic.Ground ground;
equation
  connect(dut.Anode, ground.p);
  connect(dut.Cathode, ground.p);
  connect(dut.Gate, ground.p);
  annotation(experiment(StopTime=0.001, Interval=0.0001));
end LLM_ThyristorIHZero;
