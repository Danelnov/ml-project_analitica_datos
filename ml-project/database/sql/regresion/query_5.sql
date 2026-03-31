-- Consulta para obtener el promedio de personas por cada categoria de proximidad al océano
-- Se calcula el promedio de cada vivienda

SELECT
    ocean_proximity,
    ROUND(AVG(population / households), 2) AS promedio_personas_por_hogar,
    ROUND(AVG(median_house_value), 2) AS valor_medio_vivienda
FROM regresion
GROUP BY ocean_proximity
ORDER BY promedio_personas_por_hogar DESC;