import React, { Component } from 'react';
import { Button } from 'reactstrap';
import Center from 'react-center';
import { Link } from 'react-router-dom';


class Home extends Component{

	logInfo = (link) => {
		console.log(link+" button clicked")
	}


	render(){
		return(
			<Center>
				<div className="col-md-3">
					<br/><br/><br/><br/>
					<Link to='/api'>
						<Button onClick={() => this.logInfo("API Requests")} color="dark" size="lg" block> 
							<span className="fa fa-code fa-lg"></span>
							{' '}API Requests
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to='/services'>
						<Button onClick={() => this.logInfo("MicroServices")} color="dark" size="lg" block> 
							<span className="fa fa-list fa-lg"></span>
							{' '}Micro Services 
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to= "/visualizer">
						<Button onClick={() => this.logInfo("Visualizer")} color="dark" size="lg" block>  
							<span className="fa fa-eye fa-lg"></span>
							{' '}Data Visualizer
						</Button>
					</Link>
					<br/><br/><br/> 
					<Link to= "/dbconnect">
						<Button onClick={() => this.logInfo("Database Statistics")} color="dark" size="lg" block> 
							<span className="fa fa-database fa-lg"></span>
							{' '}Database Statistics
						</Button>
					</Link>
				</div>
			</Center>
        );
    }
}

export default Home;