import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

class Login extends React.Component {
    state = { login: true, loggedIn: false, username: "", password: "", message: "" };

    switchToSignup = () => this.setState({ login: false });
    switchToLogin = () => this.setState({ login: true });

    handleLogin = (e) => {
        // run some stuff. still not sure how to keep users logged in
        let employee = ["employee", "pass"];
        let employer = ["employer", "pass"];

        if (this.state.username == employee[0]) {
            if (this.state.password == employee[1]) {
                sessionStorage.setItem("loggedIn", "true");
                sessionStorage.setItem("role", "employee");
                return <Redirect to="/employee" />
            }

            else
                this.setState({ message: "Incorrect username or password!" });
        }

        else if (this.state.username == employer[0]) {
            if (this.state.password == employer[1]) {
                sessionStorage.setItem("loggedIn", "true");
                sessionStorage.setItem("role", "employer");
                return <Redirect to="/employer" />
            }

            else
                this.setState({ message: "Incorrect username or password!" });
        }

        else
            this.setState({ message: "Incorrect username or password!" });

        e.preventDefault();
    }

    handlePasswordChange = (e) => this.setState({ "password": e.target.value });

    handleUsernameChange = (e) => this.setState({ "username": e.target.value });

    render() {
        if (sessionStorage.getItem("role") === "employee")
            return <Redirect to='/employee' />

        if (sessionStorage.getItem("role") === "employer")
            return <Redirect to='/employer' />

        return (
            <div>
                <NavigationVisitor />
                <div>
                    <button onClick={this.switchToLogin}>Login</button>
                    <button onClick={this.switchToSignup}>Sign up</button>

                    {(this.state.login ? <LoginSection
                        handleLogin={this.handleLogin}
                        handlePasswordChange={this.handlePasswordChange}
                        handleUsernameChange={this.handleUsernameChange} /> : <SignupSection />)}
                    {(sessionStorage.getItem("loggedIn") === "true"? <p>Logged in</p>:<p>Not Logged in</p>)}
                </div>

                <p>{this.state.message}</p>
            </div>
        );
    }
}

function LoginSection(props) {
    return (
        <form onSubmit={props.handleLogin}>
            <input
                required
                name="username"
                type="text"
                placeholder="Username"
                onChange={props.handleUsernameChange} />
            <input
                required
                type="password"
                placeholder="Password"
                onChange={props.handlePasswordChange} />
            <input type="submit" value="->" />
        </form>
    );
}

function SignupSection() {
    return (
        <form>
            <input required type="email" placeholder="Email" />
            <input required type="text" placeholder="Username" />
            <input required type="password" placeholder="Password" />
            <input type="submit" value="->" />
        </form>
    );
}

export default Login;
