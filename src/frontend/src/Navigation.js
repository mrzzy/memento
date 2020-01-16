import React from 'react';
import './App.css';
import { Route, NavLink, BrowserRouter as Router } from 'react-router-dom'


function NavigationEmployee() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><a href="#"><NavLink to="/employee">M</NavLink></a></li>
            <li><a href="#"><img className="signout" src="./signout.svg" alt="Sign out button" /></a></li>
        </ul>
    );
}

function NavigationVisitor() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><a href="#"><NavLink to="/">M</NavLink></a></li>
            <li><a href="#"><NavLink to="/">Home</NavLink></a></li>
            <li><a href="#"><NavLink to="/employee">Employee</NavLink></a></li>
            <li><a href="#"><NavLink to="/about">About</NavLink></a></li>
            <li><a href="#"><NavLink to="/login">Login</NavLink></a></li>
        </ul>
    );
}
export { NavigationVisitor, NavigationEmployee };