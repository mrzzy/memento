import React from 'react';
import { render } from 'react-dom';
import './index.css';
import EmployeeHome from './EmployeeHome';
import EmployerHome from './EmployerHome';
import MyEmployee from './MyEmployees';
import VisitorHome from './VisitorHome';
import About from './About';
import Login from './Login';
import * as serviceWorker from './serviceWorker';
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom';

const routing = (
    <Router>
        <Switch>
            <Route exact path="/" component={VisitorHome} />
            <Route path="/about" component={About} />
            <Route path="/employee" component={EmployeeHome} />
            <Route path="/employer" component={EmployerHome} />
            <Route path="/my-employees" component={MyEmployee} />
            <Route path="/login" component={Login} />
        </Switch>
    </Router>
)

render(routing, document.getElementById('root'));


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
