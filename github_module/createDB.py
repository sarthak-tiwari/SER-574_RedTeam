import sqlite3

class CreateDB:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.db = self.conn.cursor()

    def user_profile(self):
        self.db.execute("CREATE TABLE userProfile (\n"
                        "    githubLogin TEXT,\n"
                        "    githubUsername TEXT,\n"
                        "    githubProfile TEXT\n"
                        "    )")

    def commit_data(self):
        self.db.execute("CREATE TABLE commitData (\n"
                        "    hash TEXT,\n"
                        "    repositoryID INTEGER,\n"
                        "    author TEXT,\n"
                        "    commitMessage TEXT,\n"
                        "    timeCommitted BLOB,\n"
                        "    filesModified TEXT,\n"
                        "    noOfAdditions INTEGER,\n"
                        "    noOfDeletions INTEGER\n"
                        "    )")

    def pull_data(self):
        self.db.execute("CREATE TABLE pullData(\n"
                        "  requestID TEXT,\n"
                        "        requestTile TEXT,\n"
                        "        author TEXT,\n"
                        "        noOfComments INTEGER,\n"
                        "        targetBranch TEXT,\n"
                        "        noOfReviews INTEGER\n"
                        "        )")

    def code_complexity(self):
        self.db.execute("CREATE TABLE codeComplexity(\n"
                        "        author TEXT,\n"
                        "        repository TEXT,\n"
                        "        codeLink TEXT,\n"
                        "        booleanComplexity TEXT,\n"
                        "        dataAbstractionComplexity TEXT,\n"
                        "        fanOutComplexity TEXT,\n"
                        "        cyclomaticComplexity TEXT,\n"
                        "        javaNCSSComplexity TEXT,\n"
                        "        nPathComplexity TEXT,\n"
                        "        javaWarnings TEXT\n"
                        "        )")

    def insertValues(self,l='',n='',p=''):
        self.db.execute(f"INSERT INTO userProfile VALUES('{l}','{n}','{p}')")
        self.db.execute("SELECT* FROM userProfile")
        print(self.db.fetchall())


if __name__ == '__main__':
    create = CreateDB()
    #create.insertValues(l='login1',n='name1',p='profile1')             #Testing

    create.code_complexity()
    create.user_profile()
    create.commit_data()
    create.pull_data()

    create.conn.commit()
    create.conn.close()

