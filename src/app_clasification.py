import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

ds_path = Path("ml-project/data/raw/dataset_clasification.csv")
data = pd.read_csv(ds_path, sep=",")
var_num = data.select_dtypes(include= [np.int64, np.float64]).columns.tolist()
var_cat = data.select_dtypes(include=['string']).columns.tolist()

st.title("PCOS Dataset")

st.write("## Variables numéricas")

for var in var_num:
    data_var = data[var]
    
    st.write(f"### Grafica de {var}")    

    hist = np.histogram(
        data_var, bins="auto", range=(data_var.min(), data_var.max())
    )[0]
    st.bar_chart(hist)

st.write("## Variables categóricas")

for var in var_cat:
    counts = data[var].value_counts(dropna=False).reset_index()
    counts.columns = [var, "conteo"]
    fig = px.bar(
        counts,
        x=var,
        y="conteo",
        title=f"Frecuencia de {var}",
        text="conteo",
    )
    fig.update_layout(xaxis_title=var, yaxis_title="Conteo", bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)
