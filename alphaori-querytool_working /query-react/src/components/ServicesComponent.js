import React, { Component } from 'react';
import { Button, Col, Row } from 'reactstrap';
import { Circle } from 'react-shapes';
import { Link } from 'react-router-dom';


class Services extends Component{

	constructor(props) {
		super(props)
		this.state = {
			stat0: 'PENDING', //alerts
			stat1: 'PENDING', //eca
			stat2: 'PENDING', //ms 3
			stat3: 'PENDING' //ms 4
		};
	}

	renderDetails = (id) => {
		return(
			<Link to ={`/services/${id}`} >
				<Button color="secondary" block> Details </Button>
			</Link>
		);
	}

	sendReq = (num) => {
		fetch('http://localhost:3001/ms/msstat/' + this.props.services[num].replace(/[/]/g, "%2F") + '/-')
		.then((response) => {
	      response.json().then(data => ({
	        data: data,
	      }) //only necessary if directly fetching like this
	      ).then(res => {
	      	//console.log(state, JSON.stringify(res.data[0]));
	        var state = "stat"+num;
	        var status = JSON.stringify(res.data[0]);
	        status = status.substring(1, status.length-1);
	        console.log(status);
	        if (this.state[state] !== status) {
	        	this.setState({ [state] : status })
	        }
	      });
	    });
	}

	statToColor = (state) => {
		if (this.state[state] === '200' || this.state[state] === '304') {
			return("#00ff22") //bright green
		} else if (this.state[state] === 'PENDING') {
			return("gray")
		} else {
			return("#ff0008") //bright red
		}
	}	


	render(){
		return(
			<div>
				{this.sendReq(0)}
				{this.sendReq(1)}
				<br/><br/><br/><br/>
				<Row>	
					<Col md={{ size: 3, offset: 4 }}>
						<Button color="dark" size="lg" block > Alert Services </Button>
					</Col>
					<Col md={{ size: 0 }}>
						<Circle r={15} fill={{color: [this.statToColor("stat0")]}} stroke={{color:'#6b6b6b'}} strokeWidth={5} />
					</Col>
					<Col md={{ size: 1 }} >
						{this.renderDetails(0)}
					</Col>
				</Row>
				<br/><br/><br/>
				<Row>
					<Col md={{ size: 3, offset: 4 }}>
						<Button color="dark" size="lg" block > ECA App </Button>
					</Col>
					<Col md={{ size: 0 }}>
						<Circle r={15} fill={{color:[this.statToColor("stat1")]}} stroke={{color:'#6b6b6b'}} strokeWidth={5} />
					</Col>
					<Col md={{ size: 1 }} >
						{this.renderDetails(1)}
					</Col>
				</Row>
				<br/><br/><br/>
				<Row>
					<Col md={{ size: 3, offset: 4 }}>
						<Button color="dark" size="lg" block > MicroServices #3 </Button>
					</Col>
					<Col md={{ size: 0 }}>
						<Circle r={15} fill={{color: [this.statToColor("stat2")]}} stroke={{color:'#6b6b6b'}} strokeWidth={5} />
					</Col>
					<Col md={{ size: 1 }} >
						{this.renderDetails(2)}
					</Col>
				</Row>
				<br/><br/><br/>
				<Row>
					<Col md={{ size: 3, offset: 4 }}>
						<Button color="dark" size="lg" block >  MicroServices #4 </Button>
					</Col>
					<Col md={{ size: 0 }}>
						<Circle r={15} fill={{color: [this.statToColor("stat3")]}} stroke={{color:'#6b6b6b'}} strokeWidth={5} />
					</Col>
					<Col md={{ size: 1 }} >
						{this.renderDetails()}
					</Col>
				</Row>
			</div>
        );
    }
}

export default Services;