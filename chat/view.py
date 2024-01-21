from chat.db import ChatSession
from chat.util import generate_uuid
from chat.firebase import FirebaseHelper
from chat.constant.metadata import User, Room, Message, Collections
from datetime import datetime

class ChatService(ChatSession):
    def __init__(self, db_name, current_user_id=None):
        super().__init__(db_name)
        self.__current_user_id = current_user_id
        self.__current_user = None

    @property
    def current_user(self):
        if not self.__current_user:
            self.__current_user = self.set_current_user(self.__current_user_id)
        return self.__current_user

    def set_current_user(self, user_id):
        return self.get_doc({"_id": user_id}, Collections.USER)

    def create_user(self, username):
        """
        Creates a user in the User collection
        :param username: user nickname
        """
        user = self.get_doc({User.NAME: username}, Collections.USER)
        if user:
            return user[User.ID]
        user_id = "Us" + generate_uuid(),
        user = {
            User.ID: user_id,
            User.CREATED_AT: datetime.utcnow(),
            User.CREATED_BY: {User.ID: user_id, User.NAME: username},
            User.ROLE: "Member",
            User.NAME: username
        }
        data = self.insert_one(user, Collections.USER)
        return data.inserted_id

    def get_doc(self, filter_query, collection):
        """
        Returns a single doc based on the given filter query
        :param filter_query: filter query
        :param collection: collection name
        """
        return self.find_one(filter_query, collection)

    def send_message(self, room_id, content):
        """
        Saves the message in room <<room_id>> into the Message collection
        :param room_id: room id
        :param content: message content
        """
        user = self.current_user
        message = {
            Message.ID: "Ms" + generate_uuid(),
            Message.ROOM: room_id,
            Message.RAW_DATA: content,
            Message.CREATED_AT: datetime.utcnow(),
            Message.CREATED_BY: {User.ID: user[User.ID], User.NAME: user[User.NAME]}
        }
        self.insert_one(message, Collections.MESSAGE)
        firebase_path = f"/{room_id}"
        return FirebaseHelper().put_data(message, firebase_path)

    def create_room(self, name):
        """
        Creates a room in the Room collection with the given <<name>>
        :param name: name of the room
        """
        user = self.current_user
        room = {
            Room.ID: "Ro" + generate_uuid(),
            Room.NAME: name,
            Room.CREATED_AT: datetime.utcnow(),
            Room.CREATED_BY: {User.ID: user[User.ID], User.NAME: user[User.NAME]}
        }
        return self.insert_one(room, Collections.ROOM)

    def get_default_room(self):
        """
        Returns the details of the default chat room
        """
        return self.get_doc({}, Collections.ROOM)