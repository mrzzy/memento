import React from 'react';
import './App.css';
import {
    DeleteOrg, CreateOrg, GETOrg, GETUsers, GETUserFromId,
    CreateUsers, CreateTasks, GETTasks, CreateAssignment,
    GETAssignmentIds, GETAssignment, GETTaskFromUserId, UpdateTasks
} from './iamAPI.js';
import { assignmentExpression } from '@babel/types';

// This is for testing api functions purposes only. 
class CreateData extends React.Component {

    constructor(props) {
        super(props);

        // GET Methods
        this.getOrganisation = this.getOrganisation.bind(this);
        this.getUserIds = this.getUserIds.bind(this);
        this.getUserFromUserId = this.getUserFromUserId.bind(this);
        this.getTaskIds = this.getTaskIds.bind(this);
        this.getAssignmentIds = this.getAssignmentIds.bind(this);
        this.getAssignmentFromId = this.getAssignmentFromId.bind(this);

        // CREATE Methods
        this.createOrganisations = this.createOrganisations.bind(this);
        this.createUser = this.createUser.bind(this);
        this.createTasks = this.createTasks.bind(this);
        this.createAssigment = this.createAssigment.bind(this);

        //UPDATE Methods
        this.UpdateTasks = this.UpdateTasks.bind(this);

    }


    // GET Methods
    getOrganisation() {
        GETOrg().then(org => { document.getElementById("showId").innerHTML = "Organization Ids: " + org; })
    }

    getUserIds() {
        GETUsers().then(userId => { document.getElementById("showId").innerHTML = "User Ids: " + userId; })
    }

    getUserFromUserId() {
        let userId = document.getElementById("getUserFromUserId").value;
        GETUserFromId(userId).then(user => { console.log(user) });
    }

    getTaskIds() {
        GETTasks().then(taskIds => { document.getElementById("showId").innerHTML = "Task Ids: " + taskIds; })
    }

    getTasksFromUserId() {
        let userId = document.getElementById("getTasksUserId").value;
        GETTaskFromUserId(userId).then(tasks => { console.log(tasks) });
    }

    getAssignmentIds() {
        GETAssignmentIds().then(assignmentIds => { document.getElementById("showId").innerHTML = "Assignment Ids: " + assignmentIds; })
    }

    getAssignmentFromId() {
        let assignmentId = document.getElementById("getAssignmentFromId").value;
        GETAssignment(assignmentId).then(assignment => { document.getElementById("showId").innerHTML = "Assignment: " + JSON.stringify(assignment); });
    }


    // CREATE Methods
    createOrganisations() {
        let orgName = document.getElementById("createOrgName").value;
        console.log(orgName);
        CreateOrg(orgName);
    }

    createUser() {
        let userName = document.getElementById("createUserName").value;
        let pos = document.getElementById("posSelect").value;
        let userEmail = document.getElementById("createUserEmail").value;
        let organizationId = document.getElementById("createUserOrgId").value;

        const data = {
            kind: pos,
            name: userName,
            password: "P@ssw0rd",
            email: userEmail,
            orgId: organizationId
        }

        CreateUsers(data);
    }

    createTasks() {
        let taskName = document.getElementById("createTaskName").value;
        let des = document.getElementById("createTaskDes").value;
        let taskDuration = document.getElementById("createTaskDur").value;
        let author = document.getElementById("createTaskAuthorId").value;

        const data = {
            name: taskName,
            description: des,
            duration: taskDuration,
            deadline: '2019-12-30T09:39:25.954Z',
            authorId: author
        }

        CreateTasks(data);
    }

    createAssigment() {
        let itemId = document.getElementById("createAssignmentItemId").value;
        let assigneeId = document.getElementById("createAssignmentAssigneeId").value;
        let assignerId = document.getElementById("createAssignmentAssignerId").value;

        const data = {
            kind: "task",
            itemId: itemId,
            assigneeId: assigneeId,
            assignerId: assignerId
        }

        CreateAssignment(data);
    }

    // DELETE Methods
    deleteOrganzation() {
        let orgId = document.getElementById("deleteOrgId").value;
        DeleteOrg(orgId);
    }

    //Update Methods
    UpdateTasks() {
        let taskId = document.getElementById("updateTaskId").value;
        const data = {
            authorId: 17,
            completed: false,
                deadline: "2019-12-30T09:39:25.954000Z",
                description: "Do the presentation and pitch. Make sure to stay under time limit.",
                duration: 600,
                name: "Pitch"       
                    }
        UpdateTasks(taskId, data);
    }

    render() {
        return (
            <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
                <h1>----GET Methods----</h1>
                <button onClick={this.getOrganisation}>GET Organization</button>
                <button onClick={this.getUserIds}>Get user IDs</button>
                <div>
                    <input id="getUserFromUserId" />
                    <button onClick={this.getUserFromUserId}>Get User From User ID</button>
                </div>
                <button onClick={this.getTaskIds}>Get tasks</button>
                <div>
                    <input id="getTasksUserId" />
                    <button onClick={this.getTasksFromUserId}>Get Tasks From User ID</button>
                </div>
                <button onClick={this.getAssignmentIds}>Get Assignment</button>
                <div>
                    <input id="getAssignmentFromId" />
                    <button onClick={this.getAssignmentFromId}>Get Assignment</button>
                </div>

                <h1>----CREATE Methods----</h1>
                <div>
                    <h2>Create Organization</h2>
                    Organisation Name: <input id="createOrgName" /><br />
                    <button onClick={this.createOrganisations}>Create Organization</button>
                </div><br />

                <div>
                    <h2>Create User</h2>
                    Position: 
                    <select id="posSelect">
                        <option value="worker">Employee</option>
                        <option value="supervisor">Supervisor</option>
                    </select><br />
                    Name: <input id="createUserName" /><br />
                    Email: <input id="createUserEmail" /><br />
                    Organisation Id: <input id="createUserOrgId" /><br />
                    <button onClick={this.createUser}>Create user</button>
                </div><br />

                <div>
                    <h2>Create Task</h2>
                    Title: <input id="createTaskName" /><br />
                    Description: <input id="createTaskDes" /><br />
                    Duration: <input id="createTaskDur" /><br />
                    Author ID: <input id="createTaskAuthorId" /><br />
                    <button onClick={this.createTasks}>create tasks</button>
                </div><br />

                <div>
                    <h2>Create Assignments</h2>
                    Task id: <input id="createAssignmentItemId" /><br />
                    Assignee id: <input id="createAssignmentAssigneeId" /><br />
                    Assigner id: <input id="createAssignmentAssignerId" /><br />
                    <button onClick={this.createAssigment}>Create Assignment</button>
                </div><br />

                <h1>----DELETE Methods----</h1>
                <div>
                    <h2>Delete Organization</h2>
                    Organization Id: <input id="deleteOrgId" />
                    <button onClick={this.deleteOrganzation}>Delete Organization</button>
                </div>

                <div id="showId" style={{position: "absolute", right: "25vw", top: "50vh"}}></div>

                <h1>----UPDATE Methods----</h1>
                <div>
                <h2>Update Tasks</h2>
                    Tasks Id: <input id="updateTaskId" />
                    <button onClick={this.UpdateTasks}>Update Task</button>
                </div>

            <div id="showId" style={{ position: "absolute", right: "25vw", top: "50vh" }}></div>
            </div>  
        );
    }
}

export default CreateData
