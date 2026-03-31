--

SELECT Diagnosis, COUNT(*) as total, 
       (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clasification)) as porcentaje
FROM clasification
GROUP BY Diagnosis;