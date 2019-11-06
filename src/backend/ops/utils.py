#
# Memento
# Backend
# Operations Utilites
#

# maps the given object to a dict using given mapping
# mapping is a list of (field, key)
# returns the mappped dictionary
def map_dict(obj, mapping):
    obj_dict = {}
    for field, key in mapping:
        obj_dict[key] = getattr(obj, field)
    return obj_dict

# apply skip and limit to the given list of items
# returns the updated list
def apply_bound(items, skip=0, limit=None):
    items = items[skip:]
    if not limit is None: items = items[:limit]

    return items
