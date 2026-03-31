-- Consulta para obtener el valor medio de las viviendas por cada categoría de proximidad al océano, ordenado de mayor a menor valor

SELECT ocean_proximity, ROUND(AVG(median_house_value), 2) AS valor_medio
FROM regresion 
GROUP BY ocean_proximity 
ORDER BY valor_medio DESC;