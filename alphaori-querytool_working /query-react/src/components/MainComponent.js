import React, { Component } from 'react';
import { Switch, Route, Redirect, withRouter } from 'react-router-dom';
import Header from './HeaderComponent';
import DBStats from './dbstatscomponent/DBStatsComponent';
import Home from './HomeComponent';
import Login from './LoginComponent';
import Visualizer from './VisualizerComponent';
import Connect from './DBConnectComponent';
import Help from './helpcomponent/HelpComponent';
import API from './apicomponent/APIComponent';
import Detail from './detailcomponent/DetailComponent';
import Services from './ServicesComponent';
import { actions } from 'react-redux-form';
import { connect } from 'react-redux';
import { runPy, customQuery, request } from '../redux/ActionCreators';

/********************************************************************************************
**
** CREATES "FRONT-END" AUTHENTICATION
**
********************************************************************************************/

export const fakeAuth = {
  isAuthenticated: false,
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

/********************************************************************************************
**
** RECEIVING DATA/FUNCTIONS FROM STORE TO SEND TO VARIOUS COMPONENTS
**
********************************************************************************************/

const services = ['/v1.2/alerts', '/v1.2/eca/ecadocuments', '/v1.2/users']

const mapStateToProps = (state) => {
  return {
    queryResult: state.queryResult.result,
    dbLink: state.db.link
  }
}

const mapDispatchToProps = (dispatch) => ({
  resetLogin: () => {dispatch(actions.reset('login'))},
  resetAPI: () => {dispatch(actions.reset('request'))},
  runPy: (file, link) => dispatch(runPy(file, link)),
  customQuery: (query, link) => dispatch(customQuery(query, link)),
  request: (type, link) => dispatch(request(type, link))
});

/********************************************************************************************
**
** CREATING THE ROUTING SKELETON FOR THE APP
**
********************************************************************************************/

class Main extends Component {

  render(){

    const DBStatsPage = () => {
      return(
        <DBStats queryResult={this.props.queryResult}
          callPy={this.props.runPy}
          customQuery={this.props.customQuery}
          dbLink={this.props.dbLink}/>
      );
    }

    const DBConnectPage = () => {
      return(
        <Connect dbLink = {this.props.dbLink}/>
      );
    }

    const RequestPage = () => {
      return(
        <API apiResponse={this.props.apiResponse}
          request={this.props.request}
          resetAPI={this.props.resetAPI}/>
      );
    }

    const DetailPage = ({match}) => {
      return(
        <Detail service={services[parseInt(match.params.serviceId, 10)]}/>
      );
    }

    const HomePage = () => {
      return(
        <Home/>
      );
    }

    const ServicesPage = () => {
      return(
        <Services services={services}/>
      );
    }

    const HelpPage = () => {
      return(
        <Help/>
      );
    }

    const VisualizerPage = () => {
      return(
        <Visualizer />
      );
    }

    const LoginPage = () => {
      return(
        <Login resetLogin = {this.props.resetLogin}/>
      );
    }

    return (
      <div>
        <Header/>
        <Switch>
          <PrivateRoute exact path="/dbstats" component={DBStatsPage}/>
          <PrivateRoute exact path="/dbconnect" component={DBConnectPage}/>
          <PrivateRoute exact path="/visualizer" component={VisualizerPage}/>
          <PrivateRoute exact path="/services" component={ServicesPage}/>
          <PrivateRoute exact path="/home" component={HomePage}/>
          <PrivateRoute exact path="/api" component={RequestPage}/>
          <PrivateRoute path="/services/:serviceId" component={DetailPage}/>
          <Route exact path="/login" component={LoginPage}/>
          <Route exact path="/help" component={HelpPage}/>
          <Redirect from='/' to='/login'/>
        </Switch>
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Main));
