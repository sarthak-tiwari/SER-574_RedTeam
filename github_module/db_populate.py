#!/usr/bin/env python
################################################################################

from .Constants import Constants
from .static_code_analysis.CheckStyleManager import CheckStyleManager
from . import GithubAPI
import sqlite3
import urllib, json
import requests
from pprint import pprint
import pickle
from collections import deque
"""
=^.^=
"""


__author__ = "Ruben Acuna"
__author__ = "Carnic"
__author__ = "Sarthak Tiwari"
__author__ = "Joshua Drumm"
__copyright__ = "Copyright 2019, SER574 Red Team"


def store_repository_info(db, repo_id, username, access_token):
    repo_data = GithubAPI.get_repo(repo_id)

    clean_query = "DELETE FROM repositories WHERE id = " + str(repo_id)
    db.execute(clean_query)

    if db.fetchall():
        print("store_repository_info: unknown failure when removing old data.")

    insert_query = "INSERT INTO repositories(name, owner, id) VALUES(\""+repo_data["name"]+"\", "+str(
        repo_data["owner"]["id"])+", "+str(repo_data["id"])+")"
    db.execute(insert_query)

    if db.fetchall():
        print("store_repository_info: unknown failure when adding new data.")

    # if authentication given, also update users.
    collab_data = GithubAPI.get_contributors(repo_id)

    for collaborator in collab_data:
        githubLogin = collaborator["login"]
        githubUsername = collaborator["login"]
        githubProfile = collaborator["html_url"]
        id = collaborator["id"]

        # remove any existing collaborator data
        clean_query = "DELETE FROM userProfile WHERE id = " + str(id)
        db.execute(clean_query)

        insert_query = "INSERT INTO userProfile(githubLogin, githubUsername, githubProfile, id) VALUES(\"" + \
            githubLogin+"\", \""+githubUsername + \
            "\", \""+githubProfile+"\", "+str(id)+")"

        db.execute(insert_query)

        if db.fetchall():
            print("store_repository_info: unknown failure when adding user.")


"""
#deprecated
def store_user_info(db, repo_id):
    data = GithubAPI.get_user_info(repo_id)
    # print(data)
    # TODO: consider case where commit already has been stored.

    #extract data
    author = data["author"]["login"]                                # TEXT
    username = data["author"]["name"]                               # TEXT
    profile = data["author"]["email"]                               # BLOB

    insert_query = "INSERT INTO userProfile(githubLogin, githubUsername, githubProfile) VALUES(%s, %s, %s)"
    insert_tuple = (author, username, profile)

    display_query = "SELECT * FROM userProfile"

    db.execute(insert_query, insert_tuple)
    db.execute(display_query)

    if db.fetchall():
        print("store_user_info: unknown failure.")
"""


def store_commit(db, repo_id, hash):
    data = GithubAPI.get_commit(repo_id, hash)
    store_commit_json(db, repo_id, data)


def store_commit_json(db, repo_id, data):
    """
    Given a commit information dictionary from the GitHub API, will create a new
    entry in the commit table with it's information. Note that this function
    will create a  duplicate entry if the commit already has been stored.

    :param db: SQLlite3 database connection
    :param github_id: id of a git repository (integer).
    :param data: commit information dictionary (via GitHub API)
    :return:
    """

    #comment related
    comments_url = data["comments_url"]

    comment_data = [] #HACK: rate limiter problem
    #with urllib.request.urlopen(comments_url) as url:
    #    comment_data = json.loads(url.read().decode())

    comments = []
    for comment in comment_data:
        comments.append(comment['body'])

    #extract data
    hash = data["sha"]                                              # TEXT
    author = data["author"]["login"]                                # TEXT
    authorID = data["author"]["id"]                                 # INTEGER
    commit_message = data["commit"]["message"]                      # TEXT
    commit_message = commit_message.replace("'", "")
    commit_message = commit_message.replace("\n", "")
    date = str(data["commit"]["author"]["date"][0:4])+str(data["commit"]
                                                          ["author"]["date"][5:7])+str(data["commit"]["author"]["date"][8:10])
    time_committed = data["commit"]["author"]["date"]               # BLOB
    files_modified = (repr([f["filename"]
                            for f in data["files"]])).replace("'", "\"")  # TEXT
    num_additions = data["stats"]["additions"]                      # INTEGER
    num_deletions = data["stats"]["deletions"]                      # INTEGER"
    commitComment = comments
    commit_comment = ''.join(commitComment)

    query = "INSERT INTO commitData(hash, repositoryID, author, authorID, commitMessage, date, " \
                                   "timeCommitted, filesModified, noOfAdditions, noOfDeletions, commentMessage) " \
                            "VALUES('"+hash+"', "+str(repo_id)+", '"+author+"', "+str(authorID)+", '"+commit_message+"', "+str(date)+", '"\
                                    + time_committed+"', '"+files_modified+"', "+str(num_additions)+", "+str(num_deletions)+", '" + commit_comment + "')"

    db.execute(query)

    ret = db.fetchall()

    if ret:
        print("store_commit: unknown failure.")


