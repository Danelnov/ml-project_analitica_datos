--Edad promedio por BMI
SELECT 
    BMI,
    AVG(Age) as edad_promedio
FROM clasification
GROUP BY BMI;