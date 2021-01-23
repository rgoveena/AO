import React, { Component } from 'react';
import { Navbar, NavbarBrand, Nav, NavbarToggler, Collapse, NavItem } from 'reactstrap';
import { NavLink } from 'react-router-dom'; 

class Header extends Component {

	constructor(props) {
		super(props);
		this.state = {
			isNavOpen: false,
			isModalOpen: false
		};
		this.toggleNav = this.toggleNav.bind(this);
		this.toggleModal = this.toggleModal.bind(this);
	}

	toggleNav() {
		this.setState({
			isNavOpen: !this.state.isNavOpen
		});
	}

	toggleModal() {
		this.setState({
			isModalOpen: !this.state.isModalOpen
		});
	}


	render() {
		return (
		        <Navbar dark expand="md">
		          <div className="container">
		          	<NavbarToggler onClick={this.toggleNav} />
		            <NavbarBrand className="mr-auto">
		            	<img src={require('../alphaori.png')} height="40" width="110"
		            		alt="AlphaOri" />
		            </NavbarBrand>
		            <Collapse isOpen={this.state.isNavOpen} navbar>
		            	<Nav navbar>
		            		<NavItem>
		            			<NavLink className="nav-link" to="/login">
		            				<span className="fa fa-pencil fa-lg"></span> Login
		            			</NavLink>
		            		</NavItem>		            		
		            		<NavItem>
		            			<NavLink className="nav-link" to="/home">
		            				<span className="fa fa-home fa-lg"></span> Home
		            			</NavLink>
		            		</NavItem>
		            		<NavItem>
		            			<NavLink className="nav-link" to="/help">
		            				<span className="fa fa-search fa-lg"></span> Help
		            			</NavLink>
		            		</NavItem>
		            	</Nav>
		            </Collapse>
		          </div>
		        </Navbar>
		)
	}
}

export default Header;