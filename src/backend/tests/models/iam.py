#
# Memento
# Backend
# Unit Tests for IAM Models 
#

from unittest import TestCase
from ...app import db
from ...models import *

# unit tests for IAM model
class TestIAMModels(TestCase):
    def create_test_data(self):
        # create iam models for testing 
        self.organisation = Organisation(name="kompany")
        db.session.add(self.organisation)
        db.session.commit()

        self.team = Team(name="designers",
                         organisation=self.organisation)
        db.session.add(self.team)
        db.session.commit()

        self.supervisor = User(kind=User.Kind.Supervisor,
                               organisation=self.organisation,
                               name="Joel",
                               password="password",
                               email="joel@email.com")
        db.session.add(self.supervisor)
        db.session.commit()

        self.worker = User(kind=User.Kind.Worker,
                           organisation=self.organisation,
                           team=self.team,
                           name="James",
                           password="password",
                           email="james@email.com")
        db.session.add(self.worker)
        db.session.commit()

        self.management = Management(kind=Management.Kind.Worker,
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
        
        self.user = User(
            name="Joe",
            password="1234",
            kind=User.Kind.Admin,
            organisation=self.organisation,
            email="joe@gmail.com"
        )
        got_exception = False
        try:
            db.session.add(self.user)
            db.session.commit()
        except AssertionError:
            got_exception = True
        
        self.assertTrue(got_exception)
            
        
        self.delete_test_data()

