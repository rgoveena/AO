import React, { Component } from 'react';
import { Switch, Route, Redirect, withRouter } from 'react-router-dom';
import Header from './HeaderComponent';
import Home from './HomeComponent';
import Login from './LoginComponent';
import Help from './helpcomponent/HelpComponent';
import SampleQuiz from './quizcomponent/SampleQuiz';
import Responses from './responsescomponent/ResponseComponent';
import AdminHome from './AdminHome';
import MyForm from './formcomponent/Form';
import EditQuiz from './formcomponent/EditQuiz';
import EditResponse from './formcomponent/EditResponse';
import { actions } from 'react-redux-form';
import { fetchQuiz } from '../redux/ActionCreators';
import { connect } from 'react-redux';

/********************************************************************************************
**
** CREATES "FRONT-END" AUTHENTICATION
**
********************************************************************************************/

export const fakeAuth = {
  isAuthenticated: false,
  isAdmin: false,
  authenticate(cb) {
    this.isAuthenticated = true
    setTimeout(cb, 100) // fake async
  },
  signout(cb) {
    this.isAuthenticated = false
    setTimeout(cb, 100) // fake async
  }
}

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    fakeAuth.isAuthenticated === true
      ? <Component {...props} />
      : <Redirect to='/login' />
  )} />
)

const AdminRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    fakeAuth.isAdmin === true
      ? <Component {...props} />
      : <Redirect to='/login' />
  )} />
)

/********************************************************************************************
**
** RECEIVING DATA/FUNCTIONS FROM STORE TO SEND TO VARIOUS COMPONENTS
**
********************************************************************************************/

//const services = ['/v1.2/alerts', '/v1.2/eca/ecadocuments', '/v1.2/users']

const mapStateToProps = (state) => {
  return {
    quiz1: state.quiz.quiz1,
    quiz2: state.quiz.quiz2,
    quiz3: state.quiz.quiz3
  }
}

const mapDispatchToProps = (dispatch) => ({
  resetLogin: () => {dispatch(actions.reset('login'))},
  resetResponse: () => {dispatch(actions.reset('response'))},
  resetQuiz: () => {dispatch(actions.reset('findquiz'))},
  resetEditResponse: () => {dispatch(actions.reset('findresponse'))},
  fetchQuiz: (quizName, quizSlot) => dispatch(fetchQuiz(quizName, quizSlot))
});

/********************************************************************************************
**
** CREATING THE ROUTING SKELETON FOR THE APP
**
********************************************************************************************/

class Main extends Component {

  componentDidMount() {
    this.props.fetchQuiz("Numbers", "quiz1");
    this.props.fetchQuiz("Spelling", "quiz2");
    this.props.fetchQuiz("Colors", "quiz3");
  }

  render(){

    
    const HomePage = () => {
      return(
        <Home/>
      );
    }

    const AdminHomePage = () => {
      return(
        <AdminHome/>
      );
    }

    const Quiz1Page = () => {
      return(
        <SampleQuiz quiz={this.props.quiz1}/>
      );
    }

    const Quiz2Page = () => {
      return(
        <SampleQuiz quiz={this.props.quiz2}/>
      );
    }

    const Quiz3Page = () => {
      return(
        <SampleQuiz quiz={this.props.quiz3}/>
      );
    }

    const LoginPage = () => {
      return(
        <Login resetLogin = {this.props.resetLogin}/>
      );
    }

    const HelpPage = () => {
      return(
        <Help/>
      );
    }

    const ResponsesPage = () => {
      return(
        <Responses resetResponse = {this.props.resetResponse}/>
      );
    }

    const FormPage = () => {
      return(
        <MyForm/>
      );
    }

    const EditQuizPage = () => {
      return(
        <EditQuiz resetQuiz = {this.props.resetQuiz}/>
      );
    }

    const EditResponsePage = () => {
      return(
        <EditResponse resetResponse = {this.props.resetEditResponse}/>
      );
    }

    return (
      <div>
        <Header/>
        <Switch>
          <PrivateRoute exact path="/home" component={HomePage}/>
          <Route exact path="/login" component={LoginPage}/>
          <Route exact path="/help" component={HelpPage}/>
          <AdminRoute exact path="/addquiz" component={FormPage}/>
          <AdminRoute exact path="/adminhome" component={AdminHomePage}/>
          <AdminRoute exact path="/responses" component={ResponsesPage}/>
          <AdminRoute exact path="/editquiz" component={EditQuizPage}/>
          <AdminRoute exact path="/editresponse" component={EditResponsePage}/>
          <Route exact path="/quiz1" component={Quiz1Page}/>
          <Route exact path="/quiz2" component={Quiz2Page}/>
          <Route exact path="/quiz3" component={Quiz3Page}/>
          <Redirect from='/' to='/login'/>
        </Switch>
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Main));
