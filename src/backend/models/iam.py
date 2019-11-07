#
# Memento
# Backend
# IAM Models 
#

from ..app import db
from sqlalchemy.orm import validates
import re

# defines an organisation that users and teams belong to
class Organisation(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    logo_url = db.Column(db.String(2048), nullable=True)
    # relationships 
    teams = db.relationship("Team", backref=db.backref("organisation"), lazy=True)
    members = db.relationship("User", backref=db.backref("organisation"), lazy=True)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Company name cannot be blank')
        if len(name) < 2 or len(name) > 50:
            raise AssertionError(' must be between 2 and 50 characters long')
    

# defines a team in an organisation  that users can be belng too
class Team(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"),
                       nullable=False)
    members = db.relationship("User", backref=db.backref("team"), lazy=True)

# defines a user in the organisation.
class User(db.Model):
    # user kinds/types
    class Kind:
        Worker = "worker" # worker
        Supervisor = "worker" # supervisor of worker
        Admin = "admin" # root adminstrative user for the organisation
        Service = "service" # service account

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Name cannot be blank')
        if len(name) < 2 or len(name) > 50:
            raise AssertionError(' must be between 2 and 50 characters long')

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('Email cannot be blank')
        if email.find('@') == -1:
            raise AssertionError("Email should have a '@' sign; please check your email address.")

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('Password cannot be blank')
        if len(password) < 8:
            print("Make sure your password is at lest 8 letters")
        if re.search('[0-9]',password) is None:
            print("Make sure your password has a number in it")
        if re.search('[A-Z]',password) is None: 
            print("Make sure your password has a capital letter in it")

# defines an assignment of management (supervisors) to workers and teams
class Management(db.Model):
    # management kinds/types
    class Kind:
        Worker = "worker" # manage only a single worker
        Team = "team" # worker

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    # relationships
    target_id = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    manager = db.relationship("User", lazy=True)
