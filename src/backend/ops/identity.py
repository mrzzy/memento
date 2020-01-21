#
# Memento
# Backend
# Identity Operations
#

from ..app import db
from ..models.identity import *
from ..mapping.identity import *
from .assignment import *
from ..utils import map_dict, apply_bound
from .notification import query_channels, delete_channel
from ..api.error import NotFoundError

## Organisation Ops
# query ids of organisations. 
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_orgs(skip=0, limit=None):
    org_ids = Organisation.query.with_entities(Organisation.id)
    org_ids = [ i[0] for i in org_ids ]
    org_ids = apply_bound(org_ids, skip, limit)

    return org_ids

# get organisation by id
# throws NotFoundError if no org with org_id is found
# returns organisation as a dict
def get_org(org_id):
    org = Organisation.query.get(org_id)
    if org is None: raise NotFoundError
    # map model fields to dict
    return map_dict(org, org_mapping)

# create a new organisation
# name - name of the organisation, must be uniqu
# logo_url - logo url for organisation. Optional.
# returns the id of the new organisation
def create_org(name, logo_url=None):
    org = Organisation(name=name, logo_url=logo_url)
    db.session.add(org)
    db.session.commit()

    return org.id

# update the organisation with given org_id
# org_id - update organisation with given id
# name - name of the organisation, must be uniqu
# logo_url - logo url for organisation. Optional.
# throws NotFoundError if no org with org_id is found
def update_org(org_id, name=None, logo_url=None):
    org = Organisation.query.get(org_id)
    if org is None: raise NotFoundError

    # update org fields
    if not name is None: org.name = name
    org.logo_url = logo_url
    db.session.commit()

# delete an organisation 
# throws NotFoundError if no org with org_id is found
# also cascade deletes all objects depending on organisation
# org_id - delete organisation with given id
def delete_org(org_id):
    org = Organisation.query.get(org_id)
    if org is None: raise NotFoundError

    # cascade delete users
    user_ids = query_users(org_id=org_id)
    for user_id in user_ids: delete_user(user_id)
    # cascade delete teams
    team_ids = query_teams(org_id=org_id)
    for team_id in team_ids: delete_team(team_id)
    # cascade delete scopped roles
    role_ids = query_roles(org_id=org_id)
    for role_id in role_ids: delete_role(role_id)

    db.session.delete(org)
    db.session.commit()

## Team Ops
# query ids of teams.
# org_ids - show only teams that belong to organisation given by org_id
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_teams(org_id=None, skip=0, limit=None):
    team_ids = Team.query.with_entities(Team.id)
    if not org_id is None: team_ids = team_ids.filter_by(org_id=org_id)
    team_ids = [ i[0] for i in team_ids ]
    team_ids = apply_bound(team_ids, skip, limit)

    return team_ids

# get team by team_id
# throws NotFoundError if no team with team_id is found
# returns team as a dict
def get_team(team_id):
    team = Team.query.get(team_id)
    if team is None: raise NotFoundError
    # map model fields to dict
    return map_dict(team, team_mapping)

# create a new team
# org_id - id of organisation that team belongs to 
# name - name for team
# returns team id
def create_team(org_id, name):
    team = Team(org_id=org_id, name=name)
    db.session.add(team)
    db.session.commit()

    return team.id

# update a existing team
# team_id - id of team being updated
# org_id - id of organisation that team belongs to 
# name - name for team
# throws NotFoundError if no team with team_id is found
def update_team(team_id, org_id=None, name=None):
    team = Team.query.get(team_id)
    if team is None: raise NotFoundError
    # update team fields
    if not org_id is None: team.org_id = org_id
    if not name is None: team.name = name
    db.session.commit()


# delete team for id 
# throws NotFoundError if no team with team_id is found
def delete_team(team_id):
    team = Team.query.get(team_id)
    if team is None: raise NotFoundError

    db.session.delete(team)
    db.session.commit()

## Team membership
# teams membership using roles/rolebinds
# teams members are given the editor role with team scope by default

