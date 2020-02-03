import React from 'react';
import './Login.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

import API from './API';
import APIHelpers from './APIHelpers';

class Login extends React.Component {
    constructor() {
        super();
        const api = new API();
        const apiHelper = new APIHelpers(api);
        this.state = {
            login: true,
            loggedIn: false,
            username: "",
            password: "",
            message: "",
            api: api,
            apiHelper: apiHelper,
            employer: false,
            employee: false
        };
        this.handleLogin = this.handleLogin.bind(this);
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

    switchToSignup = () => this.setState({ login: false, message: "" });
    switchToLogin = () => this.setState({ login: true });

    async handleLogin (e) {
        // run some stuff. still not sure how to keep users logged in
        //let employee = ["employee", "pass"];
        //let employer = ["employer", "pass"];
        e.preventDefault();
        const hasLogin = await this.state.api.login(this.state.username, this.state.password);
        if (hasLogin) {
            try {
                let id = await this.state.api.authCheck();
                let hasEmployees = await this.state.apiHelper.isEmployer(id);
                this.setState({ employee: !hasEmployees, employer: hasEmployees });
            } catch (e) {
                console.error(e);
            } finally {
                this.setState({ message: "Something has gone wrong! Please try again later." });
            }
        }

        else
            this.setState({ message: "Incorrect username or password!" });

        
    }

    handlePasswordChange = (e) => this.setState({ "password": e.target.value });

    handleUsernameChange = (e) => this.setState({ "username": e.target.value });

    render() {
        //if (this.state.api.authCheck() !== null)
        //    return <Redirect to='/employee' />

        if (this.state.employee)
            return <Redirect to="/employee" />;

        if (this.state.employer)
            return <Redirect to="/employer" />;

        return (
            <div>
                <NavigationVisitor />
                <div className="container">
                    <button className="content btn" id="loginbtn" onClick={this.switchToLogin}>Login</button>
                    <button className="content btn" id="signupbtn" onClick={this.switchToSignup}>Sign up</button>

                    {(this.state.login ? <LoginSection
                        handleLogin={this.handleLogin}
                        handlePasswordChange={this.handlePasswordChange}
                        handleUsernameChange={this.handleUsernameChange} /> : <SignupSection />)}
                    <p style={{ color: "red" }}>{this.state.message}</p>
                </div>
            </div>
        );
    }
}

function LoginSection(props) {
    return (
        <form className="content forms" onSubmit={props.handleLogin}>
            <input
                required
                className="inputTxt"
                name="username"
                type="text"
                placeholder="Username"
                onChange={props.handleUsernameChange} />
            <input
                required
                className="inputTxt"
                type="password"
                placeholder="Password"
                onChange={props.handlePasswordChange} />
            <input className="submitbtn" type="submit" value=">" />
        </form>
    );
}

function SignupSection() {
    return (
        <form className="content forms">
            <input className="inputTxt" required type="email" placeholder="Email" />
            <input className="inputTxt" required type="text" placeholder="Username" />
            <input className="inputTxt" required type="password" placeholder="Password" />
            <input className="submitbtn" type="submit" value=">" />
        </form>
    );
}

export default Login;
