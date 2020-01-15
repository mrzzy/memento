import React from 'react';
import './App.css';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'


function NavigationEmployee() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><a href="#">M</a></li>
            <li><a href="#">Home</a></li>
            <li><a href="#">My Tasks</a></li>
            <li><a href="#">Notes</a></li>
            <li><a href="#"><img className="signout" src="./signout.svg" alt="Sign out button" /></a></li>
        </ul>
    );
}

function NavigationVisitor() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><a href="#"><Link to="/">M</Link></a></li>
            <li><a href="#"><Link to="/">Home</Link></a></li>
            <li><a href="#"><Link to="/employee">Employee</Link></a></li>
            <li><a href="#"><Link to="/about">About</Link></a></li>
            <li><a href="#"><Link to="/login">Login</Link></a></li>
        </ul>
    );
}
export { NavigationVisitor, NavigationEmployee };