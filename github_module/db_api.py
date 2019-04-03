import sqlite3

from . import db_populate
from .Constants import Constants

"""
This file implements several basic functions for querying and updating the state
of the database.
"""
__author__ = "Ruben Acuna"
__author__ = "Sarthak Tiwari"
__copyright__ = "Copyright 2019, SER574 Red Team"


def initialize_repo(github_id, access_token=None):
    """
    Stores the contents of a specific github repository in the interval
    database. Calling this function is required for all other API functions to
    work.
    :param github_id: id of a git repository (integer).
    :return: Success code (boolean).
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    #0) download and store basic repository/user information
    db_populate.store_repository_info(db, github_id, access_token)

    #1) TODO: download and store commit information.
    #2) TODO: download and store URL information.
    #3) TODO: download and store pull request information.
    #4) TODO: download and store commit comment information.

    return True


def list_details(query):
    """
    Returns a repository details dictionary for a specific repository. Assumes
    that query refers to a valid git repository which has already been
    initialized.

    A repository details dictionary contains:
        repoName : string
        collaborators : list of contributor details dictionaries
        repoURL:
        repoInternalId:

        A contributor details dictionary contains:
        name : string
        githubID : integer

    :param query: name of a git repository (string).
    :return: A repository details dictionary
    """

    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    #fetch main repo information
    info_query = "SELECT name, owner, id FROM repositories WHERE name=\"" + query + "\""
    db.execute(info_query)
    repository_info = db.fetchall()[0]

    details = dict()
    details["repoName"] = repository_info[0]
    details["repoInternalId"] = repository_info[2]

    #fetch owner information
    info_query = "SELECT githubUsername FROM userProfile WHERE id=\"" + \
        str(repository_info[1]) + "\""
    db.execute(info_query)
    owner_info = db.fetchall()[0]
    details["repoURL"] = "https://github.com/" + \
        owner_info[0] + "/" + details["repoName"]

    # fetch collaborators information
    collab_query = "SELECT DISTINCT userProfile.githubUsername, userProfile.id FROM userProfile, commitData WHERE commitData.repositoryID=" + \
        str(details["repoInternalId"]) + \
        " AND userProfile.githubUsername=commitData.author"
    db.execute(collab_query)
    collaborators = db.fetchall()
    details["collaborators"] = [None] * len(collaborators)
    for i in range(len(collaborators)):
        details["collaborators"][i] = {
            "name": collaborators[i][0], "githubId": collaborators[i][1]}

    return details


def fetch_commits(github_id):
    """
    Returns a repository details dictionary with commit frequency data for a
    specific repository. Assumes that query refers to a valid git repository which has already been
    initialized.

    For the contents of a repository details dictionary, see the list_details
    function. fetch_commits adds a key called "commits" to the standard
    repository details dictionary that is a list with the following format:
    (each list entry corresponds to one contributor).
        githubId: string
        numberofCommits: integer (sum of daily commits)
        distribution: list of daily commit data dictionary.

    A daily commit data dictionary looks like:
        date : integer (YYYYMMDD)
        numberOfCommits : integer

    :param github_id: id of a git repository (integer).
    :return:
    """

    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    #fetch main repo information (uses list_details but needs extra look up for id->str)
    info_query = "SELECT name FROM repositories WHERE id=" + str(github_id)
    db.execute(info_query)
    repo_name = db.fetchall()[0][0]
    result = list_details(repo_name)

    #fetch commit information
    commit_query = "SELECT authorID, commitMessage, date, timeCommitted, filesModified, noOfAdditions, noOfDeletions FROM commitData WHERE repositoryID=" + \
        str(result["repoInternalId"])
    db.execute(commit_query)
    commits = db.fetchall()
    result["commits"] = [None] * len(result["collaborators"])

    for i in range(len(result["collaborators"])):
        result["commits"][i] = {"githubId": result["collaborators"]
                                [i]["githubId"], "numberOfCommits": 0, "distribution": []}

    #update commit dictionary information from actual commits
    for i in range(len(commits)):
        commit_authorID = commits[i][0]
        commit_date = commits[i][2]  # YYYYMMDD

        #pick out which distribution/user to update
        active_entry = None
        for j in range(len(result["collaborators"])):
            if result["commits"][j]["githubId"] == commit_authorID:
                active_entry = result["commits"][j]
                break

        exists = False
        for k in range(len(active_entry["distribution"])):
            if active_entry["distribution"][k]["date"] == commit_date:
                exists = True
                active_entry["distribution"][k]["numberOfCommits"] += 1
                active_entry["numberOfCommits"] += 1

        if not exists:
            active_entry["distribution"].append(
                {"date": commit_date, "numberOfCommits": 1})
            active_entry["numberOfCommits"] += 1

    return result


def fetch_repo_hashes(github_id):
    """
    Returns a list of the hashes of all commits within a specific repository.

    :param github_id: id of a git repository (integer).
    :return: hashes of all commits in a repository (list of string).
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    display_query = "SELECT DISTINCT hash FROM commitData WHERE commitData.repositoryID=\"" + \
        str(github_id) + "\""

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

    display_query = "SELECT author, commitMessage, date, timeCommitted, filesModified, noOfAdditions, noOfDeletions FROM commitData WHERE commitData.hash=\"" + commit_hash + "\""

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


