from flask import g
from chat.view import ChatService
from chat.db import ChatSession
from chat.mock.mock_data import USER, MESSAGE


def test_create_user():
    service = ChatService("test")
    username = "anjanna"
    response = service.create_user(username)
    filter = {"_id": response.inserted_id}
    result = service.get_doc(filter, "User")
    assert result["Name"] == username

def test_create_room():
    service = ChatService("test", USER["_id"])
    room_name = "General"
    response = service.create_room(room_name)
    filter = {"_id": response.inserted_id}
    result = service.get_doc(filter, "Room")
    assert result["Name"] == room_name

def test_send_message():
    service = ChatService("test", USER["_id"])
    response = service.send_message(MESSAGE["RoomId"], MESSAGE["Content"])
    assert response.acknowledged is True

def test_get_default_room():
    service = ChatService("test")
    response = service.get_default_room()
    assert response["Name"] == "General"
