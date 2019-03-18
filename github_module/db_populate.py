#!/usr/bin/env python
################################################################################

"""
=^.^=
"""


__author__    = "Ruben Acuna"
__author__    = "Carnic"
__copyright__ = "Copyright 2019, SER574 Red Team"

import pickle
from pprint import pprint
import sqlite3
import GithubAPI
# from static_code_analysis import CheckStyleManager


def store_user_info(db, repo_id):
    data = GithubAPI.get_user_info(repo_id)
    #print(data)
    # TODO: consider case where commit already has been stored.

    #extract data
    author = data["author"]["login"]                                # TEXT
    username = data["author"]["name"]                               # TEXT
    profile = data["author"]["email"]                               # BLOB

    insert_query = "INSERT INTO user_profile(githubLogin, githubUsername, githubProfile) VALUES(%s, %s, %s)"
    insert_tuple(author, username, profile)

    display_query = "SELECT * FROM userProfile"

    db.execute(insert_query, insert_tuple)
    db.execute(display_query)

    if db.fetchall():
        print("store_user_info: unknown failure.")


def store_commit(db, repo_id, hash):
    data = GithubAPI.get_commit(repo_id, hash)
    #print(data)
    # TODO: consider case where commit already has been stored.

    #extract data
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
    #print(data)

    # TODO: consider case where pull request already has been stored.

    #extract data
    author = data["author"]["login"]                                # TEXT
    request_title = data["commit"]["message"]                       # TEXT
    no_of_comments = data["commit"]["author"]["date"]               # BLOB
    target_branch = (repr([f["filename"] for f in data["files"]])).replace("'", "\"")  # TEXT
    no_of_reviews = data["stats"]["additions"]                      # INTEGER

    # query = "INSERT INTO pull_data(requestID, requestTitle, author, noOfComments, " \
    #                                "targetBranch, noOfReviews )" \
    #                         "VALUES("str(repo_id)", '"author"', '"request_title"', " \
    #                                 "'"no_of_comments"', '"target_branch"', "no_of_reviews")"
    insert_query = "INSERT INTO pull_data(requestID, requestTitle, author, noOfComments, targetBranch, noOfReviews ) VALUES(%s, %s, %s, %s, %s)"
    insert_tuple(repo_id, author, request_title, str(no_of_comments), target_branch, str(no_of_reviews))

    display_query = "SELECT * FROM pullData"
    db.execute(insert_query, insert_tuple)
    db.execute(display_query)

    if db.fetchall():
        print("store_pull_data: unknown failure.")

# def store_complexity(repo_id, fileName):
#     data = CheckStyleManager.getStaticComplexityMetrices(fileName)
#     #print(data)
#
#     # TODO: consider case where pull request already has been stored.
#
#     #extract data
#     author = data["author"]["login"]                                # TEXT
#     BooleanExpressionComplexity = data['BooleanExpressionComplexity']
#     ClassFanOutComplexity= data['ClassFanOutComplexity']
#     JavaNCSS = data['JavaNCSS']
#     NPathComplexity = data['NPathComplexity']
#     ClassDataAbstractionCoupling = data['ClassDataAbstractionCoupling']
#
#
#     insert_query = "INSERT INTO code_complexity(author, repository, codeLink, booleanComplexity, dataAbstractionComplexity," \
#                    " fanOutComplexity, cyclomaticComplexity, javaNCSSComplexity, nPathComplexity, javaWarnings ) " \
#                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     insert_tuple(author, repo_id, codeLink, BooleanExpressionComplexity, ClassDataAbstractionCoupling, ClassFanOutComplexity,
#                  cyclomaticComplexity, JavaNCSS, NPathComplexity, javaWarnings)
#
#     display_query = "SELECT * FROM code_complexity"
#     db.execute(insert_query, insert_tuple)
#     db.execute(display_query)
#
#     if db.fetchall():
#         print("code_complexity: unknown failure.")


if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    #test parameters
    repo_id = 168214867
    sample_hash = "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"
    pull_no = 4
    newPull=str(pull_no)

    store_commit(db, repo_id, sample_hash)
    store_pull_data(repo_id, newPull)

    conn.commit()