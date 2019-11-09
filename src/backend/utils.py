#
# Memento
# Backend
# Operations Utilites
#

# reverse mapping - swap mappings ordering
# returns reverse mapping
def swap_mapping(mapping):
    return [ (a, b) for a, b in mapping ]

# maps the given object to a dict using given mapping
# mapping is a list of (field, key)
# returns the mappped dictionary
def map_dict(obj, mapping):
    obj_dict = {}
    for field, key in mapping:
        obj_dict[key] = getattr(obj, field)
    return obj_dict

# maps data from map_dict into object fields on the given object
# using the given mapping (a list of (key, field))
# returns the obj with the updated fields
def map_obj(obj, map_dict, mapping):
    for key, field in mapping:
        setattr(obj, field, map_dict[key])
    return obj

# apply skip and limit to the given list of items
# returns the updated list
def apply_bound(items, skip=0, limit=None):
    items = items[skip:]
    if not limit is None: items = items[:limit]

    return items
