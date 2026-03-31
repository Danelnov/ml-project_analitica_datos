import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

BASE_DIR /= "ml-project/database"

print("""
    Seleccione una opción:
    
    [1]: Regresión
    [2]: Clasificación
""")
opcion = int(input("Ingrese el número de la opción deseada: "))

if type(opcion) != int:
    raise ValueError("La opcioń debe ser un número")

if opcion not in [1, 2]:
    raise ValueError("Opción no válida. Por favor, ingrese 1 o 2.")

if opcion == 1:
    DB_PATH = BASE_DIR / "regresion.db" 
    SQL_DIR = BASE_DIR / "sql/regresion"
    DATA_DIR = BASE_DIR / "data/regresion"
else:
    DB_PATH = BASE_DIR / "clasification.db"
    SQL_DIR = BASE_DIR / "sql/clasification"
    DATA_DIR = BASE_DIR / "data/clasification"


def export_query(i):

    sql_file = SQL_DIR / f"query_{i}.sql"

    with open(sql_file, "r") as f:
        query = f.read()

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(query, conn)

    conn.close()

    output_file = DATA_DIR / f"query_{i}.csv"

    df.to_csv(output_file, index=False)

    print("\nConsulta ejecutada correctamente")
    print(f"Archivo generado: {output_file}")

i = int(input("¿Qué query quieres ejecutar? "))

export_query(i)