import React from 'react';
import PropTypes from 'prop-types';
import { CSSTransitionGroup } from 'react-transition-group';

function Result(props) {

  function renderQuizSummary(){
    return (
      props.quizContent.map(function(set){
        return (
          <div className="col-md-10">
            <br/>
            <div>
              Question: {set.question}
            </div>
            <div>
              Selected Answer: {set.selectedAnswer}
            </div>
            <div>
              Correct Answer: {set.correctAnswer}
            </div>
          </div>
        );
      })   
    )
  }

  return (
    <CSSTransitionGroup
      className="quiz result"
      component="div"
      transitionName="fade"
      transitionEnterTimeout={800}
      transitionLeaveTimeout={500}
      transitionAppear
      transitionAppearTimeout={500}>
      <div>
        You scored <strong>{props.quizResult}</strong>!
      </div>
      <br/>
      <div>
        <strong> Quiz Summary: </strong> {renderQuizSummary()}
      </div>
    </CSSTransitionGroup>
  );
}

Result.propTypes = {
  quizResult: PropTypes.string.isRequired,
  quizContent: PropTypes.array.isRequired
};

export default Result;
