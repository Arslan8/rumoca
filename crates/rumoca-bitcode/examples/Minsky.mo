model Minsky "A two-counter (Minsky) machine, which is Turing complete"
  // Counters and the program counter are discrete state carried across events
  // by pre(); the `when` clause is the step relation. The step is driven by a
  // state event on a continuous clock rather than by sample(), so the whole
  // thing is an ordinary hybrid DAE.
  parameter Integer seed = 7 "Input to the machine";
  discrete Integer a(start = seed, fixed = true);
  discrete Integer b(start = 0, fixed = true);
  discrete Integer pc(start = 1, fixed = true);
  discrete Integer steps(start = 0, fixed = true);
  discrete Real next(start = 0.01, fixed = true);
  Real clock(start = 0, fixed = true);
equation
  der(clock) = 1;
  when clock > next then
    // 1: if a == 0 goto 4 (halt) else a--, goto 2
    // 2: b++, goto 3
    // 3: goto 1
    // 4: halt
    next = pre(next) + 0.01;
    pc = if pre(pc) == 1 then (if pre(a) == 0 then 4 else 2)
         elseif pre(pc) == 2 then 3
         elseif pre(pc) == 3 then 1
         else 4;
    a = if pre(pc) == 1 and pre(a) <> 0 then pre(a) - 1 else pre(a);
    b = if pre(pc) == 2 then pre(b) + 1 else pre(b);
    steps = if pre(pc) == 4 then pre(steps) else pre(steps) + 1;
  end when;
end Minsky;
