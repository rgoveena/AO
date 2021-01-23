import React, { Component } from 'react'
import Styles from './Styles'
import { Field } from 'react-final-form'
import { Form as FinalForm } from 'react-final-form'
import arrayMutators from 'final-form-arrays'
import { FieldArray } from 'react-final-form-arrays'
import { Col, Row, Button } from 'reactstrap';
import { Form, Control } from 'react-redux-form';

class EditResponse extends Component {

  constructor(props) {
    super(props)
    this.state = {
      response: []
    };
  }

  sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

  onSubmit = async values => {
      await this.sleep(300)
      
      const data = new FormData();
      data.append('response', JSON.stringify(values));

      fetch('http://localhost:3001/responses', {
        method: 'PUT',
        body: data
      }).then((res) => this.giveAlert(res.status));

      this.setState({
        response: []
      });
  }

  giveAlert = (statusCode) => {
    if (statusCode===200 || statusCode === 304) {
      alert("Response successfully updated!");
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
        initialValues={this.state.response[0]}
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
                <div></div>
                <label>Quiz Score</label>
                <Field name="score" component="input" />
              </div>
              <FieldArray name="quizContent">
                {({ fields }) =>
                  fields.map((name, i) => (
                  <div>
                    <div key={name}>
                    <br/>
                      <Field
                        name={`${name}.question`}
                        component="input"
                        placeholder="Question"
                        style={{ width: "380px" }}/>
                      <Field
                        name={`${name}.selectedAnswer`}
                        component="input"
                        placeholder="Selected Answer"
                        style={{ width: "380px",
                                 marginLeft: "50px" }}/>
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

  getResponse = (values) => {
    fetch('http://localhost:3001/responses/-/-/'+values.responseID)
    .then((response) => {
      response.json().then(data => ({
        resp: data,
      }) //only necessary if directly fetching like this
      ).then(res => {
        console.log(res.resp);
        this.setState({
          response: res.resp
        });
      });
    });

    this.props.resetResponse();
  }

  renderForm = () => {
    if (this.state.response.length > 0) {
      return (this.MyForm());
    }
  }

  render(){
    return(
      <div>
        <br/><br/><br/>
        <Form model="findresponse" onSubmit={(values) => this.getResponse(values)}>
          <Row>
            <Col md={{ size: 3, offset: 4 }}>
              <Control.text model=".responseID" id="responseID" name="responseID"
                  placeholder="ID of response to be updated"
                  className="form-control" />
            </Col>
            <Col>
              <Button type="submit" color="dark" style={{ width: "150px" }}>
                  Find Response
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

export default EditResponse;