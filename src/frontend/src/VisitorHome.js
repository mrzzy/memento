import React from 'react';
import './App.css';
import { NavigationVisitor } from './Navigation';

class VisitorHome extends React.Component {
    render() {
        return (
            <div>
                <NavigationVisitor />
                <img src="./visitorhomebg.png" alt="Home Page" style={{height: "70vh", margin: "auto", display: "block"}} />
            </div>
        );
    }
}

export default VisitorHome;

