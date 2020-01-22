import React from 'react';
import { render } from 'react-dom';
import './index.css';
import EmployeeHome from './EmployeeHome';
import EmployerHome from './EmployerHome';
import VisitorHome from './VisitorHome';
import About from './About';
import Login from './Login';
import CreateData from './CreateData';
import * as serviceWorker from './serviceWorker';
import { Route, BrowserRouter as Router } from 'react-router-dom';

if (sessionStorage.getItem("loggedIn") === null) {
    sessionStorage.setItem("loggedIn", "false");
}

if (sessionStorage.getItem("role") === null) {
    sessionStorage.setItem("role", "");
}


const routing = (
    <Router>
        <Route exact path="/" component={VisitorHome} />
        <Route path="/about" component={About} />
        <Route path="/employee" component={EmployeeHome} />
        <Route path="/employer" component={EmployerHome} />
        <Route path="/login" component={Login} />
    </Router>
)

render(routing, document.getElementById('root'));


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
