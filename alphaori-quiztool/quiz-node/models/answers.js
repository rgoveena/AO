const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const contentSchema = new Schema({
    question: {
        type: String,
        required: true
    },
    selectedAnswer: {
        type: String,
        required: true
    },
    correctAnswer: {
        type: String,
        required: true
    }
});

const quizResponseSchema = new Schema({
    username: {
        type: String,
        required: true
    }, //when later developed this should refer to the actual user id in mongo
    quizName: {
        type: String,
        required: true
    },
    quizId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Quiz'
    },
    score: {
        type: Number,
        required: true
    },
    quizContent: [contentSchema]
},{
    timestamps: true
});



var Responses = mongoose.model('Response', quizResponseSchema);

module.exports = Responses;