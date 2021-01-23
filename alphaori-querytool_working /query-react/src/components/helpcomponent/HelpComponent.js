import React, { Component } from 'react';
import MuiTreeView from 'material-ui-treeview';
import Center from 'react-center';
import './help.css';

/********************************************************************************************
**
** HELP PAGE: OFFERS EXPLANATION (IN BELOW FORMAT) FOR EACH FEATURE OF THE APP
**
********************************************************************************************/
 
const tree = [
  {
    value: 'Login',
    nodes: [{ value: '– All features of this webapp are private; to access them you must login with your username and password.' }],
  },
  {
    value: 'Home',
    nodes: [{ value: '– Once you are logged in, you will be redirected to the Home page, where you can access various features.' }],
  },
  {
    value: 'API Request',
    nodes: [
      { value: '– You can access this feature from the Home page. It allows the user to custom-make and submit an API request.' },
      { value: '– The user selects a host link, enters an API signature, and specifies a method (get/post) to view the content for each API request.'}],
  },
  {
    value: 'Microservices',
    nodes: [
      { value: '– You can access this feature from the Home page. It enables management of SMARTship microservices.'},
      { value: '– Renders status code (through a green/red indicator) and content (through a corresponding details page) for each service request.' },
      { value: '– Alert Services: ALERT SERVICES DESCRIPTION' },
      { value: '– ECA App: ECA APP DESCRIPTION '},
      { value: '– Microservice #3: MICROSERVICE #3 DESCRIPTION '},
      { value: '– Microservice #4: MICROSERVICE #4 DESCRIPTION '}],
  },
  {
    value: 'Visualizer',
    nodes: [
      { value: '– You can access this feature from the Home page. It provides a graphic visualization of CSV data that you upload.'},
      { value: '– BEWARE not to use the same name for another upload in the same session.'}
    ],
  },
  {
    value: 'Database Statistics',
    nodes: [
      { value: '– You can access this feature from the Home page. It provides easy access for retrieving and viewing data.'},
      {
        value: '– Database Connection',
        nodes: [
          { value: '• Before you access statistics, you must establish a connection with the database by submitting one of the provided links.'},
          { value: '• After connecting with the database, you can redirect yourself to the DB Stats page, through the "Successfully Connected" button.'}
        ]
      },
      {
        value: '– Python Scripts',
        nodes: [
          { value: '• These buttons on the left side of the DB Stats page call on pre-built Python scripts to query the database with typical requests.' },
          { value: '• Vessel Query: Returns the ID number(s) of the vessels in the database.'},
          { value: '• Python Test: Renders a list of numbers on the frontend to ensure proper communication among various elements of program.'},
          { value: '• Python Script 3: PYTHON SCRIPT 3 DESCRIPTION'},
          { value: '• Python Script 4: PYTHON SCRIPT 4 DESCRIPTION'},
          { value: '• Python Script 5: PYTHON SCRIPT 5 DESCRIPTION'}
        ],
      },
      { value: '– Custom SQL Query: You can also submit your own SQL (Structure Query Language) query.'}
    ],
  },
];
 

class Help extends Component{

  render(){
    return(
      <Center>
        <div className="col-md-9">
          <br/><br/>
          <div id="helptree" className="col-md"> 
            <br/>
              <MuiTreeView tree={tree} />
            <br/>
          </div>
          <br/><br/>
        </div>
      </Center>
    )}

}

export default Help;