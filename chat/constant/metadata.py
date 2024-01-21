class SystemFields:
    ID = "_id"
    CREATED_AT = "_created_at"
    CREATED_BY = "_created_by"


class User(SystemFields):
    NAME = "Name"
    ROLE = "Role"


class Room(SystemFields):
    NAME = "Name"


class Message(SystemFields):
    ROOM = "Room"
    RAW_DATA = "_raw_data"


class Collections:
    USER = "User"
    ROOM = "Room"
    MESSAGE = "Message"


class DB:
    CHAT = "Chat"