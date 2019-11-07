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
    def test_task_ops(self):
        self.assertEqual(query_tasks(), [])

        org_id = create_org("kompany")
        manager_id = create_user(User.Kind.Supervisor,
                              "John",
                              "password",
                              "john@jmail.com",
                              org_id)
        worker_id = create_user(User.Kind.Worker,
                              "Joel",
                              "password",
                              "joel@jmail.com",
                              org_id)
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

        org_id = create_org("kompany")
        manager_id = create_user(User.Kind.Supervisor,
                              "John",
                              "password",
                              "john@jmail.com",
                              org_id)
        worker_id = create_user(User.Kind.Worker,
                              "Joel",
                              "password",
                              "joel@jmail.com",
                              org_id)
        event_start_time = datetime.utcnow()
        event_id = create_event("fishing trip",
                              start_time=event_start_time,
                              duration=60,
                              author_id=manager_id)

        event = get_event(event_id)
        self.assertEqual(event["name"], "fishing trip")
        self.assertEqual(query_events(), [event_id])
        self.assertEqual(query_events(pending=False), [])
        self.assertEqual(query_events(limit_by=event_start_time), [event_id])

        update_event(event_id, name="cooking competition")
        event = get_event(event_id)
        self.assertEqual(event["name"], "cooking competition")

        delete_event(event_id)
        self.assertEqual(query_events(), [])
        delete_org(event_id)
