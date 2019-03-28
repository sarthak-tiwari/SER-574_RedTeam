import json
import requests
import base64
from collections import namedtuple


def user_login():
    client_id = "5d45a5aa02a482c56abd"
    endpoint = 'https://github.com/login/oauth/authorize?client_id=' + client_id
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
    return process_get_request(endpoint)


def get_user_repos(access_token):
    endpoint = 'https://api.github.com/user/repos?access_token=' + access_token
    return process_get_request(endpoint)


def get_repo(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id)
    return process_get_request(endpoint)


def get_all_commits(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/commits'
    return process_get_request(endpoint)


def get_commit(repo_id, commit_sha, username=None, token=None):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/commits/' + commit_sha
    return process_get_request(endpoint, username, token)


def get_commits_branch(repo_id, branch, username, token, per_page=100):
    commits = []
    page = 0

    while page < 10: #HACK: hard coded limit to prevent infinite loop
        endpoint = "https://api.github.com/repositories/" + str(repo_id) + "/commits?per_page="+str(per_page)+"&page="+str(page)+"&sha=" + branch
        page_result = process_get_request(endpoint, username, token)

        if page_result and "documentation_url" not in page_result:
            commits.extend(page_result)
        else:
            break

        page += 1

    return commits


def get_all_pull_requests(repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/pulls'
    return process_get_request(endpoint)


def get_pull_request(repo_id, pull_number):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/pulls/' + pull_number
    return process_get_request(endpoint)

def get_pull_request_comments(repo_id, pull_number):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/pulls/' + pull_number + '/comments'
    return process_get_request(endpoint)

def get_collaborators(access_token, repo_id):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/collaborators?access_token=' + access_token
    return process_get_request(endpoint)

def get_file(repo_id, file_path):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/contents/' + file_path + '?ref=master'
    raw_data = process_get_request(endpoint)
    raw_data["content"] = base64.b64decode(raw_data["content"]).decode('utf-8')
    return raw_data

def process_get_request(endpoint, username=None, token=None):
    if username and token:
        return json.loads(requests.get(endpoint, auth=(username, token)).content)
    else:
        return json.loads(requests.get(endpoint).content)

# print(get_repo("168214867"))
# print(get_all_commits("168214867"))
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27")
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27", "racuna1", None)
# print(get_pull_request("168214867", '4'))
# print(get_all_pull_requests("168214867"))
# print(get_file(168214867, 'github_module/README'))
# print(user_login())
