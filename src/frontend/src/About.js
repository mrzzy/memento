import React from 'react';
import './App.css';
import './About.css';
import { NavigationVisitor } from './Navigation';
import { Redirect } from 'react-router-dom';

class About extends React.Component {
    render() {
        if (sessionStorage.getItem("role") === "employee")
            return <Redirect to='/employee' />

        else if (sessionStorage.getItem("role") === "employer")
            return <Redirect to='/employer' />

        return (
            <div>
                <NavigationVisitor />
                <div className="contain">
                <section className="banner-container" style={{backgroundImage:"url(./aboutIMG.png)"}}>
                <div className="banner" >
                        <div className="banner-txt">
                            <h2>Memento</h2>
                            <p>Memento, here for those with ASD who have troubles with switching focus between tasks. 
                            Our Team created Jack In The Box to serve as a reminder device. </p>
                        </div>
                        
                    </div>
                </section>

                    <section className="about-container">
                    <div className="aboutbox" style={{backgroundImage:"url(./aboutrasp1.webp)"}}>
                        <div className="box-text">
                            <h2>Jack In The Box</h2>
                            <p>We use Raspberry Pi as a reminder device that grabs the user’s attention 
                            and gives them the next task. Unlike other textually based reminder apps</p>
                        </div>
                    </div> 
                    </section> 
                <footer>
                <h1> &copy; TRUE MVP ZHAN YAN</h1>
                    <p> &copy; Adeline Ana Guhesh Jun Ye </p>
                </footer>
                </div>
            </div>
        );
    }
}

export default About;

