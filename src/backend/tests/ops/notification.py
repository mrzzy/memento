#
# Memento
# Backend
# Notification Ops Tests
#

from unittest import TestCase
from datetime import datetime

from ...ops.iam import *
from ...ops.notification import *

class TestsNotficationOps(TestCase):
    def create_test_data(self):
        org_id = create_org("kompany")
        user_id = create_user(User.Kind.Supervisor,
                              "John",
                              "P@$$w0rd",
                              "john@jmail.com",
                              org_id)
        return org_id, user_id

    def test_channel_ops(self):
        self.assertEqual(query_channels(), [])

        got_lookup_error = False
        try:
            get_channel(2)
        except NotFoundError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, user_id = self.create_test_data()
        channel_id = create_channel(Channel.Kind.Notice, user_id)

        channel = get_channel(channel_id)
        self.assertEqual(channel["userId"], user_id)
        self.assertEqual(query_channels(), [channel_id])
        self.assertEqual(query_channels(pending=True), [])

        update_channel(channel_id, kind=Channel.Kind.Task)
        channel = get_channel(channel_id)
        self.assertEqual(channel["kind"], Channel.Kind.Task)

        delete_channel(channel_id)
        self.assertEqual(query_tasks(), [])
        delete_org(org_id)

    def test_notify_ops(self):
        self.assertEqual(query_notifys(), [])

        got_lookup_error = False
        try:
            get_notify(2)
        except NotFoundError:
            got_lookup_error = True
        self.assertTrue(got_lookup_error)

        org_id, user_id = self.create_test_data()
        channel_id = create_channel(Channel.Kind.Notice, user_id)
        notify_id = create_notify("fish", channel_id)

        notify = get_notify(notify_id)
        self.assertEqual(notify["title"], "fish")
        self.assertEqual(query_notifys(), [notify_id])
        self.assertEqual(query_notifys(pending=True), [])

        update_notify(notify_id, title="gym")
        notify = get_notify(notify_id)
        self.assertEqual(notify["title"], "gym")

        delete_notify(notify_id)
        self.assertEqual(query_notifys(), [])
        delete_org(org_id)
