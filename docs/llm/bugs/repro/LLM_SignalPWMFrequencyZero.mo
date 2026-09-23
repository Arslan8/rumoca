within;
model LLM_SignalPWMFrequencyZero
  Modelica.Electrical.PowerConverters.DCDC.Control.SignalPWM dut(
    f=0,
    useConstantDutyCycle=true,
    constantDutyCycle=0.5);
  annotation(experiment(StopTime=0.01, Interval=0.001));
end LLM_SignalPWMFrequencyZero;

model LLM_SignalPWMFrequencyNominal
  Modelica.Electrical.PowerConverters.DCDC.Control.SignalPWM dut(
    f=1000,
    useConstantDutyCycle=true,
    constantDutyCycle=0.5);
  annotation(experiment(StopTime=0.01, Interval=0.001));
end LLM_SignalPWMFrequencyNominal;
