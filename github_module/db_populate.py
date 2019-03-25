#!/usr/bin/env python
################################################################################

"""
=^.^=
"""


__author__    = "Ruben Acuna"
__author__    = "Carnic"
__copyright__ = "Copyright 2019, SER574 Red Team"

from collections import deque
import pickle
from pprint import pprint
import sqlite3
import GithubAPI

from .static_code_analysis.CheckStyleManager import CheckStyleManager
from .Constants import Constants


def store_repository_info(db, repo_id, access_token):
    repo_data = GithubAPI.get_repo(repo_id)

    clean_query = "DELETE FROM repositories WHERE id = " + str(repo_id)
    db.execute(clean_query)

    if db.fetchall():
        print("store_repository_info: unknown failure when removing old data.")

    insert_query = "INSERT INTO repositories(name, owner, id) VALUES(\""+repo_data["name"]+"\", "+str(repo_data["owner"]["id"])+", "+str(repo_data["id"])+")"
    db.execute(insert_query)

    if db.fetchall():
        print("store_repository_info: unknown failure when adding new data.")

    # if authentication given, also update users.
    if access_token:
        collab_data = GithubAPI.get_collaborators(access_token, repo_id)

        for collaborator in collab_data:
            githubLogin = collaborator["login"]
            githubUsername = collaborator["login"]
            githubProfile = collaborator["html_url"]
            id = collaborator["id"]

            # remove any existing collaborator data
            clean_query = "DELETE FROM userProfile WHERE id = " + str(id)
            db.execute(clean_query)

            insert_query = "INSERT INTO userProfile(githubLogin, githubUsername, githubProfile, id) VALUES(\""+githubLogin+"\", \""+githubUsername+"\", \""+githubProfile+"\", "+str(id)+")"

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
    # print(data)

    store_commit_json(db, repo_id, data)

def store_commit_json(db, repo_id, data):
    # TODO: consider case where commit already has been stored.

    #extract data
    hash = data["sha"]                                              # TEXT
    author = data["author"]["login"]                                # TEXT
    commit_message = data["commit"]["message"]                      # TEXT
    date = str(data["commit"]["author"]["date"][0:4])+str(data["commit"]["author"]["date"][5:7])+str(data["commit"]["author"]["date"][8:10])
    time_committed = data["commit"]["author"]["date"]               # BLOB
    files_modified = (repr([f["filename"] for f in data["files"]])).replace("'", "\"")  # TEXT
    num_additions = data["stats"]["additions"]                      # INTEGER
    num_deletions = data["stats"]["deletions"]                      # INTEGER"

    query = "INSERT INTO commitData(hash, repositoryID, author, commitMessage, " \
                                   "timeCommitted, filesModified, noOfAdditions, noOfDeletions) " \
                            "VALUES('"+hash+"', "+str(repo_id)+", '"+author+"', '"+commit_message+"', " \
                                    "'"+time_committed+"', '"+files_modified+"', "+str(num_additions)+", "+str(num_deletions)+")"
    display_query = "SELECT * FROM commitData"
    db.execute(query)
    db.execute(display_query)

    if db.fetchall():
        print("store_commit: unknown failure.")


def store_pull_data(repo_id, pull_no):
    data = GithubAPI.get_pull_request(repo_id, pull_no)
    # print(data)
    # json_name = data['repo']['branches_url']
    #
    # print('name : ' + json_name)

    # TODO: consider case where pull request already has been stored.
    #
    #extract data

    author = data["user"]["login"]                                # TEXT
    request_title = data["body"]
    no_of_comments = data["review_comments"]

    # Might need to change DB to have both base and head branch names
    # Not sure which one target_branch should be for the time being
    base_branch = data["base"] # Usually master
    head_branch = data["head"] # Merges into the base
    target_branch = head_branch["label"]
    no_of_reviews = 4

    insert_query = "INSERT INTO pullData(requestID, requestTile, author, noOfComments, targetBranch, noOfReviews )" \
                   "VALUES(?, ?, ?, ?, ?, ?)", (repo_id, request_title, author, str(no_of_comments), target_branch, str(no_of_reviews))
                   # "VALUES("+repo_id+", "+request_title+", "+author+", "+str(no_of_comments)+", "+target_branch+", "+str(no_of_reviews)+")"
    # insert_tuple = (repo_id, request_title, author, str(no_of_comments), target_branch, str(no_of_reviews))

    # db.execute(insert_query, insert_tuple)
    db.execute(insert_query)

    if db.fetchall():
        print("store_pull_data: unknown failure.")

def store_complexity(db, repoName):

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

def store_repo(db, repo_id, branch="master"):

    root = GithubAPI.get_commit(repo_id, branch)
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
    #debug
    print(len(seen))
    print(seen)

if __name__ == "__main__":
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    #store_repo(db, 168214867)

    #test parameters
    repo_id = 168214867
    sample_hash = "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
    pull_no = 4
    newPull=str(pull_no)

    # connect_dbs()
    # store_commit(db, repo_id, sample_hash)
    store_pull_data(repo_id, newPull)
    # store_user_info(db, repo_id)
    display_query = "SELECT * FROM pullData"
    store_repository_info(db, repo_id, None)
    # store_repository_info(db, repo_id, None)
    #store_commit(db, repo_id, sample_hash)
    #store_pull_data(repo_id, newPull)
    #store_user_info(db, 43050725) #sarthak-tiwari's ID
    #display_query = "SELECT * FROM pullData"
    store_complexity(db, 'sarthak-tiwari/SER-574_RedTeam')

    # print(db.fetchall())

    conn.commit()
    conn.close()
