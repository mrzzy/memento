import React from 'react';
import './App.css';

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
export default NavigationEmployee;