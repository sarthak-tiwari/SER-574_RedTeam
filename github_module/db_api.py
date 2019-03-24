import db_populate
import sqlite3

from Constants import Constants

"""
This file implements several basic functions for querying and updating the state
of the database.
"""
__author__    = "Ruben Acuna"
__author__    = "Sarthak Tiwari"
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
    conn = sqlite3.connect(Constants.DATABASE)
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
    conn = sqlite3.connect(Constants.DATABASE)
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


# -----------------------------------------------------------------------------

# Functions to access code complexity related data


def convert_complexity_row_to_json(row):

    result = {}
    result['repositoryName'] = row[0]
    result['fileName'] = row[1]
    result['author'] = row[2]

    metrices = {}
    metrices['booleanExpressionComplexity'] = row[4]
    metrices['classFanOutComplexity'] = row[5]
    metrices['cyclomaticComplexity'] = row[6]
    metrices['javaNCSS'] = row[7]
    metrices['nPathComplexity'] = row[8]
    metrices['classDataAbstractionCoupling'] = row[9]
    metrices['javaWarnings'] = row[10]

    result['metric'] = metrices

    return result

def convert_author_complexity_row_to_json(row):

    authorComplexity = {}
    authorComplexity['repositoryName'] = row[0]
    authorComplexity['author'] = row[1]

    metrices = {}
    metrices['booleanExpressionComplexity'] = row[2]
    metrices['classFanOutComplexity'] = row[3]
    metrices['cyclomaticComplexity'] = row[4]
    metrices['javaNCSS'] = row[5]
    metrices['nPathComplexity'] = row[6]
    metrices['classDataAbstractionCoupling'] = row[7]
    metrices['javaWarnings'] = row[8]

    authorComplexity['metric'] = metrices

    return authorComplexity


def get_complexity_of_file(repoName, fileName):
    """
    Returns code complexity of fileName present in repoName.
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    query = 'SELECT * FROM codeComplexity WHERE repository="' \
                    + repoName +'" AND filename = "' + fileName + '";'

    db.execute(query)
    rows = db.fetchall()
    
    result = []

    for row in rows:
        fileComplexity = convert_complexity_row_to_json(row)
        result.append(fileComplexity)

    return result


def get_complexity_of_files_in_repo(repoName):
    """
    Return complexity of all files in this repository.
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    query = 'SELECT * FROM codeComplexity WHERE repository="' \
                    + repoName +'";'

    db.execute(query)
    rows = db.fetchall()
    
    result = []

    for row in rows:
        fileComplexity = convert_complexity_row_to_json(row)
        result.append(fileComplexity)

    return result


def get_complexity_by_author(repoName, authorName):
    """
    Return average complexity of all files authored by specified author in
    this repository
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    query = 'SELECT repository, author,'\
            +'avg(booleanExpressionComplexity) AS booleanExpressionComplexity,'\
            +'avg(classFanOutComplexity) AS classFanOutComplexity,'\
            +'avg(cyclomaticComplexity) AS cyclomaticComplexity,'\
            +'avg(javaNCSS) AS javaNCSS,'\
            +'avg(nPathComplexity) AS nPathComplexity,'\
            +'avg(classDataAbstractionCoupling) AS classDataAbstractionCoupling,'\
            +'avg(javaWarnings) AS javaWarnings '\
            +'FROM codeComplexity '\
            +'WHERE repository="' + repoName + '" AND author = "' + authorName + '";'

    db.execute(query)
    rows = db.fetchall()
    
    result = []

    for row in rows:
        authorComplexity = convert_author_complexity_row_to_json(row)
        result.append(authorComplexity)

    return result


def get_complexity_of_authors_in_repo(repoName):
    """
    Return complexity generated by all authors in this repository
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    query = 'SELECT repository, author,'\
            +'avg(booleanExpressionComplexity) AS booleanExpressionComplexity,'\
            +'avg(classFanOutComplexity) AS classFanOutComplexity,'\
            +'avg(cyclomaticComplexity) AS cyclomaticComplexity,'\
            +'avg(javaNCSS) AS javaNCSS,'\
            +'avg(nPathComplexity) AS nPathComplexity,'\
            +'avg(classDataAbstractionCoupling) AS classDataAbstractionCoupling,'\
            +'avg(javaWarnings) AS javaWarnings '\
            +'FROM codeComplexity '\
            +'WHERE repository="' + repoName + '" GROUP BY author ORDER BY author;'

    db.execute(query)
    rows = db.fetchall()
    
    result = []

    for row in rows:
        authorComplexity = convert_author_complexity_row_to_json(row)
        result.append(authorComplexity)

    return result

# print(fetch_repo_hashes(168214867))
# print(fetch_commit(168214867, "70f13b111e1147611b70f9c9f1f76ddb00fcbe27"))
