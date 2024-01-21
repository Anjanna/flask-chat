import json
from flask import request, render_template, Blueprint, g, session
from chat.view import ChatService
from chat.constant.route import Endpoint, HTTP_REQUEST_METHOD
from chat.constant.metadata import User, DB

chatapp = Blueprint("chat", __name__, url_prefix="/chat")

def home():
    return render_template("home.html")

def create_user():
    name = request.get_json().get(User.NAME)
    if not name:
        return {"success": "False"}
    service = ChatService(DB.CHAT)
    user_id = service.create_user(name)
    session['user_id'] = user_id
    return json.dumps({"success": True})

def chat_app():
    service = ChatService(DB.CHAT, g.user_id)
    room = service.get_default_room()
    return render_template("chat.html", room=room, user=service.current_user)

def send_message(room_id):
    content = request.get_json().get("Content")
    user_id = g.user_id
    if not room_id or not content or not user_id:
        return {"Success": False}
    service = ChatService(DB.CHAT, g.user_id)
    service.send_message(room_id, content)
    return json.dumps({"success": True})

chatapp.add_url_rule(rule="", endpoint=Endpoint.HOME, view_func=home,
                     methods=[HTTP_REQUEST_METHOD.GET])
chatapp.add_url_rule(rule="/user", endpoint=Endpoint.CREATE_USER, view_func=create_user,
                     methods=[HTTP_REQUEST_METHOD.PUT])
chatapp.add_url_rule(rule="/app", endpoint=Endpoint.APP, view_func=chat_app,
                     methods=[HTTP_REQUEST_METHOD.GET])
chatapp.add_url_rule(rule="/room/<room_id>/message/send", endpoint=Endpoint.SEND_MESSAGE,
                     view_func=send_message, methods=[HTTP_REQUEST_METHOD.POST])


@chatapp.before_request
def set_user():
    user_id = session.get("user_id")
    g.user_id = user_id