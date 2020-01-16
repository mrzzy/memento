import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';

class Login extends React.Component {
    state = { login: true };

    switchToSignup = () => this.setState({ login: false });
    switchToLogin = () => this.setState({ login: true });

    render() {
        return (
            <div>
                <NavigationVisitor />
                <div>
                    <button onClick={this.switchToLogin}>Login</button>
                    <button onClick={this.switchToSignup}>Sign up</button>

                    {(this.state.login? <LoginSection /> : <SignupSection />)}
                </div>
            </div>
        );
    }
}

function LoginSection() {
    return (
        <form>
            <input required type="text" placeholder="Username"/>
            <input required type="password" placeholder="Password" />
            <input type="submit" value="->" />
        </form>
    );
}

function SignupSection() {
    return <p>Sign up</p>
}

export default Login;