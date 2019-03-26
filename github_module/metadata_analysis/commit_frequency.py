#!/usr/bin/env python

"""
Implementation of an internal API for analyzing frequency of commits for a user
in a git project.
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def count_in_internal(git_repo, username, interval_start, interval_end):
    """
    Returns the number of commits made by a user in a git repository during a
    time internal. The interval is inclusive.

    Assumes valid git repo and username.

    :param git_repo: name of a git repository (string).
    :param username: username (string)
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: number of commits (integer).
    """

    return sum(count_list_internal(git_repo, username, interval_start,
                                   interval_end))



def count_on_day(git_repo, username, date):
    """
    Returns the number of commits made by a user in a git repository on a
    specific day.

    Assumes valid git repo and username.

    :param git_repo: name of a git repository (string).
    :param username: username (string)
    :param date: day (date object).
    :return: number of commits (integer).
    """

    return count_list_internal(git_repo, username, date, date)


def count_list_internal(git_repo, username, interval_start, interval_end):
    """
    Returns a list of commits made each day by a user in a git repository
    during a time internal. The interval is inclusive.

    Assumes valid git repo and username.

    :param git_repo: name of a git repository (string).
    :param username: username (string)
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: a list of commits per day (list of integers).
    """
    freq_data = __get_commit_freq_data(git_repo, interval_start, interval_end)
    result = [x["commit_count"][username] if username in x["usernames"] else 0
              for x in freq_data]

    return result

# The following are internal functions.

def __get_commit_freq_data(git_repo, interval_start, interval_end):
    """

    A daily commit status dictionary contains the following keys:
      "usernames" : (a list of strings)
      "date" : (date object)
      "commit_count" : (a dictionary)
        <contributor as string> : (integer)
        (the above is repeated for each contributor on the particular day.)

    :param git_repo: name of a git repository (string).
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: commit statuses (list of commit status dictionaries).
    """
    interval = interval_end-interval_start
    result = None

    # TODO: interface with database to retrieve contributors.

    #future debugging
    assert len(result) == interval, "See __get_commit_freq_data()."

    raise NotImplementedError

def __get_all_contributors(git_repo):
    """
    Returns a list of all contributors active in a git repo.

    :param git_repo: name of a git repository (string).
    :return: contributors (list of strings)
    """

    # TODO: interface with database to retrieve contributors.

    raise NotImplementedError