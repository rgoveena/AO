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
					<Link to='/quiz1'>
						<Button onClick={() => this.logInfo("Numbers")} color="dark" size="lg" block> 
							<span className="fa fa-pencil fa-lg"></span>
							{' '}Numbers Quiz
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to='/quiz2'>
						<Button onClick={() => this.logInfo("Spelling")} color="dark" size="lg" block> 
							<span className="fa fa-pencil fa-lg"></span>
							{' '}Spelling Quiz
						</Button>
					</Link>
					<br/><br/><br/>
					<Link to= "/quiz3">
						<Button onClick={() => this.logInfo("Colors")} color="dark" size="lg" block>  
							<span className="fa fa-pencil fa-lg"></span>
							{' '}Colors Quiz
						</Button>
					</Link>
				</div>
			</Center>
        );
    }
}

export default Home;