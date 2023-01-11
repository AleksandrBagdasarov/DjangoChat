import React from 'react'


export const Sidebar = () => {
  return (
    <>
      <div className="sidebar__item title">
        <h1 className='title-text'>Lets Code</h1>
      </div>

      <ul className="chats">

        <li className="chats__item"><p>chat 1</p></li>
        <li className="chats__item"><p>chat 2</p></li>
        <li className="chats__item"><p>chat 3</p></li>
        <li className="btn-add-chat"><button type='button' className='btn-add-chat'>+</button></li>
      </ul>



      <div className="sidebar__footer">
        <button type='button' className='btn-footer auth'> auth </button>
        <button type='button' className='btn-footer settings'>sett</button>
        <button type='button' className='btn-footer dashboard'>dash</button>
      </div>
    </>
  )
}
