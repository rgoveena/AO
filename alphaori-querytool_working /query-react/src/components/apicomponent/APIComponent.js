import React, { Component } from 'react';
import { Button, Col, Row } from 'reactstrap';
import { Form, Control } from 'react-redux-form';
import Center from 'react-center';
import ReactList from 'react-list';
import './apicomponent.css';

var properties = require("../../properties.json");

/********************************************************************************************
**
** API PAGE: SELECT LINK AND WRITE API SIGNATURE => GET/POST REQUEST => SEE RESPONSE
**
********************************************************************************************/

class API extends Component{

	constructor(props) {
		super(props)
		this.state = {
			response: []
		};
	}

/*export const request = (method, link) => (dispatch) => {

	//console.log("Fetching "+baseUrl + 'connect/' + link+" from Node");

	return fetch(baseUrl + 'api/' + method + '/' + link + '/-')
	.then(response => {
			if (response.ok){
				return response;
			}
			else {
				var error = new Error('Error '+ response.status +': '+response.statusText);
				error.response = response;
				throw error;
			}
		},
		error => {
			var errmess = new Error(error.message);
			throw errmess;
		})
		.then(response => response.json())
		.then(result => dispatch(apiResponse(result)))
		//.catch(error => console.log(error.message)); 
}*/



	/****************************************************************************************
	**
	** CALLS FUNCTION THAT SENDS API REQUEST TO NODE 
	**
	****************************************************************************************/

	handleSubmit(request) {
		var req = JSON.stringify(request.request);
		req = req.substring(1,req.length-1);
		req = req.replace(/[/]/g, "%2F");
		var link = JSON.stringify(request.link);
		link = link.substring(1,link.length-1);
		//this.props.request(request.type, link+req);

		if (request.type === 'get') {
			fetch("http://localhost:3001/api/" + request.type + '/' +link+ '/' + req)
			.then((response) => {
		      response.json().then(data => ({
		        data: data,
		      }) //only necessary if directly fetching like this
		      ).then(res => {
		        this.setState({ response : res.data });
		      });
		    });
		} else if (request.type === 'post') {
			const data = new FormData();
		    data.append('content', request.content);

		    fetch('http://localhost:3001/api/' + request.type + '/' + link+ '/' + req, {
		      method: 'POST',
		      body: data,
		    }).then((response) => {
		      response.json().then(data => ({
		        data: data,
		      }) //only necessary if directly fetching like this
		      ).then(res => {
		        console.log(res.data);
		        this.setState({ response : res.data });
		      });
		    });
		}
	}


	/****************************************************************************************
	**
	** MAPS ARGUMENTS TO POSITION FOR REACTLIST COMPONENT
	**
	****************************************************************************************/

	renderItem =(index, key) => {
    	return <div key={key}>{this.state.response[index]}</div>;
  	}

	/****************************************************************************************
	**
	** RETURNS THE URL'S FROM THE PROPERTIES FILES FOR THE DROPDOWN MENU
	**
	****************************************************************************************/
  	
  	createOptions = () => {
		var hosts = [];
		for (var i=0; i<properties.length; i++) {
			var str = JSON.stringify(properties[i].host)
			hosts.push(<option>{str.substring(1,str.length-1)}</option>)
		}
		console.log("Hosts from properties file rendered on dropdown menu");
		return hosts;
	}

	componentDidMount() {
		if (this.state.response.length === 0) {
			this.props.resetAPI();
		}
	}

	render(){
		return(
    		<div>
    			<br/><br/><br/><br/>
    			<Form model="request" onSubmit={(values) => this.handleSubmit(values)}>
			        <Row>    
			            <Col md={{ size: 4, offset: 2 }}>	
			            	<Control.select model=".link" className="form-control">
			            		<option></option>
			            		{this.createOptions()}
			            	</Control.select>
			            </Col>
			            <Col sm={{ size: 2 }}>
			            	<Control.text model=".request" placeholder="API Signature" className="form-control"/>
			            </Col>
			            <Col sm={{ size: 1 }}>	
			            	<Control.select model=".type" className="form-control">
			            		<option>get</option>
			            		<option>post</option>
			            	</Control.select>
			            </Col>
			            <Col>
			            	<Button type="submit" color="dark"> Submit </Button>
			            </Col>
			        </Row>
			        <br/>
			        <Row className="form-group">
                        <Col md={{ size: 8, offset: 2 }}>
                            <Control.textarea model=".content" className="form-control" placeholder="POST Content"/>
                        </Col>
                    </Row>
		        </Form>
		        <Col md={{ offset: 2 }}>
		        	<strong> Response (Renders up to 8191 characters) </strong>
		        </Col>
		        <Center>
			        <div style={{overflow: 'auto', height: 350}} id="resultbox" className="col-md-8">
			        	<br/>			        	
					  	<ReactList
						  	length={this.state.response.length}
						  	itemRenderer={this.renderItem}
						    type='simple'/>
						<br/>
					</div>
		        </Center>
    		</div>
        );
    }
}

export default API;