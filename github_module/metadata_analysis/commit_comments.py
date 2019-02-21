#!/usr/bin/env python

"""
Implementation of an internal API for analyzing commit comment quality for a
user in a git project.

Internally, we define "text quality measures", which are specific properties of
a message that may be analyzed. Tesults are in a internal [-1, 1], where:
    1.0 This property increases the relevance of the comment.
    0.0 This property does not impact the relevance of the comment.
    -1.0 This property decreases the relevance of the comment.
"""
import os
import math
import util_text_analysis

__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"

# The number of characters past which descriptions are not more informative.
DESCRIPTIVE_LIMIT = 1000  # Roughly 1/3rd page.

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

    # TODO: interface with database to retrieve metadata.
    commit_metadata = None
    comment_metadata = {"id": None,
                        "text": None,
                        "author": None}

    raise NotImplementedError

    return __compute_quality(commit_metadata, comment_metadata)


def __compute_quality(commit_metadata, comment_metadata):
    """
    See documentation for compute_quality.

    :param commit_metadata: commit metadata (a dictionary)
    :param comment_metadata: comment metadata (a dictionary)
    :return: A quality score (integer between -100 and 100).
    """

    filename = __get_filename_alignment(commit_metadata, comment_metadata)
    readability = __get_readability(comment_metadata)
    thoroughness = __get_thoroughness(comment_metadata)

    score = int(readability*50+thoroughness*50+filename*20)

    if score < -100:
        score = -100
    elif score > 100:
        score = 100

    return score

# The following are internal functions which are meant to compute various
# text quality measures used to compute the quality score. Each of them processes
# commit comment metadata dictionary which is produced internally by
# compute_quality and which contains the following keys:
#   id: string
#   text: string
#   username: string


def __get_filename_alignment(commit_metadata, comment_metadata):
    """
    Computes a quality measure for filenames. Checks if keywords from filenames
    are mentioned in comment. Never returns a negative value.

    :param commit_metadata: commit metadata (a dictionary)
    :param comment_metadata: comment metadata (a dictionary)
    :return: A text quality measure for filename tag alignment.
    """

    fn = [x.split(os.sep)[-1] for x in commit_metadata["filenames"]]
    found = [1 for x in fn if x in comment_metadata["text"]]
    percent = sum(found) / len(fn)

    return percent


def __get_readability(comment_metadata):
    """
    Computes a text quality measure for a piece of text.

    :param comment_metadata: comment metadata (a dictionary)
    :return: A text quality measure for filename tag alignment.
    """

    ari = util_text_analysis.compute_ari(comment_metadata["text"])

    if ari < 6:  # sixth grade and under
        return 0.0
    elif ari < 13:  # seventh grade to college
        return 1.0
    else:  # professor level
        return -1.0


def __get_thoroughness(comment_metadata):
    """
    Computes a text quality measure for length of a comment. As the comment gets
    longer, a better score will be produced with the assumption that more text is
    more information. Uses natural exponential decay.

    :param comment_metadata: comment metadata (a dictionary)
    :return: A text quality measure for conciseness.
    """
    characters = len(comment_metadata("text"))

    score = 1 - math.exp(-characters/DESCRIPTIVE_LIMIT)

    return score
