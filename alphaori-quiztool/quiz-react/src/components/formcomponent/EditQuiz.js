import React, { Component } from 'react'
import Styles from './Styles'
import { Field } from 'react-final-form'
import { Form as FinalForm } from 'react-final-form'
import arrayMutators from 'final-form-arrays'
import { FieldArray } from 'react-final-form-arrays'
import { Col, Row, Button } from 'reactstrap';
import { Form, Control } from 'react-redux-form';

class EditQuiz extends Component {

  constructor(props) {
    super(props)
    this.state = {
      quiz: []
    };
  }

  sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

  onSubmit = async values => {
      await this.sleep(300)
      
      const data = new FormData();
      data.append('quiz', JSON.stringify(values));

      fetch('http://localhost:3001/quizzes', {
        method: 'PUT',
        body: data
      }).then((res) => this.giveAlert(res.status));

      this.setState({
        quiz: []
      });
  }

  giveAlert = (statusCode) => {
    if (statusCode===200 || statusCode === 304) {
      alert("Quiz successfully updated!");
    } else {
      alert("Server not responding!")
    }
  }

  MyForm = () => (
    <Styles>
      <FinalForm
        onSubmit={this.onSubmit}
        mutators={{
          ...arrayMutators
        }}
        initialValues={this.state.quiz[0]}
        render={({
          handleSubmit,
          form: {
            mutators: { push, pop }
          }, // injected from final-form-arrays above
          pristine,
          form,
          submitting,
          values
        }) => {
          return (
            <form onSubmit={handleSubmit}>
              <div className="md">
                <label>Quiz Name</label>
                <Field name="quizName" component="input" />
                <div className="buttons">
                  <button
                    type="button"
                    onClick={() => push('questions', undefined)}>
                    Add Question
                  </button>
                </div>
              </div>
              <FieldArray name="questions">
                {({ fields }) =>
                  fields.map((name, i) => (
                  <div>
                    <div key={name}>
                    <br/>
                      <Field
                        name={`${name}.question`}
                        component="input"
                        placeholder="Question"
                        style={{ width: "350px" }}/>
                      <span
                        onClick={() => fields.remove(i)}
                        style={{ cursor: 'pointer' }}>
                        ❌
                      </span>
                      <div className="buttons" >
                        <button
                          type="button"
                          onClick={() => push(`${name}.answers`, undefined)}
                          style={{ margin: 0 }}>
                          Add Answer 
                        </button>
                      </div>
                    </div>
                    <div>
                        <br/>
                        <FieldArray name={`${name}.answers`}>
                          {({ fields }) =>
                            fields.map((name2, i) => (
                              <div key={name2}>
                                <label>Answer {i + 1}</label>
                                <Field
                                  name={`${name2}.content`}
                                  component="input"
                                  placeholder="Answer"/>
                                <Field
                                  name={`${name2}.correct`}
                                  component="input"
                                  placeholder="Correct (true/false)"/>
                                <span
                                  onClick={() => fields.remove(i)}
                                  style={{ cursor: 'pointer' }}>
                                  ❌
                                </span>
                              </div>
                            ))
                          }
                        </FieldArray>
                    </div>
                  </div>
                  ))
                }
              </FieldArray>
              
              <div className="buttons">
                <button type="submit" disabled={submitting || pristine}>
                  Update
                </button>
                <button
                  type="button"
                  onClick={form.reset}
                  disabled={submitting || pristine}>
                  Reset
                </button>
              </div>
              <pre>{JSON.stringify(values, 0, 2)}</pre>
            </form>
          )
        }}/>
    </Styles>
  )

  getQuiz = (values) => {
    fetch('http://localhost:3001/quizzes/'+values.quizName)
    .then((response) => {
      response.json().then(data => ({
        quiz: data,
      }) //only necessary if directly fetching like this
      ).then(res => {
        console.log(res.quiz);
        this.setState({
          quiz: res.quiz
        });
      });
    });

    this.props.resetQuiz();
  }

  renderForm = () => {
    if (this.state.quiz.length > 0) {
      return (this.MyForm());
    }
  }

  render(){
    return(
      <div>
        <br/><br/><br/>
        <Form model="findquiz" onSubmit={(values) => this.getQuiz(values)}>
          <Row>
            <Col md={{ size: 3, offset: 4 }}>
              <Control.text model=".quizName" id="quizName" name="quizName"
                  placeholder="Name of Quiz to be Updated"
                  className="form-control" />
            </Col>
            <Col>
              <Button type="submit" color="dark" style={{ width: "150px" }}>
                  Find Quiz
              </Button>
            </Col>
          </Row>
        </Form>
        <br/><br/>
        {this.renderForm()}
      </div>
    );
  }
}

export default EditQuiz;