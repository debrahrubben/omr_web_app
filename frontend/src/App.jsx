// App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Scannable Sheet Marker</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      <div>
        <h2>Results</h2>
        <ul>
          {results.length > 0 ? (
            results.map((result, index) => (
              <li key={index}>
                Question {result.questionNumber}: {result.markedAnswer}
              </li>
            ))
          ) : (
            <li>No results yet</li>
          )}
        </ul>
      </div>
    </div>
  );
  
}

export default App;
