# Class to launch github api service on flask
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

from flask import Flask
import json

app = Flask(__name__)

@app.route('/github/', methods=('GET', 'POST'))
def test():
    header = {'Content-Type': 'application/json'}
    data = json.dumps({"data": "Test Data"})
    return (data, header)

if __name__ == '__main__':
    app.run()