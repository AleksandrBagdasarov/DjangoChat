import React from 'react'
import { Link } from 'react-router-dom'
import { userActions } from '../store/user'
import {useDispatch, useSelector} from "react-redux";
import axios from 'axios'
import env from "../Env";
import { Navigate } from "react-router-dom";


export const SignUp = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user);

  const signin = (e) => {
    e.preventDefault();
    const username = e.target.username.value
    const password = e.target.password.value

    axios(
      {
        method: 'post',
        url: env.baseUrl + '/auth/signup',
        data: {
          username: username,
          password: password
        }
      }
    ).then(
      r => {
          dispatch(userActions.signUp({
            access: r.data.access,
            refresh: r.data.refresh
          }))
          console.log("signUp sucess!")
      }
    ).catch(
      err => console.log(err)
    )

  }

  return (
    <div>
      {user.loggedIn && (<Navigate to="/" replace={true} />)}
      <form onSubmit={signin}>
        <input name="username" placeholder="username" type="text"/>
        <input name="password" placeholder="password" type="password"/>
        <button type="submit">Sign Up</button>
        <Link to={'/sign-in'}>Sign In</Link>
      </form>
    </div>
  )
}
