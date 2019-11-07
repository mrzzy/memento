#
# Memento
# Backend
# Assignment Ops
#

from ..app import db
from ..models.assignment import *

from .utils import map_dict, apply_bound

## Task Ops
# query ids of tasks
# pending - show only tasks that are currently incomplete 
# author_id - show only tasks created by author with given user id 
# do_by -show  only tasks that are due before given do_by datetime
def query_tasks(pending=None, author_id=None, do_by=None, skip=0, limit=None):
    task_ids = Task.query.with_entities(Task.id)
    # apply filters
    if not pending is None:
        completed = not pending
        task_ids = task_ids.filter_by(completed=completed)
    if not author_id is None: task_id = task_ids.filter_by(author_id=author_id)
    if not do_by is None:
        task_ids = task_ids.filter(Task.deadline <= do_by)

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

