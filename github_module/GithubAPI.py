import json
import requests
from collections import namedtuple


def user_login():
    endpoint = 'https://github.com/login/oauth/authorize'

    # login_html is the html page that GitHub generates
    login_html = requests.get(endpoint)
    return login_html


def get_access_token(client_id, client_secret, code):
    endpoint = 'https://github.com/login/oauth/access_token'
    data = '{ "client_id": "' + client_id + '", "client_secret": "' + client_secret + '", "code": "' + code + '" }'
    headers = {"Content-Type": "application/json"}
    raw_content = requests.post(endpoint, data=data, headers=headers)
    access_token = json.loads(raw_content.content)
    return access_token


def get_user_info(access_token):
    endpoint = 'https://api.github.com/user?access_token=' + access_token
    raw_content = requests.get(endpoint)
    return raw_content


def get_user_repos(access_token):
    endpoint = 'https://api.github.com/user/repos?access_token=' + access_token
    raw_content = requests.get(endpoint)
    raw_content = json.loads(raw_content.content)
    return raw_content


def get_repo(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id)
    raw_content = requests.get(endpoint)
    raw_content = json.loads(raw_content.content)
    return raw_content


def get_all_commits(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/commits'
    raw_content = requests.get(endpoint)
    raw_content = json.loads(raw_content.content)
    return raw_content


def get_commit(repo_id, commit_sha, username=None, token=None):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/commits/' + commit_sha
    return process_get_request(endpoint, username, token)


def get_all_pull_requests(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/pulls'
    return process_get_request(endpoint)


def get_pull_request(repo_id, pull_number):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/pulls/' + pull_number
    return process_get_request(endpoint)


def get_collaborators(access_token, repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/collaborators?access_token=' + access_token
    return process_get_request(endpoint)


def process_get_request(endpoint, username=None, token=None):
    if username and token:
        return json.loads(requests.get(endpoint, auth=(username, token)).content)
    else:
        return json.loads(requests.get(endpoint).content)

# print(get_repo("168214867"))
# print(get_all_commits("168214867"))
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27")
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27", "racuna1", None)
# print(get_all_pull_requests("168214867"))