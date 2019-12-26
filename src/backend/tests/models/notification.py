#
# Memento
# Backend
# Unit Tests for Notification Models 
#

from unittest import TestCase
from datetime import datetime

from ...app import db
from ...models import *

from .iam import TestIAMModels


# unit tests for Notification models
class TestNotificationModels(TestCase):
    def create_test_data(self):
        TestIAMModels.create_test_data(self)
        self.channel = Channel(kind=Channel.Kind.Notice,
                               user_id=self.worker.id)

        db.session.add(self.channel)
        db.session.commit()

        self.notification = Notification(channel=self.channel,
                                         title="Its to stop!",
                                         description="Its time to stop",
                                         firing_time=datetime.utcnow())
        db.session.add(self.notification)
        db.session.commit()

    def delete_test_data(self):
        db.session.delete(self.notification)
        db.session.commit()
        db.session.delete(self.channel)
        db.session.commit()
        TestIAMModels.delete_test_data(self)

    def test_create_delete(self):
        self.create_test_data()
        self.delete_test_data()
