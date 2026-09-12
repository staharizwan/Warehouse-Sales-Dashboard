# Warehouse & Retail Sales Dashboard

A full-stack data analytics dashboard for exploring warehouse and retail sales data through interactive filters and visualizations.

The project demonstrates an end-to-end analytics workflow, from raw CSV data and SQL-based aggregation to a FastAPI REST API and an interactive React dashboard.

## Live Demo

https://warehouse-sales-dashboard-blond.vercel.app/

## Project Overview

The dashboard analyzes warehouse and retail sales data from Montgomery County, Maryland. Users can explore sales volumes by year, month, item type, and supplier.

The application provides:

- Warehouse sales, retail sales, and retail transfer KPIs
- Sales trends by year or month
- Sales comparison across item types
- Top suppliers by combined warehouse and retail sales volume
- Interactive filtering by year, month, and item type
- Responsive data visualizations

Sales and transfers are reported in cases rather than monetary values.

## Architecture

```
Raw CSV Dataset
      |
      v
Python / Pandas ETL
      |
      v
SQLite Database
      |
      v
SQL Analytics Queries
      |
      v
FastAPI REST API
      |
      v
React Frontend
      |
      v
Recharts Visualizations
      |
      v
Vercel Deployment
```

The frontend communicates with the backend through HTTP requests to REST API endpoints. FastAPI receives the selected filter parameters, executes parameterized SQL queries against SQLite, and returns the results as JSON. React then updates the dashboard visualizations with the returned data.

## Technology Stack

### Data & Backend

- Python
- Pandas
- SQLite
- SQL
- FastAPI
- Uvicorn

### Frontend

- React
- Vite
- JavaScript
- Recharts
- CSS

### Deployment & Version Control

- Vercel
- Git
- GitHub

## Dataset

The project uses the **Warehouse and Retail Sales** dataset containing approximately 307,000 records covering 2017–2020.

The dataset includes:

- Year
- Month
- Supplier
- Item code
- Item description
- Item type
- Retail sales
- Retail transfers
- Warehouse sales

Sales and transfer quantities are reported in **cases**.

The original dataset is provided by Montgomery County, Maryland and contains sales and movement data by item and department.

Dataset source:

- Montgomery County Open Data — Warehouse and Retail Sales
- Kaggle — Warehouse and Retail Sales

### Data Notes

Fractional quantities represent partial cases based on the product's case configuration. The source does not provide item-level case-size conversions.

Negative values are retained as reported in the source data and treated as adjustments to net sales volumes; they may represent returns, reversals, credits, or other corrections.

Missing periods are not automatically interpreted as zero sales. If a month is absent from the source data, the dashboard does not artificially create a zero-value observation.

## ETL Pipeline

The raw CSV dataset is processed using Pandas before being loaded into SQLite.

The ETL process:

1. Reads the raw CSV dataset
2. Standardizes column names to lowercase snake_case
3. Inspects missing values and duplicate records
4. Preserves the source sales values
5. Loads the processed dataset into a SQLite `sales` table

Example transformation:

```text
WAREHOUSE SALES → warehouse_sales
ITEM TYPE       → item_type
ITEM CODE       → item_code
```

## API

The FastAPI backend exposes REST endpoints used by the React frontend.

### KPI Summary

```http
GET /api/kpis
```

Optional query parameters:

```text
year
month
item_type
```

### Sales Trend

```http
GET /api/sales-trend
```

Returns annual sales when no year is selected and monthly sales when a specific year is selected.

### Sales by Item Type

```http
GET /api/item-type-sales
```

Aggregates warehouse and retail sales by product category.

### Top Suppliers

```http
GET /api/top-suppliers
```

Optional parameters include:

```text
year
month
item_type
limit
```

Suppliers are ranked using combined warehouse and retail sales volume.

## Dynamic SQL Filtering

Dashboard filters are translated into parameterized SQL conditions.

For example, selecting:

```text
Year: 2019
Item Type: WINE
```

produces logic equivalent to:

```sql
WHERE year = ?
AND item_type = ?
```

with the values passed separately as query parameters.

This approach keeps the query logic reusable while avoiding direct insertion of user-selected values into SQL statements.

## Dashboard Features

### KPI Cards

Displays total:

- Warehouse sales
- Retail sales
- Retail transfers

### Sales Trend

The trend visualization changes its aggregation level depending on the selected filters:

- No year selected → sales by year
- Specific year selected → sales by month

### Sales by Item Type

Compares warehouse and retail sales across product categories.

### Top Suppliers

Ranks suppliers according to:

```text
Warehouse Sales + Retail Sales
```

The query uses `COALESCE` so missing sales values do not remove an otherwise valid row from the aggregation.

## Project Structure

```text
DashboardProject/
|
├── api/
│   └── index.py
|
├── Backend/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   └── queries.py
|
├── Data/
│   └── Warehouse_and_Retail_Sales.csv
|
├── db/
│   └── warehouse_sales.db
|
├── Frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── package-lock.json
|
├── scripts/
│   └── load_data.py
|
├── requirements.txt
├── .gitignore
└── README.md
```

## Running Locally

### Backend

Create and activate a Python virtual environment and install the required packages.

Then run the FastAPI application from the project root:

```bash
python -m uvicorn Backend.app:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

From the `Frontend` directory:

```bash
npm install
npm run dev
```

The development frontend will normally be available at:

```text
http://localhost:5173
```

## Deployment

The application is deployed on Vercel.

The React frontend and FastAPI backend are served from the same deployment. Frontend requests use relative API paths such as:

```text
/api/kpis
/api/sales-trend
/api/item-type-sales
/api/top-suppliers
```

The SQLite database is bundled with the application and used as a read-only analytical data source for this portfolio project.

## What This Project Demonstrates

This project demonstrates practical experience with:

- Data cleaning and transformation with Pandas
- Relational data storage with SQLite
- SQL aggregation, grouping, filtering, and parameterized queries
- REST API development with FastAPI
- JSON-based frontend/backend communication
- React state management and asynchronous API requests
- Interactive visualization with Recharts
- Full-stack application deployment
- Git/GitHub version control