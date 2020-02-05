import React from 'react';
import './App.css';
import './EmployerHome.css';
import { NavigationEmployer } from './Navigation';
import { Redirect } from 'react-router-dom';
import API from './API';
import APIHelpers from './APIHelpers';

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

let testDate = new Date();
testDate.setHours(12, 30);

var myemployees = [{ userId: 1, name: "John" }, { userId: 2, name: "Adel" }, { userId: 3, name: "Jessie" }, { userId: 4, name: "Guhesh" }];
var tasks = [
    { taskId: 2, userId: 1, completed: false, deadline: testDate.toISOString(), duration: 3600, name: "Finish Project", description: "This is a test description to test out the front end." },
    { taskId: 3, userId: 3, completed: false, deadline: testDate.toISOString(), duration: 3600, name: "Start next project", description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat" },
    { taskId: 4, userId: 4, completed: false, deadline: testDate.toISOString(), duration: 36000, name: "Sweep Some floors", description: "This is a test description to test out the front end." },
    { taskId: 5, userId: 4, completed: false, deadline: testDate.toISOString(), duration: 36000, name: "Make some wine", description: "This is a test description to test out the front end." },
    { taskId: 6, userId: 4, completed: false, deadline: testDate.toISOString(), duration: 36000, name: "Drink that coke", description: "This is a test description to test out the front end." },
];


class EmployerHome extends React.Component {

    constructor() {
        super();
        //let filteredTasks = [];
        //let employees = {}
        //for (let i = 0; i < tasks.length; i++) {
        //    let stringDate = tasks[i].deadline;
        //    let mili = Date.parse(stringDate);
        //    let taskDeadline = new Date(0);
        //    taskDeadline.setMilliseconds(mili);

        //    let today = new Date();

        //    if (taskDeadline.getDate() === today.getDate())
        //        filteredTasks.push(tasks[i])
        //}

        //for (let i = 0; i < myemployees.length; i++) {
        //    employees[myemployees[i]["userId"]] = myemployees[i]["name"];
        //}

        const api = new API();
        const apiHelper = new APIHelpers(api);
        this.popUpElement = React.createRef(); 

        this.state = { api: api, apiHelper: apiHelper, tasks: null, employees: null };
    }

    async componentDidMount() {
        try {
            const loggedIn = await this.state.api.authCheck();
            const channel = await this.state.apiHelper.getChannel(loggedIn);
            this.state.api.subscribe(channel, this.wsHandler);
            let redirectToEmployee = await this.state.apiHelper.isEmployer(loggedIn);
            this.settingUp(loggedIn)
                .then(details => {
                    this.setState({
                        tasks: details[0],
                        employees: details[1],
                        userId: loggedIn,
                        redirectToEmployee: !redirectToEmployee
                    });
                })

        } catch (e) {
            console.error(e);
            if (this.state.userId !== null)
                this.setState({ userId: null });
        }
    }

    wsHandler = (notify) => {
        console.log("Logging notify...")
        console.log(notify);
        let tasks = [...this.state.tasks];
        if (notify.scope === "task") {
            if (notify.subject === "completed") {
                this.settingUp(this.state.userId)
                    .then(details => {
                        for (let task of this.state.tasks) {
                            if (task.id !== notify.scopeTarget)
                                continue;
                            this.openPopUp(this.state.employees[task.userId], task.name);
                        }
                        this.setState({
                            tasks: details[0],
                            employees: details[1]
                        });
                    })
            }

            else if (notify.subject === "started") {
                let tempTaskList = [...this.state.tasks];
                for (let i = 0; i < tempTaskList.length; i++) {
                    if (tempTaskList[i].id !== notify.scopeTarget)
                        continue;
                    tempTaskList[i].started = true;
                    break;
                }

                this.setState({ tasks: tempTaskList });
            }
        }
    }

    async settingUp(loggedIn) {
        /* taskId: 2
         * userId: 1
         * completed: false
         * deadline: ""
         * duration: 3600
         * name: "Finish Project"
         * description: "This is a test description to test out the front end." */

        let filteredTasks = []; // array of tasks
        let employees = {}; // id: name

        const manages = await this.state.api.query("manage", { "manager": loggedIn });
        const employeeIds = await manages.map((manage) => manage.match(/[0-9]+/)[0]); // returns list of employeeIds
        let myEmployees = [];
        for (const id of employeeIds) {
            let user = await this.state.api.get("user", id)
            myEmployees.push({ userId: parseInt(id), name: user.name });
        }

        let tasks = {};
        let date = new Date();

        for (const employee of myEmployees) {
            let taskIds = await this.state.apiHelper.getTasks(employee.userId);

            for (const taskId of taskIds) {
                let task = await this.state.api.get("task", taskId);

                let taskDate = new Date(0);
                taskDate.setMilliseconds(Date.parse(task.deadline));

                if (taskDate.getDate() == date.getDate() && !task.completed) {
                    task.id = taskId;
                    task.userId = employee.userId;
                    filteredTasks.push(task);
                }
            }
        }

        for (let i = 0; i < myEmployees.length; i++) {
            employees[myEmployees[i].userId] = myEmployees[i].name;
        }

        return [filteredTasks, employees];
    }

    openPopUp = (name, task) => this.popUpElement.current.setState({ visible: true, name: name, task: task }); // To create pop up notification when time is up

    render() {
        if (this.state.userId === null)
            return <Redirect to='/' />
        else if (this.state.redirectToEmployee)
            return <Redirect to='/employee' />

        return (
            <div>
                <NavigationEmployer />
                <h1 className="pagetitle">HOME</h1>
                <Calendar />
                <AllEmployeesTasks tasks={this.state.tasks} employees={this.state.employees} />
                <PopUp ref={this.popUpElement} />
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
        let tasks;
        if (this.props.tasks !== null) {
            tasks = this.props.tasks.map((task) =>
                <div className="employeeTask" key={task.id}>
                    <div className="profile">
                        <img
                            src={(this.props.employees[task.userId] === "Adeline") ? "adeline.jpg" : "./anon.png"}
                            alt="Employee Profile Pic"
                            className="employeePic" />
                        <span className="userName">{this.props.employees[task.userId]}</span>
                    </div>

                    <div className="description">
                        <span className="taskName">{task.name}</span>
                        <p>{task.description}</p>
                    </div>
                    <span className="deadline">{this.deadline(task.deadline)}</span>
                    <img style={{ width: "90px" }} src={task.started ? "./workingon.png" : "tobecompleted.png"} />
                </div>
            );
        }

        else
            tasks = null;

        return (
            <div>
                <h2 className="sectionTitle">Employees' Tasks</h2>
                {(tasks === null) ? <p style={{marginLeft:"10vw"}}>Loading...</p> : tasks}
            </div>
        );
    }
}

class PopUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = { visible: this.props.visible, name: "", task: "" };
        this.closeMe = this.closeMe.bind(this);
    }

    closeMe() {
        this.setState({ visible: false, name: "", task: "" });
    }

    render() {
        if (this.state.visible) {
            return (
                <div className="popUpBackground">
                    <div className="popUp">
                        <h1>{this.state.name} Completed<br />a Task</h1>
                        <span>{this.state.name} completed "{this.state.task}".</span>
                        <div className="buttonDiv">
                            <button onClick={this.closeMe}>Okay</button>
                        </div>
                    </div>
                </div>
            );
        }

        return null;
    }
}

export default EmployerHome;