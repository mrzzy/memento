#
# Memento
# Backend
# Assignment Ops
#

from datetime import datetime

from ..app import db
from ..models.assignment import *
from .utils import map_dict, apply_bound

## Task Ops
# query ids of tasks
# pending - show only tasks that are currently incomplete 
# author_id - show only tasks created by author with given user id 
# limit_by -show  only tasks that are due before given limit_by
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_tasks(pending=None, author_id=None, limit_by=None, skip=0, limit=None):
    task_ids = Task.query.with_entities(Task.id)
    # apply filters
    if not pending is None:
        completed = not pending
        task_ids = task_ids.filter_by(completed=completed)
    if not author_id is None: task_id = task_ids.filter_by(author_id=author_id)
    if not limit_by is None:
        task_ids = task_ids.filter(Task.deadline <= limit_by)

    # apply skip & limit
    task_ids = [ i[0] for  i in task_ids ]
    task_ids = apply_bound(task_ids, skip, limit)

    return task_ids

# get task for id
# returns task as a dict 
def get_task(task_id):
    task = Task.query.get(task_id)
    # map fields to dict
    mapping = [
        ("name", "name"),
        ("description", "description"),
        ("duration", "duraiton"),
        ("deadline", "deadline"),
        ("completed", "completed"),
        ("author_id", "authorId")
    ]
    return map_dict(task, mapping)

# create a task
# name - name of the task
# description - description of the task, optional
# deadline - completion deadline of the task 
# duration - duration of task of task in seconds
# completed - whether the task is completed
# author_id - user id of the author of the task
# returns the id of the new task
def create_task(name, deadline, duration, author_id,
                description="", completed=False):
    task = Task(name=name, deadline=deadline, description=description,
                duration= duration, author_id=author_id, completed=completed)
    db.session.add(task)
    db.session.commit()

    return task.id

# update the task for the given task_id
# name - name of the task
# description - description of the task, optional
# deadline - completion deadline of the task 
# duration - duration of task of task in seconds
# completed - whether the task is completed
# author_id - user id of the author of the task
def update_task(task_id, name=None, deadline=None, duration=None,
                author_id=None, description=None, completed=None):
    task = Task.query.get(task_id)
    if not name is None: task.name = name
    if not deadline is None: task.deadline = deadline
    if not duration is None: task.duration = duration
    if not author_id is None: task.author_id = author_id
    if not description is None: task.description = description
    if not completed is None: task.completed = completed
    db.session.commit()

# delete the task for the given task id
# cascade deletes and dependent objects on task
def delete_task(task_id):
    # TODO: cascade delete

    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

## Event Ops
# query ids of events
# pending - show only pending events
# author_id - show only events created by author with given user id
# limit_by - show only events that have to be attended before and at limit_by
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_events(pending=None, author_id=None, limit_by=None, skip=0, limit=None):
    # apply filters
    event_ids = Event.query.with_entities(Event.id)
    if not pending is None:
        now = datetime.utcnow()
        if pending == True:
            event_ids = event_ids.filter(Event.start_time <= now)
        else:
            event_ids = event_ids.filter(Event.start_time > now)
    if not author_id is None: event_id = event_ids.filter_by(author_id=author_id)
    if not limit_by is None:
        event_ids = event_ids.filter(Event.start_time <= limit_by)

    # apply skip & limit
    event_ids = [ i[0] for  i in event_ids ]
    event_ids = apply_bound(event_ids, skip, limit)

    return event_ids

# get event for id
# returns event as a dict 
def get_event(event_id):
    event = Event.query.get(event_id)
    # map fields to dict
    mapping = [
        ("name", "name"),
        ("description", "description"),
        ("start_time", "startTime"),
        ("duration", "duraiton"),
        ("author_id", "authorId")
    ]
    return map_dict(event, mapping)

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
def update_event(event_id=None, name=None, start_time=None,
                 duration=None, author_id=None, description=None):
    event = Event.query.get(event_id)
    if not name is None: event.name = name
    if not start_time is None: event.start_time = start_time
    if not duration is None: event.duration = duration
    if not author_id is None: event.author_id = author_id
    if not description is None: event.description = description
    db.session.commit()

# delete the event for the given event id
# cascade deletes and dependent objects on event
def delete_event(event_id):
    # TODO: cascade delete

    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
