#
# Memento
# Backend
# Notification mappings
#

# defines the mapping from channel model fields to json api representation
channel_mapping = [
    ("title", "title"),
    ("description", "description"),
    ("firing_time", "firingTime"),
    ("channel_id", "channelId")
]

# defines the mapping from notification model fields to json api representation
notify_mapping = [
    ("title", "title"),
    ("description", "description"),
    ("firing_time", "firingTime"),
    ("channel_id", "channelId")
]
