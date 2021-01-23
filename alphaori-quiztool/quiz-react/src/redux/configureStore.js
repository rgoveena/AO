import { createForms } from 'react-redux-form';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { loginInfo, responseInfo, quizInfo, editResponse } from './forms';
import { Quiz } from './quiz';


export const ConfigureStore = () => {
	const store = createStore(
		combineReducers({
			quiz: Quiz,
			...createForms({
				login: loginInfo,
				response: responseInfo,
				findquiz: quizInfo,
				findresponse: editResponse
			})
		}),
		applyMiddleware(thunk, logger)
	);

	return store;
}