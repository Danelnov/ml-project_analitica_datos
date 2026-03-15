# House Price Dataset

- [House Price Dataset](#house-price-dataset)
  - [Fuente (URL)](#fuente-url)
  - [Descripción General del Problema](#descripción-general-del-problema)
  - [Objetivo del Análisis](#objetivo-del-análisis)
  - [Variable Objetivo (Variable Respuesta)](#variable-objetivo-variable-respuesta)
  - [Diccionario de variables](#diccionario-de-variables)
  - [Número de Observaciones](#número-de-observaciones)
  - [Número de Variables](#número-de-variables)
  - [Posibles Hipótesis de Estudio](#posibles-hipótesis-de-estudio)

## Fuente (URL)

[https://www.kaggle.com/datasets/hosammhmdali/house-price-dataset](https://www.kaggle.com/datasets/hosammhmdali/house-price-dataset)

## Descripción General del Problema

Este conjunto de datos recopila información socioeconómica y características físicas de las viviendas correspondientes a distintos grupos de bloques (distritos) en California. El problema central consiste en entender la dinámica del mercado inmobiliario y cómo diversas variables (geográficas, estructurales y demográficas) influyen en el valor de las propiedades en una zona determinada.

## Objetivo del Análisis

El objetivo principal es construir y entrenar un **modelo de regresión** capaz de predecir el valor mediano de una vivienda en un distrito dado, basándose en las características aportadas (como ingresos de la zona, antigüedad de las casas, proximidad al océano, etc.).

## Variable Objetivo (Variable Respuesta)

**`median_house_value`**: Representa el valor mediano de las viviendas (medido en dólares estadounidenses) para los hogares dentro de un bloque determinado. Al ser un valor numérico continuo, confirma que se trata de un problema de regresión.

## Diccionario de variables

| Nombre de la variable    | Descripción                                                                                              | Tipo de variable   |
| :----------------------- | :------------------------------------------------------------------------------------------------------- | :----------------- |
| **`longitude`**          | Coordenada de longitud. Indica qué tan al oeste se encuentra el distrito.                                | Numérica continua  |
| **`latitude`**           | Coordenada de latitud. Indica qué tan al norte se encuentra el distrito.                                 | Numérica continua  |
| **`housing_median_age`** | Edad mediana de las viviendas dentro del bloque.                                                         | Numérica continua  |
| **`total_rooms`**        | Número total de habitaciones presentes en el distrito o bloque.                                          | Numérica discreta  |
| **`total_bedrooms`**     | Número total de dormitorios en el distrito o bloque. *(Contiene valores nulos)*.                         | Numérica discreta  |
| **`population`**         | Número total de personas (población) que residen en ese bloque.                                          | Numérica discreta  |
| **`households`**         | Número total de hogares (personas que conviven en una misma unidad) en el bloque.                        | Numérica discreta  |
| **`median_income`**      | Ingreso mediano de los hogares en el bloque (escalado en decenas de miles de dólares).                   | Numérica continua  |
| **`median_house_value`** | Valor mediano de las viviendas en el bloque (en dólares). **[Variable Objetivo]**                        | Numérica continua  |
| **`ocean_proximity`**    | Ubicación de la vivienda respecto al océano (`<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY`, `ISLAND`). | Categórica nominal |

## Número de Observaciones

El conjunto de datos contiene **20,640** observaciones (filas), cada una representando un grupo de bloques (distrito) de California.

> ***Nota:*** California esta compuesta de 23,212 grupos de bloques.

## Número de Variables

El conjunto de datos está compuesto por **10** variables en total (9 variables predictoras/independientes y 1 variable objetivo/dependiente).

## Posibles Hipótesis de Estudio

1. **Hipótesis sobre el poder adquisitivo:** Existe una correlación  directa entre el ingreso mediano de los hogares (`median_income`) y el valor mediano de la vivienda (`median_house_value`). A mayores ingresos en el distrito, mayor es el precio de las propiedades.
2. **Hipótesis sobre la ubicación geográfica:** Las viviendas que tienen una mayor proximidad al océano (categorías `NEAR OCEAN` o `ISLAND` en `ocean_proximity`) presentan valores de mercado significativamente superiores en comparación con aquellas ubicadas en el interior del estado (`INLAND`).
3. **Hipótesis sobre la densidad poblacional:** Los distritos que presentan un alto índice de densidad (lo cual se puede calcular dividiendo `population` entre `households` o analizando `total_rooms` vs `population`) tienden a estar asociados con valores de vivienda más bajos.
