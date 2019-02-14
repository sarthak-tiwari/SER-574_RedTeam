#!/usr/bin/env python

"""
Implementation of an internal API for analyzing commit message quality for a
user in a git project.

Internally, we define "quality measures", which are specific properties of a
message that may be analyzed. Analysis results in one of three possible values:
    1 This property increases the relevance of the commit.
    0 This property does not impact the relevance of the commit.
    -1 This property decreases the relevance of the commit.
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"

VALID_TAGS = ["ADD, CHANGE, REMOVE, BUGFIX"]
COMMENT_MAX_LENGTH = 80


def compute_quality(github_repo, commit_hash):
    """
    Returns a quality index for a commit in a git repository. The measure is
    between -100 and 100, where 0 is an empty message, -100 is a misleading
    message, and 100 is a useful message.

    A useful message is one that is descriptive (uses tags, valid links to
    taiga, relates to files) and concise (less than message length threshold).

    Assumes valid git repo and commit hash.

    :param github_repo: name of a git repository (string).
    :param commit_hash: hash of a git commit (string).
    :return: A quality score (integer between -100 and 100).
    """

    commit_metadata = {"hash": None,
                       "comment": None,
                       "timestamp": None,
                       "username": None,
                       "filenames": None}

    raise NotImplementedError



# The following are internal functions which are meant to compute various
# quality measures used to compute the quality score. Each of them processes a
# commit metadata dictionary which is produced internally by compute_quality and
# which contains the following keys:
#   hash: string
#   comment: string
#   timestamp: string
#   username: sting
#   filenames: string


def __get_tag_alignment(commit_metadata):
    """
    Computes a quality measure for tags. Checks for whether a commit contains
    whitelisted tags. Never returns a negative value.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure for tag alignment.
    """
    raise NotImplementedError


def __get_tagia_alignment(commit_metadata):
    """
    Computes a quality measure for taiga alignments. Checks to see if any
    mentioned USs or tasks are valid taiga tasks.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure fore taiga alignment.
    """
    raise NotImplementedError


def __get_filename_alignment(commit_metadata):
    """
    Computes a quality measure for filenames. Checks if keywords from filenames
    are mentioned in comment. Never returns a negative value.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure for filename tag alignment.
    """
    raise NotImplementedError


def __get_conciseness(commit_metadata):
    """
    Computes a quality measure for length of a comment. If a is too short (0) or
    long (see threshold), the commit will produce a negative quality measure.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure for conciseness.
    """
    raise NotImplementedError
