const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('./cors');

//const authenticate = require('../authenticate');

const Responses = require('../models/answers');
const Quizzes = require('../models/quiz');

const router = express.Router();

router.use(bodyParser.json());

router.route('/responses/:quizName/:username/:id')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req, res, next) => {
    var query = {};
    if (req.params.quizName != '-') {
        query.quizName = req.params.quizName;
    }
    if (req.params.username != '-') {
        query.username = req.params.username;
    }
    if (req.params.id != '-') {
        query._id = req.params.id;
    }
    Responses.find(query)
    //.populate('comments.author')
    .then((responses) => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(responses);
    }, (err) => next(err))
    .catch((err) => next(err));
});

router.route('/responses')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.post(cors.cors, (req, res, next) => {
    req.body.quizContent = JSON.parse(req.body.quizContent);
    req.body.score = parseFloat(req.body.score, 10);
    Responses.create(req.body)
    .then((response) => {
        console.log('Response Created ', response);
        res.sendStatus(200);
    }, (err) => next(err))
    .catch((err) => next(err));
})
.put(cors.cors, (req, res, next) => {
    req.body.response = JSON.parse(req.body.response);
    Responses.updateOne({ _id: req.body.response._id }, { $set: req.body.response })
    .then((response) => {
        console.log('Response Updated ', response);
        res.sendStatus(200);
    }, (err) => next(err))
    .catch((err) => next(err));
});
/*.delete(authenticate.verifyUser, authenticate.verifyAdmin, (req, res, next) => {
    Responses.remove({})
    .then((resp) => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(resp);
    }, (err) => next(err))
    .catch((err) => next(err));    
});*/

router.route('/quizzes/:quizName')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req, res, next) => {
    console.log(req.params.quizName);
    Quizzes.find({ quizName: req.params.quizName })
    //.populate('comments.author')
    .then((quiz) => {
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.json(quiz);
        console.log('Found quiz', quiz);
    }, (err) => next(err))
    .catch((err) => next(err));
});

router.route('/quizzes')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.post(cors.cors, (req, res, next) => {
    req.body.quiz = JSON.parse(req.body.quiz);
    Quizzes.create(req.body.quiz)
    .then((quiz) => {
        console.log('Quiz Created ', quiz);
        res.sendStatus(200);
    }, (err) => next(err))
    .catch((err) => next(err));
})
.put(cors.cors, (req, res, next) => {
    req.body.quiz = JSON.parse(req.body.quiz);
    Quizzes.updateOne({ quizName: req.body.quiz.quizName }, { $set: req.body.quiz })
    .then((quiz) => {
        console.log('Quiz Updated ', quiz);
        res.sendStatus(200);
    }, (err) => next(err))
    .catch((err) => next(err));
});

module.exports = router;