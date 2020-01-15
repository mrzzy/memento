import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';

class Login extends React.Component {
    render() {
        return (
            <div>
                <NavigationVisitor />
                <div>
                    <button>USER</button>
                    <button>BOSS</button>
                </ div>
            </div>
        );
    }
}

export default Login;