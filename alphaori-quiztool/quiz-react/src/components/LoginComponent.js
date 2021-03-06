import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Col, Row, Button } from 'reactstrap';
import { Form, Control, Errors } from 'react-redux-form';
import { fakeAuth } from './MainComponent.js';

const required = (val) => val && val.length;
export var name = 'anonymous';

export default class Login extends Component {

  constructor(props) {
    super(props);
    this.handleLogin = this.handleLogin.bind(this);
    this.state = {
      redirect: false
    }
  }

  handleLogin(values){
    console.log("Login button clicked")
    name = values.name;
    if (values.username==='user' && values.password==='user' && values.name.length > 0){
      fakeAuth.isAuthenticated = true;
      this.setState({redirect: true});
      console.log("Login authentication successful")
    } else if (values.username==='admin' && values.password==='admin' && values.name.length > 0){
      fakeAuth.isAuthenticated = true;
      fakeAuth.isAdmin = true;
      this.setState({redirect: true});
      console.log("Login authentication successful")
    } else {
      console.log("Login authentication failed")
      alert("Your username or password is incorrect. Or, you have not entered a name. Please try logging in again!")
    } 
    this.props.resetLogin();
  }

/*
  // This will be called when the user clicks on the login button
  login(e) {
    e.preventDefault();
    // Here, we call an external AuthService. We’ll create it in the next step
    Auth.login(this.state.user, this.state.password)
      .catch(function(err) {
        console.log("Error logging in", err);
      });
  }
*/
  render() {
    if (this.state.redirect) {
        return (<Redirect to='/home'/>)
    }
    return (
      <div className = "container">
        <br/><br/>
        <Form model="login" onSubmit={(values) => this.handleLogin(values)}>
          <Row className="form-group">
              <Col md={{ size: 6, offset: 3 }}>
                  <Control.text model=".username" id="username" name="username"
                      placeholder="Login username"
                      className="form-control"
                      validators={{
                          required
                      }} />
                  <Errors
                      className="text-danger"
                      model=".username"
                      show="touched"
                      messages={{
                          required: 'Required'
                      }}
                  />
              </Col>
          </Row>
          <Row className="form-group">
              <Col md={{ size: 6, offset: 3 }}>
                  <Control.text model=".password" type="password" id="password" name="password"
                      placeholder="Login password"
                      className="form-control"
                      validators={{
                          required
                      }} />
                  <Errors
                      className="text-danger"
                      model=".password"
                      show="touched"
                      messages={{
                          required: 'Required'
                      }}
                  />
              </Col>
          </Row>
          <Row className="form-group">
              <Col md={{ size: 6, offset: 3 }}>
                  <Control.text model=".name" id="name" name="name"
                      placeholder="Your name (recorded for quiz)"
                      className="form-control"
                      validators={{
                          required
                      }} />
                  <Errors
                      className="text-danger"
                      model=".name"
                      show="touched"
                      messages={{
                          required: 'Required'
                      }}
                  />
              </Col>
          </Row>
          <Row className="form-group">
            <Col md={{ size: 6, offset: 3}}>
                <Button type="submit" color="dark">
                  Login
                </Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}
