from flask import Flask
from chat.route import chatapp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatapp)
    return app

app = create_app()

app.secret_key = '35b69b12458df628f040c2e0c200584fd603b67e03b95eb2f6ed18d1abf9f038'
