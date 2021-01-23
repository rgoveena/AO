import * as ActionTypes from './ActionTypes';
const baseUrl = "http://localhost:3001/";

/********************************************************************************************
**
** COMMUNICATES WITH NODE SERVER TO EXECUTE PYTHON SCRIPT WHICH CALLS PRE-WRITTEN QUERY TO DB
**
********************************************************************************************/

export const runPy = (path, link) => (dispatch) => {
	console.log("Fetching "+baseUrl + 'python/' + path + '/' + link+" from Node");
	return fetch(baseUrl + 'python/' + path + '/' + link)
	.then(response => {
			if (response.ok){
				return response;
			}
			else {
				var error = new Error('Error '+ response.status +': '+response.statusText);
				error.response = response;
				throw error;
			}
		},
		error => {
			var errmess = new Error(error.message);
			throw errmess;
		})
		.then(response => response.json())
		.then(result => dispatch(addQueryResult(result)))
		//.catch(error => dispatch(shirtsFailed(error.message)));*/
}


/********************************************************************************************
**
** STORES RESPONSE DATA FROM THE CUSTOM OR PRE-WRITTEN QUERY ON REACT SIDE
**
********************************************************************************************/


export const addQueryResult = (result) => ({
	type: ActionTypes.ADD_QUERYRESULT,
	payload: result
});

/********************************************************************************************
**
** COMMUNICATES WITH NODE SERVER TO CALL CUSTOM-MADE QUERY TO DB 
**
********************************************************************************************/

export const customQuery = (query, link) => (dispatch) => {
	console.log("Fetching "+baseUrl + 'custom/' + query + '/' + link+" from Node");
	return fetch(baseUrl + 'custom/' + query + '/' + link)
	/*return fetch(baseUrl + 'custom', {
		//mode: 'no-cors',
		method: 'POST',
		body: query,
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'same-origin'
	})*/
	.then(response => {
			if (response.ok){
				return response;
			}
			else {
				var error = new Error('Error '+ response.status +': '+response.statusText);
				error.response = response;
				throw error;
			}
		},
		error => {
			var errmess = new Error(error.message);
			throw errmess;
		})
	.then(response => response.json())
	.then(result => dispatch(addQueryResult(result)))
}

/********************************************************************************************
**
** COMMUNICATES WITH NODE SERVER TO MAKE AN API REQUEST TO THE SPECIFIED LINK
**
********************************************************************************************/

export const request = (method, link) => (dispatch) => {

	//console.log("Fetching "+baseUrl + 'connect/' + link+" from Node");

	return fetch(baseUrl + 'api/' + method + '/' + link + '/-')
	.then(response => {
			if (response.ok){
				return response;
			}
			else {
				var error = new Error('Error '+ response.status +': '+response.statusText);
				error.response = response;
				throw error;
			}
		},
		error => {
			var errmess = new Error(error.message);
			throw errmess;
		})
		.then(response => response.json())
		.then(result => dispatch(apiResponse(result)))
		//.catch(error => console.log(error.message)); 
}

/********************************************************************************************
**
** STORES RESPONSE DATA FROM THE API REQUEST ON REACT SIDE
**
********************************************************************************************/

export const apiResponse = (result) => ({
	type: ActionTypes.API_RESPONSE,
	payload: result
});

