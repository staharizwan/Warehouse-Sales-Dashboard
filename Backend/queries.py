#%%
from Backend.database import get_connection

## To run the backend, run the follwoing....
## uvicorn Backend.app:app --reload 

# KPI query
#%%
def get_kpis(year = None, month = None, item_type = None):
    conn = get_connection()
    query = """
    SELECT
        SUM(warehouse_sales) AS total_warehouse_sales,
        SUM(retail_sales) AS total_retail_sales,
        SUM(retail_transfers) AS total_retail_transfers
    FROM sales
    """
    params = []
    conditions = []
    
    if year is not None:
        conditions.append("year = ?")
        params.append(year)
    
    if month is not None:
        conditions.append("month = ?")
        params.append(month)
    
    if item_type is not None:
        conditions.append("item_type = ?")
        params.append(item_type)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    
    return result

# Yearly sales query

def get_yearly_sales():
    conn = get_connection()
    
    query = """
    SELECT
        year,
        SUM(warehouse_sales) AS warehouse_sales,
        SUM(retail_sales) AS retail_sales
    
    FROM sales
    GROUP BY year
    ORDER BY year
    """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    conn.close()
    
    return result

# Sales item by type    

def get_sales_by_item_type():
    conn = get_connection()
    query = """
    SELECT 
        item_type, SUM(warehouse_sales) AS warehouse_sales,
        SUM(retail_sales) AS retail_sales
    FROM sales
    GROUP BY item_type
    ORDER BY warehouse_sales DESC
    
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    
    return result

# Temporary tests
#%% 

print("KPIs: ")
print(get_kpis())

print("\nYearly Sales: ")
print(get_yearly_sales())

print("\nSales by Item Type: ")
print(get_sales_by_item_type())
# %%
