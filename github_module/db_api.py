import db_populate
import sqlite3

"""
This file implements several basic functions for querying and updating the state
of the database.
"""
__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def fetch_commit(github_id, commit_hash):

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


# print(fetch_commit(168214867, "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"))