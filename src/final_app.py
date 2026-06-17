from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_CONFIGS = {
    "Regresión - House Pricing": {
        "key": "regression",
        "kind": "regression",
        "title": "Predicción de median_house_value",
        "dataset_name": "regresión",
        "data_path": PROJECT_ROOT / "ml-project" / "data" / "raw" / "dataset_regresion.csv",
        "model_path": PROJECT_ROOT / "models" / "linear_regression_model.joblib",
        "features_path": PROJECT_ROOT / "models" / "feature_names_regression.joblib",
        "target": "median_house_value",
        "submit_label": "Predecir valor",
        "empty_state": "Completa las variables y presiona Predecir valor.",
    },
    "Clasificación - PCOS": {
        "key": "classification",
        "kind": "classification",
        "title": "Clasificación de diagnóstico PCOS",
        "dataset_name": "clasificación",
        "data_path": PROJECT_ROOT
        / "ml-project"
        / "data"
        / "raw"
        / "dataset_clasification.csv",
        "model_path": PROJECT_ROOT / "models" / "clasificacion_reg_logistica.joblib",
        "features_path": PROJECT_ROOT / "models" / "feature_names_clasificacion.joblib",
        "target": "Diagnosis",
        "submit_label": "Predecir diagnóstico",
        "empty_state": "Completa las variables y presiona Predecir diagnóstico.",
    },
}

CLASS_LABELS = {
    0: "No PCOS",
    1: "PCOS",
    "No": "No PCOS",
    "Yes": "PCOS",
}


@st.cache_data
def load_data(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_path)


@st.cache_resource
def load_model(model_path: str, features_path: str):
    model = joblib.load(model_path)
    feature_names = joblib.load(features_path)
    return model, list(feature_names)


def numeric_default(series: pd.Series) -> float:
    return float(series.dropna().median())


def format_stats_value(value) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, int | float):
        return f"{value:,.4f}".rstrip("0").rstrip(".")
    return str(value)


