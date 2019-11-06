#
# Memento
# Backend
# IAM Operations
#

from ..app import db
from ..models.iam import *

from .utils import map_dict, apply_bound

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
# returns organisation as a dict
def get_org(org_id):
    org = Organisation.query.get(org_id)
    # map model fields to dict
    mapping = [
        ("name", "name"),
        ("logo_url", "logoUrl")
    ]
    return map_dict(org, mapping)

# create a new organisation
# name - name of the organisation, must be uniqu
# logo_url - logo url for organisation. Optional.
# returns the id of the new organisation
def create_org(name, logo_url=None):
    org = Organisation(name=name, logo_url=logo_url)
    db.session.add(org)
    db.session.commit()

    return org.id

# update an organisation
# org_id - update organisation with given id
# name - name of the organisation, must be uniqu
# logo_url - logo url for organisation. Optional.
def update_org(org_id, name=None, logo_url=None):
    org = Organisation.query.get(org_id)
    if not name is None: org.name = name
    if not logo_url is None : org.logo_url = logo_url
    db.session.commit()

# delete an organisation 
# also cascade deletes all objects refering to organisation
# org_id - delete organisation with given id
def delete_org(org_id):
    org = Organisation.query.get(org_id)

    # TODO: cascade delete all

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
# returns team as a dict
def get_team(team_id):
    team = Team.query.get(team_id)
    # map model fields to dict
    mapping = [
        ("name", "name"),
        ("org_id", "orgId")
    ]
    return map_dict(team, mapping)

# create a new team
# org_id - id of organisation that team belongs to 
# name - name for team
def create_team(org_id, name):
    team = Team(org_id=org_id, name=name)
    db.session.add(team)
    db.session.commit()

    return team.id

# update a existing team
# team_id - id of team being updated
# org_id - id of organisation that team belongs to 
# name - name for team
def update_team(team_id, org_id=None, name=None):
    team = Team.query.get(team_id)
    if not org_id is None: team.org_id = org_id
    if not name is None: team.name = name
    db.session.commit()


# delete team for id 
def delete_team(team_id):
    team = Team.query.get(team_id)
    db.session.delete(team)
    db.session.commit()
