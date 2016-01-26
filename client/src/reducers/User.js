import { handleActions } from "redux-actions";
import { types } from "../actions/User";
import API from "../API";

export default handleActions({
    [types.USER_LOGIN]: (state, action) => {
        const user = action.payload;
        return {
            ...user, 
            api: new API(user.key)
        }
    },

    [types.USER_MODULES]: (state, action) => {
        const { modules } = action.payload;
        return {...state, modules }
    }
}, null);