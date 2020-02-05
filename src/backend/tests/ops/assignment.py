#
# Memento
# Backend
# Assignment Ops Tests
#

from unittest import TestCase
from datetime import datetime
from functools import partial

from ...ops.identity import *
from ...ops.assignment import *
from ...ops.notification import *

class TestAssigmentOps(TestCase):

    def create_test_data(self):
        org_id = create_org("kompany")
        manager_id = create_user("John",
                                 "P@$$w0rd",
                                 "john@jmail.com",
                                 org_id)
        worker_id = create_user("Joel",
                                "P@$$w0rd",
                                "joel@jmail.com",
                                org_id)

        return org_id, manager_id, worker_id

    def test_task_ops(self):
        self.assertEqual(query_tasks(), [])

        got_lookup_error = False
        try:
            get_task(2)
        except NotFoundError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, manager_id, worker_id = self.create_test_data()
        task_deadline = datetime.utcnow()
        task_id = create_task("fish",
                              deadline= task_deadline,
                              duration=60,
                              author_id=manager_id)
        assign_id = create_assign(Assignment.Kind.Task,
                                  task_id,
                                  worker_id,
                                  manager_id)
        query_task_notifys = partial(query_notifys,
                                     scope=Notification.Scope.Task,
                                     scope_target=task_id)
        # check auto notifications are created properly
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=worker_id)),
                                          subject=Notification.Subject.Assigned)) > 0)
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=manager_id)),
                                          subject=Notification.Subject.Overdue)) > 0)
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=worker_id)),
                                          subject=Notification.Subject.DueSoon)) > 0)

        task = get_task(task_id)
        self.assertEqual(task["name"], "fish")
        self.assertEqual(query_tasks(), [task_id])
        self.assertEqual(query_tasks(pending=False), [])
        self.assertEqual(query_tasks(due_by=task_deadline), [task_id])
        self.assertEqual(query_tasks(for_day=datetime.today()), [task_id])
        self.assertEqual(query_tasks(assignee_id=worker_id), [task_id])


        update_task(task_id, name="cook", started=True)
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=manager_id)),
                                               subject=Notification.Subject.Started)) > 0)
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=manager_id)),
                                               subject=Notification.Subject.Late)) > 0)

        update_task(task_id, name="cook", completed=True)
        self.assertTrue(len(query_task_notifys(channel_id=str(Channel(user_id=manager_id)),
                                               subject=Notification.Subject.Completed)) > 0)
        task = get_task(task_id)
        self.assertEqual(task["name"], "cook")

        delete_task(task_id)
        self.assertEqual(query_tasks(), [])
        delete_org(org_id)

    def test_event_ops(self):
        self.assertEqual(query_events(), [])

        got_lookup_error = False
        try:
            get_event(2)
        except NotFoundError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, manager_id, worker_id = self.create_test_data()
        event_start_time = datetime.utcnow()
        event_id = create_event("fishing trip",
                              start_time=event_start_time,
                              duration=60,
                              author_id=manager_id)
        assign_id = create_assign(Assignment.Kind.Event,
                                  event_id,
                                  worker_id,
                                  manager_id)

        event = get_event(event_id)
        self.assertEqual(event["name"], "fishing trip")
        self.assertEqual(query_events(), [event_id])
        self.assertEqual(query_events(pending=False), [event_id])
        self.assertEqual(query_events(due_by=event_start_time), [event_id])
        self.assertEqual(query_events(for_day=datetime.today()), [event_id])
        self.assertEqual(query_events(assignee_id=worker_id), [event_id])

        update_event(event_id, name="cooking competition")
        event = get_event(event_id)
        self.assertEqual(event["name"], "cooking competition")

        delete_event(event_id)
        self.assertEqual(query_events(), [])
        delete_org(org_id)

    def test_assign_ops(self):
        self.assertEqual(query_assigns(), [])

        got_lookup_error = False
        try:
            get_assign(2)
        except NotFoundError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, manager_id, worker_id = self.create_test_data()
        task_deadline = datetime.utcnow()
        task_id = create_task("fish",
                              deadline=task_deadline,
                              duration=60,
                              author_id=manager_id)
        assign_id = create_assign(Assignment.Kind.Task,
                                  task_id,
                                  worker_id,
                                  manager_id)

        assign = get_assign(assign_id)
        self.assertEqual(assign["assigneeId"], worker_id)
        self.assertEqual(query_assigns(), [assign_id])
        self.assertEqual(query_assigns(for_day=datetime.today()), [assign_id])
        self.assertEqual(query_assigns(pending=False,
                                       due_by=datetime.utcnow()), [])
        # check notification sent on assignment
        self.assertTrue(len(query_notifys(channel_id=str(Channel(user_id=worker_id)),
                                          scope=Notification.Scope.Task,
                                          scope_target=task_id)) > 0)

        delete_assign(assign_id)
        self.assertEqual(query_assigns(), [])
        delete_org(org_id)
