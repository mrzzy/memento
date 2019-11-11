#
# Memento
# Backend
# Assignment mappings
#


# defines the mapping from task model fields to json api representation
task_mapping = [
    ("name", "name"),
    ("description", "description"),
    ("duration", "duration"),
    ("deadline", "deadline"),
    ("completed", "completed"),
    ("author_id", "authorId")
]

# defines the mapping from event model fields to json api representation
event_mapping = [
    ("name", "name"),
    ("description", "description"),
    ("start_time", "startTime"),
    ("duration", "duraiton"),
    ("author_id", "authorId")
]

# defines the mapping from assign model fields to json api representation
assign_mapping = [
    ("kind", "kind"),
    ("item_id", "itemId"),
    ("assignee_id", "assigneeId"),
    ("assigner_id", "assignerId")
]
