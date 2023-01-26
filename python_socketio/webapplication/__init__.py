import os, pyrebase
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'webapplication/frontend/')

def create_server():
    app = Flask(__name__, template_folder=TEMPLATE_PATH + '/templates', static_folder=TEMPLATE_PATH + 'static/',)
    app.config['SECRET_KEY'] = 'al_procedure'
    
    CORS(app)
    sio = SocketIO(app, cors_allowed_origins='*')

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .socketNamespace import RoomServices
    sio.on_namespace(RoomServices('/room'))
   
    return app, sio


def firebase_init():
    from .firebaseInit import config

    firebase = pyrebase.initialize_app(config)  
    database = firebase.database()

    return database

db = firebase_init()