#!/usr/bin/env python

"""
01234567890123456789012345678901234567890123456789012345678901234567890123456789

Implementation of an internal API for analyzing commit comment quality for a
user in a git project.

Internally, we define "quality measures", which are specific properties of a
message that may be analyzed. Analysis results in one of three possible values:
    1 This property increases the relevance of the comment.
    0 This property does not impact the relevance of the comment.
    -1 This property decreases the relevance of the comment.
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def compute_quality(github, commit_hash, comment_id):
    """

    Returns a quality index for a commit's comment in a github repository. The
    measure is between -100 and 100, where 0 is an empty message, -100 is a
    misleading message, and 100 is a useful message.

    A useful message is one that is descriptive (relates to files), readable
    (few spelling mistakes), and thoroughness (less than message length threshold).

    Assumes valid git repo and commit hash.

    :param github: name of a git repository (string).
    :param commit_hash: hash of a git commit (string).
    :return: A quality score (integer between -100 and 100).
    """

    #
    comment_metadata = {"id": None,
                       "text": None,
                       "author": None}

    raise NotImplementedError



# The following are internal functions which are meant to compute various
# quality measures used to compute the quality score. Each of them processes a
# commit comment metadata dictionary which is produced internally by
# compute_quality and which contains the following keys:
#   id: string
#   text: string
#   username: sting


def __get_filename_alignment(comment_metadata):
    """
    Computes a quality measure for filenames. Checks if keywords from filenames
    are mentioned in comment. Never returns a negative value.

    :param comment_metadata: comment metadata (a dictionary)
    :return: A quality measure for filename tag alignment.
    """
    raise NotImplementedError

def __get_readability(comment_metadata):
    """

    :param comment_metadata: comment metadata (a dictionary)
    :return: A quality measure for filename tag alignment.
    """
    raise NotImplementedError

def __get_thoroughness(comment_metadata):
    """
    Computes a quality measure for length of a comment. As the comment gets
    longer, a better score will be produce with the assumption that more text is
    more information.

    :param comment_metadata: comment metadata (a dictionary)
    :return: A quality measure for conciseness.
    """
    raise NotImplementedError
