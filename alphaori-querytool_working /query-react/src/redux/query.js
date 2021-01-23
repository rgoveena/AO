import * as ActionTypes from './ActionTypes';

export const QueryResult = (state = {
		result: []
	}, action) => {
	switch(action.type) {
		case ActionTypes.ADD_QUERYRESULT:
			return {...state, result: action.payload};

		default: 
			return state;
	}
}