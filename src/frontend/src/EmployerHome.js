import React from 'react';
import './App.css';
import './EmployerHome.css';
import { NavigationEmployer } from './Navigation';
import { Redirect } from 'react-router-dom';
import API from './API';

// Dummy data.

// Task object
/*
{
    "authorId": {{supervisor_id}},
    "completed": true,
    "deadline": "2099-11-11T11:51:53.334Z",
    "description": "Complete the fishing quota by going fishing",
    "duration": 3600,
    "name": "fishing"
}
 * */

/* Employee Object
 * "userId": {{employee_id}}
 * "name": Joel
 */

// date object with new Date(0), setMiliseconds to Date.parse("ISOstring")

var myemployees = [{ userId: 1, name: "John" }, { userId: 2, name: "Adel" }, { userId: 3, name: "Jessie" }, { userId: 4, name: "Guhesh" }];
var tasks = [
    { taskId: 2, userId: 1, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 3600, name: "Finish Project", description: "This is a test description to test out the front end." },
    { taskId: 3, userId: 3, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 3600, name: "Start next project", description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat" },
    { taskId: 4, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Sweep Some floors", description: "This is a test description to test out the front end." },
    { taskId: 5, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Make some wine", description: "This is a test description to test out the front end." },
    { taskId: 6, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Drink that coke", description: "This is a test description to test out the front end." },
];


class EmployerHome extends React.Component {

    constructor() {
        super();
        let filteredTasks = [];
        let employees = {}
        for (let i = 0; i < tasks.length; i++) {
            let stringDate = tasks[i].deadline;
            let mili = Date.parse(stringDate);
            let taskDeadline = new Date(0);
            taskDeadline.setMilliseconds(mili);

            let today = new Date();

            if (taskDeadline.getDate() === today.getDate())
                filteredTasks.push(tasks[i])
        }

        for (let i = 0; i < myemployees.length; i++) {
            employees[myemployees[i]["userId"]] = myemployees[i]["name"];
        }

        const api = new API();

        this.state = { api: api, tasks: filteredTasks, employees: employees };
    }

    render() {
        if (this.state.api.authCheck() === null)
            return <Redirect to='/' />

        return (
            <div>
                <NavigationEmployer />
                <h1 className="pagetitle">HOME</h1>
                <Calendar />
                <AllEmployeesTasks tasks={this.state.tasks} employees={this.state.employees} />
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

class AllEmployeesTasks extends React.Component {
    deadline = (dateString) => {
        let date = new Date(0);
        let mili = Date.parse(dateString);
        date.setMilliseconds(mili);
        let minutes = date.getMinutes().toString();
        if (minutes.length === 1)
            minutes = "0" + minutes;
        let deadline = "" + date.getHours() + ":" + minutes;
        return deadline;
    }

    render() {
        const tasks = this.props.tasks.map((task) =>
                <div className="employeeTask" key={task.taskId}>
                    <div className="profile">
                        <img src="./anon.png" alt="Employee Profile Pic" />
                        <span className="userName">{this.props.employees[task.userId]}</span>
                    </div>

                    <div className="description">
                        <span className="taskName">{task.name}</span>
                        <p>{task.description}</p>
                    </div>
                    <span className="deadline">{this.deadline(task.deadline)}</span>
                </div>
        );

        return (
            <div>
                <h2 className="sectionTitle">Employees' Tasks</h2>
                {tasks}
            </div>
        );
    }
}

export default EmployerHome;