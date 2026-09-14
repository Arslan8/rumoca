model Orifice "Flow through an orifice follows a square-root law."
  parameter Real k = 1.0 "discharge coefficient";
  parameter Real bias = 0.5 "static pressure offset";
  parameter Real drain = 0.5 "constant draw-down rate";
  Real head(start = 1.0) "pressure head";
  Real q "volumetric flow";
equation
  // Real-valued only while head + bias stays non-negative. The head falls at a
  // fixed rate, so a small enough bias takes the radicand under zero mid-run.
  q = k * sqrt(head + bias);
  der(head) = -drain;
end Orifice;
