model Tank "Drains through a flow restriction."
  parameter Real area(min = 0.0) = 1.0 "tank cross-section";
  parameter Real resistance = 2.0 "flow restriction";
  Real level(start = 1.0, min = 0.0, max = 2.0) "liquid level";
  Real flow_out "outflow rate";
equation
  flow_out = level / resistance;
  der(level) = -flow_out / area;
end Tank;
