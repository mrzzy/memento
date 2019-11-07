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
        self.assertEqual(query_tasks(do_by=task_deadline), [task_id])

        update_task(task_id, name="cook")
        task = get_task(task_id)
        self.assertEqual(task["name"], "cook")

        delete_task(task_id)
        self.assertEqual(query_tasks(), [])
        delete_org(task_id)
