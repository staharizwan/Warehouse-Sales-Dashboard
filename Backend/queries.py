#%%
from Backend.database import get_connection


# KPI query
#%%
def get_kpis():
    conn = get_connection()
    query = """
    SELECT
        SUM(warehouse_sales) AS total_warehouse_sales,
        SUM(retail_sales) AS total_retail_sales,
        SUM(retail_transfers) AS total_retail_transfers
    FROM sales;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
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
    ORDER BY year;
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
    ORDER BY warehouse_sales DESC;
    
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
