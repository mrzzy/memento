#
# Memento
# Backend
# Assignment Ops
#

from datetime import datetime

from ..app import db
from ..models.assignment import *
from ..mapping.assignment import *
from ..utils import map_dict, apply_bound
from ..api.error import NotFoundError

## Task Ops
# query ids of tasks
# pending - show only tasks that are currently incomplete 
# started - show only tasks that are currently started 
# author_id - show only tasks created by author with given user id 
# due_by - show only tasks that are due before given due_by
# skip - skip the first skip tasks
# limit - output ids limit to the first limit tasks
# assignee_id - show only tasks assigned to the user with the given user id
def query_tasks(pending=None, started=None, author_id=None, due_by=None, skip=0,
                limit=None, assignee_id=None):
    task_ids = Task.query.with_entities(Task.id)
    # apply filters
    if not pending is None:
        completed = not pending
        task_ids = task_ids.filter_by(completed=completed)
    if not started is None:
        task_ids = task_ids.filter_by(started=started)
    if not author_id is None: task_id = task_ids.filter_by(author_id=author_id)
    if not due_by is None:
        task_ids = task_ids.filter(Task.deadline <= due_by)
    if not assignee_id is None:
        task_ids = task_ids.join(Assignment, (Task.id == Assignment.item_id)
                                 & (Assignment.kind == Assignment.Kind.Task))
        task_ids = task_ids.filter(Assignment.assignee_id == assignee_id)

    # apply skip & limit
    task_ids = [ i[0] for  i in task_ids ]
    task_ids = apply_bound(task_ids, skip, limit)

    return task_ids

# get task for id
# throws NotFoundError if no task with task_id is found
# returns task as a dict 
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None: raise NotFoundError
    # map fields to dict
    return map_dict(task, task_mapping)

# create a task
# name - name of the task
# description - description of the task, optional
# deadline - completion deadline of the task 
# duration - duration of task of task in seconds
# completed - whether the task is completed
# started - whether the task is completed
# author_id - user id of the author of the task
# returns the id of the new task
def create_task(name, deadline, duration, author_id,
                description="", started=False, completed=False):
    task = Task(name=name, deadline=deadline, description=description,
                duration= duration, author_id=author_id, started=started,
                completed=completed)
    db.session.add(task)
    db.session.commit()

    return task.id

# update the task for the given task_id
# name - name of the task
# description - description of the task, optional
# deadline - completion deadline of the task 
# duration - duration of task of task in seconds
# completed - whether the task is completed
# started - whether the task is started 
# author_id - user id of the author of the task
# throws NotFoundError if no task with task_id is found
def update_task(task_id, name=None, deadline=None, duration=None,
                author_id=None, description=None, completed=None, started=None):
    task = Task.query.get(task_id)
    if task is None: raise NotFoundError
    # update task fields
    if not name is None: task.name = name
    if not deadline is None: task.deadline = deadline
    if not duration is None: task.duration = duration
    if not author_id is None: task.author_id = author_id
    if not description is None: task.description = description
    if not completed is None: task.completed = completed
    if not started is None: task.started = started

    db.session.commit()

# delete the task for the given task id
# cascade deletes and dependent objects on task
# throws NotFoundError if no task with task_id is found
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None: raise NotFoundError

    # cascade delete dependent assignments
    assign_ids = query_assigns(Assignment.Kind.Task, task_id)
    for assign_id in assign_ids: delete_assign(assign_id)

    db.session.delete(task)
    db.session.commit()

## Event Ops
# query ids of events
# pending - show only pending events
# author_id - show only events created by author with given user id
# due_by - show only events that have to be attended before and at due_by
# skip - skip the first skip events
# limit - output ids limit to the first limip events
# assignee_id - show only events that are assigned to the user with user id
def query_events(pending=None, author_id=None, due_by=None, skip=0, limit=None,
                 assignee_id=None):
    # apply filters
    event_ids = Event.query.with_entities(Event.id)
    if not pending is None:
        now = datetime.utcnow()
        if pending == True:
            event_ids = event_ids.filter(Event.start_time >= now)
        else:
            event_ids = event_ids.filter(Event.start_time < now)
    if not author_id is None: event_id = event_ids.filter_by(author_id=author_id)
    if not due_by is None:
        event_ids = event_ids.filter(Event.start_time <= due_by)
    if not assignee_id is None:
        event_ids = event_ids.join(Assignment, (Event.id == Assignment.item_id)
                                   & (Assignment.kind == Assignment.Kind.Event))
        event_ids = event_ids.filter(Assignment.assignee_id == assignee_id)

    # apply skip & limit
    event_ids = [ i[0] for  i in event_ids ]
    event_ids = apply_bound(event_ids, skip, limit)

    return event_ids

# get event for id
# returns event as a dict 
# throws NotFoundError if no event with event_id is found
def get_event(event_id):
    event = Event.query.get(event_id)
    if event is None: raise NotFoundError
    # map fields to dict
    return map_dict(event, event_mapping)

