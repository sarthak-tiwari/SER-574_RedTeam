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


def get_user_repos(git_username):
    endpoint = 'https://api.github.com/users/' + git_username + 'repos'
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

def get_commit_comments(repo_id, commit_sha):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/commits/' + commit_sha + '/comments'
    return process_get_request(endpoint)

def get_all_commits_with_comments(repo_id):
    commits = get_all_commits(repo_id)
    for commit in commits:
        commit_sha = commit["sha"]
        comments = get_commit_comments(repo_id, commit_sha)
        commit["comments"] = comments
        full_commit = get_commit(repo_id, commit_sha)
        commit["files"] = full_commit["files"]
        commit["stats"] = full_commit["stats"]
    return commits

def get_commit_files(repo_id, commit_sha):
    return get_commit(repo_id, commit_sha)["files"]


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

def get_all_files(repo_id):
    return get_all_files_recursive(repo_id, '')

def get_all_files_recursive(repo_id, path):
    endpoint = 'https://api.github.com/repositories/' + str(repo_id) + '/contents' + str(path)
    raw_data = process_get_request(endpoint)
    data = []
    data_for_other_folders = []
    for files in raw_data:
        if files["type"] == "file":
            data.append(files["path"])
        elif files["type"] == "dir":
            data_for_other_folders.extend(get_all_files_recursive(repo_id, path + "/" + files["name"]))
    
    data.extend(data_for_other_folders)
    return data

def process_get_request(endpoint, username=None, token=None):
    if username and token:
        return json.loads(requests.get(endpoint, auth=(username, token)).content)
    else:
        return json.loads(requests.get(endpoint + "?client_id=5d45a5aa02a482c56abd&client_secret=ac05cfd61eeecd795374868b9a9965ca9999c999").content)

# print(get_repo("168214867"))
# print(get_all_commits("168214867"))
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27")
# print(get_commit("168214867", "70f13b111e1147611b70f9c9f1f76ddb00fcbe27", "racuna1", None)
# print(get_pull_request("168214867", '4'))
# print(get_all_pull_requests("168214867"))
# print(get_file(168214867, 'github_module/README'))
# print(get_all_files(168214867))
# print(user_login())
# print(get_all_commits_with_comments(168214867))