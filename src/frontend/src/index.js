import React from 'react';
import { render } from 'react-dom';
import './index.css';
import EmployeeHome from './EmployeeHome';
import VisitorHome from './VisitorHome';
import Login from './Login';
import { NavigationEmployee, NavigationVisitor } from './Navigation';
import CreateData from './CreateData';
import * as serviceWorker from './serviceWorker';
import { Route, BrowserRouter as Router } from 'react-router-dom';

if (localStorage.getItem("loggedIn") === null) {
    localStorage.setItem("loggedIn", "false");
}


const routing = (
    <Router>
        {(localStorage.getItem("loggedIn") === "true")? <NavigationEmployee /> : <NavigationVisitor />}
        <Route exact path="/" component={VisitorHome} />
        <Route path="/about" component={VisitorHome} />
        <Route path="/employee" component={EmployeeHome} />
        <Route path="/login" component={Login} />
    </Router>
)

render(routing, document.getElementById('root'));


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
