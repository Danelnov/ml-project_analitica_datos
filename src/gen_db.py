import pandas as pd
import sqlite3
from pathlib import Path


def dataset_to_db(csv_path, db_path, db_name):
    """Función para convertir un dataset en formato CSV a una base de datos SQLite."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_csv(csv_path, sep=",")
        df.to_sql(db_name, conn, if_exists="replace", index=False)
    print(f"¡Tabla {db_name} Creada Correctamente!")


BASE_DIR = Path(__file__).resolve().parents[1]

csv_regre_path = BASE_DIR / "ml-project/data/raw/dataset_regresion.csv"
csv_clasi_path = BASE_DIR / "ml-project/data/raw/dataset_clasification.csv"

db_regre_path = BASE_DIR / "ml-project/database/regresion.db"
db_clasi_path = BASE_DIR / "ml-project/database/clasification.db"

dataset_to_db(csv_regre_path, db_regre_path, "regresion")
dataset_to_db(csv_clasi_path, db_clasi_path, "clasification")