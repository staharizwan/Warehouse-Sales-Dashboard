import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/kpis")
      .then((response) => response.json())
      .then((data) => {
        setKpis(data);
      });
  }, []);

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
        Sales and distribution performance overview
      </p>

      {kpis ? (
        <div className="kpi-container">

          <div className="kpi-card">
            <h3>Warehouse Sales</h3>
            <p>{formatNumber(kpis.total_warehouse_sales)}</p>
          </div>

          <div className="kpi-card">
            <h3>Retail Sales</h3>
            <p>{formatNumber(kpis.total_retail_sales)}</p>
          </div>

          <div className="kpi-card">
            <h3>Retail Transfers</h3>
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