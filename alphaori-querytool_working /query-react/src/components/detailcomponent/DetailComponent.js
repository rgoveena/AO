import React, { Component } from 'react';
import Center from 'react-center';
import ReactList from 'react-list';
import './detail.css';

/********************************************************************************************
**
** DETAIL PAGE: GENERALIZED LAYOUT TO RENDER RESPONSE DATA FOR EACH MICROSERVICE
**
********************************************************************************************/

class Detail extends Component{

	constructor(props) {
		super(props)
		this.state = {
			detail: []
		};
	}

	/****************************************************************************************
	**
	** MAPS ARGUMENTS TO POSITION FOR REACTLIST COMPONENT 
	**
	****************************************************************************************/

	renderItem =(index, key) => {
    	return <div key={key}>{this.state.detail[index]}</div>;
  	}

  	getDetail = (end) => {
		fetch('http://localhost:3001/ms/msdetail/' + this.props.service.replace(/[/]/g, "%2F") + '/' +  end)
		.then((response) => {
	      response.json().then(data => ({
	        detail: data,
	      }) //only necessary if directly fetching like this
	      ).then(res => {
        	this.setState(state => {
      			const detail = state.detail.concat(res.detail[0]);
			    return {
			      detail
			    };
    		});
    		if (end < parseInt(res.detail[1], 10)) {
    			this.getDetail(end+8000);
    		}
	      });
	    });
	}

	componentDidMount() {
		this.getDetail(8000);
	}

	render(){
		return(
    		<div>
    			<br/><br/><br/><br/>
		        <Center>
			        <div style={{overflow: 'auto', height: 500}} id="resultbox" className="col-md-8">
			        	<br/>			        	
					  	<ReactList
						  	length={this.state.detail.length}
						  	itemRenderer={this.renderItem}
						    type='simple'/>
						<br/>
					</div>
		        </Center>
    		</div>
        );
    }
}

export default Detail;