# constructs the id of the role/rolebind that is used to track the the team membership
# team_id - id specifying the team in the team membership relationship
# user_id - id specifying the user in the team membership relationship
# returns role_id of the role, rolebind_id of the rolebindig
def get_team_member_ids(team_id, user_id):
    role_id  = str(Role(kind=Role.Kind.Editor, scope_kind=Role.ScopeKind.Team,
                        scope_target=team_id))
    rolebind_id = str(RoleBinding(role_id=role_id, user_id=user_id))
    return role_id, rolebind_id

# assign a user to the given team
# team_id - id of the target team being in assigned to 
# user_id - id of the user being assigned to the team
def assign_team(team_id, user_id):
    role_id, rolebind_id = get_team_member_ids(team_id, user_id)
    return create_role_relation(role_id, rolebind_id)

# reverse an assignment of the given user to the team
# rolebind_id - id of the rolebinding that tracks the team membership
def unassign_team(rolebind_id):
    delete_role_relation(rolebind_id)

## User Ops
# query ids of users
# org_id - show only users that belong to organisation given by org_id
# team_id - show only users that belong to team given by team_id
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_users(org_id=None, team_id=None, skip=0, limit=None):
    user_ids = User.query.with_entities(User.id)
    # apply filters
    if not org_id is None: user_ids = user_ids.filter_by(org_id=org_id)
    if not team_id is None:
        user_ids = user_ids.join(RoleBinding, RoleBinding.user_id == User.id)
        user_ids = user_ids.join(Role, Role.id == RoleBinding.role_id)
        user_ids = user_ids.filter(Role.scope_kind == Role.ScopeKind.Team,
                                     Role.scope_target == team_id,
                                     Role.kind == Role.Kind.Editor)
    # apply skip & limit
    user_ids = [ i[0] for i in user_ids ]
    user_ids = apply_bound(user_ids, skip, limit)

    return user_ids

# get user by id
# returns user as dict
# throws NotFoundError if no user with user_id is found
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None: raise NotFoundError
    # map fields to dict
    return map_dict(user, user_mapping)

# create a user
# name - name of the user
# password - password of the user
# email - email address of the user
# org_id - id of organisation that the user belongs to
# team_id - id of the team that the user belongs to, optional
# returns the id of the created user
def create_user(name, password, email, org_id, team_id=None):
    user = User(name=name, password=password,
                email=email, org_id=org_id, team_id=team_id)
    db.session.add(user)
    db.session.commit()

    return user.id

# update the user for the given user_id
# name - name of the user
# password - password of the user
# email - email address of the user
# org_id - id of organisation that the user belongs to
# team_id - id of the team that the user belongs to, optional
# throws NotFoundError if no user with user_id is found
def update_user(user_id, name=None, password=None,
                email=None, org_id=None, team_id=None):
    user = User.query.get(user_id)
    if user is None: raise NotFoundError
    # update user fields
    if not name is None: user.name = name
    if not password is None: user.password = password
    if not email is None: user.email = email
    if not org_id is None: user.org_id = org_id
    user.team_id = team_id
    db.session.commit()

# delete a user
# also cascade deletes all objects depending on user
# user_id - delete organisation with given id
# throws NotFoundError if no user with user_id is found
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None: raise NotFoundError
    # cascade delete
    # cascade delete mangement 
    manage_ids = query_manage(manager_id=user_id) + \
        query_manage(managee_id=user_id)
    for manage_id in manage_ids: delete_manage(manage_id)
    # cascade delete assignments created
    assign_ids = query_assigns(assigner_id=user_id)
    for assign_id in assign_ids: delete_assign(assign_id)
    # cascade delete tasks/events created
    task_ids = query_tasks(author_id=user_id)
    for task_id in task_ids: delete_task(task_id)
    event_ids = query_events(author_id=user_id)
    for event_id in event_ids: delete_event(event_id)
    # cascde delete channel
    channel_ids = query_channels(user_id=user_id)
    for channel_id in channel_ids: delete_channel(channel_id)
    # cascade delete scopped roles
    role_ids = query_roles(user_id=user_id)
    for role_id in role_ids: delete_role(role_id)
    # cascade delete bound rolebindings
    rolebind_ids = query_role_bindings(user_id=user_id)
    for rolebind_id in rolebind_ids: delete_role_binding(rolebind_id)

    db.session.delete(user)
    db.session.commit()

