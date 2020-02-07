import React from 'react';
import './App.css';
import { Redirect, NavLink } from 'react-router-dom'
import API from './API';

class NavigationEmployee extends React.Component {

    constructor() {
        super();
        const api = new API();
        this.state = { api: api, loggedIn: true };
    }

    signOut = () => {

        // for some reason this.state.api.logout() skips the lines afterwards
        // so doing manually for now
        this.state.api.setState({
            "accessToken": null,
            "refreshToken": null
        });
        this.setState({ loggedIn: false });
    }

    render() {
        if (!this.state.loggedIn)
            return <Redirect to="/" />;

        return (
            <ul className="navigationBar">
                <li className="headerLogo"><NavLink to="/employee">M</NavLink></li>
                <li><a href="" onClick={this.signOut}><img className="signout" src="./signout.svg" alt="Sign out button" /></a></li>
            </ul>
        );
    }
}

class NavigationEmployer extends React.Component {

    constructor() {
        super();
        const api = new API();
        this.state = { api: api, loggedIn: true };
    }

    signOut = () => {
        this.state.api.setState({
            "accessToken": null,
            "refreshToken": null
        });
        this.setState({ loggedIn: false });
    }

    render() {
        if (!this.state.loggedIn)
            return <Redirect to="/" />;

        return (
            <ul className="navigationBar">
                <li className="headerLogo"><NavLink to="/employee">M</NavLink></li>
                <li><NavLink to="/employer">Home</NavLink></li>
                <li><NavLink to="/my-employees">My Employees</NavLink></li>
                <li><a href="" onClick={this.signOut}><img className="signout" src="./signout.svg" alt="Sign out button" /></a></li>
            </ul>
        );
    }
}

function NavigationVisitor() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><NavLink to="/">M</NavLink></li>
            <li><NavLink to="/">Home</NavLink></li>
            <li><NavLink to="/about">About</NavLink></li>
            <li><NavLink to="/login">Login</NavLink></li>
        </ul>
    );
}

export { NavigationVisitor, NavigationEmployee, NavigationEmployer };