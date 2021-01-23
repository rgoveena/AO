import React, { Component } from 'react';
import Quiz from './QuizComponent';
//import quizQuestions from '../QuizQuestions';
import Result from './ResultComponent';
import { name } from '../LoginComponent';

class SampleQuiz extends Component {
  constructor(props) {
    super(props);

    this.state = {
      counter: 0,
      questionId: 1,
      question: '',
      answerOptions: [],
      answer: '',
      accuracy: 0,
      result: 0.0,
      resultPage: 0,
      quizContent: []
    };

    this.handleAnswerSelected = this.handleAnswerSelected.bind(this);
  }

  componentDidMount() {
    const shuffledAnswerOptions = this.props.quiz[0].questions.map(question =>
      this.shuffleArray(question.answers)
    );
    this.setState({
      question: this.props.quiz[0].questions[0].question,
      answerOptions: shuffledAnswerOptions[0]
    });
    console.log(this.props.quiz[0].questions);
  }

  shuffleArray(array) {
    var currentIndex = array.length,
      temporaryValue,
      randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  handleAnswerSelected(event) {
    
    console.log(event.currentTarget);
    this.setUserAnswer(event.currentTarget.value, event.currentTarget.id);

    if (this.state.questionId < this.props.quiz[0].questions.length) {
      setTimeout(() => this.setNextQuestion(), 300);
    } else {
      setTimeout(() => this.getResults(), 300);
    }
  }

  setUserAnswer(correct, id) {
    console.log(id);
    if (correct === "true") {
      console.log("changing accuracy state")
      this.setState({accuracy: this.state.accuracy + 1});
    }
    console.log(this.state.accuracy);

    this.setState((state, props) => ({
      answer: id
    }));
  }

  setNextQuestion() {
    
    this.updateQuizContent();

    const counter = this.state.counter + 1;
    const questionId = this.state.questionId + 1;

    this.setState({
      counter: counter,
      questionId: questionId,
      question: this.props.quiz[0].questions[counter].question,
      answerOptions: this.props.quiz[0].questions[counter].answers,
      answer: ''
    });
  }

  getResults() {
    this.updateQuizContent();
    const accuracy = this.state.accuracy;
    const quizLength = this.props.quiz[0].questions.length;
    console.log(accuracy, quizLength, accuracy/quizLength);
    this.setState({ result: accuracy/quizLength,
                    resultPage: 1 });
  }

  updateQuizContent() {
    var correctAnswer = this.state.answerOptions.filter(function(answer) {
      return (answer.correct === true);
    })

    if (correctAnswer.length > 1) {
      for (var i=1; i<correctAnswer.length; i++){
        if (correctAnswer[i].content === this.state.answer){
          correctAnswer = correctAnswer[i];
          break;
        }
      }
      if (correctAnswer.length > 1) {
        correctAnswer = correctAnswer[0];
      }
    } else {
      correctAnswer = correctAnswer[0];
    }


    this.setState(state => {
      const quizContent = state.quizContent.concat({
        "correctAnswer": correctAnswer.content, 
        "selectedAnswer": this.state.answer,
        "question": this.state.question
      });
      return {quizContent};
    });
  }

  renderQuiz() {
    
    return (
      <Quiz
        answer={this.state.answer}
        answerOptions={this.state.answerOptions}
        questionId={this.state.questionId}
        question={this.state.question}
        questionTotal={this.props.quiz[0].questions.length}
        onAnswerSelected={this.handleAnswerSelected}/>
    );
  }

  sendResult() {
    const data = new FormData();
    data.append('username', {name}.name);
    data.append('quizName', this.props.quiz[0].quizName);
    data.append('quizId', this.props.quiz[0]._id);
    data.append('score', this.state.result);
    data.append('quizContent', JSON.stringify(this.state.quizContent));

    fetch('http://localhost:3001/responses', {
      method: 'POST',
      body: data
    })
  }

  renderResult() {
    //console.log(this.state.quizContent);
    this.sendResult()
    return <Result quizResult={ (Math.round(this.state.result*10000)/100) + "%" }
                   quizContent={this.state.quizContent} />;
  }

  render() {
    return (
      <div>
        {this.state.resultPage ? this.renderResult() : this.renderQuiz()}
      </div>
    );
  }
}

export default SampleQuiz;
