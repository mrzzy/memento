import React from 'react';
import './App.css';
import './MyEmployees.css';
import { NavigationEmployer } from './Navigation';
import { Redirect } from 'react-router-dom';
import API from './API';
import APIHelpers from './APIHelpers';
import { type } from 'os';

// Dummy data.
// Converting from ISOString to date object. new Date(0), setMiliseconds to Date.parse("ISOstring")

var myemployees = [{ userId: 1, name: "John" }, { userId: 2, name: "Adel" }, { userId: 3, name: "Jessie" }, { userId: 4, name: "Guhesh" }];
var tasks = [
    { taskId: 2, userId: 1, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 3600, name: "Finish Project", description: "This is a test description to test out the front end." },
    { taskId: 3, userId: 3, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 3600, name: "Start next project", description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat" },
    { taskId: 4, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Sweep Some floors", description: "This is a test description to test out the front end." },
    { taskId: 5, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Make some wine", description: "This is a test description to test out the front end." },
    { taskId: 6, userId: 4, completed: false, deadline: "2020-01-30T04:30:05.244Z", duration: 36000, name: "Drink that coke", description: "This is a test description to test out the front end." },
];

class MyEmployees extends React.Component {

    constructor() {
        super();

        // [filteredTasks, employees, employeeToTask]
        //let details = this.settingUp();
        const api = new API();
        const apiHelper = new APIHelpers(api);
        this.createTask = this.createTask.bind(this);

        this.state = {
            tasks: [],
            employees: [],
            employeeToTask: [],
            myEmployees: null,
            activated: -1,
            popUp: null,
            newTask: {},
            api: api,
            apiHelper: apiHelper
        };
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
                        employeeToTask: details[2],
                        myEmployees: details[3],
                        userId: loggedIn,
                        redirectToEmployee: !redirectToEmployee
                    });
                })

        } catch (e) {
            if (this.state.userId !== null)
                this.setState({ userId: null });
        }
    }

    // Obtaining data and sorting it out again
    async settingUp(loggedIn) {
        let filteredTasks = []; // array of tasks
        let employees = {}; // id: name
        let employeeToTask = {}; // id: task

        const manages = await this.state.api.query("manage", { "manager": loggedIn });
        const employeeIds = await manages.map((manage) => manage.match(/[0-9]+/)[0]); // returns list of employeeIds
        let myEmployees = [];
        for (const id of employeeIds) {
            let user = await this.state.api.get("user", id)
            myEmployees.push({ userId: parseInt(id), name: user.name });
        }

        let tasks = [];
        
        for (const employee of myEmployees) {
            let taskIds = await this.state.apiHelper.getTasks(employee.userId);

            for (const taskId of taskIds) {
                let task = await this.state.api.get("task", taskId);
                task.id = taskId;
                task.userId = employee.userId;
                tasks.push(task);
            }
        }

        for (let i = 0; i < tasks.length; i++) {
            let stringDate = tasks[i].deadline;
            let mili = Date.parse(stringDate);
            let taskDeadline = new Date(0);
            taskDeadline.setMilliseconds(mili);

            let today = new Date();

            if (taskDeadline.getDate() === today.getDate() && !tasks[i].completed) {
                filteredTasks.push(tasks[i]);
                if (employeeToTask[tasks[i].userId] === undefined) {
                    employeeToTask[tasks[i].userId] = [tasks[i]]
                }

                else
                    employeeToTask[tasks[i].userId].push(tasks[i]);
            }
        }

        for (let i = 0; i < myEmployees.length; i++) {
            employees[myEmployees[i].userId] = myEmployees[i].name;
        }

        return [filteredTasks, employees, employeeToTask, myEmployees];
    }

    wsHandler = (notify) => {
        console.log("Logging notify...");
        console.log(notify);
        if (notify.scope === "task") {
            if (notify.subject === "completed") {
                this.settingUp(this.state.userId)
                    .then(details => {
                        this.setState({ tasks: details[0] });
                    })
            }
        }
    }

    // change "30-12-2020" to date object
    parseDate(sD, sT) {
        let b = sD.split(/\D/);
        let deadline = new Date(b[0], --b[1], b[2]);
        let a = sT.split(/\D/);
        deadline.setHours(a[0]);
        deadline.setMinutes(a[1]);

        return deadline;
    }

    showMore = (employee, e) => {
        this.setState({ activated: employee["userId"] });
    }

    onChange = (e) => {
        let newTask = this.state.newTask;
        if (e.target.name === "duration")
            newTask[e.target.name] = e.target.value * 60;
        else
            newTask[e.target.name] = e.target.value;
        this.setState({ newTask: newTask });
    }

    async createTask(employee, e) {
        //{ taskId: 2, userId: 1, completed: false, deadline: ISOString, duration: 3600, name: "", description: "" },
        // employee.userId
        e.preventDefault();
        let newTask = {};
        //newTask["completed"] = false;
        //newTask["userId"] = employee.userId;
        newTask["authorId"] = this.state.userId;
        newTask["deadline"] = this.parseDate(this.state.newTask["deadlineDate"], this.state.newTask["deadlineTime"]).toISOString();
        newTask["duration"] = this.state.newTask["duration"];
        newTask["name"] = this.state.newTask["taskTitle"];
        newTask["description"] = this.state.newTask["taskDesc"];

        const responseTask = await this.state.api.post("task", newTask);
        const newAssign = { kind: "task", itemId: responseTask.id, assigneeId: employee.userId, assignerId: this.state.userId };
        await this.state.api.post("assign", newAssign);

        let details = await this.settingUp(this.state.userId);

        this.setState({
            popUp: false,
            activated: -1,
            tasks: details[0],
            employees: details[1],
            employeeToTask: details[2],
            myemployees: myemployees
        });
    }

    addTaskPopUp = (employee, e) => {
        this.setState({
            popUp:
                <AddEmployeeTask
                    employeeId={employee["userId"]}
                    name={employee["name"]}
                    cancelPopUp={this.cancelPopUp}
                    onChange={this.onChange}
                    createTask={this.createTask.bind(null, employee)} />
        })
    }

    cancelPopUp = () => {
        this.setState({ popUp: null });
    }

    render() {
        if (this.state.userId === null)
            return <Redirect to='/' />
        else if (this.state.redirectToEmployee)
            return <Redirect to='/employee' />

        return (
            <div>
                <NavigationEmployer />
                <h1 className="pagetitle">MY EMPLOYEES</h1>
                <Calendar />
                <div>
                    {(this.state.myEmployees !== null)? this.state.myEmployees.map((employee) =>
                        <Employee
                            key={employee["userId"]}
                            tasks={(this.state.employeeToTask[employee["userId"]] === undefined) ? [] : this.state.employeeToTask[employee["userId"]]}
                            name={employee["name"]}
                            employeeId={employee["userId"]}
                            showMore={this.showMore.bind(null, employee)}
                            addTaskPopUp={this.addTaskPopUp.bind(null, employee)}
                            showTasks={(this.state.activated === employee["userId"]) ? true : false} />
                    ) : <p style={{ marginLeft: "10vw" }}>Loading...</p>}
                </div>
                {this.state.popUp}
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

class Employee extends React.Component {
    // props:tasks list, employee name, employee id, showTasks

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

    tasks = () => {
        this.setState({ tasks: tasks });
    }

    render() {
        const tasks = this.props.tasks.map((task) =>
            <div className="aTask" key={task.id}>
                <div className="details">
                    <span className="taskTitle">{task.name}</span>
                    <span className="taskDesc">{task.description}</span>
                </div>
                <span className="deadline">{this.deadline(task.deadline)}</span>
            </div>
        );

        return (
            <div onClick={this.props.showMore} className="employee">
                <div className="employeeTop">
                    <img src="./anon.png" alt="Employee Profile Pic" />
                    <h3>{this.props.name}</h3>
                    <span className="numTasks">{this.props.tasks.length} Task(s) <span>left</span></span>
                </div>

                {(this.props.showTasks) ?
                    <div className="aTaskList">
                        <button onClick={this.props.addTaskPopUp}>Add Task</button>
                        {tasks}
                    </div> :
                    null}
            </div>
        );
    }
}

class AddEmployeeTask extends React.Component {
    // props: employeeId, name

    render() {
        return (
            <div className="popUp">
                <button className="btnX" onClick={this.props.cancelPopUp}>X</button>
                <h2>Task For <span className="popUpName">{this.props.name}</span></h2>
                <form onSubmit={this.props.createTask}>
                    <input onChange={this.props.onChange} className="forminput" id="taskTitle" type="text" name="taskTitle" placeholder="TITLE" required />
                    <input onChange={this.props.onChange} className="forminput" id="taskDesc" type="text" name="taskDesc" placeholder="DESCRIPTION" required />
                    <input onChange={this.props.onChange} className="forminput" type="date" name="deadlineDate" required />
                    <input onChange={this.props.onChange} className="forminput" type="time" id="deadlineTime" name="deadlineTime" min="09:00" max="18:00" required />
                    <input onChange={this.props.onChange} className="forminput" type="number" name="duration" min="1" max="1000" />
                    <input type="submit" value=">" />
                </form>
            </div>
        );
    }
}

export default MyEmployees;