def store_pull_data(db, repo_id, pull_no):
    data = GithubAPI.get_pull_request(repo_id, pull_no)
    # print(data)
    # json_name = data['repo']['branches_url']
    #
    # print('name : ' + json_name)

    # TODO: consider case where pull request already has been stored.
    #
    #extract data
    # print (data)

    comments_url = data["review_comments_url"]
    # print(comments_url)

    with urllib.request.urlopen(comments_url) as url:
        comment_data = json.loads(url.read().decode())

    comments = []
    for comment in comment_data:
        comments.append(comment['body'])
    # print(comments)
    count = 0
    for reviewers in data["requested_reviewers"]:
        count = count + 1
    # print (count)
    author = data["user"]["login"]                                # TEXT
    request_title = data["body"]
    no_of_comments = data["review_comments"]
    repository_id = repo_id
    request_id = data["id"]
    # print(request_id)
    # Might need to change DB to have both base and head branch names
    # Not sure which one target_branch should be for the time being
    base_branch = data["base"]  # Usually master
    head_branch = data["head"]  # Merges into the base
    target_branch = head_branch["label"]
    no_of_reviews = count
    pullComment = comments
    pull_comment = ''.join(pullComment)
    # pull_comment = "sample comment"
    insert_query = "INSERT INTO pullData(repositoryId, requestID, requestTile, author, noOfComments, targetBranch, noOfReviews, commentMessage ) " \
                   "VALUES('"+str(repository_id)+"','"+str(request_id)+"', '"+request_title+"', '"+author+"', '"+str(
                       no_of_comments)+"', '"+str(target_branch)+"', '"+str(no_of_reviews)+"', '" + pull_comment + "')"

    db.execute(str(insert_query))
    conn.commit()


def store_complexity(repoName):

    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        getFileLinkQuery = 'SELECT codeLink FROM codeComplexity WHERE repository="' + repoName + '";'
        db.execute(getFileLinkQuery)
        fileLinks = db.fetchall()

        for row in fileLinks:
            metrics = CheckStyleManager.getComplexity(row[0])

            updateQuery = 'UPDATE codeComplexity SET ' \
                + 'booleanExpressionComplexity = ?' \
                + ',classFanOutComplexity = ?' \
                + ',cyclomaticComplexity = ?' \
                + ',javaNCSS = ?' \
                + ',nPathComplexity = ?' \
                + ',classDataAbstractionCoupling = ?' \
                + ',javaWarnings = ?' \
                + ' WHERE codeLink = ?;'

            updateTuple = (metrics['BooleanExpressionComplexity'],
                           metrics['ClassFanOutComplexity'],
                           metrics['CyclomaticComplexity'],
                           metrics['JavaNCSS'],
                           metrics['NPathComplexity'],
                           metrics['ClassDataAbstractionCoupling'],
                           metrics['JavaWarnings'],
                           row[0])

            db.execute(updateQuery, updateTuple)

def store_files(db, repo_id):
    files = GithubAPI.get_all_files(repo_id)
    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        for gitFile in files:
            insert_query = 'INSERT INTO codeComplexity(repository, fileName, author, codeLink) VALUES(?, ?, ?, ?);'

            insert_tuple = (str(repo_id),
                           gitFile["path"],
                           "Not yet Supported",
                           gitFile["download_url"])

            db.execute(insert_query, insert_tuple)
    


def store_repo_commits(db, repo_id, branch, username, token):

    #remove any existing commits
    clean_query = "DELETE FROM commitData WHERE repositoryID = " + str(repo_id)
    db.execute(clean_query)

    if db.fetchall():
        print("store_repo_commits: unknown failure when removing old data.")

    commits_on_master = GithubAPI.get_commits_branch(repo_id, branch, username, token)

    for commit in commits_on_master:
        hash = commit["sha"]

        #check if commit already exists.
        #display_query = "SELECT hash, repositoryID FROM commitData WHERE commitData.hash=\""+hash+"\""
        #display_query = "SELECT hash, repositoryID FROM commitData"
        #db.execute(display_query)
        #ret = db.fetchall()

        # update DB
        #print(display_query)
        complete_data = GithubAPI.get_commit(repo_id, hash, username, token)
        store_commit_json(db, repo_id, complete_data)



    """
    #BFS algorithm for traversing graph from root commit
    root_sha = root["sha"]

    seen = [root_sha]
    q = deque()
    q.append(root_sha)

    while len(q):
        hash = q.popleft()
        commit = GithubAPI.get_commit(repo_id, hash)
        store_commit_json(db, repo_id, commit)
        if "parents" in commit:
            for parent in commit["parents"]:
                parent_sha = parent["sha"]
                if not parent_sha in seen:
                    seen.append(parent_sha)
                    q.append(parent_sha)
    """

def store_repo_pulls(db, repo_id, branch="master"):

    #remove any existing pulls
    clean_query = "DELETE FROM pullData WHERE repositoryID = " + str(repo_id)
    db.execute(clean_query)

    if db.fetchall():
        print("store_repo_pulls: unknown failure when removing old data.")

    pulls_on_master = GithubAPI.get_pulls_branch(repo_id, branch)

    for pull in pulls_on_master:
        id = pull["id"]

        store_pull_data(db, repo_id, id)

if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    db = conn.cursor()

    #store_repo(db, 168214867)

    #test parameters
    repo_id = 168214867
    sample_hash = "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
    pull_no = 4
    newPull = str(pull_no)

    # connect_dbs()
    store_repo_commits(db, 168214867, "master", "racuna1", "REPLACEME")
    # store_commit(db, repo_id, sample_hash)
    # store_pull_data(repo_id, newPull)
    # store_user_info(db, repo_id)
    # display_query = "SELECT * FROM pullData"
    # store_repository_info(db, repo_id, None)
    # store_repository_info(db, repo_id, None)
    #store_commit(db, repo_id, sample_hash)
    # store_pull_data(repo_id, newPull)
    #store_user_info(db, 43050725) #sarthak-tiwari's ID
    #display_query = "SELECT * FROM pullData"
    # store_complexity(db, 'sarthak-tiwari/SER-574_RedTeam')

    # print(db.fetchall())

    conn.commit()
    conn.close()
