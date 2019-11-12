#
# Memento
# Backend
# Assignment Ops Tests
#

from unittest import TestCase
from datetime import datetime


from ...ops.iam import *
from ...ops.assignment import *

class TestAssigmentOps(TestCase):

    def create_test_data(self):
        org_id = create_org("kompany")
        manager_id = create_user(User.Kind.Supervisor,
                              "John",
                              "P@$$w0rd",
                              "john@jmail.com",
                              org_id)
        worker_id = create_user(User.Kind.Worker,
                              "Joel",
                              "P@$$w0rd",
                              "joel@jmail.com",
                              org_id)

        return org_id, manager_id, worker_id

    def test_task_ops(self):
        self.assertEqual(query_tasks(), [])

        got_lookup_error = False
        try:
            get_task(2)
        except LookupError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, manager_id, worker_id = self.create_test_data()
        task_deadline = datetime.utcnow()
        task_id = create_task("fish",
                              deadline= task_deadline,
                              duration=60,
                              author_id=manager_id)

        task = get_task(task_id)
        self.assertEqual(task["name"], "fish")
        self.assertEqual(query_tasks(), [task_id])
        self.assertEqual(query_tasks(pending=False), [])
        self.assertEqual(query_tasks(limit_by=task_deadline), [task_id])

        update_task(task_id, name="cook")
        task = get_task(task_id)
        self.assertEqual(task["name"], "cook")

        delete_task(task_id)
        self.assertEqual(query_tasks(), [])
        delete_org(task_id)

    def test_event_ops(self):
        self.assertEqual(query_events(), [])

        got_lookup_error = False
        try:
            get_event(2)
        except LookupError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, manager_id, worker_id = self.create_test_data()
        event_start_time = datetime.utcnow()
        event_id = create_event("fishing trip",
                              start_time=event_start_time,
                              duration=60,
                              author_id=manager_id)

        event = get_event(event_id)
        self.assertEqual(event["name"], "fishing trip")
        self.assertEqual(query_events(), [event_id])
        self.assertEqual(query_events(pending=False), [event_id])
        self.assertEqual(query_events(limit_by=event_start_time), [event_id])

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
        except LookupError:
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

        assign = get_assign(assign_id)
        self.assertEqual(assign["assigneeId"], worker_id)
        self.assertEqual(query_assigns(), [assign_id])
        self.assertEqual(query_assigns(pending=False,
                                       limit_by=datetime.utcnow()), [])

        # swap worker and manager in assignment as a proof of concept
        update_assign(assign_id, assigner_id=worker_id, assignee_id=manager_id)
        assign = get_assign(assign_id)
        self.assertEqual(assign["assigneeId"], manager_id)

        delete_assign(assign_id)
        self.assertEqual(query_assigns(), [])
        delete_org(org_id)
