-- Consulta para contar la cantidad de registros por cada categoría de proximidad al océano

SELECT ocean_proximity, count(*) AS cantidad 
FROM regresion 
GROUP BY ocean_proximity 
ORDER BY cantidad DESC;