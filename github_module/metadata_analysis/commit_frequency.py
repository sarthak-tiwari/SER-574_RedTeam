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
    raise NotImplementedError


def count_on_day(git_repo, username, date):
    """
    Returns the number of commits made by a usre in a git repository on a
    specific day.

    Assumes valid git repo and username.

    :param git_repo: name of a git repository (string).
    :param username: username (string)
    :param date: day (date object).
    :return: number of commits (integer).
    """
    raise NotImplementedError


def count_list_internal(git_repo, username, interval_start, interval_end):
    """
    Returns a list of commits made each day by a user in a git repository
    during a time internal.The interval is inclusive.

    Assumes valid git repo and username.

    :param git_repo: name of a git repository (string).
    :param username: username (string)
    :param interval_start: day for start of internal (date object).
    :param interval_end: day for end of internal (date object).
    :return: a list of commits per day (list of integers).
    """
    raise NotImplementedError
