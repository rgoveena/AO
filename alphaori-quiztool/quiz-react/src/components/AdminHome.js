import React, { Component } from 'react';
import { Button } from 'reactstrap';
import Center from 'react-center';
import { Link } from 'react-router-dom';


class AdminHome extends Component{

	logInfo = (link) => {
		console.log(link+" button clicked")
	}


	render(){
		return(
			<Center>
				<div className="col-md-3">
					<br/><br/><br/><br/>
					<Link to='/addquiz'>
						<Button onClick={() => this.logInfo("Add Quiz")} color="dark" size="lg" block> 
							<span className="fa fa-plus fa-lg"></span>
							{' '}Add Quiz
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to='/editquiz'>
						<Button onClick={() => this.logInfo("Edit Quiz")} color="dark" size="lg" block> 
							<span className="fa fa-pencil fa-lg"></span>
							{' '}Edit Quiz
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to= "/responses">
						<Button onClick={() => this.logInfo("View Responses")} color="dark" size="lg" block>  
							<span className="fa fa-eye fa-lg"></span>
							{' '}View Responses
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to= "/editresponse">
						<Button onClick={() => this.logInfo("Edit Response")} color="dark" size="lg" block>  
							<span className="fa fa-pencil fa-lg"></span>
							{' '}Edit Response
						</Button>
					</Link>
				</div>
			</Center>
        );
    }
}

export default AdminHome;