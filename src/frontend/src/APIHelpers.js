/*
 * Memento
 * Frontend 
 * API Helpers
*/

// defines a decorator that decorates the API object with various 
// helper convience functions
export default class APIHelpers {
    // wrap & decorate the given api with helpers
    constructor(api) {
        this.api = api;
    }
        
    // retrieve employee userIds for employer with the given employer id
    // employerId - user id of the employee to create tasks for 
    // returns user ids of employee of employer
    getEmployeesForEmployer(employerId) {
        // get managment relationships for employer
        const manages =  this.api.query("manage", {"manager": employerId});
        const employeeeIds = manages.map((manage) => manage.manageeId);
    
        return employeeeIds
    }
    
    // get tasks assigned to userId
    // userId - id of the employee to get tasks for
    // return tasks
    getTasks(userId) {
        const taskIds = this.api.query("task", {"assignee": userId});
        return taskIds
    }

    // get tasks assigned to userId for the given date
    // userId - id of the employee to get tasks for
    // date - UTC datetime specifying the day to get tasks
    // returns task ids
    getTasksForDate(userId, date) {
        const taskIds = this.api.query("task", {"assignee": userId, "for-day": date});
        return taskIds
    }

    // check if the user specified by the given userId is an employer
    isEmployer(userId) {
        const manageIds = this.api.query("manage", {"manager": userId});
        return manageIds.length > 0;
    }
}
