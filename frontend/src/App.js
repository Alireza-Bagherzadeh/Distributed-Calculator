import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  // اشاره به دامین جداگانه بک‌ند
  const API_URL = "/parse";
  const HISTORY_URL = "/history";
  const fetchHistory = async () => {
    try {
      const response = await axios.get(HISTORY_URL);
      setHistory(response.data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };
  useEffect(() => {
    fetchHistory();
  }, []);
  const handleCalculate = async () => {
    try {
      const response = await axios.post(API_URL, { expression });
      setResult(response.data);
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "Arial" }}>
      <h1>☁️ Distributed Calculator</h1>
      <input
        value={expression}
        onChange={e => setExpression(e.target.value)}
        placeholder="(10+20)*3"
                style={{ padding: "10px", fontSize: "16px" }}
      />
      <button onClick={handleCalculate} style={{ padding: "10px", marginLeft: "10px" }}>Calculate</button>

      {result && (
        <div style={{ marginTop: "20px", padding: "20px", border: "1px solid #ccc", display: "inline-block" }}>
          <h2>Result: {result.final_result}</h2>
          <p>Logic Flow: {result.flow}</p>
          <p>DB Saved: {result.db_saved ? "✅" : "❌"}</p>
        </div>
      )}
      <div style={{ marginTop: "30px" }}>
        <h3>📜 Calculation History</h3>
        {history.length === 0 ? (
          <p>No records found yet.</p>
        ) : (
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {history.map((item, index) => (
              <li key={index} style={{ background: "#f9f9f9", margin: "5px auto", padding: "10px", width: "300px", borderRadius: "5px", border: "1px solid >
                <strong>{item.expression}</strong> = {item.result}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
export default App;