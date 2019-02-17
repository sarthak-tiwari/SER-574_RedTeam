import json
import requests
from collections import namedtuple

def user_login():
    endpoint = 'https://github.com/login/oauth/authorize'

    #login_html is the html page that GitHub generates
    login_html = requests.get(endpoint)
    return login_html
    

def get_access_token(client_id, client_secret, code):
    endpoint = 'https://github.com/login/oauth/access_token'
    data = '{ "client_id": "' + client_id + '", "client_secret": "' + client_secret + '", "code": "' + code + '" }'
    headers = {"Content-Type":"application/json"}
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
    endpoint = 'https://api.github.com/repositories/' + repo_id
    raw_content = requests.get(endpoint)
    raw_content = json.loads(raw_content.content)
    return raw_content

print(get_repo("168214867"))