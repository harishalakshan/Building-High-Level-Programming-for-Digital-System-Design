import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState({});
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get('/temperature', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      }).then(res => {
        setData(res.data);
        const now = new Date().toLocaleTimeString();
        setHistory(prev => [...prev.slice(-19), { time: now, ...res.data }]);
      }).catch(console.error);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>🌡️ Real-Time Temperature Monitor</h1>
      <p>Temperature: {data.temperature} °C</p>
      <p>Humidity: {data.humidity} %</p>
    </div>
  );
}

export default App;
