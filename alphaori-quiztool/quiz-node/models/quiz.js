const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const answerSchema = new Schema({
    content: {
        type: String,
        required: true
    },
    correct: {
        type: Boolean,
        required: true
    }
});

const questionSchema = new Schema({
    question: {
        type: String,
        required: true
    },
    answers: [answerSchema]
});

const quizSchema = new Schema({
    quizName: {
        type: String,
        required: true,
        unique: true
    },
    /*quizId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Quiz'
    },*/
    questions: [questionSchema]
},{
    timestamps: true
});



var Quizzes = mongoose.model('Quiz', quizSchema);

module.exports = Quizzes;