# create a event
# name - name of the event
# description - description of the event, optional
# start_time - the begin time of the event
# duration - duration of event of event in seconds
# author_id - user id of the author of the event
# returns the id of the new event
def create_event(name, start_time, duration, author_id, description=""):
    event = Event(name=name, start_time=start_time, description=description,
                  duration=duration, author_id=author_id)
    db.session.add(event)
    db.session.commit()

    return event.id

# update the event for the given event_id
# name - name of the event
# description - description of the event, optional
# start_time - the begin time of the event
# duration - duration of event of event in seconds
# author_id - user id of the author of the event
# throws NotFoundError if no event with event_id is found
def update_event(event_id=None, name=None, start_time=None,
                 duration=None, author_id=None, description=None):
    event = Event.query.get(event_id)
    if event is None: raise NotFoundError
    # update event fields
    if not name is None: event.name = name
    if not start_time is None: event.start_time = start_time
    if not duration is None: event.duration = duration
    if not author_id is None: event.author_id = author_id
    if not description is None: event.description = description
    db.session.commit()

# delete the event for the given event id
# cascade deletes and dependent objects on event
# throws NotFoundError if no event with event_id is found
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event is None: raise NotFoundError
    # cascade delete depedent assignments
    assign_ids = query_assigns(Assignment.Kind.Event, event_id)
    for assign_id in assign_ids: delete_assign(assign_id)

    db.session.delete(event)
    db.session.commit()

## Assignment Ops
# query ids of assignments
# kind - show only assignments of the given kind
# item_id - show only assigns for given assignment type
# assigner_id - show only assignments assigned by user with assigner_id
# assignee_id - show only assignments assigned to user with assignee_id
# pending - show only assignments with items that are pending
# due_by - show only assignments with items that relevant before due_by
# skip - skip the first skip assignments
# limit - output ids limit to the first limit assignments
def query_assigns(kind=None, item_id=None, assigner_id=None, assignee_id=None,
                  pending=None, due_by=None, skip=0, limit=None):
    assign_ids = Assignment.query.with_entities(Assignment.id)
    # apply filters
    if not kind is None: assign_ids = assign_ids.filter_by(kind=kind)
    if not item_id is None: assign_ids = assign_ids.filter_by(item_id=item_id)
    if not assigner_id is None: assign_ids = assign_ids.filter_by(assigner_id=assigner_id)
    if not assignee_id is None: assign_ids = assign_ids.filter_by(assignee_id=assignee_id)

    if not pending is None or not due_by is None:
        # join with all assigned items
        task_assign_ids = assign_ids.join(Task, (Assignment.item_id == Task.id)
                                     & (Assignment.kind == Assignment.Kind.Task))
        event_assign_ids = assign_ids.join(Event, (Assignment.item_id == Event.id)
                                     & (Assignment.kind == Assignment.Kind.Event))
        assign_ids = task_assign_ids.union(event_assign_ids)

        if not pending is None:
            # task assignments
            completed = not pending
            assign_ids = assign_ids.filter(Task.completed == completed)
            # event assignments
            now = datetime.utcnow()
            assign_ids = assign_ids.filter(Event.start_time >= now)
        if not due_by is None:
            now = datetime.utcnow()
            # tasks assignments
            assign_ids = assign_ids.filter(Task.deadline <= due_by)
            # event assignments
            assign_ids = assign_ids.filter(Event.start_time <= due_by)

    # apply skip & limit
    assign_ids = [ i[0] for i in assign_ids ]
    return apply_bound(assign_ids, skip, limit)

# get assignment by id
# returns assignment as a dictionary
# throws NotFoundError if no assign with assign_id is found
def get_assign(assign_id):
    assign = Assignment.query.get(assign_id)
    if assign is None: raise NotFoundError
    # map model fields to dict
    return map_dict(assign, assign_mapping)

# create a new assignment
# kind - kind of assignment item (task, event)
# item_id - id of the item in the assignment
# assignee_id - id of the user that is assigned this assignment
# assigner_id - id of the user that assigned this assignement
def create_assign(kind, item_id, assignee_id, assigner_id):
    assign = Assignment(kind=kind, item_id=item_id, assigner_id=assigner_id,
                        assignee_id=assignee_id)
    db.session.add(assign)
    db.session.commit()

    return assign.id

# update assignment with the given assign_id
# kind - kind of assignment item (task, event)
# item_id - id of the item in the assignment
# assignee_id - id of the user that is assigned this assignment
# assigner_id - id of the user that assigned this assignement
# throws NotFoundError if no assign with assign_id is found
def update_assign(assign_id, kind=None, item_id=None, assignee_id=None, assigner_id=None):
    assign = Assignment.query.get(assign_id)
    if assign is None: raise NotFoundError
    # update assignment fields
    if not kind is None: assign.kind = kind
    if not item_id is None: assign.item_id = item_id
    if not assignee_id is None: assign.assignee_id = assignee_id
    if not assigner_id is None: assign.assigner_id = assigner_id
    db.session.commit()

# delete assignment with given id
# throws NotFoundError if no assign with assign_id is found
def delete_assign(assign_id):
    assign = Assignment.query.get(assign_id)
    if assign is None: raise NotFoundError
    db.session.delete(assign)
    db.session.commit()
