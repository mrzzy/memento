#
# Memento
# Backend
# API utils
#

from ..utils import map_keys, reverse_mapping

# parse the params from the given request's body
# using the given mapping to parse the paramsf
# returns the parsed params
def parse_params(request, mapping):
    params = request.get_json()
    params = map_keys(params, reverse_mapping(mapping))
    return params
