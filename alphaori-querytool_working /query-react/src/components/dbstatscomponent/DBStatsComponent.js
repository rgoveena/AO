import React, { Component } from 'react';
import { Button, Col, Row } from 'reactstrap';
import { Form, Control } from 'react-redux-form';
import SplitterLayout from 'react-splitter-layout';
import Center from 'react-center';
import ReactList from 'react-list';
import { Circle } from 'react-shapes';
import './dbstats.css';

/********************************************************************************************
**
** DBSTATS => PRE-WRITTEN QUERY (PYTHON SCRIPT) OR CUSTOM-MADE QUERY TO DB => SEE RESPONSE
**
********************************************************************************************/

class DBStats extends Component{

	constructor(props) {
		super(props)
		this.state = {
			dbStatus: 'Successfully connected'
		};
	}
	
	/****************************************************************************************
	**
	** DETERMINES THE RENDERING OF THE DATABASE CONNECTION INDICATOR 
	**
	****************************************************************************************/

	connectStatus = () => {

		fetch('http://localhost:3001/connect/' + this.props.dbLink)
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

	statToColor = () => {
		console.log(this.state.dbStatus)
		if (this.state.dbStatus === 'Successfully connected') {
			return("#00ff22") //bright green
		} else if (this.state.dbStatus === 'Failed to connect') {
			return("#ff0008")
		}
	}

	/****************************************************************************************
	**
	** CALLS FUNCTION THAT SENDSs THE CUSTOM-MADE QUERY TO NODE
	**
	****************************************************************************************/

	handleSubmit(query) {
		var str = JSON.stringify(query.query);
		str = str.substring(1,str.length-1);
		console.log("Custom query request submitted ("+str+") to DB host link: "+this.props.dbLink);
		this.props.customQuery(str, this.props.dbLink);
	}

	/****************************************************************************************
	**
	** MAPS ARGUMENTS TO POSITION FOR REACTLIST COMPONENT 
	**
	****************************************************************************************/

	renderItem =(index, key) => {
    	return <div key={key}>{this.props.queryResult[index]}</div>;
  	}
  	
	render(){
		return(
        	<SplitterLayout primaryMinSize={300} secondaryMinSize={1000}>
        		<Center>
	        		<div>
						<br/><br/><br/><br/>
						<Button color="dark" size="lg" block onClick={() => this.props.callPy('vessel-query.py', this.props.dbLink)}> Vessel Query </Button>
						<br/><br/>
						<Button color="dark" size="lg" block onClick={() => this.props.callPy('test.py', this.props.dbLink)}> Python Test </Button>
						<br/><br/> 
	    				<Button color="dark" size="lg" block> Python Script 3 </Button>
	    				<br/><br/>
	    				<Button color="dark" size="lg" block> Python Script 4 </Button>
	    				<br/><br/>
	    				<Button color="dark" size="lg" block> Python Script 5 </Button>
	        		</div>
	   			</Center>
        		<div>
        			<br/><br/><br/><br/>
        			{this.connectStatus()}
        			<Form model="query" onSubmit={(values) => this.handleSubmit(values)}>
				        <Row>    
				        	<Col md={{ size: 0, offset: 1 }}>
								<Circle r={15} fill={{color: [this.statToColor()]}} stroke={{color:'#6b6b6b'}} strokeWidth={5} />
							</Col>
				            <Col sm={{ size: 8 }}>	
				            	<Control.text model=".query" placeholder="SQL Query" className="form-control"/>
				            </Col>
				            <Col>
				            	<Button type="submit" color="dark"> Submit </Button>
				            </Col>
				        </Row>
			        </Form>
			        <br/><br/>
			        <Center>
				        <div style={{overflow: 'auto', height: 350}} id="resultbox" className="col-md-10">
				        	<br/>			        	
						  	<ReactList
							  	length={this.props.queryResult.length}
							  	itemRenderer={this.renderItem}
							    type='simple'/>
							<br/>
						</div>
			        </Center>
        		</div>
      		</SplitterLayout>
        );
    }
}

export default DBStats;