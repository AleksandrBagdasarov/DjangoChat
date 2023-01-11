import { createSlice } from "@reduxjs/toolkit";

const userSlice = createSlice(
    {
        name: "user",
        initialState: {
            refresh: "",
            access: "",
            loggedIn: false
        },
        reducers: {
            signUp(state, action) {
                state.access = action.payload.access
                state.refresh = action.payload.refresh
                state.loggedIn = true
            }
        }
    }
)

export const userActions = userSlice.actions;
export default userSlice;
