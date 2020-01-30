#
# Memento
# Backend
# Notification mappings
#

# defines the mapping from channel model fields to json api representation
channel_mapping = [
    ("user_id", "userId")
]

# defines the mapping from notification model fields to json api representation
notify_mapping = [
    ("title", "title"),
    ("description", "description"),
    ("firing_time", "firingTime"),
    ("channel_id", "channelId")
]
