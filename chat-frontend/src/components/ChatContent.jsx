import React from 'react'

export const ChatContent = () => {
  return (
    <> 
    <div className='chat'>

      <ul className="chat-list">
        <li className="chat-list_item">smmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmms<span>00:00</span></li>
        <li className="chat-list_item owner">smmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmms<span>00:00</span></li>
        <li className="chat-list_item">sms<span>00:00</span></li>
      </ul>
    
      <form className='input-form'>
        <textarea className='owner-input'  placeholder='message ...' name="new-massage" id="new-massage" cols="3" rows="3"></textarea> 
        <button className='btn-submit' type='submit'>SEND</button>
      </form>

    </div>
    </>
  )

}
