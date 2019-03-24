# Class to launch github api service on flask
#
# Author: Sarthak Tiwari, Ruben Acuna
# E-Mail: sarthak.tiwari@asu.edu, racuna1@asu.edu

from flask import Flask, request
import datetime
import json

from github_module.GitHubAPI_Launcher import github_api

app = Flask(__name__)
app.register_blueprint(github_api, url_prefix='/github')