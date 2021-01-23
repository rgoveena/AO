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
    nodes: [{ value: '– All features of this webapp are private; to access them you must login with your username, password, and name.' }],
  },
  {
    value: 'Home',
    nodes: [
      { value: '– Once you are logged in, you will be redirected to the Home page, where you can access and take various quizzes.'},
      { value: '– Once you are logged in, you will be redirected to the Home page, where you can access and take various quizzes.'}
    ]
  },
  {
    value: 'Admin Home',
    nodes: [
      { value: '– A user, who is an admin, can access special features, through which they can view and edit quizzes and responses.'},
      {
        value: '– Add Quiz',
        nodes: [
          { value: '• This interactive form allows you to name your quiz, add (or remove) questions, and add (or remove) answer options.'},
          { value: '• You can also view the dynamic JSON rendering of the quiz that will be sent to the database.'}
        ]
      },
      {
        value: '– Edit Quiz',
        nodes: [
          { value: '• This interactive form allows you to find and consequently, edit a quiz by searching its name. (Each quiz has a unique name.)'},
          { value: '• You can edit a prefilled form, very similar in appearance to the "add quiz" form, and press update to update the quiz. '},
          { value: '• You can also view the dynamic JSON rendering of the quiz that will be sent to the database.'}
        ]
      },
      { value: '– View Response: You can find responses to quizzes from the database by applying optional filters (name of quiz and name of user).' },
      {
        value: '– Edit Response',
        nodes: [
          { value: '• This interactive form allows you to find and consequently, edit a response by searching its ID. (Each response has a unique ID.)'},
          { value: '• You can find the ID of a specific response by using the "View Response" feature. '},
          { value: '• You can edit a prefilled form, very similar in appearance to the "edit response" form, and press update to update the response. '},
          { value: '• The fields you can edit are limited to the quiz name, score, question, and selected answer. You can not remove anything. '},
          { value: '• You can also view the dynamic JSON rendering of the response that will be sent to the database.'}
        ],
      }
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