from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "ml-project" / "data" / "raw" / "dataset_regresion.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "linear_regression_model.joblib"
FEATURES_PATH = PROJECT_ROOT / "models" / "feature_names_regression.joblib"
TARGET = "median_house_value"


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    return model, list(feature_names)


def numeric_default(series: pd.Series) -> float:
    return float(series.dropna().median())


def feature_stats(df: pd.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    rows = []
    for feature in feature_names:
        if pd.api.types.is_numeric_dtype(df[feature]):
            rows.append(
                {
                    "variable": feature,
                    "tipo": "numérica",
                    "mínimo": df[feature].min(),
                    "mediana": df[feature].median(),
                    "máximo": df[feature].max(),
                }
            )
        else:
            rows.append(
                {
                    "variable": feature,
                    "tipo": "categórica",
                    "mínimo": "",
                    "mediana": df[feature].mode(dropna=True).iloc[0],
                    "máximo": df[feature].nunique(),
                }
            )
    return pd.DataFrame(rows)


def numeric_min_max(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include="number")
    return (
        numeric_df.agg(["min", "max"])
        .transpose()
        .reset_index()
        .rename(columns={"index": "variable", "min": "mínimo", "max": "máximo"})
    )


def predict_price(model, values: dict, feature_names: list[str]) -> float:
    input_df = pd.DataFrame([values], columns=feature_names)
    prediction = model.predict(input_df)[0]
    return float(prediction)


st.set_page_config(
    page_title="Predicción House Pricing",
    layout="wide",
)

st.title("Predicción de median_house_value")

try:
    data = load_data()
    model, feature_names = load_model()
except FileNotFoundError as exc:
    st.error(f"No se encontró el archivo requerido: {exc.filename}")
    st.stop()
except Exception as exc:
    st.error(f"No fue posible cargar la app: {exc}")
    st.stop()

features_df = data[feature_names].copy()
target_data = data[TARGET]

with st.sidebar:
    st.header("Datos")
    st.metric("Registros", f"{len(data):,}")
    st.metric("Variables del modelo", len(feature_names))
    st.metric("Target promedio", f"${target_data.mean():,.0f}")

    selected_index = st.number_input(
        "Fila de referencia",
        min_value=0,
        max_value=len(data) - 1,
        value=0,
        step=1,
    )

    reference_row = data.iloc[int(selected_index)]
    st.caption(f"Valor real: ${reference_row[TARGET]:,.0f}")

prediction_tab, dataset_tab, model_tab = st.tabs(["Predicción", "Dataset", "Modelo"])

with prediction_tab:
    st.subheader("Variables de entrada")

    with st.form("prediction_form"):
        values = {}

        col_left, col_right = st.columns(2)
        numeric_features = [
            feature
            for feature in feature_names
            if pd.api.types.is_numeric_dtype(features_df[feature])
        ]
        categorical_features = [
            feature
            for feature in feature_names
            if not pd.api.types.is_numeric_dtype(features_df[feature])
        ]

        for index, feature in enumerate(numeric_features):
            series = features_df[feature]
            ref_value = reference_row[feature]
            default_value = (
                numeric_default(series) if pd.isna(ref_value) else float(ref_value)
            )
            min_value = float(series.min())
            max_value = float(series.max())

            container = col_left if index % 2 == 0 else col_right
            with container:
                values[feature] = st.number_input(
                    feature,
                    min_value=min_value,
                    max_value=max_value,
                    value=default_value,
                    step=0.01,
                    format="%.4f",
                    key=f"{feature}_{selected_index}",
                )

        for feature in categorical_features:
            categories = sorted(features_df[feature].dropna().unique().tolist())
            ref_value = reference_row[feature]
            selected_position = categories.index(ref_value) if ref_value in categories else 0
            values[feature] = st.selectbox(
                feature,
                categories,
                index=selected_position,
                key=f"{feature}_{selected_index}",
            )

        submitted = st.form_submit_button("Predecir valor")

    if submitted:
        ordered_values = {feature: values[feature] for feature in feature_names}
        prediction = predict_price(model, ordered_values, feature_names)

        metric_col, real_col = st.columns(2)
        metric_col.metric("Predicción", f"${prediction:,.0f}")
        real_col.metric(
            "Valor real de la fila de referencia",
            f"${reference_row[TARGET]:,.0f}",
            delta=f"${prediction - reference_row[TARGET]:,.0f}",
        )

        st.dataframe(
            pd.DataFrame([ordered_values]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Completa las variables y presiona Predecir valor.")

with dataset_tab:
    st.subheader("Dataset de regresión")
    st.dataframe(data.head(100), use_container_width=True, hide_index=True)

    st.subheader("Valores mínimos y máximos de variables numéricas")
    st.dataframe(
        numeric_min_max(data),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Resumen de la variable objetivo")
    st.dataframe(
        target_data.describe().to_frame(name=TARGET),
        use_container_width=True,
    )

with model_tab:
    st.subheader("Variables usadas por el modelo")
    st.dataframe(
        feature_stats(data, feature_names),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Archivos cargados")
    st.code(
        f"Modelo: {MODEL_PATH.relative_to(PROJECT_ROOT)}\n"
        f"Features: {FEATURES_PATH.relative_to(PROJECT_ROOT)}\n"
        f"Dataset: {DATA_PATH.relative_to(PROJECT_ROOT)}",
        language="text",
    )
