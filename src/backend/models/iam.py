#
# Memento
# Backend
# IAM Models 
#

from enum import Enum
from ..app import db

# defines an organisation that users and teams belong to
class Organisation(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    logo_url = db.Column(db.String(2048), nullable=True)
    # relationships 
    teams = db.relationship("Team", backref="organisation", lazy=True)
    members = db.relationship("User", backref="organisation", lazy=True)

# defines a team in an organisation  that users can be belng too
class Team(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"),
                       nullable=False)
    members = db.relationship("User", backref="team", lazy=True)

# defines a user in the organisation.
class User(db.Model):
    # user kinds
    class Kind(Enum):
        Worker = "worker" # worker
        Supervisor = "worker" # supervisor of worker
        Admin = "admin" # root adminstrative user for the organisation
        Service = "service" # service account

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind=db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
