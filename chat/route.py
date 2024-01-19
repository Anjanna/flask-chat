import json
from flask import request, render_template, Blueprint, g, session
from chat.view import ChatService

chatapp = Blueprint("chat", __name__, url_prefix="/chat")

def home():
    return render_template("home.html")

def create_user():
    name = request.get_json().get("Name")
    if not name:
        return {"success": "False"}
    service = ChatService("Chat")
    user_id = service.create_user(name)
    session['user_id'] = user_id
    return json.dumps({"success": True})

def chat_app():
    service = ChatService("Chat", g.user_id)
    room = service.get_default_room()
    return render_template("chat.html", room=room, user=service.current_user)

def send_message(room_id):
    content = request.get_json().get("Content")
    user_id = g.user_id
    if not room_id or not content or not user_id:
        return {"Success": False}
    service = ChatService("Chat", g.user_id)
    service.send_message(room_id, content)
    return json.dumps({"success": True})

chatapp.add_url_rule(rule="", endpoint="home", view_func=home, methods=["GET"])
chatapp.add_url_rule(rule="/user", endpoint="create_user", view_func=create_user,
                     methods=["PUT"])
chatapp.add_url_rule(rule="/app", endpoint="app", view_func=chat_app, methods=["GET"])
chatapp.add_url_rule(rule="/room/<room_id>/message/send", endpoint="send-message",
                     view_func=send_message, methods=["POST"])


@chatapp.before_request
def set_user():
    user_id = session.get("user_id")
    g.user_id = user_id