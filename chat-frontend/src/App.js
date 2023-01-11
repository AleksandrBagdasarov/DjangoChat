import React from 'react';
import './App.css';
import { Home } from './pages/Home';
import { Sidebar } from './components/Sidebar';
import { ChatContent } from './components/ChatContent';
import useWebSocket from 'react-use-websocket';
import env from './Env';


function App() {
  // useWebSocket(env.socketUrl + 'some/', {
  //   onOpen: () => {
  //     console.log('WebSocket connection established.');
  //   }
  // });

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
