--
SELECT 
    Diagnosis,
    BMI,
    "Insulin Resistance",
    COUNT(*) as cantidad
FROM clasification
GROUP BY Diagnosis, BMI, "Insulin Resistance";