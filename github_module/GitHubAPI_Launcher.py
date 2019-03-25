# Class to launch github api service on flask
#
# Author: Sarthak Tiwari, Ruben Acuna
# E-Mail: sarthak.tiwari@asu.edu, racuna1@asu.edu

from flask import Flask, request
import datetime
import json
import sqlite3
import GithubAPI

from static_code_analysis.CheckStyleManager import CheckStyleManager
import metadata_analysis.commit_frequency as CF

app = Flask(__name__)


# TODO: this should be somewhere else
def parse_str_date(str_date):
    year = int(str_date[0:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    proper_date = datetime.datetime(year, month, day)
    return proper_date

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
    # result = CF.compute_quality(git_id, username, date)
    # def compute_quality(github_id, commit_hash):

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)

################################################################################
# Comment Analysis::Comments


@app.route('/github/pull_request', methods=('GET', 'POST'))
def api_count_pull():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    db.execute("SELECT * FROM pullData")
    result = db.fetchall()
    pulls_data = []
    for data in result:
        pull_data = {}
        pull_data['request_title']: data.requestTile
        pull_data['author']: data.author
        pull_data['no_of_comments']: data.noOfComments
        pull_data['target_branch']: data.targetBranch
        pull_data['no_of_reviews']: data.noOfReviews
        pulls_data.append(pull_data)
    return jsonify({'result': pulls_data})


@app.route('/github/user', methods=('GET', 'POST'))
def api_count_pull():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    db.execute("SELECT * FROM userProfile")
    result = db.fetchall()
    users_data = []
    for data in result:
        user_data = {}
        user_data['github_login']: data.githubLogin
        user_data['github_username']: data.githubUsername
        user_data['github_profile']: data.githubProfile
        users_data.append(user_data)
    return jsonify({'result': users_data})


@app.route('/github/', methods=('GET', 'POST'))
def test():
    filename = request.args.get('filename')

    header = {'Content-Type': 'application/json'}
    metrics = CheckStyleManager.getDummyComplexities(filename)
    data = json.dumps({"filename": filename, "metrics": metrics})
    return (data, header)


if __name__ == '__main__':
    app.debug = True
    app.run()
