import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice(
    {
        name: "user",
        initialState: {
            refresh: "",
            access: "",
            loggedIn: false,
            chats: []
        },
        reducers: {
            signUp(state, action) {
                state.access = action.payload.access
                state.refresh = action.payload.refresh
                state.loggedIn = true
            },
            logOut(state) {
                state.access = ""
                state.refresh = ""
                state.loggedIn = false
                state.chats = []
            },
            setChats(state, action) {
                state.chats = action.payload
                // todo add unique by id
            },
            addChat(state, action) {
                state.chats.push(action.payload)
            },
            removeChat(state, action) {
                console.log("Not Implemented!")
            }
        }
    }
)

export const userActions = userSlice.actions;
export default userSlice;
