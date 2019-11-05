#
# Memento
# Backend
# Unit Tests for Notification Models 
#

from unittest import TestCase
from datetime import datetime

from ...app import db
from ...models import *


# unit tests for Notification models
class TestNotificationModels(TestCase):
    def create_test_data(self):
        self.channel = Channel(id="worker/tasks/0")
        db.session.add(self.channel)
        db.session.commit()

        self.notification = Notification(kind=Notification.Kind.Event,
                                         channel=self.channel,
                                         title="Its to stop!",
                                         description="Its time to stop",
                                         firing_time=datetime.now())
        db.session.add(self.notification)
        db.session.commit()

    def delete_test_data(self):
        db.session.delete(self.notification)
        db.session.commit()
        db.session.delete(self.channel)
        db.session.commit()

    def test_create_delete(self):
        self.create_test_data()
        self.delete_test_data()
