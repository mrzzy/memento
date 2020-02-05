#
# Memento
# Backend
# Assignment Ops
#

from datetime import datetime, timedelta, timezone
from functools import partial
from sqlalchemy.exc import IntegrityError

from ..app import db
from ..models.assignment import *
from ..models.notification import *
from ..mapping.assignment import *
from ..utils import map_dict, apply_bound
from ..api.error import NotFoundError
from ..ops.notification import *

## Task Ops
# query ids of tasks
# pending - show only tasks that are currently incomplete 
# started - show only tasks that are currently started 
# author_id - show only tasks created by author with given user id 
# due_by - show only tasks that are due before given due_by
# for_day - show only tasks that are due for the given date
# skip - skip the first skip tasks
# limit - output ids limit to the first limit tasks
# assignee_id - show only tasks assigned to the user with the given user id
def query_tasks(pending=None, started=None, author_id=None, due_by=None, skip=0,
                limit=None, assignee_id=None, for_day=None):
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
    if not for_day is None:
        begin_day = for_day.replace(hour=0, minute=0, second=0)
        end_day = for_day.replace(hour=23, minute=59, second=59)
        task_ids = task_ids.filter(Task.deadline >= begin_day,
                                   Task.deadline <= end_day)
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
    # check for task completion and started 
    has_completed = True if completed and not task.completed else False
    has_started = True if started and not task.started else False

    # update task fields
    if not name is None: task.name = name
    if not deadline is None: task.deadline = deadline
    if not duration is None: task.duration = duration
    if not author_id is None: task.author_id = author_id
    if not description is None: task.description = description
    if not started is None: task.started = started
    if not completed is None: task.completed = completed

    db.session.commit()

    # notify assigner that task is completed or started
    create_task_notify = partial(create_notify,
                                 scope=Notification.Scope.Task,
                                 scope_target=task_id)

    query_pending_task_notify = partial(query_notifys,
                                        pending=True,
                                        scope=Notification.Scope.Task,
                                        scope_target=task_id)
    if has_completed or has_started:
        assigns = [ get_assign(i) for i in query_assigns("task", task_id) ]
        assigner_ids = list(set([ assign["assignerId"] for assign in  assigns ]))
        assigner_channel_ids = [ str(Channel(user_id=i)) for i in assigner_ids ]

        if has_started:
            # send task started notification to assigner
            for channel_id in assigner_channel_ids:
                create_task_notify(title="task started",
                                   channel_id=channel_id,
                                   subject=Notification.Subject.Started)

            # send task late notification to assigner
            latetime = datetime.utcnow() + timedelta(seconds=task.duration + 1)
            for channel_id in assigner_channel_ids:
                create_task_notify(title="task is late",
                                   channel_id=channel_id,
                                   subject=Notification.Subject.Late,
                                   firing_time=latetime)

        if has_completed:
            # send completed  notificationf
            for channel_id in assigner_channel_ids:
                create_task_notify(title="task completed",
                                   channel_id=channel_id,
                                   subject=Notification.Subject.Completed)

            # stop overdue or duesoon or late notification from firing since task is now completed
            overdue_ids = query_pending_task_notify(subject=Notification.Subject.Overdue)
            duesoon_ids = query_pending_task_notify(subject=Notification.Subject.DueSoon)
            late_ids = query_pending_task_notify(subject=Notification.Subject.Late)

            for notify_id in overdue_ids + duesoon_ids + late_ids:
                delete_notify(notify_id)


    # update duesoon & duetime notification to the new deadline if changeed
    if deadline:
        # deadline timezone naive
        duetime = deadline.replace(tzinfo=None)
        # notify assignee when deadline
        overdue_ids = query_pending_task_notify(subject=Notification.Subject.Overdue)
        for notify_id in overdue_ids:
            update_notify(notify_id, firing_time=duetime)

        # notify assignee when due soon
        due_secs = (datetime.utcnow() - duetime).seconds
        # notify assignee when 25% time left
        duesoon = duetime + timedelta(seconds=0.75 * due_secs)
        duesoon_ids = query_pending_task_notify(subject=Notification.Subject.DueSoon)
        for notify_id in overdue_ids:
            update_notify(notify_id, firing_time=duesoon)

# delete the task for the given task id
# cascade deletes and dependent objects on task
# throws NotFoundError if no task with task_id is found
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None: raise NotFoundError

    # cascade delete dependent assignments
    assign_ids = query_assigns(Assignment.Kind.Task, task_id)
    for assign_id in assign_ids: delete_assign(assign_id)
    # cascade delete notifications
    notify_ids = query_notifys(scope=Notification.Scope.Task,
                               scope_target=task_id)
    for notify_id in notify_ids: delete_notify(notify_id)

    db.session.delete(task)
    db.session.commit()

