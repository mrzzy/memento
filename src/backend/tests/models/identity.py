#
# Memento
# Backend
# Unit Tests for Identity Models 
#

from unittest import TestCase
from ...app import db
from ...models import *

# unit tests for Identity model
class TestIdentityModels(TestCase):
    def create_test_data(self):
        # create identity models for testing 
        self.organisation = Organisation(name="kompany")
        db.session.add(self.organisation)
        db.session.commit()

        self.team = Team(name="designers",
                         organisation=self.organisation)
        db.session.add(self.team)
        db.session.commit()

        self.supervisor = User(organisation=self.organisation,
                               name="Joel",
                               password="Pa$$w0rd",
                               email="joel@email.com")
        db.session.add(self.supervisor)
        db.session.commit()

        self.worker = User(organisation=self.organisation,
                           team=self.team,
                           name="James",
                           password="Pa$$w0rd",
                           email="james@email.com")
        db.session.add(self.worker)
        db.session.commit()

        self.management = Management(kind=Management.Kind.User,
                                     target_id=self.worker.id,
                                     manager=self.supervisor)

        db.session.add(self.management)
        db.session.commit()

    def delete_test_data(self):
        db.session.delete(self.management)
        db.session.commit()
        db.session.delete(self.worker)
        db.session.commit()
        db.session.delete(self.supervisor)
        db.session.commit()
        db.session.delete(self.team)
        db.session.commit()
        db.session.delete(self.organisation)
        db.session.commit()

    def test_create_delete(self):
        self.create_test_data()
        self.delete_test_data()

    def test_validate_user(self):
        self.create_test_data()

        got_exception = False
        try:
            self.user = User(
                name="Joe",
                password="Pa$$wrd",
                organisation=self.organisation,
                email="joe@gmail.com"
            )
            db.session.add(self.user)
            db.session.commit()
        except AssertionError:
            got_exception = True

        self.assertTrue(got_exception)
        self.delete_test_data()
