#
# Memento/Backend
# Notification service
# datastore
#

from abc import ABC, abstractmethod

# defines a abstract datastore for storing notification service objects
class DataStore(ABC):
    ## query methods
    # Get ids objects with the given for the given parameters
    # kind - kind of object are quering
    # pending - show only objects that are pending (ie notifications not fired)
    # user - show objects associated with user id
    # skip - skip the first n results
    # limit - show the first n results (after skip)
    # Returns a list of matching object ids
    @abstractmethod
    def query(kind, pending=False, user=None, skip=0, limit=None):
        pass

    # Get ids objects with the given for the given parameters
    # kind - kind of object we are querying
    # obj_id - id of the specific object to get.
    # Returns the object or None if no matching object is found
    @abstractmethod
    def get(kind, obj_id):
        pass

    # create the given object of the given kind  in the datastore.
    # Returns the obj_id of the created object.
    @abstractmethod
    def create(kind, obj):
        pass

    # update the object the given kind with the given obj_id 
    # with the contents of the given obj
    # Returns the obj_id of the updated object.
    @abstractmethod
    def update(kind, obj_id, obj):
        pass

    # Delete the object of the given kind with the given obj_id
    # Returns the obj_id of the updated object.
    def delete(kind, obj_id):
        pass
