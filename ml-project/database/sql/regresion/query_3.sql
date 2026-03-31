-- Consulta para contar la cantidad de registros con valores nulos en la columna total_bedrooms

SELECT COUNT(*) AS total_nulos_dormitorios
FROM regresion
WHERE total_bedrooms IS NULL;