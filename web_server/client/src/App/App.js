import React, { Component } from 'react';
import './App.css';
import HouseForm from '../HouseForm/HouseForm';

class App extends Component {
  render() {
    return (
      <div>
        <div className='container'>
          <HouseForm />
        </div>
      </div>
    );
  }
}

export default App;
