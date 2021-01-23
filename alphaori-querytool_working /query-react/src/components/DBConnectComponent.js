import React, { Component } from 'react';
import { Button, Col, Row } from 'reactstrap';
import { Form, Control } from 'react-redux-form';
import Center from 'react-center';
import { Link } from 'react-router-dom';

var properties = require("../properties.json");

class Connect extends Component{

	constructor(props) {
		super(props)
		this.state = {
			link: '',
			dbStatus: 'Not Connected'
		};
	}
	
	handleSubmit(value) {
		var host = JSON.stringify(value.link);
		host = host.substring(1,host.length-1);
		console.log("DB Connect request submitted for host link: "+host);

		fetch('http://localhost:3001/connect/' + host)
		.then((response) => {
	      response.json().then(data => ({
	        connection: data,
	      }) //only necessary if directly fetching like this
	      ).then(res => {
	      	console.log(res.connection)
	      	if (this.state.dbStatus !== res.connection) {
        		this.setState({ dbStatus : res.connection })
        	}
	      });
	    });
	}


	createOptions = () => {
		var hosts = [];
		for (var i=0; i<properties.length; i++) {
			var str = JSON.stringify(properties[i].host)
			hosts.push(<option>{str.substring(1,str.length-1)}</option>)
		}
		console.log("Hosts from properties file rendered on dropdown menu");
		return hosts;
	}

	renderRedirect = () => {
		if (this.state.link !== this.props.dbLink) {
			this.setState({ link: this.props.dbLink })
			this.setState({ dbStatus: 'Not Connected' })
		}
		console.log("Updating DB status on browser to: "+this.state.dbStatus)
		if (this.state.dbStatus==='Successfully connected') {
	        return (
	        	<Link to='/dbstats'> 
	        		<Button onClick = {() => console.log("Redirecting to DB Query page")} color="success" size="sm"> Successfully Connected </Button>
	        	</Link>)
	    } else if (this.state.dbStatus==='Failed to connect') {
	    	return (<Button color="danger" size="sm"> Failed to Connect </Button>)
	    } else {
	    	return (<strong> {this.state.dbStatus} </strong>)
	    }
	}

	render(){
		return(
			<div>	
				<br/><br/><br/><br/><br/><br/>
				<Center>	
					<div className= "col-md-6">
						Connect to database using the host: 
					</div>
				</Center>
				<br/>
				<Center>
					<div className= "col-md-6">
					<Form model="db" onSubmit={(values) => this.handleSubmit(values)}>
				        <Row>    
				            <Col sm={{ size: 10 }}>	
				            	<Control.select model=".link" className="form-control">
				            		<option></option>
				            		{this.createOptions()}
				            	</Control.select>
				            </Col>
				            <Col>
				            	<Button type="submit" color="dark"> Submit </Button>
				            </Col>
				        </Row>
			        </Form>
			        </div>
				</Center>
				<br/>
				<Center>	
					<div className= "col-md-6">
						<span> Current Connection Status: </span>
						{this.renderRedirect()}
					</div>
				</Center>
        	</div>
        );
    }
}

export default Connect;