## Management Ops
# management is implemented using roles/rolebinds: 
# managers are given the admin role in user scope for the target user

# constructs the id of the role/rolebind that is used to track the management relationship 
# managee_id - the id of the user that acts as the managed in the relationship
# manager_id - the id of the user that acts as the manager in the relationship
# returns role_id of the role, rolebind_id of the rolebindig
def get_manage_ids(managee_id, manager_id):
    role_id  = str(Role(kind=Role.Kind.Admin, scope_kind=Role.ScopeKind.User,
                        scope_target=managee_id))
    rolebind_id = str(RoleBinding(role_id=role_id,
                                  user_id=manager_id))
    return role_id, rolebind_id

# query managment rolebinds
# org_id - show only managements that belong to the given organisation
# mangee_id - show managements that manage the given user.
# manager_id - show only mangements with manager with given id
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_manage(org_id=None, managee_id=None,
                 manager_id=None, skip=0, limit=None):
    # filter rolebinds to those that like a management relationship
    rolebind_ids = RoleBinding.query.with_entities(RoleBinding.id)
    rolebind_ids.join(Role, Role.id == RoleBinding.role_id)
    rolebind_ids = rolebind_ids.filter(Role.kind == Role.Kind.Admin,
                                       Role.scope_kind == Role.ScopeKind.User)

    # apply filters
    if not managee_id is None:
        rolebind_ids = rolebind_ids.filter(Role.scope_target == managee_id)
    if not manager_id is None:
        rolebind_ids = rolebind_ids.filter_by(user_id=manager_id)
    if not org_id is None:
        rolebind_ids = rolebind_ids.join(User, User.id == RoleBinding.user_id)
        rolebind_ids = rolebind_ids.filter(User.org_id == org_id)

    # apply skip & limit
    rolebind_ids = [ i[0] for i in rolebind_ids ]
    rolebind_ids = apply_bound(rolebind_ids, skip, limit)

    return rolebind_ids

# get management for id
# returns managements as a dict
# throws NotFoundError if no manage with manage_id is found
def get_manage(rolebind_id):
    rolebind = RoleBinding.query.get(rolebind_id)
    if rolebind is None: raise NotFoundError
    # map fields to dict
    manage_dict = {
        "manageeId": rolebind.role.scope_target,
        "managerId": rolebind.user_id
    }
    return manage_dict

# create a management by creating the corresponding role and rolebind
# managee_id - id of the worker/team that is being managed
# manager_id - id of the user that is assigned to manage target
# returns the id of the rolebind that represents the managment relationship
def create_manage(managee_id, manager_id):
    role_id, rolebind_id = get_manage_ids(managee_id, manager_id)
    return create_role_relation(role_id, rolebind_id)

# update management for given rolebind_id
# managee_id - id of the worker/team that is being managed
# manager_id - id of the user that is assigned to manage target
# throws NotFoundError if no management relationship with rolebind_id is found
def update_manage(rolebind_id, managee_id=None, manager_id=None):
    manage = get_manage(rolebind_id)
    if managee_id is None: managee_id = manage["manageeId"]
    if manager_id is None: manager_id = manage["managerId"]

    delete_manage(rolebind_id)
    create_manage(managee_id, manager_id)

# delete management for given rolebind_id
# throws NotFoundError if no management relationship with rolebind_id is found
# cascade deletes role if no other role bound to it
def delete_manage(rolebind_id):
    delete_role_relation(rolebind_id)

## Role Ops
# query id of roles based on params:
# org_id - show only managements that are scoped to the given organisation
# user_id - show only roles that are scoped to the given user
# bound_to - show only role that are bound to the given user
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_roles(org_id=None, user_id=None, bound_to=None, skip=None, limit=None):
    role_ids = Role.query.with_entities(Role.id)
    # apply filters
    if not org_id is None:
        role_ids = role_ids.filter_by(scope_kind=Role.ScopeKind.Organisation,
                                      scope_target=org_id)
    if not user_id is None:
        role_ids = role_ids.filter_by(scope_kind=Role.ScopeKind.User,
                                      scope_target=user_id)
    if not bound_to is None:
        role_ids = role_ids.join(RoleBinding, RoleBinding.role_id == Role.id)
        role_ids = role_ids.filter(RoleBinding.user_id == bound_to)
    # apply skip & limit
    role_ids = [ i[0] for i in role_ids ]
    role_ids = apply_bound(role_ids, skip, limit)

    return role_ids

