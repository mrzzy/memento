import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';
import API from './API';

class VisitorHome extends React.Component {
    constructor() {
        super();
        const api = new API();
        this.state = { api: api };
    }

    async componentDidMount() {
        let loggedIn = await this.state.api.authCheck();
        if (loggedIn !== null)
            return <Redirect to='/employee' />
    }

    render() {
        return (
            <div>
                <NavigationVisitor />
                <img src="./visitorhomebg.png" alt="Home Page" style={{height: "70vh", margin: "auto", display: "block"}} />
            </div>
        );
    }
}

export default VisitorHome;