def feature_stats(df: pd.DataFrame, feature_names: list[str]) -> pd.DataFrame:
    rows = []
    for feature in feature_names:
        if pd.api.types.is_numeric_dtype(df[feature]):
            rows.append(
                {
                    "variable": feature,
                    "tipo": "numérica",
                    "mínimo": format_stats_value(df[feature].min()),
                    "mediana": format_stats_value(df[feature].median()),
                    "máximo": format_stats_value(df[feature].max()),
                }
            )
        else:
            rows.append(
                {
                    "variable": feature,
                    "tipo": "categórica",
                    "mínimo": "",
                    "mediana": format_stats_value(
                        df[feature].mode(dropna=True).iloc[0]
                    ),
                    "máximo": format_stats_value(df[feature].nunique()),
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


def categorical_summary(df: pd.DataFrame) -> pd.DataFrame:
    categorical_df = df.select_dtypes(exclude="number")
    rows = []

    for column in categorical_df.columns:
        value_counts = categorical_df[column].value_counts(dropna=False)
        mode_value = value_counts.index[0]
        mode_count = int(value_counts.iloc[0])

        rows.append(
            {
                "variable": column,
                "categorías": categorical_df[column].nunique(dropna=True),
                "moda": format_stats_value(mode_value),
                "frecuencia moda": mode_count,
                "porcentaje moda": f"{mode_count / len(df):.2%}",
                "valores faltantes": int(categorical_df[column].isna().sum()),
            }
        )

    return pd.DataFrame(rows)


def get_best_estimator(model):
    return getattr(model, "best_estimator_", model)


def get_pipeline_steps(model) -> list[tuple[str, object]]:
    estimator = get_best_estimator(model)
    return list(getattr(estimator, "steps", []))


def get_final_estimator(model):
    steps = get_pipeline_steps(model)
    if steps:
        return steps[-1][1]
    return get_best_estimator(model)


def get_transformed_feature_names(model, feature_names: list[str]) -> list[str]:
    for _, step in get_pipeline_steps(model):
        if step.__class__.__name__ != "ColumnTransformer":
            continue

        try:
            return list(step.get_feature_names_out(feature_names))
        except TypeError:
            return list(step.get_feature_names_out())

    return feature_names


def original_feature_name(transformed_name: str, feature_names: list[str]) -> str:
    clean_name = transformed_name.split("__", 1)[-1]

    for feature in sorted(feature_names, key=len, reverse=True):
        if clean_name == feature or clean_name.startswith(f"{feature}_"):
            return feature

    return clean_name


def feature_importance(model, feature_names: list[str]) -> pd.DataFrame:
    final_estimator = get_final_estimator(model)
    transformed_names = get_transformed_feature_names(model, feature_names)

    if hasattr(final_estimator, "feature_importances_"):
        raw_importance = final_estimator.feature_importances_
        source = "feature_importances"
    elif hasattr(final_estimator, "coef_"):
        raw_importance = final_estimator.coef_
        if raw_importance.ndim > 1:
            raw_importance = abs(raw_importance).mean(axis=0)
        source = "coeficiente absoluto"
    else:
        return pd.DataFrame()

    if len(raw_importance) != len(transformed_names):
        if len(raw_importance) == len(feature_names):
            transformed_names = feature_names
        else:
            return pd.DataFrame()

    importance_df = pd.DataFrame(
        {
            "variable_transformada": transformed_names,
            "variable": [
                original_feature_name(name, feature_names) for name in transformed_names
            ],
            "importancia": abs(raw_importance),
        }
    )

    grouped_df = (
        importance_df.groupby("variable", as_index=False)["importancia"]
        .sum()
        .sort_values("importancia", ascending=False)
    )
    total_importance = grouped_df["importancia"].sum()
    if total_importance:
        grouped_df["importancia (%)"] = grouped_df["importancia"] / total_importance * 100
    else:
        grouped_df["importancia (%)"] = 0

    grouped_df["fuente"] = source
    return grouped_df


def render_feature_importance(model, feature_names: list[str]) -> None:
    importance_df = feature_importance(model, feature_names)

    if importance_df.empty:
        st.info("Este modelo no expone importancia de variables.")
        return

    chart_df = importance_df.sort_values("importancia (%)", ascending=True)
    fig = px.bar(
        chart_df,
        x="importancia (%)",
        y="variable",
        orientation="h",
        text=chart_df["importancia (%)"].map("{:.1f}%".format),
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=max(360, 34 * len(chart_df)),
        xaxis_title="Importancia (%)",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=10, r=40, t=10, b=10),
    )

    st.plotly_chart(fig, width="stretch")
    st.dataframe(
        importance_df[["variable", "importancia (%)", "fuente"]],
        width="stretch",
        hide_index=True,
    )


def target_summary(target_data: pd.Series) -> pd.DataFrame:
    if pd.api.types.is_numeric_dtype(target_data):
        return target_data.describe().to_frame(name=target_data.name)

    counts = target_data.value_counts(dropna=False).reset_index()
    counts.columns = [target_data.name, "registros"]
    counts["porcentaje"] = counts["registros"] / len(target_data) * 100
    return counts


def format_class_label(value) -> str:
    if pd.isna(value):
        return "Sin dato"

    normalized_value = int(value) if isinstance(value, (bool, int)) else value
    return CLASS_LABELS.get(normalized_value, str(value))


def model_class_from_target(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        return 1 if value.lower() == "yes" else 0
    return int(value)


def build_input_dataframe(values: dict, feature_names: list[str]) -> pd.DataFrame:
    ordered_values = {feature: values[feature] for feature in feature_names}
    return pd.DataFrame([ordered_values], columns=feature_names)


def predict_price(model, values: dict, feature_names: list[str]) -> float:
    input_df = build_input_dataframe(values, feature_names)
    prediction = model.predict(input_df)[0]
    return float(prediction)


def predict_classification(model, values: dict, feature_names: list[str]):
    input_df = build_input_dataframe(values, feature_names)
    prediction = model.predict(input_df)[0]

    probabilities = None
    if hasattr(model, "predict_proba"):
        classes = list(getattr(model, "classes_", []))
        probabilities = dict(zip(classes, model.predict_proba(input_df)[0]))

    return int(prediction), probabilities


def render_prediction_inputs(
    features_df: pd.DataFrame,
    feature_names: list[str],
    reference_row: pd.Series,
    selected_index: int,
    model_key: str,
) -> dict:
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
        default_value = numeric_default(series) if pd.isna(ref_value) else ref_value

        container = col_left if index % 2 == 0 else col_right
        with container:
            if pd.api.types.is_integer_dtype(series):
                values[feature] = st.number_input(
                    feature,
                    min_value=int(series.min()),
                    max_value=int(series.max()),
                    value=int(default_value),
                    step=1,
                    key=f"{model_key}_{feature}_{selected_index}",
                )
            else:
                values[feature] = st.number_input(
                    feature,
                    min_value=float(series.min()),
                    max_value=float(series.max()),
                    value=float(default_value),
                    step=0.001,
                    format="%.4f",
                    key=f"{model_key}_{feature}_{selected_index}",
                )

    for feature in categorical_features:
        categories = sorted(features_df[feature].dropna().unique().tolist())
        ref_value = reference_row[feature]
        selected_position = categories.index(ref_value) if ref_value in categories else 0
        values[feature] = st.selectbox(
            feature,
            categories,
            index=selected_position,
            key=f"{model_key}_{feature}_{selected_index}",
        )

    return values


def show_regression_result(
    model,
    values: dict,
    feature_names: list[str],
    reference_row: pd.Series,
    target: str,
) -> None:
    prediction = predict_price(model, values, feature_names)

    metric_col, real_col = st.columns(2)
    metric_col.metric("Predicción", f"${prediction:,.0f}")
    real_col.metric(
        "Valor real de la fila de referencia",
        f"${reference_row[target]:,.0f}",
        delta=f"${prediction - reference_row[target]:,.0f}",
    )


def show_classification_result(
    model,
    values: dict,
    feature_names: list[str],
    reference_row: pd.Series,
    target: str,
) -> None:
    prediction, probabilities = predict_classification(model, values, feature_names)
    actual_class = model_class_from_target(reference_row[target])

    prediction_col, probability_col, real_col = st.columns(3)
    prediction_col.metric("Predicción", format_class_label(prediction))
    real_col.metric("Diagnóstico real", format_class_label(reference_row[target]))

    if probabilities:
        positive_probability = probabilities.get(1)
        if positive_probability is not None:
            probability_col.metric("Probabilidad PCOS", f"{positive_probability:.1%}")

        probabilities_df = pd.DataFrame(
            [
                {
                    "clase": format_class_label(class_value),
                    "probabilidad": probability,
                }
                for class_value, probability in probabilities.items()
            ]
        )
        probabilities_df["probabilidad"] = probabilities_df["probabilidad"].map(
            "{:.2%}".format
        )
        st.dataframe(probabilities_df, width="stretch", hide_index=True)
    else:
        probability_col.metric("Probabilidad PCOS", "No disponible")

    if actual_class is not None:
        if prediction == actual_class:
            st.success("La predicción coincide con la fila de referencia.")
        else:
            st.warning("La predicción no coincide con la fila de referencia.")


st.set_page_config(
    page_title="Predicción de modelos ML",
    layout="wide",
)

with st.sidebar:
    st.header("Modelo")
    selected_model = st.selectbox("Selecciona el modelo", list(MODEL_CONFIGS))

config = MODEL_CONFIGS[selected_model]
model_key = config["key"]
data_path = config["data_path"]
model_path = config["model_path"]
features_path = config["features_path"]
target = config["target"]

st.title(config["title"])

try:
    data = load_data(str(data_path))
    model, feature_names = load_model(str(model_path), str(features_path))
except FileNotFoundError as exc:
    st.error(f"No se encontró el archivo requerido: {exc.filename}")
    st.stop()
except Exception as exc:
    st.error(f"No fue posible cargar la app: {exc}")
    st.stop()

missing_columns = [column for column in [*feature_names, target] if column not in data]
if missing_columns:
    st.error(
        "El dataset seleccionado no contiene estas columnas requeridas: "
        + ", ".join(missing_columns)
    )
    st.stop()

features_df = data[feature_names].copy()
target_data = data[target]

with st.sidebar:
    st.header("Datos")
    st.metric("Registros", f"{len(data):,}")
    st.metric("Variables del modelo", len(feature_names))

    if config["kind"] == "regression":
        st.metric("Target promedio", f"${target_data.mean():,.0f}")
    else:
        positive_count = int((target_data == "Yes").sum())
        positive_rate = positive_count / len(target_data)
        st.metric("Casos PCOS", f"{positive_count:,}", f"{positive_rate:.1%}")

    selected_index = st.number_input(
        "Fila de referencia",
        min_value=0,
        max_value=len(data) - 1,
        value=0,
        step=1,
        key=f"reference_row_{model_key}",
    )

    reference_row = data.iloc[int(selected_index)]
    if config["kind"] == "regression":
        st.caption(f"Valor real: ${reference_row[target]:,.0f}")
    else:
        st.caption(f"Diagnóstico real: {format_class_label(reference_row[target])}")

prediction_tab, dataset_tab, model_tab = st.tabs(["Predicción", "Dataset", "Modelo"])

with prediction_tab:
    st.subheader("Variables de entrada")

    with st.form(f"prediction_form_{model_key}"):
        values = render_prediction_inputs(
            features_df,
            feature_names,
            reference_row,
            int(selected_index),
            model_key,
        )
        submitted = st.form_submit_button(config["submit_label"])

    if submitted:
        ordered_values = {feature: values[feature] for feature in feature_names}

        if config["kind"] == "regression":
            show_regression_result(
                model,
                ordered_values,
                feature_names,
                reference_row,
                target,
            )
        else:
            show_classification_result(
                model,
                ordered_values,
                feature_names,
                reference_row,
                target,
            )

        st.dataframe(
            pd.DataFrame([ordered_values]),
            width="stretch",
            hide_index=True,
        )
    else:
        st.info(config["empty_state"])

with dataset_tab:
    st.subheader(f"Dataset de {config['dataset_name']}")
    st.dataframe(data.head(100), width="stretch", hide_index=True)

    st.subheader("Valores mínimos y máximos de variables numéricas")
    st.dataframe(
        numeric_min_max(data),
        width="stretch",
        hide_index=True,
    )

    categorical_df = categorical_summary(data)
    if not categorical_df.empty:
        st.subheader("Resumen de variables categóricas")
        st.dataframe(
            categorical_df,
            width="stretch",
            hide_index=True,
        )

    st.subheader("Resumen de la variable objetivo")
    st.dataframe(
        target_summary(target_data),
        width="stretch",
        hide_index=not pd.api.types.is_numeric_dtype(target_data),
    )

with model_tab:
    st.subheader("Importancia de variables")
    render_feature_importance(model, feature_names)

    st.subheader("Variables usadas por el modelo")
    st.dataframe(
        feature_stats(data, feature_names),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Archivos cargados")
    st.code(
        f"Modelo: {model_path.relative_to(PROJECT_ROOT)}\n"
        f"Features: {features_path.relative_to(PROJECT_ROOT)}\n"
        f"Dataset: {data_path.relative_to(PROJECT_ROOT)}",
        language="text",
    )
