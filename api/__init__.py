from flask import Flask
from firebase_admin import credentials,initialize_app

import firebase_admin


cred = credentials.Certificate("api/key.json")


default_app=initialize_app(cred)

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='12345JFG'

    from .Routes import Routes
    app.register_blueprint(Routes,url_prefix='/myfin')

    return app