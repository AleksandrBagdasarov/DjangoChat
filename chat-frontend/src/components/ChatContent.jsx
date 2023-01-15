import env from '../Env';
import React, { useState, useCallback, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import {useDispatch, useSelector} from "react-redux";
import { userActions } from '../store/user';
// import { ChatMessage } from './ChatMessage';
import axios from 'axios';



export const ChatContent = () => {
  let user = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState("");

  let client = new W3CWebSocket('ws://@127.0.0.1:8000/ws/chat/1/?access=' + user.access);

  useEffect(() => {
    client.onopen = () => console.log("Connected!");
    client.onmessage = (message) => {
        const msg = JSON.parse(message.data);
        console.log("received", msg)
        console.log((msg.message), msg.message)
        if (msg.message) {
          dispatch(userActions.pushMessage(msg.message));
          setMessages([user.messages, msg.message]);
        }
      }
    loadMessages();
    setMessages(user.messages);
    },
    []
  )

  const loadMessages = () => {
    axios(
      {
        method: 'get',
        url: env.baseUrl + '/chat/messages?chat_id=1',
        headers: {
          'Authorization': 'Bearer ' + user.access
        }
      }
    ).then(
      r => {
          dispatch(userActions.setMessages(r.data))
          setMessages(r.data)
        }
    ).catch(
      err => console.log(err)
    );
  }
  console.log(user.messages);




  const handleSendMessage = (e) => {
    e.preventDefault();
    console.log('input', messageText);
    client.send(JSON.stringify({
        type: 'scheduled_message',
        execute_at: '2023-01-15 21:47:21.080100',
        message: messageText,
    }))
    setMessageText("");
  }

  return (
    <>
    <div className='chat'>

      <ul className="chat-list">
        {messages.map((msg) => {
            return (
                <li className={"chat-list_item" + (msg.owner ? ' owner': '')}>{msg.text}<span>00:00</span></li>
              )
        })}
      </ul>

      <form className='input-form'>
        <textarea className='owner-input' onChange={(e) => setMessageText(e.target.value)} value={messageText} placeholder='message ...' name="newMassage" id="new-massage" cols="3" rows="3"></textarea>
        <button className='btn-submit' onClick={handleSendMessage} type='button'>SEND</button>
      </form>

    </div>
    </>
  )

}
