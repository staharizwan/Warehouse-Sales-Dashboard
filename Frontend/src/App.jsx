import { useEffect, useState } from "react";
import "./App.css";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts"

function App() {
  const [kpis, setKpis] = useState(null);
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [itemType, setItemType] = useState("");
  const [yearlySales, setYearlySales] = useState([])

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

    const url =
      `http://127.0.0.1:8000/api/sales-trend?${params.toString()}`;

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })
      .then((data) => {
        console.log("Sales trend data:", data);
        setYearlySales(data);
      })
      .catch((error) => {
        console.error("Sales trend fetch failed:", error);
        setYearlySales([]);
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
      <div className="data-note">
        <strong>Data note:</strong> Sales and transfers are reported in cases.
        Fractional values represent partial cases based on the product's case
        configuration; the source does not provide item-level case-size conversions.
      </div>
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

     <div>
       <div className="chart-card">

          <h2>
            {year
              ? `Monthly Sales Volume — ${year}`
              : "Sales Volume by Year"}
          </h2>

          {yearlySales.length > 0 ? (

            <ResponsiveContainer width="100%" height={350}>

              <LineChart data={yearlySales}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="period"
                  tickFormatter={(value) => {
                    if (year) {
                      const months = [
                        "Jan", "Feb", "Mar", "Apr",
                        "May", "Jun", "Jul", "Aug",
                        "Sep", "Oct", "Nov", "Dec"
                      ];

                      return months[value - 1];
                    }

                    return value;
                  }}
                />

                <YAxis
                  tickFormatter={(value) => {
                    if (Math.abs(value) >= 1000000) {
                      return `${(value / 1000000).toFixed(1)}M`;
                    }

                    if (Math.abs(value) >= 1000) {
                      return `${(value / 1000).toFixed(0)}K`;
                    }

                    return value;
                  }}
                />

                <Tooltip
                    contentStyle={{
                    backgroundColor: "#1e293b",
                    border: "1px solid #475569",
                    borderRadius: "8px",
                    color: "#f8fafc",
                  }}
                  labelStyle={{
                    color: "#f8fafc",
                    fontWeight: "600",
                  }}
                  itemStyle={{
                    color: "#e2e8f0",
                  }}
                  formatter={(value) =>
                    `${Number(value).toLocaleString("en-US", {
                      maximumFractionDigits: 2,
                    })} cases`
                  }
                />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="warehouse_sales"
                  name="Warehouse Sales"
                  stroke="#38bdf8"
                  strokeWidth={3}
                />

                <Line
                  type="monotone"
                  dataKey="retail_sales"
                  name="Retail Sales"
                  stroke="#14b8a6"
                  strokeWidth={3}
                />

              </LineChart>

            </ResponsiveContainer>

          ) : (

            <p>No sales data available for the selected filters.</p>

          )}

        </div>

     </div>
    

    </div>
  );
}

export default App;