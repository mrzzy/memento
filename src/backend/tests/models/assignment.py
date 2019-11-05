#
# Memento
# Backend
# Unit Tests for Assignment Models 
#


from unittest import TestCase
from datetime import datetime

from ...app import db
from ...models import *

from .iam import TestIAMModels

# unit tests for Assignment models
class TestAssignmentModels(TestCase):
    def create_test_data(self):
        TestIAMModels.create_test_data(self)

        self.task = Task(name="Fishing",
                         description="Time to catch some endanged whales",
                         deadline=datetime.now(),
                         duration=3600, # 1 hour
                         author=self.supervisor)
        db.session.add(self.task)
        db.session.commit()

        self.event = Event(name="Fishing Day",
                           description="Fishy presents for all",
                           start_time=datetime.now(),
                           duration=8 * 3600, # 8 hours
                           author=self.supervisor)
        db.session.add(self.event)
        db.session.commit()

        self.assignment = Assignment(kind=Assignment.Kind.Task,
                                     item_id=self.task.id,
                                     assignee=self.worker,
                                     assigner=self.supervisor)
        db.session.add(self.assignment)
        db.session.commit()

    def delete_test_data(self):
        db.session.delete(self.assignment)
        db.session.commit()
        db.session.delete(self.task)
        db.session.commit()
        db.session.delete(self.event)
        db.session.commit()
        TestIAMModels.delete_test_data(self)

    def test_create_delete(self):
        self.create_test_data()
        self.delete_test_data()
