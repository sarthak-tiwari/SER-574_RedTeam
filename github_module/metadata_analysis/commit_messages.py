#!/usr/bin/env python
################################################################################

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

import sqlite3

#A list of tags which may occur in a comment.
VALID_TAGS = ["ADD", "CHANGE", "REMOVE", "BUGFIX"]

#the hard upper limit for the length of a comment.
COMMENT_MAX_LENGTH = 70

#[0, 1] representing a margin where a comment's length may be too short or too
#long, but which should not be penalized.
COMMENT_MARGIN = .1


def compute_quality(github_id, commit_hash):
    """
    Returns a quality index for a commit in a git repository. The measure is
    between -100 and 100, where 0 is an empty message, -100 is a misleading
    message, and 100 is a useful message.

    A useful message is one that is descriptive (uses tags, valid links to
    taiga) and concise (less than message length threshold).

    Assumes valid git repo and commit hash.

    :param github_id: id of a git repository (string).
    :param commit_hash: hash of a git commit (string).
    :return: A quality score (integer between -100 and 100).
    """

    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    display_query = "SELECT commitMessage, timeCommitted, author, filesModified FROM commitData WHERE commitData.hash=\"" + commit_hash +"\""
    db.execute(display_query)
    found = db.fetchall()

    #prepare metadata dictionary
    commit_metadata = dict()
    commit_metadata["hash"] = commit_hash
    commit_metadata["comment"] = found[0][0]
    commit_metadata["timestamp"] = found[0][1]
    commit_metadata["username"] = found[0][2]
    commit_metadata["filenames"] = found[0][3]

    return __compute_quality(commit_metadata)


def __compute_quality(commit_metadata):
    """
    See compute_quality for more information. This function serves as an
    internal helper so that functionality can be tested independently of database.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality score (integer between -100 and 100).
    """
    tag = __get_tag_alignment(commit_metadata)
    tagia = 0 #TODO: see __get_tagia_alignment
    conciseness = __get_conciseness(commit_metadata)

    #RA: this is silly.
    internal_score = tag * 20 + tagia * 50 + conciseness * 50

    if internal_score > 100:
        return 100
    else:
        return internal_score


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

    #if comment contains any tag, then return 1, else return zero
    used_tags = [tag for tag in VALID_TAGS if tag in commit_metadata["comment"]]

    return len(used_tags) > 0


def __get_tagia_alignment(commit_metadata):
    """
    Computes a quality measure for taiga alignments. Checks to see if any
    mentioned USs or tasks are valid taiga tasks.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure fore taiga alignment.
    """

    #TODO: need to access taiga data.

    raise NotImplementedError


def __get_conciseness(commit_metadata):
    """
    Computes a quality measure for length of a comment. If a is too short (0) or
    long (see threshold), the commit will produce a negative quality measure.

    :param commit_metadata: commit metadata (a dictionary)
    :return: A quality measure for conciseness.
    """

    first_line_len = len(commit_metadata["comment"].split("\n")[0])
    margin = int(COMMENT_MAX_LENGTH * COMMENT_MARGIN)

    if first_line_len == 0 or first_line_len > COMMENT_MAX_LENGTH:
        return -1

    if first_line_len < margin or first_line_len > COMMENT_MAX_LENGTH-margin:
        return 0

    return 1
