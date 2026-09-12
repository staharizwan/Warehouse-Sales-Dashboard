from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from Backend.queries import(
    get_kpis,
    get_sales_by_item_type,
    get_yearly_sales,
    get_sales_trend,
    get_item_type_sales,
    get_top_suppliers
)

# FASTAPI app
#%%
app = FastAPI(
    title="Warehouse & Retail Sales API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://warehouse-sales-dashboard-blond.vercel.app"
                ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    
)

# Root endpoint
#%%
@app.get("/")
def root():
    return {
        "message" : "Warehouse & retail sales API is running"
    }
    
@app.get("/api/kpis")
def kpis(year:Optional[int] = None,
         month: Optional[int] = None,
         item_type: Optional[str] = None
         
        ):
    
    result = get_kpis(year, month, item_type)
    
    return {
        "total_warehouse_sales" : result[0],
        "total_retail_sales" : result[1],
        "total_retail_transfers" : result[2]
    }
    
@app.get("/api/yearly-sales")
def yearly_sales():
    result = get_yearly_sales()
    
    return[
        {
            "year" : row[0],
            "warehouse_sales": row[1],
            "retail_sales": row[2]
        }
        
        for row in result
    ]
    
@app.get("/api/item-types")
def item_types():
    result = get_sales_by_item_type()
    
    return [
        {
            "item_type": row[0],
            "warehouse_sales" : row[1],
            "retail_sales": row[2]
        }
        for row in result
    ]
    
@app.get("/api/sales-trend")
def sales_trend(
    year: Optional[int] = None,
    month : Optional[int] = None,
    item_type : Optional[str] = None
    ):
    result = get_sales_trend(year, month, item_type)
    return [
        {
            "period" : row[0],
            "warehouse_sales" : row[1],
            "retail_sales" : row[2]
        }
        for row in result
    ]
    
@app.get("/api/item-type-sales")
def item_type_sales(
    year : Optional[int] = None,
    month : Optional[int] = None
    ):
    result = get_item_type_sales(year, month)
    
    return[
        {
            "item_type": row[0],
            "warehouse_sales" : row[1],
            "retail_sales" : row[2]
        }
        for row in result
    ]
    
@app.get("/api/top-suppliers")
def top_suppliers(
    year : Optional[int] = None,
    month : Optional[int] = None,
    item_type : Optional[str] = None,
    limit: int = 10
    ):
    result = get_top_suppliers(year, month, item_type, limit)
    return[
        {
            "supplier": row[0],
            "total_sales" : row[1]
        }
        for row in result
    ]