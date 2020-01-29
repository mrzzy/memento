import React from 'react';
import { GETTaskFromUserId, UpdateTasks, CreateChannel, CreateNotification } from './iamAPI';
import './App.css';
import { NavigationEmployee } from './Navigation';
import { Redirect } from 'react-router-dom';

import API from './API';
import APIHelpers from './APIHelpers';

/* ----------------DUMMY DATA.---------------- */
// Used for testing when the server is down
const dummyTaskList = [
    {
        id: 0,
        name: "Pitch",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 60,
        completed: true
    },
    {
        id: 1,
        name: "Presentation",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 300,
        completed: false
    },
    {
        id: 2,
        name: "Pitch",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 60,
        completed: false
    },
    {
        id: 3,
        name: "Report Writing",
        description: "Create a report about our upcoming application.",
        duration: 3600,
        completed: false
    },
    {
        id: 4,
        name: "Create App",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 8649,
        completed: false
    },
    {
        id: 5,
        name: "Clean Up",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 5,
        completed: false
    },
    {
        id: 6,
        name: "Shift Boxes",
        description: "Start on storyboarding If you're visiting this page, you're likely here because you're searching for a random sentence",
        duration: 6,
        completed: false
    }
];


/* ----------------EMPLOYEE HOME---------------- */
class EmployeeHome extends React.Component {
    constructor() {
        super();
        this.state = { taskList: [] }
        this.taskListElement = React.createRef();
        const api = new API();
        /* To use for testing when the server is down
         * uncomment to see website with tasks */
        this.state = { taskList: dummyTaskList, api: api, apiHelpers: new APIHelpers(api) };
    }

    componentDidMount() {
        const self = this;
        // Default user id for testing.
        //GETTaskFromUserId(17)
        //    .then(tasks => {
        //        self.taskListElement.current.updateAllTasksList(tasks);
        //    });
    }

    render() {
        if (this.state.api.state.accessToken === null)
            return <Redirect to='/' />

        return (
            <div>
                <NavigationEmployee />
                <h1 className="pagetitle">HOME</h1>
                <Calendar />
                <TaskList allTasksList={this.state.taskList} ref={this.taskListElement} />
            </div>
        );
    }
}


 /* ----------------1. TOP TASK LIST.---------------- */
class TaskList extends React.Component {
    constructor(props) {
        super(props);
        this.updateCurrentTaskElement = this.updateCurrentTaskElement.bind(this);
        this.updateToDoListElement = this.updateToDoListElement.bind(this);
        this.secondsToHMS = this.secondsToHMS.bind(this);
        this.createPopUp = this.createPopUp.bind(this);

        // Getting reference to child to call their methods.
        this.toDoListElement = React.createRef(); 
        this.currentTaskElement = React.createRef(); 
        this.popUpElement = React.createRef(); 
    }

    updateCurrentTaskElement(task) {
        this.currentTaskElement.current.updateCurrentTask(task); // To update the current task component when a user starts a task
    }

    updateToDoListElement(id) {
        this.toDoListElement.current.updateCompletedTask(id); // To update the completed property of task object to true
    }

    updateAllTasksList(tasks) {
        this.toDoListElement.current.updateAllTasksList(tasks);
    }

    createPopUp() {
        this.popUpElement.current.setState({ visible: true }); // To create pop up notification when time is up
    }

    secondsToHMS(duration) {
        // Math.floor(equation) to get the integer part (e.g. 10 from 10.6)
        // % gets remainder of an equation.
        let hoursAndMin = Math.floor(duration / 60);
        let seconds = Math.floor(duration % 60);
        let hours = Math.floor(hoursAndMin / 60);
        let minutes = hoursAndMin % 60;
        return [hours, minutes, seconds];
    }
    
    render() {
        return (
            <div className="taskList">
                <ToDoList
                    allTasksList={this.props.allTasksList}
                    updateCurrentTaskElement={this.updateCurrentTaskElement}
                    secondsToHMS={this.secondsToHMS}
                    ref={this.toDoListElement} />
                <CurrentTask
                    ref={this.currentTaskElement}
                    updateToDoListElement={this.updateToDoListElement}
                    secondsToHMS={this.secondsToHMS}
                    createPopUp={this.createPopUp} />
                <PopUp
                    visible={false}
                    ref={this.popUpElement} />
            </div>
        );
    }
}


/* ----------------1.1 CALENDAR AT THE TOP.---------------- */
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

        this.setState({daysLeftList: ans});
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


/* ----------------1.2 TO DO LIST CONTAINING ALL THE TASKS---------------- */
class ToDoList extends React.Component {
    constructor(props) {
        super(props);
        this.state = { allTasksList: props.allTasksList, unfinishedTasksList: [], currentTaskNull: true};
        this.removeTask = this.removeTask.bind(this);
    }

    componentDidMount() {
        // To get all the tasks that have not been finished.
        let allTasksList = [...this.state.allTasksList];
        let unfinishedTasks = allTasksList.filter(task => task.completed === false);
        this.setState({ unfinishedTasksList: unfinishedTasks });
    }

    updateAllTasksList(tasks) {
        let unfinishedTasks = tasks.filter(task => task.completed === false);
        this.setState({ unfinishedTasksList: unfinishedTasks, allTasksList: tasks });
    }

    updateCompletedTask(id) {
        // Loop through the list of tasks to find the specific task.
        for (let i = 0; i < this.state.allTasksList.length; i++) {
            if (this.state.allTasksList[i].id === id) {
                let tempTaskList = [...this.state.allTasksList];
                tempTaskList[i].completed = true;
                this.setState({ allTasksList: tempTaskList, currentTaskNull: true });

                // update the task in the database
                UpdateTasks(tempTaskList[i]);
                break;
            }
        }
    }

