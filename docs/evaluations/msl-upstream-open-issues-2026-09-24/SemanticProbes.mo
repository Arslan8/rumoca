within;
package SemanticProbes
  model GasRoundTrip
    package Medium = Modelica.Media.Air.SimpleAir;
    parameter Real p=1.01*Medium.reference_p;
    parameter Real targetT=300;
    Real s;
    Real recoveredT;
    Medium.ThermodynamicState originalState;
    Medium.ThermodynamicState recoveredState;
  equation
    originalState = Medium.setState_pTX(p,targetT);
    s = Medium.specificEntropy(originalState);
    recoveredState = Medium.setState_psX(p,s);
    recoveredT = recoveredState.T;
  end GasRoundTrip;

  model GasControl
    extends GasRoundTrip(p=Medium.reference_p);
  end GasControl;

  model WaterRoundTrip
    package Medium = Modelica.Media.Water.ConstantPropertyLiquidWater;
    Real s;
    Real recoveredT;
    Medium.ThermodynamicState originalState;
    Medium.ThermodynamicState recoveredState;
  equation
    originalState = Medium.setState_pTX(100000,300);
    s = Medium.specificEntropy(originalState);
    recoveredState = Medium.setState_psX(100000,s);
    recoveredT = recoveredState.T;
  end WaterRoundTrip;

  model PulsePast
    Modelica.Blocks.Sources.BooleanPulse dut(period=1,startTime=-1.25,width=50);
    Boolean actual=dut.y;
  end PulsePast;

  model PulseControl
    Modelica.Blocks.Sources.BooleanPulse dut(period=1,startTime=-0.25,width=50);
    Boolean actual=dut.y;
  end PulseControl;

  model Delay
    Modelica.Blocks.Discrete.UnitDelay dut(samplePeriod=0.05,y_start=0);
    Real actual=dut.y;
  equation
    dut.u=sin(2*Modelica.Constants.pi*time);
  end Delay;

  model Quantization
    Modelica.Clocked.RealSignals.Sampler.SampleWithADeffects dut(
      limited=true,quantized=true,bits=2);
    Modelica.Blocks.Sources.Sine sine(f=1);
    Modelica.Clocked.ClockSignals.Clocks.PeriodicRealClock clock(period=0.01);
    Modelica.Clocked.RealSignals.Sampler.AssignClock assignClock;
  equation
    connect(sine.y,dut.u);
    connect(clock.y,assignClock.clock);
    connect(dut.y,assignClock.u);
  end Quantization;
end SemanticProbes;
