import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

class VisitorHome extends React.Component {
    render() {
        if (localStorage.getItem("loggedIn") === "true")
            return <Redirect to='/employee' />

        return (
            <div>
                <img src="./visitorhomebg.png" alt="Home Page" style={{height: "70vh", margin: "auto", display: "block"}} />
            </div>
        );
    }
}

export default VisitorHome;

