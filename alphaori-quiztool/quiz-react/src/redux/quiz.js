import * as ActionTypes from './ActionTypes';

export const Quiz = (state = {
		quiz1: [],
		quiz2: [],
		quiz3: []
	}, action) => {
	switch(action.type) {

		case ActionTypes.ADD_QUIZ1:
			return {...state, quiz1: action.payload};

		case ActionTypes.ADD_QUIZ2:
			return {...state, quiz2: action.payload};

		case ActionTypes.ADD_QUIZ3:
			return {...state, quiz3: action.payload};

		default: 
			return state;
	}
}