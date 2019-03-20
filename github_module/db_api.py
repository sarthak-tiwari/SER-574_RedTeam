import db_populate
import sqlite3

"""
This file implements several basic functions for querying and updating the state
of the database.
"""
__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def initialize_repo(github_id):
    """
    Stores the contents of a specific github repository in the interval
    database. Calling this function is required for all other API functions to
    work.
    :param github_id: id of a git repository (integer).
    :return: Success code (boolean).
    """

    # TODO: implement this

    return True

def fetch_repo_hashes(github_id):
    """
    Returns a list of the hashes of all commits within a specific repository.

    :param github_id: id of a git repository (integer).
    :return: hashes of all commits in a repository (list of string).
    """
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    display_query = "SELECT DISTINCT hash FROM commitData WHERE commitData.repositoryID=\"" + str(github_id) +"\""

    db.execute(display_query)
    found = db.fetchall()

    return [x[0] for x in found]


def fetch_commit(github_id, commit_hash):
    """
    Returns a dictionary containing information (hash, repositoryID, author,
    message, date, time committed, files, additions, and deletions) for a
    specific commit.

    Assumes that commit_hash is the hash of commit existing in local database.

    :param github_id: id of a git repository (integer).
    :param commit_hash: hash of a git commit (string).
    :return: a commit_metadata dictionary containing information about a commit (dictionary).
    """
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    display_query = "SELECT author, commitMessage, date, timeCommitted, filesModified, noOfAdditions, noOfDeletions FROM commitData WHERE commitData.hash=\"" + commit_hash +"\""

    db.execute(display_query)
    found = db.fetchall()

    #prepare metadata dictionary
    commit_metadata = dict()
    commit_metadata["hash"] = commit_hash
    commit_metadata["repositoryID"] = github_id
    commit_metadata["author"] = found[0][0]
    commit_metadata["message"] = found[0][1]
    commit_metadata["date"] = found[0][2]
    commit_metadata["timeCommitted"] = found[0][3]
    commit_metadata["files"] = found[0][4]
    commit_metadata["additions"] = found[0][5]
    commit_metadata["deletions"] = found[0][6]

    return commit_metadata


# print(fetch_repo_hashes(168214867))
# print(fetch_commit(168214867, "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"))
