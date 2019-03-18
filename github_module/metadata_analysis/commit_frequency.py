#!/usr/bin/env python

"""
Implementation of an internal API for analyzing frequency of commits for a user
in a git project.
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"

import datetime
import sqlite3

def count_in_internal(git_id, username, interval_start, interval_end):
    """
    Returns the number of commits made by a user in a git repository during a
    time internal. The interval is inclusive.

    Assumes valid git repo and username.

    :param git_id: id of a git repository (string).
    :param username: username (string)
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: number of commits (integer).
    """

    return sum(count_list_interval(git_id, username, interval_start,
                                   interval_end))


def count_on_day(git_id, username, date):
    """
    Returns the number of commits made by a user in a git repository on a
    specific day.

    Assumes valid git repo and username.

    :param git_id: id of a git repository (string).
    :param username: username (string)
    :param date: day (date object).
    :return: number of commits (integer).
    """

    return count_list_interval(git_id, username, date, date)[0]


def count_list_interval(git_id, username, interval_start, interval_end):
    """
    Returns a list of commits made each day by a user in a git repository
    during a time interval. The interval is inclusive.

    Assumes valid git repo and username.

    :param git_id: id of a git repository (string).
    :param username: username (string)
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: a list of commits per day (list of integers).
    """

    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    freq_data = __get_commit_freq_data(db, git_id, interval_start, interval_end)
    result = [x["commit_count"][username] if username in x["usernames"] else 0
              for x in freq_data]

    return result

# The following are internal functions.

def __get_commit_freq_data(db, git_id, interval_start, interval_end):
    """

    A daily commit status dictionary contains the following keys:
      "usernames" : (a list of strings)
      "date" : (date object)
      "commit_count" : (a dictionary)
        <contributor as string> : (integer)
        (the above is repeated for each contributor on the particular day.)

    :param git_id: id of a git repository (string).
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: commit statuses (list of commit status dictionaries).
    """
    interval = (interval_end-interval_start).days+1
    contributors = __get_all_contributors(db, git_id)
    result = [None] * interval

    for day in range(interval):
        #prepare dictionary outline
        result[day] = dict()
        result[day]["usernames"] = contributors
        result[day]["date"] = interval_start + datetime.timedelta(days=day)
        result[day]["commit_count"] = dict()
        for contributor in contributors:
            result[day]["commit_count"][contributor] = 0

        #interface with database to retrieve contributors.
        query_date = str(result[day]["date"].year).zfill(4) + str(result[day]["date"].month).zfill(2) + str(result[day]["date"].day).zfill(2)
        display_query = "SELECT author FROM commitData WHERE commitData.repositoryID="+str(git_id)+" AND date="+query_date
        db.execute(display_query)
        found = db.fetchall()

        if found:
            for commit in found:
                contributor = commit[0]
                result[day]["commit_count"][contributor] += 1

    #debugging
    assert len(result) == interval, "See __get_commit_freq_data()."

    return result


def __get_all_contributors(db, git_id):
    """
    Returns a list of all contributors active in a git repo.

    :param git_id: id of a git repository (string).
    :return: contributors (list of strings)
    """

    display_query = "SELECT DISTINCT author FROM commitData WHERE commitData.repositoryID="+str(git_id)
    db.execute(display_query)

    contributors = [x[0] for x in db.fetchall()]

    return contributors