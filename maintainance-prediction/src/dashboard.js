// src/dashboard.js
import React, { useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [inputData, setInputData] = useState({
    'Type': '',
    'Air temperature': '',
    'Process temperature': '',
    'Rotational speed': '',
    'Torque': '',
    'Tool wear': '',
  });

  const [predictions, setPredictions] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputData({ ...inputData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Data to be sent:", inputData);
      const response = await axios.post('http://localhost:5000/api/predict', inputData, {
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );
      setPredictions(response.data);
    } catch (error) {
      console.error('Error making prediction:', error);
    }
  };

  return (
    <div className="input-section">
      <h2>Enter Machine Parameters</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="type">Type:</label>
        <input type="text" id="type" name="Type" required value={inputData.Type} onChange={handleChange} />

        <label htmlFor="airTemp">Air Temperature:</label>
        <input type="number" id="airTemp" name="Air temperature" step="0.01" required value={inputData['Air temperature']} onChange={handleChange} />

        <label htmlFor="processTemp">Process Temperature:</label>
        <input type="number" id="processTemp" name="Process temperature" step="0.01" required value={inputData['Process temperature']} onChange={handleChange} />

        <label htmlFor="rotationalSpeed">Rotational Speed:</label>
        <input type="number" id="rotationalSpeed" name="Rotational speed" required value={inputData['Rotational speed']} onChange={handleChange} />

        <label htmlFor="torque">Torque:</label>
        <input type="number" id="torque" name="Torque" step="0.01" required value={inputData.Torque} onChange={handleChange} />

        <label htmlFor="toolWear">Tool Wear:</label>
        <input type="number" id="toolWear" name="Tool wear" required value={inputData['Tool wear']} onChange={handleChange} />

        <button type="submit">Predict</button>
      </form>

      {predictions && (
        <div className="output-section">
          <h2>Prediction Results</h2>
          <div id="results">
            <p><strong>Machine Failure:</strong> {predictions.machineFailure}</p>
            <p><strong>TWF:</strong> {predictions.TWF}</p>
            <p><strong>HDF:</strong> {predictions.HDF}</p>
            <p><strong>PWF:</strong> {predictions.PWF}</p>
            <p><strong>OSF:</strong> {predictions.OSF}</p>
            <p><strong>RNF:</strong> {predictions.RNF}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
