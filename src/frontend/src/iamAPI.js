// JavaScript source code


// const fetch = require('node-fetch');

//-------------------------------------Organization---------------------//

async function GETOrg() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/orgs');
    const json = await response.json();
    return json;
}


async function CreateOrg(orgName) {
    const data = { name: orgName }
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/org', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
}


async function DeleteOrg(orgId) {
    let data = { org_id: orgId };
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/org/' + data.org_id.toString(), {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
}

//-------------------------------Users---------------------------------//

async function GETUsers() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/users');
    const json = await response.json();
    return json;
}

async function GETUserFromId(userId) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/user/' + userId);
    const json = await response.json();
    return json;
}

async function CreateUsers(data) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
}

//-----------------------------------Tasks---------------------------------//

async function CreateTasks(data) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
}

async function GETTasks() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/tasks');
    const json = await response.json();
    return json;
}

async function GETTaskFromTaskId(taskId) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/task/' + taskId);
    const json = await response.json();
    return json;
}


async function GETTaskFromUserId(userId) {
    // Get assignment IDs
    let assignmentIdList = await GETAssignmentIds();

    // Get task ids from assignment IDs
    let tasksForUser = [];

    for (let i = 0; i < assignmentIdList.length; i++) {
        let assignment = await GETAssignment(assignmentIdList[i]);
        if (assignment.assigneeId == userId) {
            let task = await GETTaskFromTaskId(assignment.itemId);
            task.id = assignment.itemId;
            tasksForUser.push(task);
        }
    }

    return tasksForUser;
}

async function UpdateTasks(data) {
    if (data.id == null) {
        console.error("taskId is null.")
    }
    else
    {
        let taskId = data.id;
        delete data.id;
        const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/task/' + taskId, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        const json = await response.json();
    }
}
//-----------------------------------Assignments---------------------------------//
async function CreateAssignment(data) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/assign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
}

async function GETAssignmentIds() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/assigns');
    const json = await response.json();
    return json;
}

async function GETAssignment(id) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/assign/' + id);
    const json = await response.json();
    return json;
}

//-----------------------------------Channel---------------------------------//
async function CreateChannel(kind, userId) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/notification/channel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kind: kind, userId: userId })
    })
    const json = await response.json();
    return json;
}


//-----------------------------------Notification---------------------------------//
async function CreateNotification(task, firingTime, channelId) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/notification/notify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: task.name,
            description: task.description,
            firingTime: firingTime,
            channelId: channelId
        })
    })

    const json = await response.json();
    return json;
}

export {
    DeleteOrg, CreateOrg, GETOrg, GETUsers, CreateUsers, GETUserFromId,
    CreateTasks, GETTasks, CreateAssignment, GETAssignmentIds, GETAssignment,
    GETTaskFromUserId, UpdateTasks, CreateChannel, CreateNotification
};