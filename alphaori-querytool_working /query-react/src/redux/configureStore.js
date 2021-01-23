import { createForms } from 'react-redux-form';
import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import { queryInfo, loginInfo, dbInfo, requestInfo } from './forms';
import { QueryResult } from './query';


export const ConfigureStore = () => {
	const store = createStore(
		combineReducers({
			queryResult: QueryResult,
			...createForms({
				query: queryInfo,
				login: loginInfo,
				db: dbInfo,
				request: requestInfo
			})
		}),
		applyMiddleware(thunk, logger)
	);

	return store;
}