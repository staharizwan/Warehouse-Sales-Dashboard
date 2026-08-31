import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [kpis, setKpis] = useState(null);
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [itemType, setItemType] = useState("");


useEffect(() => {
    const params = new URLSearchParams();

    if (year) {
      params.append("year", year);
    }

    if (month) {
      params.append("month", month);
    }

    if (itemType) {
      params.append("item_type", itemType);
    }

    const url = `http://127.0.0.1:8000/api/kpis?${params.toString()}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setKpis(data);
      });

    }, [year, month, itemType]);

  const formatNumber = (value) => {
    return Number(value).toLocaleString("en-US", {
      maximumFractionDigits: 2,
    });
  };

  return (
    <div className="dashboard">
      <h1>Warehouse & Retail Sales Dashboard</h1>
      <p className="subtitle">
        <br></br>
        Sales and Distribution Performance Overview
      </p>

      <div className="filter-section">

        <div className="filters">

          <label>
            Year
            <select
              value={year}
              onChange={(e) => setYear(e.target.value)}
            >
              <option value="">All Years</option>
              <option value="2017">2017</option>
              <option value="2018">2018</option>
              <option value="2019">2019</option>
              <option value="2020">2020</option>
            </select>
          </label>

          <label>
            Month
            <select
              value={month}
              onChange={(e) => setMonth(e.target.value)}
            >
              <option value="">All Months</option>
              <option value="1">January</option>
              <option value="2">February</option>
              <option value="3">March</option>
              <option value="4">April</option>
              <option value="5">May</option>
              <option value="6">June</option>
              <option value="7">July</option>
              <option value="8">August</option>
              <option value="9">September</option>
              <option value="10">October</option>
              <option value="11">November</option>
              <option value="12">December</option>
            </select>
          </label>

          <label>
            Item Type
            <select
              value={itemType}
              onChange={(e) => setItemType(e.target.value)}
            >
              <option value="">All Item Types</option>
              <option value="BEER">Beer</option>
              <option value="WINE">Wine</option>
              <option value="LIQUOR">Liquor</option>
              <option value="KEGS">Kegs</option>
              <option value="NON-ALCOHOL">Non-Alcohol</option>
              <option value="STR_SUPPLIES">Store Supplies</option>
              <option value="REF">REF</option>
              <option value="DUNNAGE">Dunnage</option>
            </select>
          </label>

        </div>

        <button
          className="reset-button"
          onClick={() => {
            setYear("");
            setMonth("");
            setItemType("");
          }}
        >
          Reset Filters
        </button>

      </div>
      <br />
    
      {kpis ? (
        
        <div className="kpi-container">

          <div className="kpi-card">
            <h3>Cases: Warehouse Sales</h3>
            <p>{formatNumber(kpis.total_warehouse_sales)}</p>
          </div>

          <div className="kpi-card">
            <h3>Cases: Retail Sales</h3>
            <p>{formatNumber(kpis.total_retail_sales)}</p>
          </div>

          <div className="kpi-card">
            <h3>Cases: Retail Transfers</h3>
            <p>{formatNumber(kpis.total_retail_transfers)}</p>
          </div>

        </div>
      ) : (
        <p>Loading dashboard...</p>
      )}
    </div>
  );
}

export default App;