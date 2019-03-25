#
# ___author___ = Carnic
#
import json
import sqlite3

class SendPullData:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.db = self.conn.cursor()

    def store(request_id):
        pullVal = []
        select_author = "SELECT author FROM pullData WHERE requestID=(?)", (request_id)
        select_noOfComments = "SELECT noOfComments FROM pullData WHERE requestID=(?)", (request_id)
        select_targetBranch = "SELECT targetBranch FROM pullData WHERE requestID=(?)", (request_id)
        select_noOfReviews = "SELECT noOfReviews FROM pullData WHERE requestID=(?)", (request_id)
        pullVal.append(
            {
                "Request ID": request_id,
                "Author": select_author,
                "No Of Comments": select_noOfComments,
                "Target Branch": select_targetBranch,
                "No of Reviews": select_noOfReviews
            }
        )
        sendPull = json.dumps(pullVal)

        return sendPull


if __name__ == '__main__':
    sendData = SendPullData()
    request_id = "168214867"
    sendData.store("168214867")