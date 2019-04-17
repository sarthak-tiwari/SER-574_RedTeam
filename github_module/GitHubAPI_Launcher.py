# Class to launch github api service on flask
#
# Author: Sarthak Tiwari, Ruben Acuna, Carnic
# E-Mail: sarthak.tiwari@asu.edu, racuna1@asu.edu, clnu2@asu.edu

from flask import Blueprint, Flask, request
import datetime
import json
import sqlite3

from . import GithubAPI
from .static_code_analysis.CheckStyleManager import CheckStyleManager
#import metadata_analysis.commit_frequency as CF
from . import db_api as DB
from .Constants import Constants
from . import db_populate as DP

github_api = Blueprint('github_api', __name__,)


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


# ex: 127.0.0.1:5000/github/core_initialize_repo?repoName=sarthak-tiwari/SER-574_RedTeam&username=racuna1&access_token=REPLACEME
@github_api.route('/core_initialize_repo', methods=('GET', 'POST'))
def api_core_initialize_repo():
    git_repo_name = request.args.get('repoName')
    usr = request.args.get('username')
    acctok = request.args.get('access_token')

    if not git_repo_name:
        return ("", "501: need git repo slug.")
    else:
        status = "wip"
        result = DB.initialize_repo_data(git_repo_name, usr, acctok)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": status, "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/listdetails/?format=json&repoName=sarthak-tiwari/SER-574_RedTeam
@github_api.route('/listdetails/', methods=('GET', 'POST'))
def api_core_listdetails():

    fo = request.args.get('format')
    repoName = request.args.get('repoName')

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        result = DB.list_details(repoName)

        header = {'Content-Type': 'application/json'}
        data = json.dumps(result)
        return (data, header)


# ex: 127.0.0.1:5000/github/commits/?format=json&repoName=sarthak-tiwari/SER-574_RedTeam
@github_api.route('/commits/', methods=('GET', 'POST'))
def api_core_commits():

    fo = request.args.get('format')
    repoName = request.args.get('repoName')

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        result = DB.fetch_commits(repoName)

        header = {'Content-Type': 'application/json'}
        data = json.dumps(result)
        return (data, header)


# ex: 127.0.0.1:5000/github/fetch_repo_hashes/?format=json&repoName="sarthak-tiwari/SER-574_RedTeam"
@github_api.route('/fetch_repo_hashes/', methods=('GET', 'POST'))
def api_core_fetch_repo_hashes():
    fo = request.args.get('format')
    repoName = request.args.get('repoName')

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        #result = {"hashes" : ['70f13b111e1147611b70f9c9f1f76ddb00fcbe27', '70f13b111e1147611b70f9c9f1f76ddb00fcbe28',
        #          '70f13b111e1147611b70f9c9f1f76ddb00fcbe29', '70f13b111e1147611b70f9c9f1f76ddb00fcbe2a', '70f13b111e1147611b70f9c9f1f76ddb00fcbe2b']}
        result = DB.fetch_repo_hashes(repoName)

    header = {'Content-Type': 'application/json'}
    data = json.dumps(result)
    return (data, header)


# ex: 127.0.0.1:5000/github/fetch_commit/?format=json&repoName="sarthak-tiwari/SER-574_RedTeam"&commit_hash="  "
@github_api.route('/fetch_commit/', methods=('GET', 'POST'))
def api_core_fetch_commit():
    fo = request.args.get('format')
    repoName = request.args.get('repoName')
    commit_hash = request.args.get('commit_hash')

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        #result = {'hash': '70f13b111e1147611b70f9c9f1f76ddb00fcbe27', 'repositoryID': 168214867, 'author': 'test', 'message': 'Added gitignore for python to the source directory',
        #          'date': 20190206, 'timeCommitted': '2019-02-07T23:39:00Z', 'files': '[".gitignore"]', 'additions': 116, 'deletions': 0}
        result = DB.fetch_commit(repoName, commit_hash)

    header = {'Content-Type': 'application/json'}
    data = json.dumps(result)
    return (data, header)

################################################################################
# Comment Analysis::Frequency


