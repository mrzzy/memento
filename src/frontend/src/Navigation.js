import React from 'react';
import './App.css';
import { DeleteOrg, CreateOrg, GETOrg, GETUsers, CreateUsers, CreateTasks, GETTasks } from './iamAPI.js';

function NavigationEmployee() {
    return (
        <ul className="navigationBar">
            <li className="headerLogo"><a href="#">M</a></li>
            <li><a href="#">Home</a></li>
            <li><a href="#">My Tasks</a></li>
            <li><a href="#">Notes</a></li>
            <button onClick={CreateOrg}>Create</button>
            <button onClick={GETOrg}>GET</button>
            <button onClick={DeleteOrg}>Delete</button>
            <button onClick={CreateUsers}>Create user</button>
            <button onClick={GETUsers}>Get user</button>
            <button onClick={CreateTasks}>create tasks</button>
            <button onClick={GETTasks}>Get tasks</button>
            <li><a href="#"><img className="signout" src="./signout.svg" alt="Sign out button" /></a></li>
        </ul>
    );
}
export default NavigationEmployee;