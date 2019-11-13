// JavaScript source code


const fetch = require('node-fetch');

//-------------------------------------Organization---------------------//

async function GETOrg() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/orgs');
    const json = await response.json();
    console.log(json);
    return json;
}

//data is name (John & wick fishery)
async function CreateOrg() {
    const data = { name: 'John & Wick Fishery' }
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/org', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
    console.log(json);
}

//data is org-id (pre-populated org id)
async function DeleteOrg(data) {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/org/' + data.org_id.toString(), {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
    console.log(json);
}

//-------------------------------Users---------------------------------//

async function GETUsers() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/users');
    const json = await response.json();
    console.log(json);
    return json;
}

async function CreateUsers() {
    const data = {
        kind:"worker",
        name:"gugu",
        password:"P@ssw0rd",
        email:"gugu@gmail.com",
        orgId:16
    }
    const response = await fetch('https://memento.mrzzy.co/api/v0/iam/user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
    console.log(json);
}

//-----------------------------------Tasks---------------------------------//

async function CreateTasks() {
    const data = {
        name: "Guhesh's tasks",
        description:"Go to shower.",
        duration: 1200,
        deadline:'2019-12-30T09:39:25.954Z',
        authorId:13
    }
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    const json = await response.json();
    console.log(json);
}

async function GETTasks() {
    const response = await fetch('https://memento.mrzzy.co/api/v0/assignment/tasks');
    const json = await response.json();
    console.log(json);
    return json;
}


export { DeleteOrg, CreateOrg, GETOrg, GETUsers, CreateUsers, CreateTasks, GETTasks};