def fetch_pull(github_id, pull_id):
    """
    Returns a dictionary containing information (pull_id, repositoryID, author,
    noOfComments, targetBranch, and noOfReviews) for a
    specific pull request.

    Assumes that pull_id is the id of pull request existing in local database.

    :param github_id: id of a git repository (integer).
    :param pull_id: pull request number of a git pull (integer).
    :return: a pull_metadata dictionary containing information about a pull request (dictionary).
    """
    conn = sqlite3.connect(Constants.DATABASE)
    db = conn.cursor()

    display_query = "SELECT requestTitle, author, noOfComments, targetBranch, noOfReviews FROM pullData WHERE pullData.requestID=\"" + pull_id + "\""

    db.execute(display_query)
    found = db.fetchall()

    #prepare metadata dictionary
    pull_metadata = dict()
    pull_metadata["requestID"] = pull_id
    pull_metadata["repositoryID"] = github_id
    pull_metadata["author"] = found[0][0]
    pull_metadata["noOfComments"] = found[0][1]
    pull_metadata["targetBranch"] = found[0][2]
    pull_metadata["noOfReviews"] = found[0][3]

    return pull_metadata

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
    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        query = 'SELECT * FROM codeComplexity WHERE repository="' \
            + repoName + '" AND filename = "' + fileName + '";'

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
    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        query = 'SELECT * FROM codeComplexity WHERE repository="' \
            + repoName + '";'

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
    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        query = 'SELECT repository, author,'\
                + 'avg(booleanExpressionComplexity) AS booleanExpressionComplexity,'\
                + 'avg(classFanOutComplexity) AS classFanOutComplexity,'\
                + 'avg(cyclomaticComplexity) AS cyclomaticComplexity,'\
                + 'avg(javaNCSS) AS javaNCSS,'\
                + 'avg(nPathComplexity) AS nPathComplexity,'\
                + 'avg(classDataAbstractionCoupling) AS classDataAbstractionCoupling,'\
                + 'avg(javaWarnings) AS javaWarnings '\
                + 'FROM codeComplexity '\
                + 'WHERE repository="' + repoName + '" AND author = "' + authorName + '";'

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
    with sqlite3.connect(Constants.DATABASE) as conn:
        db = conn.cursor()

        query = 'SELECT repository, author,'\
                + 'avg(booleanExpressionComplexity) AS booleanExpressionComplexity,'\
                + 'avg(classFanOutComplexity) AS classFanOutComplexity,'\
                + 'avg(cyclomaticComplexity) AS cyclomaticComplexity,'\
                + 'avg(javaNCSS) AS javaNCSS,'\
                + 'avg(nPathComplexity) AS nPathComplexity,'\
                + 'avg(classDataAbstractionCoupling) AS classDataAbstractionCoupling,'\
                + 'avg(javaWarnings) AS javaWarnings '\
                + 'FROM codeComplexity '\
                + 'WHERE repository="' + repoName + '" GROUP BY author ORDER BY author;'

        db.execute(query)
        rows = db.fetchall()

        result = []

        for row in rows:
            authorComplexity = convert_author_complexity_row_to_json(row)
            result.append(authorComplexity)

        return result

def get_commits_on_stories():

    #TODO: Update the code to use live data, currently returning dummy data
    
    data = []

    storyOne = {
        "number" : 78,
        "subject" : "As a front-end developer, I want live data to be served so that we could develop and test the front-end accordingly.",
        "start_date" : 20190327,
        "end_date" : 20190405,
        "commit_count" : 8,
        "first_commit_date" : 20190329,
        "last_commit_date" : 20190401,
        "late_start_days" : 2,
        "early_start_days" : 0,
        "early_finish_days" : 4,
        "late_finish_days" : 0 }

    storyTwo = {
        "number" : 80,
        "subject" : "As a backend developer, I want to store the overall GitHub repository data in the database.",
        "start_date" : 20190327,
        "end_date" : 20190405,
        "commit_count" : 10,
        "first_commit_date" : 20190325,
        "last_commit_date" : 20190408,
        "late_start_days" : 0,
        "early_start_days" : 2,
        "early_finish_days" : 0,
        "late_finish_days" : 3 }

    data.append(storyOne)
    data.append(storyTwo)

    return data
