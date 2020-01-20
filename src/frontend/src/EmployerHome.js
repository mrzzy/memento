import React from 'react';
import './App.css';
import { NavigationEmployer } from './Navigation';
import { Redirect } from 'react-router-dom';

class EmployerHome extends React.Component {

    render() {
        if (localStorage.getItem("role") === "employee")
            return <Redirect to="/employee" />

        else if (localStorage.getItem("role") === "")
            return <Redirect to="/" />

        return (
            <div>
                <NavigationEmployer />
                <h1 className="pagetitle">HOME</h1>
                <Calendar />
                <AllEmployeesTask />
            </div>
        );
	}
}

class Calendar extends React.Component {
    constructor() {
        super()
        this.state = { daysLeftList: [] };
        this.getDayOfDate = this.getDayOfDate.bind(this);
    }

    componentDidMount() {
        let date = new Date(); // for today's date
        let time = new Date(date.getTime()); // to get the date of the first day of the next month
        time.setMonth(date.getMonth() + 1);
        time.setDate(0);

        let daysLeft = (time.getDate() > date.getDate() ? time.getDate() - date.getDate() : 0); // get the no. days of the month left
        let ans = [];
        for (let i = date.getDate(); i <= (date.getDate() + daysLeft); i++) {
            ans.push(i); // get the days of the month left
        }

        this.setState({ daysLeftList: ans });
    }

    getDayOfDate(day) {
        let date = new Date();
        date.setDate(day);
        let dayNo = date.getDay();
        switch (dayNo) {
            case 0:
                return "SUN";
            case 1:
                return "MON";
            case 2:
                return "TUE";
            case 3:
                return "WED";
            case 4:
                return "THU";
            case 5:
                return "FRI";
            case 6:
                return "SAT";
        }
    }

    render() {
        return (
            <div className="calendar">
                {
                    this.state.daysLeftList.map(days => <div key={"calendar-" + days}><span className="calendarday">{this.getDayOfDate(days)}</span><span className="calendarnum">{days}</span></div>)
                }
            </div>
        );
    }
}

class AllEmployeesTask extends React.Component {
    render() {
        return (
            <div>
                <h2>Employees' Tasks</h2>
            </div>
        );
    }
}

export default EmployerHome;