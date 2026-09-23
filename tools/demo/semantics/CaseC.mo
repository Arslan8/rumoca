model CaseC "nothing in the model says which rad/s is the wheel"
  parameter Modelica.Units.SI.AngularVelocity w_fan = 300 "fan";
  parameter Modelica.Units.SI.AngularVelocity w_fl = 42 "front left wheel";
  parameter Modelica.Units.SI.Length r_fl = -0.31 "front left wheel radius";
  parameter Modelica.Units.SI.Velocity v_veh = 13.2 "chassis";
  parameter Modelica.Units.SI.Velocity vehicle_speed = 13.2 "an estimator's copy";
  Real x;
equation
  der(x) = v_veh - r_fl * w_fl + 0 * w_fan + 0 * vehicle_speed;
end CaseC;
