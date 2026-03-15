# PCOS Prediction Dataset (Top 75 Countries)

- [Fuente (URL)](#fuente-url)
- [Descripción General del Problema](#descripción-general-del-problema)
- [Objetivo del Análisis](#objetivo-del-análisis)
- [Variable Objetivo (Variable Respuesta)](#variable-objetivo-variable-respuesta)
- [Diccionario de variables](#diccionario-de-variables)
- [Número de Observaciones](#número-de-observations)
- [Número de Variables](#número-de-variables)
- [Posibles Hipótesis de Estudio](#posibles-hipótesis-de-estudio)

## Fuente (URL)

[https://www.kaggle.com/datasets/ankushpanday1/pcos-prediction-datasettop-75-countries](https://www.kaggle.com/datasets/ankushpanday1/pcos-prediction-datasettop-75-countries)

## Descripción General del Problema

El Síndrome de Ovario Poliquístico (SOP o PCOS) es un trastorno hormonal común entre mujeres en edad reproductiva. Este conjunto de datos abarca registros de salud de mujeres en 75 países diferentes, recopilando métricas físicas, síntomas clínicos y factores de estilo de vida. El desafío consiste en identificar patrones globales que permitan diagnosticar la condición de manera eficiente, considerando la diversidad geográfica y étnica.

## Objetivo del Análisis

El objetivo principal es desarrollar un **modelo de clasificación binaria** que prediga si una paciente tiene PCOS (`Diagnosis`) basándose en un conjunto de indicadores clínicos y demográficos, permitiendo una herramienta de apoyo al diagnóstico temprano y escalable a nivel internacional.

## Variable Objetivo (Variable Respuesta)

La variable objetivo es **`Diagnosis`**, la cual indica si la paciente presenta el síndrome:
- **Yes (1):** Positivo para PCOS.
- **No (0):** Negativo para PCOS.

## Diccionario de variables

| Variable | Descripción | Tipo de Dato |
| :--- | :--- | :--- |
| **`Country`** | País de residencia de la paciente (75 países incluidos). | Categórica nominal |
| **`Age`** | Edad de la paciente. | Numérica discreta|
| **`BMI`** | Índice de Masa Corporal categorizado. | Categórica ordinal |
| **`Menstrual Regularity`** | Indica si el ciclo es regular o irregular. | Categórica nominal (binaria) |
| **`Hirsutism`** | Presencia de vello corporal excesivo. | Categórica nominal (binaria) |
| **`Acne Severity`** | Nivel de severidad del acné. | Categórica ordinal (binaria) |
| **`Family History of PCOS`** | Antecedentes de la condición en la familia. | Categórica nominal (binaria) |
| **`Insulin Resistance`** | Presencia de resistencia a la insulina. | Categórica nominal (binaria) |
| **`Lifestyle Score`** | Evaluación de hábitos de vida (dieta, ejercicio, etc.). | Numérica discreta |
| **`Stress Levels`** | Nivel de estrés reportado (Low, Medium, High). | Categórica ordinal |
| **`Urban/Rural`** | Tipo de entorno de vivienda. | Categórica nominal (binaria) |
| **`Socioeconomic Status`** | Nivel de ingresos/estatus social. | Categórica ordinal |
| **`Awareness of PCOS`** | Conocimiento previo de la paciente sobre la enfermedad. | Categórica nominal (binaria) |
| **`Fertility Concerns`** | Si la paciente tiene preocupaciones sobre su fertilidad. | Categórica nominal (binaria) |
| **`Undiagnosed PCOS Likelihood`** | Estimación estadística de probabilidad previa. | Numérica continua |
| **`Ethnicity`** | Grupo étnico de la paciente. | Categórica nominal |
| **`Diagnosis`** | **Variable Objetivo**: Confirmación del diagnóstico. | Categórica nominal (binaria) |

## Número de Observaciones

El dataset cuenta con un total de **120,000** registros, lo que proporciona una base sólida para el entrenamiento de modelos de aprendizaje automático y validación cruzada.

## Número de Variables

El conjunto de datos contiene **17** variables en total: 16 características predictoras y 1 etiqueta de clase (Diagnosis).

## Posibles Hipótesis de Estudio

1. **Hipótesis Clínica Principal:** Los síntomas externos como el `Hirsutism` y la `Acne Severity` tienen un peso predictivo mayor en el diagnóstico que los factores demográficos como el país de origen.
2. **Hipótesis Socioeconómica:** Las pacientes en entornos urbanos y con mayor `Socioeconomic Status` muestran una mayor `Awareness of PCOS`, lo que podría influir en la frecuencia de diagnósticos registrados frente a zonas rurales.
3. **Hipótesis de Estilo de Vida:** Existe una interacción significativa entre el `Stress Levels` y el `Lifestyle Score` que aumenta la probabilidad de `Menstrual Regularity` irregular, actuando como un precursor clave para el diagnóstico positivo.