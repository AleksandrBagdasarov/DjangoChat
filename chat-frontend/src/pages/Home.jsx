import React from 'react'
import { Sidebar } from '../components/Sidebar'
import { ChatList } from '../components/ChatList'
import { ChatContent } from '../components/ChatContent'
import { Footer } from '../components/Footer'

export const Home = () => {
  return (
    <div>
        <div className="sidebar">
          <Sidebar/>
        </div>
        <div className="content">
          <ChatContent/>
        </div>
      </div>
  )
}
