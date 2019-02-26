#!/usr/bin/env python
################################################################################

"""
Various helper functions for analyzing textual information.
"""


__author__    = "Ruben Acuna"
__copyright__ = "Copyright 2019, SER574 Red Team"


def compute_ari(text: str):
    """
    Compute the Automated_readability_index score (US grade level for input. See
    https://en.wikipedia.org/wiki/Automated_readability_index for more
    information.

    :param text: comment
    :return: score (integer)
    """
    characters = len(text.replace(" ", "").replace(".", "").replace(",", "").replace(";", ""))
    words = text.count(" ") + 1
    sentences = text.count(".")

    score = 4.71 * (characters / words) + .5 * (words / sentences) - 21.43

    return score


if __name__ == "__main__":
    #Validate ARI on sample data. Test data and results are from:
    #http://www.readabilityformulas.com/automated-readability-index.php
    input = "The rule of rhythm in prose is not so intricate. Here, too, we write in groups, or phrases, as I prefer to call them, for the prose phrase is greatly longer and is much more nonchalantly uttered than the group in verse; so that not only is there a greater interval of continuous sound between the pauses, but, for that very reason, word is linked more readily to word by a more summary enunciation. Still, the phrase is the strict analogue of the group, and successive phrases, like successive groups, must differ openly in length and rhythm. The rule of scansion in verse is to suggest no measure but the one in hand; in prose, to suggest no measure at all. Prose must be rhythmical, and it may be as much so as you will; but it must not be metrical. It may be anything, but it must not be verse."
    assert(int(compute_ari(input)) == 10), "Failed to calculate ARI properly."