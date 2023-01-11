import env from '../Env';
import React, { useState, useCallback, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";


export const ChatContent = () => {
  const [messageHistory, setMessageHistory] = useState([]);
  let client = new W3CWebSocket('ws://127.0.0.1:8000/ws/chat/1/');
  useEffect(() => {
    client.onopen = () => console.log("Connected!")
    client.onmessage = (message) => {
        const msg = JSON.parse(message.data);
        console.log("msg", msg)
      }
    }
  )


  const handleSendMessage = (e) => {
    e.preventDefault();
    const message = e.target.newMassage.value;
    console.log('input', message);
    client.send(JSON.stringify({
      type: 'message',
      message: message,
    }))
  }

  return (
    <>
    <div className='chat'>

      <ul className="chat-list">
        <li className="chat-list_item">smmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmms<span>00:00</span></li>
        <li className="chat-list_item owner">smmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmms<span>00:00</span></li>
        <li className="chat-list_item">sms<span>00:00</span></li>
      </ul>

      <form className='input-form' onSubmit={handleSendMessage}>
        <textarea className='owner-input'  placeholder='message ...' name="newMassage" id="new-massage" cols="3" rows="3"></textarea>
        <button className='btn-submit' type='submit'>SEND</button>
      </form>

    </div>
    </>
  )

}
