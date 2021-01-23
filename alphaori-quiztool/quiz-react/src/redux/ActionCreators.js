import * as ActionTypes from './ActionTypes';
const baseUrl = 'http://localhost:3001/';

export const fetchQuiz = (quizName, quizSlot) => (dispatch) => {

	const func = (quizslot, quiz) => {
		if (quizslot === "quiz1") {
			return addQuiz1(quiz);
		} else if (quizslot === "quiz2") {
			return addQuiz2(quiz);
		} else if (quizslot === "quiz3") {
			return addQuiz3(quiz);
		}
	}

	return fetch(baseUrl + 'quizzes/' + quizName)
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
		.then(quiz => dispatch(func(quizSlot, quiz)));
}

export const addQuiz1 = (quiz) => ({
	type: ActionTypes.ADD_QUIZ1,
	payload: quiz
});

export const addQuiz2 = (quiz) => ({
	type: ActionTypes.ADD_QUIZ2,
	payload: quiz
});

export const addQuiz3 = (quiz) => ({
	type: ActionTypes.ADD_QUIZ3,
	payload: quiz
});