# get role for given role_id
# returns role as a dict
# throws NotFoundError if no role with role_id is found
def get_role(role_id):
    role = Role.query.get(role_id)
    if role is None: raise NotFoundError
    # map model fields to dict
    return map_dict(role, role_mapping)

# create a new role
# kind - kind of role to create
# scope_kind - kind of scope to place the role in
# scope_target - target id of the object of the scope to place the role in
# returns the id of the new  role
def create_role(kind, scope_kind, scope_target=None):
    role = Role(kind=kind, scope_kind=scope_kind, scope_target=scope_target)
    role.id = str(role)
    db.session.add(role)
    db.session.commit()
    return role.id

# delete role for the given role_id
# cascade deletes relate objects
# throws NotFoundError if no role with role_id is found
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role is None: raise NotFoundError
    # casacade delete role bindings
    binding_ids = query_role_bindings(role_id=role_id)
    for binding_id in binding_ids: delete_role_binding(binding_id)
    db.session.delete(role)
    db.session.commit()

## Role Binding Ops
# query id of role bindings based on params:
# role_id - filter role bindings by role
# user_id  - filter role bindings by user
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_role_bindings(role_id=None, user_id=None, skip=None, limit=None):
    binding_ids = RoleBinding.query.with_entities(RoleBinding.id)
    # apply filters
    if not role_id is None: binding_ids = binding_ids.filter_by(role_id=role_id)
    if not user_id is None: binding_ids = binding_ids.filter_by(user_id=user_id)
    # apply skip & limit
    binding_ids = [ i[0] for i in binding_ids ]
    binding_ids = apply_bound(binding_ids, skip, limit)
    return binding_ids

# get the role binding for the given role binding id
# returns a dictionary representation of the role binding
# throws NotFoundError if no manage with manage_id is found
def get_role_binding(binding_id):
    binding = RoleBinding.query.get(binding_id)
    if binding is None: raise NotFoundError
    # map model fields to dict
    return map_dict(binding, role_binding_mapping)

# create a role binding
# role_id - id of the role to bind to
# user_id - id of the user to bind to
# returns the id of the new role binding
def create_role_binding(role_id, user_id):
    binding = RoleBinding(role_id=role_id, user_id=user_id)
    binding.id = str(binding)

    db.session.add(binding)
    db.session.commit()
    return binding.id

# delete the role binding for the given role binding id
# throws NotFoundError if no manage with manage_id is found
def delete_role_binding(binding_id):
    binding = RoleBinding.query.get(binding_id)
    if binding is None: raise NotFoundError
    db.session.delete(binding)
    db.session.commit()

## Role Relation ops
# role relations are relationships represented as roles and rolebindings

# create role & rolebinding used to represent an relationship
# only tries to create role if does not already exist
# role_id - the id of the role used to represent the relationship
# rolebind_id - the id of the rolebind used to represent the relationship
def create_role_relation(role_id, rolebind_id):
    # create role if does already exist
    if Role.query.get(role_id) is None:
        role = Role.from_id(role_id)
        db.session.add(role)
        db.session.commit()

    # create rolebind that represents the management relationship
    rolebind = RoleBinding.from_id(rolebind_id)
    db.session.add(rolebind)
    db.session.commit()

    return rolebind_id

# delete role & rolebinding  used to represent the relationshipa
# only tries to casacade delete role if not used by other rolebindings
# rolebind_id - the id of the rolebind used to represent the relationship
def delete_role_relation(rolebind_id):
    # delete rolebinding
    rolebind = RoleBinding.query.get(rolebind_id)
    if rolebind is None: raise NotFoundError
    role_id = rolebind.role.id
    delete_role_binding(rolebind_id)

    # check if role has any rolebindings, if so delete role too
    rolebind_ids = RoleBinding.query.filter_by(role_id=role_id)
    if rolebind_ids.count() < 1:
        delete_role(role_id)


