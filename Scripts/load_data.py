#%%
import sqlite3
from pathlib import Path

import pandas as pd
print("done")
#%%
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "Warehouse_and_Retail_Sales.csv"
DB_PATH = BASE_DIR / "db" / "warehouse_sales.db"

print("CSV:", CSV_PATH)
print("Database:", DB_PATH)

#%%
df = pd.read_csv(CSV_PATH)
print(df.shape)
print(df.head())
print(df.info())


# Renaming the columns
# %%
df = df.rename(
    columns = {
        "YEAR": "year",
        "MONTH" : "month",
        "SUPPLIER" : "supplier",
        "ITEM CODE" : "item_code",
        "ITEM DESCRIPTION" : "item_description",
        "ITEM TYPE" : "item_type",
        "RETAIL SALES" : "retail_sales",
        "RETAIL TRANSFERS" : "retail_transfers",
        "WAREHOUSE SALES" : "warehouse_sales"
        
    }
)
print(df.columns)

# Checking data quality
#%%
print(df.isna().sum())
print("Duplicates:", df.duplicated().sum())

# Creating a database
# %%
DB_PATH.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(DB_PATH)

df.to_sql(
    "sales",
    conn,
    if_exists = "replace",
    index = False
)

print("Data loaded successfully")
# %%
