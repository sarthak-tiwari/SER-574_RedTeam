#!/usr/bin/env python
################################################################################

"""
=^.^=
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"

import pickle
from pprint import pprint
import sqlite3
import GithubAPI


"""
        self.db.execute("CREATE TABLE commitData (\n"
                        "    hash TEXT,\n"
                        "    repositoryID TEXT,\n"
                        "    author TEXT,\n"
                        "    commitMessage TEXT,\n"
                        "    timeCommitted BLOB,\n"
                        "    fileModified TEXT,\n"
                        "    noOfAdditions INTEGER,\n"
                        "    noOfDeletions INTEGER\n"
                        "    )")
"""

def store_commit(db, repo_id, hash):
    data = GithubAPI.get_commit(repo_id, hash)

    # TODO: consider case where commit already has been stored.

    #extract data
    author = data["author"]["login"]                                # TEXT
    commit_message = data["commit"]["message"]                      # TEXT
    time_committed = data["commit"]["author"]["date"]               # BLOB
    files_modified = (repr([f["filename"] for f in data["files"]])).replace("'", "\"")  # TEXT
    num_additions = data["stats"]["additions"]                      # INTEGER
    num_deletions = data["stats"]["deletions"]                      # INTEGER"

    query = "INSERT INTO commitData(hash, repositoryID, author, commitMessage, " \
                                   "timeCommitted, filesModified, noOfAdditions, noOfDeletions) " \
                            "VALUES('"+hash+"', "+str(repo_id)+", '"+author+"', '"+commit_message+"', " \
                                    "'"+time_committed+"', '"+files_modified+"', "+str(num_additions)+", "+str(num_deletions)+")"

    db.execute(query)

    if db.fetchall():
        print("store_commit: unknown failure.")

if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    #test parameters
    repo_id = 168214867
    sample_hash = "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"

    store_commit(db, repo_id, sample_hash)

    conn.commit()