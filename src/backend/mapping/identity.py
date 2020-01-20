#
# Memento
# Backend
# Identity mappings
#

# defines the mapping from org model fields to json api representation
org_mapping = [
    ("name", "name"),
    ("logo_url", "logoUrl")
]

# defines the mapping from team model fields to json api representation
team_mapping = [
    ("name", "name"),
    ("org_id", "orgId")
]

# defines the mapping from user model fields to json api representation
user_mapping = [
    ("name", "name"),
    ("password", "password"),
    ("email", "email"),
    ("org_id", "orgId"),
    ("team_id", "teamId")
]

# defines the mapping from management model fields to json api representation
manage_mapping = [
    ("managee_id", "manageeId"),
    ("manager_id",  "managerId")
]

# defines the mapping from role  model fields to json api representation
role_mapping = [
    ("kind", "kind"),
    ("scope_kind", "scopeKind"),
    ("scope_target", "scopeTarget")
]

# defines the mapping from rolebinding  model fields to json api representation
role_binding_mapping = [
    ("user_id", "userId"),
    ("role_id", "roleId")
]
