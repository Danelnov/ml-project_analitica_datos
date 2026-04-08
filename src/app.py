import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from scipy.stats import gaussian_kde, chi2_contingency, kruskal
from sklearn.impute import SimpleImputer

ds_pcos_path = Path("ml-project/data/raw/dataset_clasification.csv")
ds_house_path = Path("ml-project/data/raw/dataset_regresion.csv")
data_pcos = pd.read_csv(ds_pcos_path, sep=",")
data_house = pd.read_csv(ds_house_path, sep=",")

var_cat_pcos = data_pcos.select_dtypes(include="object").columns
var_num_pcos = data_pcos.select_dtypes(include=np.number).columns
var_cat_house = data_house.select_dtypes(include="object").columns
var_num_house = data_house.select_dtypes(include=np.number).columns


def resum_missing(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() * 100 / df.isnull().count()).sort_values(
        ascending=False
    )
    missing_data = pd.concat([total, percent], axis=1, keys=["Total", "Porcentaje"])
    return missing_data


def count_zeros(df):
    total = (df == 0).astype(int).sum(axis=0)
    percent = (df == 0).astype(int).sum(axis=0) * 100 / df.count()
    missing_data = pd.concat(
        [total, percent], axis=1, keys=["Total_ceros", "Porcentaje"]
    )
    return missing_data.sort_values(by="Porcentaje", ascending=False)


# Paleta de colores
colors = [
    "#613F75",
    "#1ee3b5",
    "#d62728",
    "#006948",
    "#ffd449",
    "#3F88C5",
]


with st.sidebar:
    match (
        ds_name := st.selectbox("Seleccionar el dataset", ["PCOS", "House Pricing"])
    ):
        case "PCOS":
            data = data_pcos
            var_cat = var_cat_pcos
            var_num = var_num_pcos
            data_imputed = data.copy()
            cat_imp = SimpleImputer(strategy="most_frequent")
            data_imputed[["Acne Severity"]] = cat_imp.fit_transform(
                data[["Acne Severity"]]
            )
            st.header("Dataset PCOS")
        case "House Pricing":
            data = data_house
            var_cat = var_cat_house
            var_num = var_num_house

            data_imputed = data.copy()
            mean_imp = SimpleImputer(strategy="mean")
            data_imputed["total_bedrooms"] = mean_imp.fit_transform(
                data[["total_bedrooms"]]
            )

            st.header("Dataset House Pricing")

    var_nums = st.multiselect("Variables numéricas", var_num, default=var_num)
    var_cats = st.multiselect("Variables categóricas", var_cat, default=var_cat)


exploracion, graficos, imputacion, correlacion, chi_cuadrado, anova = st.tabs(
    ["Exploración", "Gráficos", "Imputación", "Correlación", "Chi-cuadrado", "Anova"]
)

with exploracion:
    st.header("Exploración de datos")

    st.subheader("Primeras filas del dataset")
    st.write(data.head(100))

    st.subheader("Estadísticas de Variables Numéricas")
    stats_num = data[var_nums].agg(["mean", "median", "std", "min", "max"]).T
    st.write(stats_num.style.format("{:.2f}"))

    st.subheader("Estadísticas de Variables Categóricas")
    mode_data = {}
    for col in var_cats:
        mode_val = data[col].mode()
        mode_data[col] = mode_val.iloc[0]

    mode_df = pd.DataFrame.from_dict(mode_data, orient="index", columns=["Moda"])
    st.write(mode_df)

