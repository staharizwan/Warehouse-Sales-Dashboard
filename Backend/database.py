#%% Imports

import sqlite3
from pathlib import Path


#%% Database path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "warehouse_sales.db"


#%% Connection function

def get_connection():
    return sqlite3.connect(DB_PATH)



#%% Test database connection

conn = get_connection()

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales;")

result = cursor.fetchone()

print("Rows in sales table:", result[0])

conn.close()

# %%

