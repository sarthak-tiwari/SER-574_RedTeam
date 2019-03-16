# Class to launch github api service on flask
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

from flask import Flask, request
import json

from static_code_analysis.CheckStyleManager import CheckStyleManager

app = Flask(__name__)

@app.route('/github/', methods=('GET', 'POST'))
def test():
    filename = request.args.get('filename')

    header = {'Content-Type': 'application/json'}
    metrics = CheckStyleManager.getDummyComplexities(filename)
    data = json.dumps({"filename": filename, "metrics": metrics})
    return (data, header)

if __name__ == '__main__':
    app.run()