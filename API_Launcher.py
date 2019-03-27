# Class to launch api service on flask
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

from flask import Flask

#from github_module.GitHubAPI_Launcher import github_api
from taiga_module.taiga_sp_di_api import taiga_api

app = Flask(__name__)

#app.register_blueprint(github_api, url_prefix='/github')
app.register_blueprint(taiga_api, url_prefix='/taiga')
