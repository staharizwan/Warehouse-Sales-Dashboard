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

# Sales trend
def get_sales_trend(year=None, month=None, item_type=None):

    if year is not None:
        group_column = "month"
    else:
        group_column = "year"

    conditions = []
    params = []

    if year is not None:
        conditions.append("year = ?")
        params.append(year)

    if month is not None:
        conditions.append("month = ?")
        params.append(month)

    if item_type is not None:
        conditions.append("item_type = ?")
        params.append(item_type)

    query = f"""
    SELECT
        {group_column},
        SUM(warehouse_sales) AS warehouse_sales,
        SUM(retail_sales) AS retail_sales
    FROM sales
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f"""
    GROUP BY {group_column}
    ORDER BY {group_column}
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)
    result = cursor.fetchall()

    conn.close()

    return result

# Sales by item type
def get_item_type_sales(year=None, month=None):
    conditions = ["item_type IS NOT NULL"]
    params = []

    if year is not None:
        conditions.append("year = ?")
        params.append(year)

    if month is not None:
        conditions.append("month = ?")
        params.append(month)

    query = """
    SELECT
        item_type,
        SUM(warehouse_sales) AS warehouse_sales,
        SUM(retail_sales) AS retail_sales
    FROM sales
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
    GROUP BY item_type
    ORDER BY warehouse_sales DESC
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    result = cursor.fetchall()
    conn.close()

    return result


# Top supplier(s)
 
def get_top_suppliers(year=None, month=None, item_type=None, limit=10):
    conditions = ["supplier IS NOT NULL"]
    params = []

    if year is not None:
        conditions.append("year = ?")
        params.append(year)

    if month is not None:
        conditions.append("month = ?")

    if item_type is not None:
        conditions.append("item_type = ?")
        params.append(item_type)

    query = """
    SELECT
        supplier,
        SUM(warehouse_sales + retail_sales) AS total_sales
    FROM sales
    """

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
    GROUP BY supplier
    ORDER BY total_sales DESC
    LIMIT ?
    """

    params.append(limit)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    result = cursor.fetchall()
    conn.close()

    return result





# Temporary tests
#%% 
if __name__ == "__main__":
    print("Y")
    print("KPIs: ")
    print(get_kpis())

    print("\nYearly Sales: ")
    print(get_yearly_sales())

    print("\nSales by Item Type: ")
    print(get_sales_by_item_type())
    print(get_item_type_sales())
    
    print("X")
# %%
