# Class to launch github api service on flask
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

from flask import Flask

app = Flask(__name__)

@app.route('/github/')
def test():
    return 'Test Data'