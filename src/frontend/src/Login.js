import React from 'react';
import './Login.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

class Login extends React.Component {
    state = { login: true, loggedIn: false };

    switchToSignup = () => this.setState({ login: false });
    switchToLogin = () => this.setState({ login: true });

    handleLogin = () => {
        // run some stuff. still not sure how to keep users logged in
        localStorage.setItem("loggedIn", "true");
        this.setState({login: true})
    }

    render() {
        if (localStorage.getItem("loggedIn") === "true")
            return <Redirect to='/employee' />
        return (
            <div>
                <NavigationVisitor />
                <div class="container">
                    <button class="content btn" id="loginbtn" onClick={this.switchToLogin}>Login</button>
                    <button class="content btn" id="signupbtn" onClick={this.switchToSignup}>Sign up</button>
                    {(this.state.login ? <LoginSection  handleLogin={this.handleLogin} /> : <SignupSection />)}
                </div>
            </div>
        );
    }
}

function LoginSection(props) {
    return (
        <form class="content forms" onSubmit={props.handleLogin}>
            <input  class="inputTxt" required type="text" placeholder="Username"/>
            <input class="inputTxt" required type="password" placeholder="Password" />
            <input class="submitbtn"type="submit" value=">" />
        </form>
    );
}

function SignupSection() {
    return (
        <form class="content forms">
            <input class="inputTxt" required type="email" placeholder="Email" />
            <input class="inputTxt" required type="text" placeholder="Username" />
            <input class="inputTxt" required type="password" placeholder="Password" />
            <input class="submitbtn" type="submit" value="->" />
        </form>
    );
}

export default Login;
