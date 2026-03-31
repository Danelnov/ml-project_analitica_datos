-- Consulta para obtener el valor medio del inmueble por el valor medio de ingresos calculado en miles de dolares.

SELECT 
    ROUND(median_income) AS nivel_ingreso_aproximado,
    COUNT(*) AS cantidad_bloques,
    ROUND(AVG(median_house_value), 2) AS valor_medio_vivienda
FROM regresion
GROUP BY ROUND(median_income)
ORDER BY nivel_ingreso_aproximado ASC;