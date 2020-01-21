#
# Memento
# Backend
# Identity Models 
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
            raise AssertionError('Organisation name must not be empty')
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError(' must be between 2 and 256 characters long')
        else:
            return name

# defines a team in an organisation  that users can be belng too
class Team(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"),
                       nullable=False)
    members = db.relationship("User", backref=db.backref("team"), lazy=True)

# defines a user in the organisation.
class User(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), unique=True, nullable=False)
    # relationships 
    org_id = db.Column(db.Integer, db.ForeignKey("organisation.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    role_bindings = db.relationship("RoleBinding", backref=db.backref("user"), lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Name must not be empty')
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError(' must be between 2 and 256 characters long')
        else:
            return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('Email must not be empty')
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            raise AssertionError('Ensure it is the correct email input')
        else:
            return email

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('Password must not be empty')
        elif not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$",password):
            raise AssertionError('at least one digit, one uppercase letter, at least one lowercase letter, at least one special character')
        else:
         return password

# defines a role that can be assigned to users
class Role(db.Model):
    # kinds of scope in which a role can be scoped
    class ScopeKind:
        Global = "global"
        Organisation = "org" # scope of role limited to specific organisation
        Team = "team" # scope of role limited to specific team
        User = "user" # scope of role limited to specific user
    # kinds of roles that can be assigned to users
    class Kind:
        Admin = "admin" # allows CRUD access to resource & changing ACL
        Editor = "editor" # allows R/W access to resource
        Viewer = "viewer" # allows R/O access to the resource
    # model fields
    id = db.Column(db.String(512), primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    scope_kind = db.Column(db.String(64), default=ScopeKind.User, nullable=False)
    scope_target = db.Column(db.Integer, default=0)

    # relationships
    bindings = db.relationship("RoleBinding", backref=db.backref("role"), lazy=True)

    # generates a unique str representation of the role based on model fields
    # this string should be used as the model's id on creation
    # returns a string representation of the role
    def __str__(self):
        scope_part = self.scope_kind + \
            f"__{self.scope_target}" if not self.scope_target is None else ""
        return f"{scope_part}..{self.kind}"

    # loads model fields with infomation decoded from the given role id
    @classmethod
    def from_id(cls, id):
        scope_part, kind = id.split("..")
        scope_kind, scope_target = scope_part.split("__")
        return cls(id=id,kind=kind, scope_kind=scope_kind,
                   scope_target=int(scope_target))

# define a binding between a role and user
class RoleBinding(db.Model):
    # model fields
    id = db.Column(db.String(640), primary_key=True)
    # relationships
    role_id = db.Column(db.String(512), db.ForeignKey("role.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # generates a unique str representation of the role based on model fields
    # this string should be used as the model's id on creation
    # returns a string representation of the role
    def __str__(self):
        return f"{self.role_id}~~{self.user_id}"

    # loads model fields with infomation decoded from the given role binding id
    @classmethod
    def from_id(cls, id):
        role_id, user_id = id.split("~~")
        return cls(id=id, role_id=role_id, user_id=int(user_id))
