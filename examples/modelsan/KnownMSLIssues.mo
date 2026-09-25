within;
package KnownMSLIssues
  // Actual MSL APIs; expected properties live outside the model in the campaign.
  function gasRoundTrip
    input Real p;
    input Real T;
    output Real recovered;
  protected
    Modelica.Media.Air.SimpleAir.ThermodynamicState state;
    Real s;
  algorithm
    state := Modelica.Media.Air.SimpleAir.setState_pTX(p,T);
    s := Modelica.Media.Air.SimpleAir.specificEntropy(state);
    state := Modelica.Media.Air.SimpleAir.setState_psX(p,s);
    recovered := state.T;
    annotation(Inline=false);
  end gasRoundTrip;

  function waterRoundTrip
    input Real T;
    output Real recovered;
  protected
    Modelica.Media.Water.ConstantPropertyLiquidWater.ThermodynamicState state;
    Real s;
  algorithm
    state := Modelica.Media.Water.ConstantPropertyLiquidWater.setState_pTX(100000,T);
    s := Modelica.Media.Water.ConstantPropertyLiquidWater.specificEntropy(state);
    state := Modelica.Media.Water.ConstantPropertyLiquidWater.setState_psX(100000,s);
    recovered := state.T;
    annotation(Inline=false);
  end waterRoundTrip;

  model GasControl
    parameter Real p=101325;
    Real original=300+time;
    Real actual=gasRoundTrip(p,original);
  end GasControl;

  model GasRoundTrip
    extends GasControl(p=102338.25);
  end GasRoundTrip;

  model WaterRoundTrip
    Real original=300+time;
    Real actual=waterRoundTrip(original);
  end WaterRoundTrip;

  model PulseControl
    Modelica.Blocks.Sources.BooleanPulse dut(period=1,startTime=-0.25,width=50);
    Boolean actual=dut.y;
  end PulseControl;

  model PulsePast
    Modelica.Blocks.Sources.BooleanPulse dut(period=1,startTime=-1.25,width=50);
    Boolean actual=dut.y;
  end PulsePast;

  model Delay
    Modelica.Blocks.Discrete.UnitDelay dut(samplePeriod=0.05,y_start=0);
    Real u=sin(2*Modelica.Constants.pi*time);
    Real actual=dut.y;
  equation
    dut.u=u;
  end Delay;

  model DelayControl
    Real u=sin(2*Modelica.Constants.pi*time);
    discrete Real sampled(start=0,fixed=true);
    discrete Real actual(start=0,fixed=true);
  equation
    when sample(0,0.05) then
      sampled=u;
      actual=pre(sampled);
    end when;
  end DelayControl;

  model Quantization
    parameter Real amplitude=1;
    Modelica.Clocked.RealSignals.Sampler.SampleWithADeffects dut(
      limited=true,quantized=true,bits=2);
    Modelica.Blocks.Sources.Sine sine(f=1,amplitude=amplitude);
    Modelica.Clocked.ClockSignals.Clocks.PeriodicRealClock clock(period=0.01);
    Modelica.Clocked.RealSignals.Sampler.AssignClock assignClock;
  equation
    connect(sine.y,dut.u);
    connect(clock.y,assignClock.clock);
    connect(dut.y,assignClock.u);
  end Quantization;

  model QuantizationControl
    extends Quantization(amplitude=0.5);
  end QuantizationControl;

  model MoistAirFull
    parameter Real s=Modelica.Media.Air.MoistAir.s_pTX(100000,300,{0,1});
    Real actual=Modelica.Media.Air.MoistAir.temperature_psX(100000,s,{0,1});
  end MoistAirFull;

  model MoistAirReduced
    parameter Real s=Modelica.Media.Air.MoistAir.s_pTX(100000,300,{0,1});
    Real actual=Modelica.Media.Air.MoistAir.temperature_psX(100000,s,{0});
  end MoistAirReduced;
end KnownMSLIssues;
