# ML Project - Analítica de Datos

Proyecto de analítica de datos y machine learning con dos casos de uso:

- **Regresión - House Pricing:** predicción de `median_house_value` a partir de variables geográficas, demográficas y de vivienda.
- **Clasificación - PCOS:** predicción del diagnóstico de PCOS a partir de variables clínicas, hábitos y factores socioeconómicos.

El proyecto incluye datasets, modelos entrenados y aplicaciones en Streamlit para exploración, predicción y visualización de resultados.

## Estructura Principal

```text
.
├── ml-project/data/raw/
│   ├── dataset_clasification.csv
│   └── dataset_regresion.csv
├── models/
│   ├── clasificacion_reg_logistica.joblib
│   ├── feature_names_clasificacion.joblib
│   ├── feature_names_regression.joblib
│   └── linear_regression_model.joblib
├── src/
│   ├── app.py
│   └── final_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requisitos

- Python `>=3.12`
- `uv` para gestionar el entorno virtual y las dependencias

El proyecto ya incluye `pyproject.toml` y `uv.lock`, por lo que las dependencias se pueden instalar directamente con `uv`.

## Instalar uv

La referencia oficial de instalación está en la documentación de Astral:

https://docs.astral.sh/uv/getting-started/installation/

En macOS o Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después de instalar, reinicia la terminal o recarga tu shell y verifica:

```bash
uv --version
```

## Crear el Entorno e Instalar Dependencias

Desde la raíz del proyecto:

```bash
uv python install 3.14
uv venv --python 3.14
uv sync
```

`uv sync` instala las dependencias definidas en `pyproject.toml` usando las versiones bloqueadas en `uv.lock`.

También puedes dejar que `uv run` sincronice el entorno automáticamente al ejecutar comandos del proyecto.

## Ejecutar Streamlit

Aplicación principal de predicción de modelos:

```bash
uv run streamlit run src/final_app.py
```

Aplicación exploratoria de datasets:

```bash
uv run streamlit run src/app.py
```

Streamlit abrirá una URL local similar a:

```text
http://localhost:8501
```

Si el puerto `8501` está ocupado, puedes usar otro:

```bash
uv run streamlit run src/final_app.py --server.port 8502
```

## Uso General

En `src/final_app.py` puedes seleccionar el modelo desde la barra lateral:

- `Regresión - House Pricing`
- `Clasificación - PCOS`

La aplicación permite:

- cargar el modelo correspondiente;
- seleccionar una fila de referencia;
- modificar las variables de entrada;
- generar predicciones;
- revisar el dataset;
- consultar variables numéricas y categóricas;
- visualizar la importancia de variables del modelo.
