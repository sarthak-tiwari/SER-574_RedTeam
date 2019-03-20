# Class to launch github api service on flask
#
# Author: Sarthak Tiwari, Ruben Acuna
# E-Mail: sarthak.tiwari@asu.edu, racuna1@asu.edu

from flask import Flask, request
import datetime
import json

from static_code_analysis.CheckStyleManager import CheckStyleManager
#import metadata_analysis.commit_frequency as CF
#import db_api as DB

app = Flask(__name__)


# TODO: this should be somewhere else
def parse_str_date(str_date):
    year = int(str_date[0:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    proper_date = datetime.datetime(year, month, day)
    return proper_date

################################################################################
# General DB Access Calls


# ex: 127.0.0.1:5000/github/core_fetch_commit?git_id=168214867&commit_hash="70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
@app.route('/github/core_fetch_commit', methods=('GET', 'POST'))
def api_core_fetch_commit():
    git_id = request.args.get('git_id', type=int)
    commit_hash = request.args.get('commit_hash')

    result = {'hash': '70f13b111e1147611b70f9c9f1f76ddb00fcbe27', 'repositoryID': 168214867, 'author': 'test', 'message': 'Added gitignore for python to the source directory', 'date': 20190206, 'timeCommitted': '2019-02-07T23:39:00Z', 'files': '[".gitignore"]', 'additions': 116, 'deletions': 0}
    # result = DB.fetch_commit(git_id, commit_hash)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)

################################################################################
# Comment Analysis::Frequency


# ex: 127.0.0.1:5000/github/count_in_internal?git_id=168214867&username="test"&interval_start=20190201&interval_end=20190228
@app.route('/github/count_in_internal', methods=('GET', 'POST'))
def api_count_in_internal():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = 1
    # result = CF.count_in_internal(git_id, username, interval_start, interval_end)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/count_on_day?git_id=168214867&username="test"&date=20190208
@app.route('/github/count_on_day', methods=('GET', 'POST'))
def api_count_on_day():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    date = parse_str_date(request.args.get('date'))

    result = 0
    # result = CF.count_on_day(git_id, username, date)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/count_list_interval?git_id=168214867&username="test"&interval_start=20190201&interval_end=20190228
@app.route('/github/count_list_interval', methods=('GET', 'POST'))
def count_list_interval():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # result = CF.count_list_interval(git_id, username, interval_start, interval_end)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)

################################################################################
# Comment Analysis::Commit Messages

# ex: 127.0.0.1:5000/github/compute_quality?git_id=168214867&commit_hash="70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
@app.route('/github/compute_quality', methods=('GET', 'POST'))
def api_compute_quality():
    git_id = request.args.get('git_id', type=int)
    commit_hash = request.args.get('commit_hash')

    result = 50
    # result = CF.compute_quality(git_id, commit_hash)
    # def compute_quality(github_id, commit_hash):

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)

################################################################################
# Comment Analysis::Comments

@app.route('/github/', methods=('GET', 'POST'))
def test():
    filename = request.args.get('filename')

    header = {'Content-Type': 'application/json'}
    metrics = CheckStyleManager.getDummyComplexities(filename)
    data = json.dumps({"filename": filename, "metrics": metrics})
    return (data, header)

if __name__ == '__main__':
    app.run()
