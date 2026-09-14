package Drive
  connector Flange
    Real phi(unit = "rad") "angle";
    flow Real tau(unit = "N.m") "torque";
  end Flange;

  model Inertia
    parameter Real J(unit = "kg.m2") = 0.5 "moment of inertia";
    Flange a;
    Flange b;
    Real w(unit = "rad/s", start = 2) "angular velocity";
  equation
    a.phi = b.phi;
    der(a.phi) = w;
    J * der(w) = a.tau + b.tau;
  end Inertia;

  model Spring
    parameter Real c(unit = "N.m/rad") = 20 "stiffness";
    Flange a;
    Flange b;
  equation
    b.tau = c * (a.phi - b.phi);
    a.tau + b.tau = 0;
  end Spring;

  model Fixed
    Flange b;
  equation
    b.phi = 0;
  end Fixed;

  model System
    Inertia inertia(J = 0.5);
    Spring spring(c = 20);
    Fixed ground;
  equation
    connect(inertia.b, spring.a);
    connect(spring.b, ground.b);
  end System;
end Drive;
