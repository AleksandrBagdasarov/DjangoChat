import React from 'react'


export const ChatMessage = (text, owner) => {

    const chat_message = (text) => {
        return (
            <li className="chat-list_item">{text}<span>00:00</span></li>
        )
    }

    const owner_message = (text) => {
        return (
            <li className="chat-list_item owner">{text}<span>00:00</span></li>
        )
    }


    return (
        <>
            {owner? chat_message(text): owner_message(text)}
        </>
    )
}
