import React from 'react';
import './App.css';
import elviraImage from './images/elvira.png'; // Mettez à jour le chemin d'importation

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={elviraImage} className="Elvira-logo" alt="logo" />
        <p>
          Bienvenue sur mon application React.
        </p>
      </header>
    </div>
  );
}

export default App;
