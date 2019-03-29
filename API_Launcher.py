# Class to launch api service on flask
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

from flask import Flask
from flask_cors import CORS

from github_module.GitHubAPI_Launcher import github_api
from taiga_module.taiga_sp_di_api import taiga_api

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': ['http://10.153.48.199:8080', 'https://ser574-redteam-ui.firebaseapp.com', 'http://192.168.0.20:8080', '127.0.0.1']}})

app.register_blueprint(github_api, url_prefix='/github')
app.register_blueprint(taiga_api, url_prefix='/taiga')