## Event Ops
# query ids of events
# pending - show only pending events
# author_id - show only events created by author with given user id
# due_by - show only events that have to be attended before and at due_by
# for_day - show only events that are due for the given date
# skip - skip the first skip events
# limit - output ids limit to the first limip events
# assignee_id - show only events that are assigned to the user with user id
def query_events(pending=None, author_id=None, due_by=None, skip=0, limit=None,
                 assignee_id=None, for_day=None):
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
    if not for_day is None:
        begin_day = for_day.replace(hour=0, minute=0, second=0)
        end_day = for_day.replace(hour=23, minute=59, second=59)
        event_ids = event_ids.filter(Event.start_time >= begin_day,
                                     Event.start_time <= end_day)
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

    # update event staring notification
    notify_ids = query_notifys(scope=Notification.Scope.Task,
                               scope_target=event_id,
                               subject=Notification.Subject.Started)
    for notify_id in notify_ids:
        update_notify(notify_id, firing_time=start_time)


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
# for_day - show only assigns that are due for the given date
# skip - skip the first skip assignments
# limit - output ids limit to the first limit assignments
def query_assigns(kind=None, item_id=None, assigner_id=None, assignee_id=None,
                  pending=None, due_by=None, skip=0, limit=None, for_day=None):
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
        if not for_day is None:
            begin_day = for_day.replace(hour=0, minute=0, second=0)
            end_day = for_day.replace(hour=23, minute=59, second=59)
            # tasks assignments
            assign_ids = assign_ids.filter(Task.deadline >= begin_day,
                                           Task.deadline <= end_day)
            # event assignments
            assign_ids = assign_ids.filter(Event.start_time >= begin_day,
                                         Event.start_time <= end_day)
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
    # check if we already have an assignment with the same fields
    duplicate_ids = Assignment.query.filter_by(kind=kind, item_id=item_id,
                                               assignee_id=assignee_id,
                                               assigner_id=assigner_id)
    if duplicate_ids.count() > 0:
        raise IntegrityError("Duplicate Assignment")

    assign = Assignment(kind=kind, item_id=item_id, assigner_id=assigner_id,
                        assignee_id=assignee_id)
    db.session.add(assign)
    db.session.commit()

    assignee_channel_id = str(Channel(user_id=assignee_id))
    assigner_channel_id = str(Channel(user_id=assigner_id))

    # notify assignee of new assignment
    create_assign_notify = partial(create_notify,
                                   scope=kind,
                                   scope_target=item_id)

    create_assign_notify(title=f"new {kind} assignment",
                         channel_id=assignee_channel_id,
                         subject=Notification.Subject.Assigned)

    # timed assignment notifications
    if kind == Assignment.Kind.Task:
        duetime = get_task(item_id)["deadline"]
        # notify assignee when overdue
        create_assign_notify(title=f"overdue {kind} assignment",
                             subject=Notification.Subject.Overdue,
                             channel_id=assigner_channel_id,
                             firing_time=duetime)

        # notify assignee when due soon
        due_secs = (datetime.utcnow() - duetime).seconds
        # notify assignee when 25% time left
        duesoon = duetime + timedelta(seconds=0.75 * due_secs)
        create_assign_notify(title=f"{kind} assignment due soon",
                             subject=Notification.Subject.DueSoon,
                             channel_id=assignee_channel_id,
                             firing_time=duesoon)

        print(f"duetime: {duetime}, duesoon: {duesoon}, duesecs: {due_secs}")

    elif kind == Assignment.Kind.Event:
        duetime = get_event(item_id)["startTime"]
        # notify assignee when event starting 
        create_assign_notify(title=f"{kind} assignment starting",
                             subject=Notification.Subject.Started,
                             channel_id=assignee_channel_id,
                             firing_time=duetime)

    return assign.id

# delete assignment with given id
# throws NotFoundError if no assign with assign_id is found
def delete_assign(assign_id):
    assign = Assignment.query.get(assign_id)
    if assign is None: raise NotFoundError

    # cascade delete notifications created by assignment
    query_assign_notifys = partial(query_notifys,
                                   scope=assign.kind,
                                   scope_target=assign.item_id)
    assigner_channel_id = str(Channel(user_id=assign.assigner_id))
    assigner_notify_ids = query_assign_notifys(channel_id=assigner_channel_id)
    assignee_channel_id = str(Channel(user_id=assign.assignee_id))
    assignee_notify_ids = query_assign_notifys(channel_id=assignee_channel_id)
    for notify_id in assigner_notify_ids + assignee_notify_ids:
        delete_notify(notify_id)

    db.session.delete(assign)
    db.session.commit()
