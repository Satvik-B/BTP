import { React } from 'react';
import './App.css';
import MainRouter from './routers/MainRouter';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <MainRouter />
        {/* Hi there */}
      </header>
    </div>
  );
}

export default App;
