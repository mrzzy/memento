import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';
import API from './API';
import APIHelpers from './APIHelpers'

class VisitorHome extends React.Component {
    constructor() {
        super();
        const api = new API();
        const apiHelper = new APIHelpers(api);
        this.state = { api: api, apiHelper: apiHelper, employer: false, employee: false };
    }

    async componentDidMount() {
        try {
            let loggedIn = await this.state.api.authCheck();
            let hasEmployers = await this.state.apiHelper.isEmployer(loggedIn);
            this.setState({ employer: hasEmployers, employee: !hasEmployers });
        } catch (e) {
            console.error(e);
        }
    }

    render() {
        if (this.state.employee)
            return <Redirect to='/employee' />

        if (this.state.employer)
            return <Redirect to='/employer' />

        return (
            <div>
                <NavigationVisitor />
                <img src="./visitorhomebg.png" alt="Home Page" style={{height: "70vh", margin: "auto", display: "block"}} />
            </div>
        );
    }
}

export default VisitorHome;

