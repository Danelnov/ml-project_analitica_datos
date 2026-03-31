--Porcentajes de BMI según el diagnostico
SELECT 
    Diagnosis,
    BMI,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Diagnosis) as porcentaje
FROM clasification
GROUP BY Diagnosis, BMI;