import React from 'react';
import './App.css';
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
                <div>
                    <button onClick={this.switchToLogin}>Login</button>
                    <button onClick={this.switchToSignup}>Sign up</button>

                    {(this.state.login ? <LoginSection handleLogin={this.handleLogin} /> : <SignupSection />)}
                    {(localStorage.getItem("loggedIn") === "true"? <p>Logged in</p>:<p>Not Logged in</p>)}
                </div>
            </div>
        );
    }
}

function LoginSection(props) {
    return (
        <form onSubmit={props.handleLogin}>
            <input required type="text" placeholder="Username"/>
            <input required type="password" placeholder="Password" />
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