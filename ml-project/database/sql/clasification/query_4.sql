--- Convierte BMI en numérico y encuentra el promedio
SELECT 
    Diagnosis,
    AVG(
        CASE 
            WHEN BMI = 'Underweight' THEN 1
            WHEN BMI = 'Normal' THEN 2
            WHEN BMI = 'Overweight' THEN 3
            WHEN BMI = 'Obese' THEN 4
        END
    ) as bmi_numerico_promedio
FROM clasification
GROUP BY Diagnosis;