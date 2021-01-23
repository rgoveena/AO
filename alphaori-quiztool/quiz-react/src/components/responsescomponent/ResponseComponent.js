import React, { Component } from 'react';
import Center from 'react-center';
import './responses.css';
import { Col, Row, Button } from 'reactstrap';
import { Form, Control } from 'react-redux-form';

class Responses extends Component{

	constructor(props) {
		super(props)
		this.state = {
			responses: []
		};
	}

  	getResponses = (values) => {

  		var quizName = values.quizName;
  		var username = values.username;
  		if (values.quizName.length === 0) {
  			quizName = '-'
  		}
  		if (values.username.length === 0) {
  			username = '-'
  		}
		fetch('http://localhost:3001/responses/'+quizName+'/'+username+'/-')
		.then((response) => {
	      response.json().then(data => ({
	        responses: data,
	      }) //only necessary if directly fetching like this
	      ).then(res => {
	      	console.log(res.responses);
        	this.setState({
      			responses: res.responses
    		});
	      });
	    });

	    this.props.resetResponse();
	}

	render(){
		return(
    		<div>
    			<br/><br/><br/><br/>
    			<Form model="response" onSubmit={(values) => this.getResponses(values)}>
    				<Row>
		            	<Col md={{ size: 3, offset: 2 }}>
		                  <Control.text model=".quizName" id="quizName" name="quizName"
		                      placeholder="Filter by Quiz Name (optional)"
		                      className="form-control" />
		                </Col>
		                <Col md={{ size: 3 }}>
		                  <Control.text model=".username" id="username" name="username"
		                      placeholder="Filter by Username (optional)"
		                      className="form-control" />
		                </Col>
			            <Col>
		                  <Button type="submit" color="dark" style={{ width: "200px" }}>
		                  	  Search Responses
		                  </Button>
			            </Col>
			        </Row>
		        </Form>
		        <br/><br/>
		        <Center>
			        <div style={{overflow: 'auto', height: 400}} id="resultbox" className="col-md-8">
			        	<br/>			        	
					  		<pre>{JSON.stringify(this.state.responses, null, 2) }</pre>
						<br/>
					</div>
		        </Center>
    		</div>
        );
    }
}

export default Responses;