import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

class About extends React.Component {
    render() {
        if (sessionStorage.getItem("role") === "employee")
            return <Redirect to='/employee' />

        else if (sessionStorage.getItem("role") === "employer")
            return <Redirect to='/employer' />

        return (
            <div>
                <NavigationVisitor />
                <p>From About.js</p>
            </div>
        );
    }
}

export default About;

