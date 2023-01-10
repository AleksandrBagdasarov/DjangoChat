import React from 'react';
import './App.css';
import { Home } from './pages/Home';
import { Sidebar } from './components/Sidebar';
import { ChatContent } from './components/ChatContent';

function App() {
  return (
    <div className="container">
      <div className='sidebar'>
        <Sidebar/>
      </div>
      <div className='content'>
        <ChatContent/>
      </div>
    </div>
  );
}

export default App;
