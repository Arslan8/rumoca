within;
model LLM_CompareTransformersRatioZero
  extends Modelica.Electrical.Analog.Examples.CompareTransformers(n=0);
end LLM_CompareTransformersRatioZero;

model LLM_CompareTransformersRatioNominal
  extends Modelica.Electrical.Analog.Examples.CompareTransformers(n=2);
end LLM_CompareTransformersRatioNominal;
