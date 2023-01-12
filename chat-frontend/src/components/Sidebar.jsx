import React from 'react'
import env from '../Env'
import axios from 'axios'
import { Link } from 'react-router-dom'
import {useDispatch, useSelector} from "react-redux";
import { userActions } from '../store/user'


export const Sidebar = () => {
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const setLogout = () => {
    dispatch(userActions.logOut())
  }


  const auth = (
    <Link to={"/signup"} type='button' className='btn-footer auth'>auth</Link>
  )
  const logount = (
    <button onClick={setLogout} type='button' className='btn-footer auth'>logout</button>
  )

  return (
    <>
      <div className="sidebar__item title">
        <h1 className='title-text'>Lets Code</h1>
      </div>

      <ul className="chats">

        <li className="chats__item"><p>{"(Anonymous)"}</p></li>
        <li className="chats__item"><p>chat 2</p></li>
        <li className="chats__item"><p>chat 3</p></li>
        <li className="btn-add-chat"><button type='button' className='btn-add-chat'>+</button></li>
      </ul>



      <div className="sidebar__footer">
        {user.loggedIn ? logount: auth}

        <button type='button' className='btn-footer settings'>sett</button>
        <button type='button' className='btn-footer dashboard'>dash</button>
      </div>
    </>
  )
}