with graficos:
    st.header("Gráficos")

    num_cols = 2

    if var_nums:
        st.markdown("### Variables Numéricas")
        color_idx = 0
        for i in range(0, len(var_nums), num_cols):
            cols = st.columns(num_cols)

            for j in range(num_cols):
                if i + j < len(var_nums):
                    var = var_nums[i + j]
                    with cols[j]:
                        fig = px.histogram(
                            data,
                            x=var,
                            nbins=30,
                            title=f"Distribución de {var}",
                            labels={var: var},
                            marginal="box",
                        )
                        fig.update_traces(marker_color=colors[color_idx % len(colors)])
                        fig.update_layout(
                            height=400, showlegend=False, title_font_size=14
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        color_idx += 1

    # Gráficos de variables categóricas
    if var_cats:
        st.markdown("### Variables Categóricas")
        color_idx = 0
        for i in range(0, len(var_cats), num_cols):
            cols = st.columns(num_cols)

            for j in range(num_cols):
                if i + j < len(var_cats):
                    var = var_cats[i + j]
                    with cols[j]:
                        # Gráfico de barras
                        value_counts = data[var].value_counts()
                        fig = px.bar(
                            x=value_counts.index,
                            y=value_counts.values,
                            title=f"Frecuencia de {var}",
                            labels={"x": var, "y": "Cantidad"},
                            text_auto=True,
                        )
                        fig.update_traces(marker_color=colors[color_idx % len(colors)])
                        fig.update_layout(
                            height=400,
                            showlegend=False,
                            title_font_size=14,
                            xaxis_title=var,
                            yaxis_title="Cantidad",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        color_idx += 1


with imputacion:
    st.header("Imputación de datos")

    nulos, zeros = st.columns(2)

    with nulos:
        st.subheader("Resumen de valores faltantes")
        missing_data = resum_missing(data)
        st.write(missing_data)

    with zeros:
        st.subheader("Resumen de valores cero")
        zeros_data = count_zeros(data[var_nums])
        st.write(zeros_data)

    st.subheader("Comparación original vs imputado")
    if ds_name == "PCOS":
        if "Acne Severity" in data.columns:
            counts_original = (
                data["Acne Severity"].value_counts(dropna=False).rename("Original")
            )
            counts_imputed = (
                data_imputed["Acne Severity"]
                .value_counts(dropna=False)
                .rename("Imputado")
            )
            compare_df = (
                pd.concat([counts_original, counts_imputed], axis=1)
                .fillna(0)
                .reset_index()
            )
            compare_df.columns = ["Acne Severity", "Original", "Imputado"]

            fig = px.bar(
                compare_df,
                x="Acne Severity",
                y=["Original", "Imputado"],
                title="Comparación de frecuencia: Acne Severity (original vs imputado)",
                labels={"value": "Cantidad", "variable": "Dataset"},
                barmode="group",
                text_auto=True,
            )
            fig.update_layout(height=450, title_font_size=16)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(
                "La variable 'Acne Severity' no está disponible en el dataset PCOS."
            )

    elif ds_name == "House Pricing":
        if "total_bedrooms" in data.columns:
            original = data["total_bedrooms"].dropna()
            imputado = data_imputed["total_bedrooms"].dropna()

            xmin = min(original.min(), imputado.min())
            xmax = max(original.max(), imputado.max())
            xs = np.linspace(xmin, xmax, 200)

            kde_original = gaussian_kde(original)
            kde_imputado = gaussian_kde(imputado)

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=kde_original(xs),
                    mode="lines",
                    name="Original",
                    line=dict(color=colors[5], width=3),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=kde_imputado(xs),
                    mode="lines",
                    name="Imputado",
                    line=dict(color=colors[2], width=3, dash="dash"),
                )
            )

            fig.update_layout(
                height=450,
                title="Distribución KDE de total_bedrooms: original vs imputado",
                xaxis_title="total_bedrooms",
                yaxis_title="Densidad",
                title_font_size=16,
                legend=dict(title="Dataset", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(
                "La variable 'total_bedrooms' no está disponible en el dataset House Pricing."
            )

with correlacion:
    st.header("Correlación entre variables numéricas")

    if len(var_nums) >= 2:
        corr = data[var_nums].corr()

        # Máscara triangular superior (incluye diagonal), equivalente a seaborn + np.triu.
        mask = np.triu(np.ones_like(corr, dtype=bool), k=0)
        corr_masked = corr.mask(mask)

        # Etiquetas con 2 decimales solo en celdas visibles.
        text = corr_masked.round(2).astype(str).mask(corr_masked.isna(), "")

        fig = go.Figure(
            data=go.Heatmap(
                z=corr_masked.values,
                x=corr.columns,
                y=corr.index,
                colorscale="RdBu_r",
                zmin=-1,
                zmax=1,
                zmid=0,
                text=text.values,
                texttemplate="%{text}",
                hoverongaps=False,
                hovertemplate="%{y} vs %{x}<br>Corr: %{z:.2f}<extra></extra>",
                colorbar=dict(title="Corr"),
            )
        )

        fig.update_layout(
            title="Matriz de Correlación - Variables Numéricas",
            xaxis=dict(side="bottom", tickangle=-45, ticks=""),
            yaxis=dict(
                ticks="",
                autorange="reversed",
                scaleanchor="x",
                scaleratio=1,
            ),
            margin=dict(l=120, r=60, t=80, b=140),
            height=800,
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "Selecciona al menos dos variables numéricas para mostrar la matriz de correlación."
        )

with chi_cuadrado:
    st.header("Prueba de independencia Chi-cuadrado")

    if len(var_cats) >= 2:
        alpha = st.slider(
            "Alpha (Chi-cuadrado)",
            min_value=0.001,
            max_value=0.20,
            value=0.05,
            step=0.001,
            key="alpha_chi2",
        )
        n = len(var_cats)
        p_matrix = np.ones((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                tabla = pd.crosstab(data_imputed[var_cats[i]], data_imputed[var_cats[j]])
                _, p_value, _, _ = chi2_contingency(tabla)
                p_matrix[i, j] = p_value
                p_matrix[j, i] = p_value

        p_df = pd.DataFrame(p_matrix, index=var_cats, columns=var_cats)

        # Máscara triangular superior (incluye diagonal), similar a seaborn + np.triu.
        mask = np.triu(np.ones_like(p_df, dtype=bool), k=0)
        p_masked = p_df.mask(mask)

        text = p_masked.round(4).astype(str).mask(p_masked.isna(), "")

        zmax = min(1.0, max(0.10, alpha * 2))

        fig = go.Figure(
            data=go.Heatmap(
                z=p_masked.values,
                x=p_df.columns,
                y=p_df.index,
                colorscale="RdYlGn_r",
                zmin=0,
                zmax=zmax,
                zmid=alpha,
                text=text.values,
                texttemplate="%{text}",
                hoverongaps=False,
                hovertemplate="%{y} vs %{x}<br>p-value: %{z:.4f}<extra></extra>",
                colorbar=dict(title="p-value"),
            )
        )

        fig.update_layout(
            title=(
                "Mapa de Calor de p-values de Prueba de Independencia Chi-cuadrado"
                "<br>(Variables Categóricas)"
            ),
            xaxis=dict(side="bottom", tickangle=-45, ticks=""),
            yaxis=dict(
                ticks="",
                autorange="reversed",
                scaleanchor="x",
                scaleratio=1,
            ),
            margin=dict(l=140, r=80, t=100, b=150),
            height=800,
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            f"Referencia: valores p menores a {alpha:.3f} sugieren dependencia entre variables."
        )
    else:
        st.info(
            "Este dataset tiene menos de 2 variables categóricas; se omite el mapa de Chi-cuadrado."
        )


with anova:
    st.header("Kruskal-Wallis entre variables categóricas y numéricas")

    if len(var_cats) >= 1 and len(var_nums) >= 1:
        alpha = st.slider(
            "Alpha (Kruskal-Wallis)",
            min_value=0.001,
            max_value=0.20,
            value=0.05,
            step=0.001,
            key="alpha_kruskal",
        )
        pvals = pd.DataFrame(index=var_nums, columns=var_cats, dtype=float)

        def kruskal_test(df: pd.DataFrame, x: str, y: str) -> float:
            tmp = df[[x, y]].dropna()
            grupos = [g[y].values for _, g in tmp.groupby(x)]
            grupos = [g for g in grupos if len(g) > 0]
            if len(grupos) < 2:
                return np.nan
            try:
                _, p_value = kruskal(*grupos)
                return p_value
            except ValueError:
                # Casos degenerados (ej. todos los valores iguales en los grupos).
                return np.nan

        for y in var_nums:
            for x in var_cats:
                pvals.loc[y, x] = kruskal_test(data_imputed, x, y)

        sig = pd.DataFrame(
            np.where(pvals.isna(), np.nan, (pvals < alpha).astype(int)),
            index=pvals.index,
            columns=pvals.columns,
        )
        sig_txt = sig.replace({0: "No", 1: "Sí"}).astype(object).where(~sig.isna(), "")

        fig = go.Figure(
            data=go.Heatmap(
                z=sig.values,
                x=sig.columns,
                y=sig.index,
                colorscale=[
                    [0.0, "#d73027"],
                    [0.4999, "#d73027"],
                    [0.5, "#1a9850"],
                    [1.0, "#1a9850"],
                ],
                zmin=0,
                zmax=1,
                text=sig_txt.values,
                texttemplate="%{text}",
                customdata=pvals.values,
                hoverongaps=False,
                hovertemplate=(
                    "Numérica: %{y}<br>"
                    "Categórica: %{x}<br>"
                    "Significativo: %{text}<br>"
                    "p-value: %{customdata:.4f}<extra></extra>"
                ),
                showscale=False,
            )
        )

        fig.update_layout(
            title=f"Kruskal-Wallis (binario, alpha={alpha})",
            xaxis=dict(title="Variables categóricas", side="bottom", tickangle=-45),
            yaxis=dict(title="Variables numéricas", autorange="reversed"),
            margin=dict(l=140, r=40, t=80, b=140),
            height=max(500, int(45 * len(var_nums) + 180)),
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "Se requiere al menos una variable categórica y una numérica para ejecutar Kruskal-Wallis."
        )