    removeTask(id) {
        for (let i = 0; i < this.state.unfinishedTasksList.length; i++) {
            if (this.state.unfinishedTasksList[i].id === id) {
                let tempTaskList = [...this.state.unfinishedTasksList];
                let newCurrentTask = tempTaskList.splice(i, 1);
                this.setState({ unfinishedTasksList: tempTaskList, currentTaskNull: false });

                // Updating current task in CurrentTask component
                this.props.updateCurrentTaskElement(newCurrentTask[0]);
                break;
            }
        }
    }

    render() {
        return (
            <div className="toDoList">
                <h2>TO DO LIST</h2>
                {
                    this.state.unfinishedTasksList.map(task =>
                        <Task
                            key={task.id}
                            taskId={task.id}
                            name={task.name}
                            description={task.description}
                            duration={task.duration}
                            remove={this.removeTask}
                            secondsToHMS={this.props.secondsToHMS}
                            currentTaskNull={this.state.currentTaskNull} />)
                }
            </div>
        );
    }
}


/* ----------------1.2.1 Individual Tasks ----------------*/
class Task extends React.Component {
    constructor(props) {
        super(props);
        this.state = { name: props.name, description: props.description, duration: props.duration };
        this.startTask = this.startTask.bind(this);
    }

    startTask() {
        this.props.remove(this.props.taskId);
    }

    render() {
        let duration = this.props.secondsToHMS(this.state.duration);

        return (
            <div className="task">
                <div>
                    <h2>{this.state.name}</h2>
                    <p>{this.state.description}</p>
                </div>
                <div className="duration">{duration[0]}h {duration[1]}m</div>
                {this.props.currentTaskNull ? <button onClick={this.startTask}>START</button> : null}
            </div>
        );
    }
}


/* ----------------1.3 CURRENT TASK AT HAND---------------- */
class CurrentTask extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hour: null, minute: null, second: null, endTime: null, countDownTimer: null, currentTask: this.props.task };
        this.updateCountDown = this.updateCountDown.bind(this);
        this.updateCurrentTask = this.updateCurrentTask.bind(this);
        this.finishTask = this.finishTask.bind(this);
    }

    updateCountDown() {
        let now = new Date();
        let durationLeft = Math.floor(this.state.endTime - now.getTime()) / 1000;
        let timer = this.props.secondsToHMS(durationLeft);
        this.setState({ hour: timer[0], minute: timer[1], second: timer[2] });

        if (this.state.hour === 0 && this.state.minute === 0 && this.state.second === 0) {
            this.finishTask();
        }
    }

    updateCurrentTask(task) {
        let hms = this.props.secondsToHMS(task.duration);
        let endTiming = new Date().getTime() + (task.duration * 1000);
        let countDownTimerId = setInterval(this.updateCountDown, 200); // set for updateCountDown to be called every 200ms to ensure count down is smooth
        this.setState({ hour: hms[0], minute: hms[1], second: hms[2], endTime: endTiming, countDownTimer: countDownTimerId, currentTask: task });

        // To create a notification  for the raspberry pi
        let firingTime = new Date(endTiming).toISOString();
        CreateNotification(task, firingTime, 3);
    }

    finishTask() {
        this.props.updateToDoListElement(this.state.currentTask.id); // to update to do list component's allTaskList
        clearInterval(this.state.countDownTimer);
        this.setState({ hour: null, minute: null, second: null, endTime: null, countDownTimer: null, currentTask: null });
        this.props.createPopUp();
    }

    render() {
        // return the current task if they are working on one
        if (this.state.currentTask != null) {

            // The zero before each number (e.g. 08 : 23 : 03 ----> hours minute second)
            var zeroHour = (this.state.hour.toString().length > 1) ? "" : "0";
            var zeroMin = (this.state.minute.toString().length > 1) ? "" : "0";
            var zeroSec = (this.state.second.toString().length > 1) ? "" : "0";

            return (
                <div className="currentTask">
                    <h2>TASK OF THE DAY</h2>
                    <div className="currentTaskContent withTask">
                        <h2>{this.state.currentTask.name}</h2>
                        <p>{this.state.currentTask.description}</p>
                        <div className="countdown"><span className="countdownH">{zeroHour + this.state.hour}</span>:
                            <span className="countdownM">{zeroMin + this.state.minute}</span>:
                            <span className="countdownS">{zeroSec + this.state.second}</span></div>
                        <button className="underline" onClick={this.finishTask}>FINISHED</button>
                    </div>
                </div>
            );
        }

        // Display message saying to pick a task
        else {
            return (
                <div className="currentTask">
                    <h2>TASK OF THE DAY</h2>
                    <div className="currentTaskContent noTasks">
                        <h2>START A TASK</h2>
                        <p>THERE ARE NO TASK SELECTED</p>
                    </div>
                </div>
            );
        }

    }
}

/* ---------------------1.4 POP UP DIALOG--------------------- */
class PopUp extends React.Component {
    constructor(props) {
        super(props);
        this.state = { visible: this.props.visible };
        this.closeMe = this.closeMe.bind(this);
    }

    closeMe() {
        this.setState({ visible: false });
    }

    render() {
        if (this.state.visible) {
            return (
                <div className="popUpBackground">
                    <div className="popUp">
                        <h1>Task<br />Completed?</h1>
                        <span>Ms. Wong will be notified</span>
                        <div className="buttonDiv">
                            <button onClick={this.closeMe}>No</button>
                            <button onClick={this.closeMe}>Yes</button>
                        </div>
                    </div>
                </div>
            );
        }

        return null;
    }
}

export default EmployeeHome;
