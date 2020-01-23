import React from 'react';
import './App.css';
import './MyEmployees.css';
import { NavigationEmployer } from './Navigation';
import { Redirect } from 'react-router-dom';

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
    { taskId: 2, userId: 1, completed: false, deadline: "2020-01-26T11:55:51.569Z", duration: 3600, name: "Finish Project", description: "This is a test description to test out the front end." },
    { taskId: 3, userId: 3, completed: false, deadline: "2020-01-23T02:20:00.115Z", duration: 3600, name: "Start next project", description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat" },
    { taskId: 4, userId: 4, completed: false, deadline: "2020-01-23T02:00:00.115Z", duration: 36000, name: "Sweep Some floors", description: "This is a test description to test out the front end." },
    { taskId: 5, userId: 4, completed: false, deadline: "2020-01-23T03:30:00.115Z", duration: 36000, name: "Make some wine", description: "This is a test description to test out the front end." },
    { taskId: 6, userId: 4, completed: false, deadline: "2020-01-23T04:20:00.115Z", duration: 36000, name: "Drink that coke", description: "This is a test description to test out the front end." },
];

class MyEmployees extends React.Component {

    constructor() {
        super();

        // [filteredTasks, employees, employeeToTask]
        let details = this.settingUp();

        this.state = {
            tasks: details[0],
            employees: details[1],
            employeeToTask: details[2],
            myemployees: myemployees,
            activated: -1,
            popUp: null,
            newTask: {}
        };
    }

    // Obtaining data and sorting it out again
    settingUp() {
        let filteredTasks = []; // array of tasks
        let employees = {}; // id: name
        let employeeToTask = {}; // id: task

        for (let i = 0; i < tasks.length; i++) {
            let stringDate = tasks[i].deadline;
            let mili = Date.parse(stringDate);
            let taskDeadline = new Date(0);
            taskDeadline.setMilliseconds(mili);

            let today = new Date();

            if (taskDeadline.getDate() == today.getDate()) {
                filteredTasks.push(tasks[i]);
                if (employeeToTask[tasks[i].userId] === undefined) {
                    employeeToTask[tasks[i].userId] = [tasks[i]]
                }

                else
                    employeeToTask[tasks[i].userId].push(tasks[i]);
            }
        }

        for (let i = 0; i < myemployees.length; i++) {
            employees[myemployees[i]["userId"]] = myemployees[i]["name"];
        }

        return [filteredTasks, employees, employeeToTask];
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
        newTask[e.target.name] = e.target.value;
        this.setState({ newTask: newTask });
    }

    createTask = (employee, e) => {
        //{ taskId: 2, userId: 1, completed: false, deadline: ISOString, duration: 3600, name: "", description: "" },
        let newTask = {};
        newTask["completed"] = false;
        newTask["taskId"] = Math.floor(Math.random() * 100); // testing purposes only
        newTask["userId"] = employee.userId;
        newTask["deadline"] = this.parseDate(this.state.newTask["deadlineDate"], this.state.newTask["deadlineTime"]).toISOString();
        newTask["duration"] = this.state.newTask["duration"];
        newTask["name"] = this.state.newTask["taskTitle"];
        newTask["description"] = this.state.newTask["taskDesc"];

        tasks.push(newTask);
        let details = this.settingUp();

        e.preventDefault();

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
        if (sessionStorage.getItem("role") === "employee")
            return <Redirect to="/employee" />

        else if (sessionStorage.getItem("role") === "")
            return <Redirect to="/" />

        return (
            <div>
                <NavigationEmployer />
                <h1 className="pagetitle">MY EMPLOYEES</h1>
                <Calendar />
                <div>
                    {this.state.myemployees.map((employee) =>
                        <Employee
                            key={employee["userId"]}
                            tasks={(this.state.employeeToTask[employee["userId"]] === undefined) ? [] : this.state.employeeToTask[employee["userId"]]}
                            name={employee["name"]}
                            employeeId={employee["userId"]}
                            showMore={this.showMore.bind(null, employee)}
                            addTaskPopUp={this.addTaskPopUp.bind(null, employee)}
                            showTasks={(this.state.activated == employee["userId"]) ? true : false} />
                    )}
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
        if (minutes.length == 1)
            minutes = "0" + minutes;
        let deadline = "" + date.getHours() + ":" + minutes;
        return deadline;
    }

    tasks = () => {
        this.setState({ tasks: tasks });
    }

    render() {
        const tasks = this.props.tasks.map((task) =>
            <div className="aTask" key={task.taskId}>
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
                    <img src="./anon.png" alt="Employee Picture" />
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
                <button onClick={this.props.cancelPopUp}>X</button>
                <h2>Task For <span className="popUpName">{this.props.name}</span></h2>
                <form onSubmit={this.props.createTask}>
                    <input onChange={this.props.onChange} id="taskTitle" type="text" name="taskTitle" placeholder="TITLE" required />
                    <input onChange={this.props.onChange} id="taskDesc" type="text" name="taskDesc" placeholder="DESCRIPTION" required />
                    <input onChange={this.props.onChange} type="date" name="deadlineDate" required />
                    <input onChange={this.props.onChange} type="time" id="deadlineTime" name="deadlineTime" min="09:00" max="18:00" required />
                    <input onChange={this.props.onChange} type="number" name="duration" min="1" max="240" />
                    <input type="submit" value=">" />
                </form>
            </div>
        );
    }
}

export default MyEmployees;
