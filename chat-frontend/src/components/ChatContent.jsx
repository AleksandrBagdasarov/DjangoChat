import React from 'react'

export const ChatContent = () => {
  return (
    <div className='chat'>
      <div className='message'>ChatContent 1</div>
      <div className='message'>ChatContent 2</div>
      <div className='message owner'>ChatContent 3</div>
      <div className='chat-input'>
        <input placeholder='message ...'/>
        <button className='chat-send'>Send!</button>

      </div>
    </div>
  )

}
