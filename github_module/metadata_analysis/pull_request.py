#!/usr/bin/env python

"""
Implementation of an internal API for analyzing pull requests to determine if
they have been handled correctly.

"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def get_merged_status(github_repo):
    """
    Returns a merged pull request status dictionary.

    A merged pull request status dictionary contains the following keys:
      "requests" : (a list of integers)
      "request_data : (a dictionary)
        <pull request as integer> : (a dictionary)
            "creator" : (string)
            "authorizer" : (string)
            "merged_properly" : (boolean)
        (the above is repeated for each pull request.)

    :param github_repo: name of a github repository (string).
    :return: status for each merged pull request (dictionary)
    """
    raise NotImplementedError


def get_pull_requests(github_repo):
    """
    Returns a list of all pull requests that have been made in a project.

    :param github_repo: name of a github repository (string).
    :return: list of pull requests (list of integers).
    """
    raise NotImplementedError


def get_merged_pull_requests(github_repo):
    """
    Returns a list of all pull requests which have been merged.

    Assumes valid github repo and pull request number.

    :param github_repo: name of a github repository (string).
    :return: list of pull requests (list of integers)
    """
    raise NotImplementedError


def handled_correctly(github_repo, pr_num):
    """
    Returns a boolean to indicate if a particular pull request was handled correctly.
    
    Assumes valid github repo and pull request number. 
    :param github_repo: name of a github repository (string).
    :param pr_num: pull request number. (integer)
    :return: if a pull request was handled correctly (boolean)
    """
    raise NotImplementedError


# The following are internal functions.

def __get_pr_rules(github_repo, branch):
    """
    Finds and returns the current rules for handling pull requests in a specific branch.

    Returns a dictionary which contains the following keys:
      "reviewers_required" : (integer)

    :param github_repo: name of a github repository (string).
    :param branch: name of a branch in git.
    :return: rules for handling pull requests (dictionary)
    """
    raise NotImplementedError