# ex: 127.0.0.1:5000/github/get_commit_count_interval?git_id=168214867&username="test"&interval_start=20190201&interval_end=20190228
@github_api.route('/get_commit_count_interval', methods=('GET', 'POST'))
def api_get_commit_count_interval():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = 1
    # result = CF.get_commit_count_interval(git_id, username, interval_start, interval_end)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/get_commit_count_day?git_id=168214867&username="test"&date=20190208
@github_api.route('/get_commit_count_day', methods=('GET', 'POST'))
def api_get_commit_count_day():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    date = parse_str_date(request.args.get('date'))

    result = 0
    # result = CF.commit_count_day(git_id, username, date)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/count_list_interval?git_id=168214867&username="test"&interval_start=20190201&interval_end=20190228
@github_api.route('/get_commit_counts_interval', methods=('GET', 'POST'))
def api_get_commit_counts_interval():
    git_id = request.args.get('git_id', type=int)
    username = request.args.get('username')
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # result = CF.get_commit_counts_interval(git_id, username, interval_start, interval_end)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


# ex: 127.0.0.1:5000/github/get_commit_freq_data?git_id=168214867&interval_start=20190201&interval_end=20190214
@github_api.route('/get_commit_freq_data', methods=('GET', 'POST'))
def api_get_commit_freq_data():
    git_id = request.args.get('git_id', type=int)
    interval_start = parse_str_date(request.args.get('interval_start'))
    interval_end = parse_str_date(request.args.get('interval_end'))

    result = [{'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 1, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 2, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 3, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 4, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 5, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 6, 0, 0), 'commit_count': {'test': 1, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 7, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 4}}, {
        'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 8, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 9, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 10, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 11, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 12, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 13, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}, {'usernames': ['test', 'sarthak-tiwari'], 'date': datetime.datetime(2019, 2, 14, 0, 0), 'commit_count': {'test': 0, 'sarthak-tiwari': 0}}]
    # result = CF.get_commit_freq_data(git_id, interval_start, interval_end)

    #repack python datetime objects
    for entry in result:
        entry["date"] = dateobj_to_strdate(entry["date"])

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)


################################################################################
# Comment Analysis::Commit Messages

# ex: 127.0.0.1:5000/github/messagequality/?format=json&repoName=racuna1/ser222-public
@github_api.route('/messagequality/', methods=('GET', 'POST'))
def api_messagequality_ui():

    fo = request.args.get('format')
    repoName = request.args.get('repoName')

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        result = DB.message_quality(repoName)

        header = {'Content-Type': 'application/json'}
        data = json.dumps(result)
        return (data, header)

# ex: 127.0.0.1:5000/github/compute_commit_message_quality?git_id=168214867&commit_hash="70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
@github_api.route('/compute_commit_message_quality', methods=('GET', 'POST'))
def api_compute_commit_message_quality():
    git_id = request.args.get('git_id', type=int)
    commit_hash = request.args.get('commit_hash')

    result = 50
    # result = CF.compute_commit_message_quality(git_id, commit_hash)

    header = {'Content-Type': 'application/json'}
    data = json.dumps({"status": "unimplemented", "result": result})
    return (data, header)

################################################################################
# Comment Analysis::Comments

#################################################################################
# pull request info
# ex : http://127.0.0.1:5000/github/pull_request/?repo_id=168214867
@github_api.route('/pull_request/',  methods=('GET', 'POST'))
def api_count_pull():
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()
    repo_id = request.args.get('repo_id', type=int)
    db.execute("SELECT * FROM pullData WHERE repositoryID = ?", (repo_id,))
    # db.execute("SELECT * FROM pullData ")
    result = db.fetchall()
    # print(str(result))
    # return result
    # print(str(result[0][0]))
    pulls_data = []
    for data in result:
        pull_data = {}
        pull_data['repository_id'] = data[0]
        pull_data['request_id'] = data[1]
        pull_data['request_title'] = data[2]
        pull_data['author'] = data[3]
        pull_data['no_of_comments'] = data[4]
        pull_data['target_branch'] = data[5]
        pull_data['no_of_reviews'] = data[6]
        pull_data['comments'] = data[7]
        pulls_data.append(pull_data)

    return str(pulls_data), {'Content-Type': 'application/json'}


#################################################################################
# user info

@github_api.route('/user', methods=('GET', 'POST'))
def api_count_user():
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()
    db.execute("SELECT * FROM userProfile")
    result = db.fetchall()
    print(result)
    users_data = []
    for data in result:
        user_data = {}
        # user_data['github_login'] = data[1]
        user_data['github_username'] = data[1]
        user_data['github_profile'] = data[2]
        users_data.append(user_data)

    return str(users_data), {'Content-Type': 'application/json'}
    # return jsonify({'result': users_data})


################################################################################
# Code Analysis

# ex: 127.0.0.1:5000/github/baseline_for_complexity"
# Returns baseline values for code complexity metrices.
@github_api.route('/baseline_for_complexity', methods=('GET', 'POST'))
def api_get_baseline_for_complexity():

    baselineData = CheckStyleManager.getBaselineForComplexities()
    data = json.dumps(baselineData)

    return (data, {'Content-Type': 'application/json'})

# ex: 127.0.0.1:5000/github/complexity_of_file?repoName="someRepo"&fileName="package/another/abc.java"
# Returns code complexity of fileName present in repoName.
@github_api.route('/complexity_of_file', methods=('GET', 'POST'))
def api_get_complexity_of_file():
    repoName = request.args.get('reponame')
    fileName = request.args.get('filename')

    complexityData = DB.get_complexity_of_file(repoName, fileName)
    baselineData = CheckStyleManager.getBaselineForComplexities()
    data = json.dumps({'complexities' : complexityData, 'baselines' : baselineData})

    return (data, {'Content-Type': 'application/json'})

# ex: 127.0.0.1:5000/github/complexity_of_files_in_repo?repoName="someRepo"
# Return complexity of all files in this repository.
@github_api.route('/complexity_of_files_in_repo', methods=('GET', 'POST'))
def api_get_complexity_of_files_in_repo():
    repoName = request.args.get('reponame')

    complexityData = DB.get_complexity_of_files_in_repo(repoName)
    baselineData = CheckStyleManager.getBaselineForComplexities()
    data = json.dumps({'complexities' : complexityData, 'baselines' : baselineData})

    return (data, {'Content-Type': 'application/json'})

# ex: 127.0.0.1:5000/github/complexity_by_author?repoName="someRepo"&authorname="some author"
# Return average complexity of all files authored by specified author in this repository
@github_api.route('/complexity_by_author', methods=('GET', 'POST'))
def api_get_complexity_by_author():
    repoName = request.args.get('reponame')
    authorName = request.args.get('authorname')

    complexityData = DB.get_complexity_by_author(repoName, authorName)
    baselineData = CheckStyleManager.getBaselineForComplexities()
    data = json.dumps({'complexities' : complexityData, 'baselines' : baselineData})

    return (data, {'Content-Type': 'application/json'})

# ex: 127.0.0.1:5000/github/complexity_of_authors_in_repo?repoName="someRepo"
# Return complexity generated by all authors in this repository
@github_api.route('/complexity_of_authors_in_repo', methods=('GET', 'POST'))
def api_get_complexity_of_authors_in_repo():
    repoName = request.args.get('reponame')

    complexityData = DB.get_complexity_of_authors_in_repo(repoName)
    baselineData = CheckStyleManager.getBaselineForComplexities()
    data = json.dumps({'complexities' : complexityData, 'baselines' : baselineData})

    return (data, {'Content-Type': 'application/json'})

################################################################################

# ex: 127.0.0.1:5000/github/pulls/?format=json&query=168214867
@github_api.route('/pulls/', methods=('GET', 'POST'))
def api_core_pulls():

    fo = request.args.get('format')
    query = request.args.get('query', type=int)

    if fo != "json":
        return ("", "501: only json is supported for format.")
    else:
        result = DB.fetch_pull(query)

        header = {'Content-Type': 'application/json'}
        data = json.dumps(result)
        return (data, header)

################################################################################
# GitHub - Taiga Overlap

# ex: 127.0.0.1:5000/github/commits_on_stories?projectSlug="someSlug"&repoName="someRepo"
# Returns commit information in someRepo for each user story in the project with someSlug
@github_api.route('/commits_on_stories', methods=('GET', 'POST'))
def api_get_commits_on_stories():
    projectSlug = request.args.get('projectSlug')
    repoName = request.args.get('repoName')

    commitOnStoryData = DB.get_commits_on_stories(projectSlug)
    
    data = json.dumps(commitOnStoryData)

    return (data, {'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.debug = True
    app.run()
