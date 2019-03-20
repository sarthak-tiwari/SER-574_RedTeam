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


# TODO: these should be somewhere else
def parse_str_date(str_date):
    year = int(str_date[0:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    proper_date = datetime.datetime(year, month, day)
    return proper_date


def dateobj_to_strdate(date):
    return str(date.year).zfill(4) + str(date.month).zfill(2) + str(date.day).zfill(2)

################################################################################
# General DB Access Calls


# ex: 127.0.0.1:5000/github/core_initialize_repo?git_id=168214867
@app.route('/github/core_initialize_repo', methods=('GET', 'POST'))
def api_core_initialize_repo():
    git_id = request.args.get('git_id', type=int)

    if not git_id:
        status = "error"
        result = "Failed to parse git_id parameter."
    else:
        status = "unimplemented"
        result = True
        # result = DB.initialize_repo_data(git_id)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": status, "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/core_fetch_repo_hashes?git_id=168214867
@app.route('/github/core_fetch_repo_hashes', methods=('GET', 'POST'))
def api_core_fetch_repo_hashes():
    git_id = request.args.get('git_id', type=int)

    if not git_id:
        status = "error"
        result = "Failed to parse git_id parameter."
    else:
        status = "unimplemented"
        result = ['70f13b111e1147611b70f9c9f1f76ddb00fcbe27', '70f13b111e1147611b70f9c9f1f76ddb00fcbe28', '70f13b111e1147611b70f9c9f1f76ddb00fcbe29', '70f13b111e1147611b70f9c9f1f76ddb00fcbe2a', '70f13b111e1147611b70f9c9f1f76ddb00fcbe2b']
        # result = DB.fetch_repo_hashes(git_id)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": status, "result": result})
    return (data, header)


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
def api_count_list_interval():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # result = CF.count_list_interval(git_id, username, interval_start, interval_end)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/get_commit_freq_data?git_id=168214867&interval_start=20190201&interval_end=20190214
@app.route('/github/get_commit_freq_data', methods=('GET', 'POST'))
def api_get_commit_freq_data():
    git_id = request.args.get('git_id', type=int)
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = [{'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 1, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 2, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 3, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 4, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 5, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 6, 0, 0), 'commit_count': {'test': 1, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 7, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 4}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 8, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 9, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 10, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 11, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 12, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 13, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 14, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}]
    # result = CF.get_commit_freq_data(git_id, interval_start, interval_end)

    #repack python datetime objects
    for entry in result:
        entry["date"] = dateobj_to_strdate(entry["date"])

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
