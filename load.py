import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Float, String
from sqlalchemy_utils import database_exists, create_database
import os
import re

# --- Config ---
csv_folder = "data"   # folder containing all your CSV files
engine = create_engine("postgresql+psycopg2://report:ccsd@localhost:5432/report_card_2024")

if not database_exists(engine.url):
    create_database(engine.url)

# --- Function to map pandas dtype to SQLAlchemy type ---
def map_dtype(series):
    if pd.api.types.is_integer_dtype(series):
        return Integer()
    elif pd.api.types.is_float_dtype(series):
        return Float()
    else:
        return String()

# --- Load each CSV ---
for filename in os.listdir(csv_folder):

    path = os.path.join(csv_folder, filename)
    df = pd.read_csv(path)

    # Clean column names
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

    # Map dtypes automatically
    dtype = {col: map_dtype(df[col]) for col in df.columns}

    # Table name (use filename without extension)
    table_name = re.sub(r'(?<=[a-z])([A-Z,0-9])', r'_\1', os.path.splitext(filename)[0]).lower()

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",   # create new table or replace
        index=False,
        dtype=dtype
    )

    print(f"Imported {filename} as {table_name}")
