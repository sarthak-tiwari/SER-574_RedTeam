import commit_comments
import commit_frequency
import commit_messages
import pull_request

################################################################################
#commit_messages related
#def compute_quality(github, commit_hash):

commit_metadata = {"hash": None, "comment": "US#6-TASK#16: Designed backend API for frequency analysis.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__compute_quality(commit_metadata) >= 50
commit_metadata = {"hash": None, "comment": "US#6-TASK#16: BUGFIX blah blah.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__compute_quality(commit_metadata) >= 70
commit_metadata = {"hash": None, "comment": "US#6-TASK#16: BUGFIX blah blah blah blah blah blah blah blah blah blah.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__compute_quality(commit_metadata) >= -30

commit_metadata = {"hash": None, "comment": "", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_tag_alignment(commit_metadata) == 0
commit_metadata = {"hash": None, "comment": "BUGFIX: something something", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_tag_alignment(commit_metadata) == 1
commit_metadata = {"hash": None, "comment": "BUGTHINGY: something something something", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_tag_alignment(commit_metadata) == 0

#def __get_tagia_alignment(commit_metadata):

commit_metadata = {"hash": None, "comment": "", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_conciseness(commit_metadata) == -1
commit_metadata = {"hash": None, "comment": "Fix.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_conciseness(commit_metadata) == 0
commit_metadata = {"hash": None, "comment": "A bug that is explained properly.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_conciseness(commit_metadata) == 1
commit_metadata = {"hash": None, "comment": "A bug fix that is being explained with way too words and which should actually be penalized.", "timestamp": None, "username": None, "filenames": None}
assert commit_messages.__get_conciseness(commit_metadata) == -1

"""
    commit_metadata = {"hash": None,
                       "comment": None,
                       "timestamp": None,
                       "username": None,
                       "filenames": None}
"""