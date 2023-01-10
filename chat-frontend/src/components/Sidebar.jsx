import React from 'react'

export const Sidebar = () => {
  return (
    <div className='sidebar-items'>
      <div className="side-item brand">
        <h2>Lets Code</h2>
      </div>
      <div className="side-item ">
        <div>Sign Up</div>
        <div>Sign In</div>
      </div>
      <div className="side-item">
        <h4>Chat List</h4>
        <div>Chat 1</div>
        <div>Chat 2</div>
        <div>Chat 3</div>
        <button>Add +</button>
      </div>
      <div className="side-item">
        <h4>Dashboard</h4>
        <div>dashboard 1</div>
        <div>dashboard 2</div>
        <div>dashboard 3</div>
      </div>
      <div className="side-item">
        <h4>Settings</h4>

      </div>
    </div>
  )
}
