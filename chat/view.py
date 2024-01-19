from flask import session, g
from chat.db import ChatSession
from chat.util import generate_uuid
from chat.firebase import FirebaseHelper
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
        return self.get_doc({"_id": user_id}, "User")

    def create_user(self, username):
        """
        Creates a user in the User collection
        :param username: user nickname
        """
        user = self.get_doc({"Name": username}, "User")
        if user:
            return user["_id"]
        user = {
            "_id": "Us" + generate_uuid(),
            "_created_at": datetime.utcnow(),
            "Role": "Member",
            "Name": username
        }
        data = self.insert_one(user, "User")
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
            "_id": "Ms" + generate_uuid(),
            "Room": room_id,
            "_raw_data": content,
            "_created_at": datetime.utcnow(),
            "_created_by": {"_id": user["_id"], "Name": user["Name"]}
        }
        self.insert_one(message, "Message")
        firebase_path = f"/{room_id}"
        return FirebaseHelper().put_data(message, firebase_path)

    def create_room(self, name):
        """
        Creates a room in the Room collection with the given <<name>>
        :param name: name of the room
        """
        user = self.current_user
        room = {
            "_id": "Ro" + generate_uuid(),
            "Name": name,
            "_created_at": datetime.utcnow(),
            "_created_by": {"_id": user["_id"], "Name": user["Name"]}
        }
        return self.insert_one(room, "Room")

    def get_default_room(self):
        """
        Returns the details of the default chat room
        """
        return self.get_doc({}, "Room")