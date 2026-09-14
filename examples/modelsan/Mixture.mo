model Mixture "A mass fraction that must stay inside [0, 1]."
  parameter Real inflow = 0.01 "dilution rate";
  parameter Real reaction = 0.05 "consumption rate";
  Real fraction(start = 0.5, min = 0.0, max = 1.0) "solute mass fraction";
equation
  // Physical only while the rates keep `fraction` inside its declared range.
  der(fraction) = inflow - reaction * fraction;
end Mixture;
