import commit_comments
import commit_frequency
import commit_messages
import pull_request

################################################################################
# frequency related

import datetime
import sqlite3

################################################################################
#commit_messages related



#baseline testing environment
git_id = 168214867 #our repo
feb_start = datetime.datetime(2019, 2, 1)
feb_end = datetime.datetime(2019, 2, 28)

#need to test helpers
conn = sqlite3.connect('database.db')
db = conn.cursor()
a = commit_frequency.count_in_internal(git_id, "test", feb_start, feb_end)
b = commit_frequency.count_on_day(git_id, "test", datetime.datetime(2019, 2, 7)) #1
c = commit_frequency.count_list_internal(git_id, "test", feb_start, feb_end)
commit_frequency.__get_commit_freq_data(db, git_id, feb_start, feb_end)
commit_frequency.__get_all_contributors(db,git_id)



################################################################################
#commit_messages related

commit_messages.compute_quality(git_id, "70f13b111e1147611b70f9c9f1f76ddb00fcbe27") #50

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