#
# Memento
# Backend
# IAM Operations
#

from ..app import db
from ..models.iam import *

## Organisation Ops
# query ids of organisations. 
# skip - skip the first skip organisations
# limit - output ids limit to the first limit organisations
def query_orgs(skip=0, limit=None):
    # obtain a list of organisation ids
    org_ids = Organisation.query.with_entities(Organisation.id)
    org_ids = [ i[0] for i in org_ids ]
    # apply skip and limit
    org_ids = org_ids[skip:]
    if not limit is None: org_ids = org_ids[:limit]

    return org_ids

# get organisation by id
# returns organisation as a dict
def get_org(org_id):
    org = Organisation.query.get(org_id)
    # map model fields to dict
    mapping = [
        ("name", "name"),
        ("logo_url", "logo_url")
    ]
    org_dict = {}
    for key, field in mapping:
        org_dict[key] = getattr(org, field)
    return org_dict

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
    if name: org.name = name
    if logo_url: org.logo_url = logo_url
    db.session.commit()

# delete an organisation 
# also cascade deletes all objects refering to organisation
# org_id - delete organisation with given id
def delete_org(org_id):
    org = Organisation.query.get(org_id)

    # TODO: cascade delete all

    db.session.delete(org)
    db.session.commit()
