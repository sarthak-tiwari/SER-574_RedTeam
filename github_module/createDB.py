# Class to create database
#
# Author : Carnic
# Email : clnu2@asu.edu

import sqlite3

class CreateDB:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.db = self.conn.cursor()

    def repositories(self):
        self.db.execute("CREATE TABLE repositories (\n"
                        "    name TEXT,\n"
                        "    owner TEXT,\n"
                        "    id INTEGER,\n"
                        "    PRIMARY KEY(\"id\")\n"
                        "    )")

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
                        "    date INTEGER,\n"
                        "    timeCommitted BLOB,\n"
                        "    filesModified TEXT,\n"
                        "    noOfAdditions INTEGER,\n"
                        "    noOfDeletions INTEGER\n"
                        "    )")

    def pull_data(self):
        self.db.execute("CREATE TABLE pullData(\n"
                        "        requestID TEXT,\n"
                        "        requestTile TEXT,\n"
                        "        author TEXT,\n"
                        "        noOfComments INTEGER,\n"
                        "        targetBranch TEXT,\n"
                        "        noOfReviews INTEGER\n"
                        "        )")

    def code_complexity(self):
        self.db.execute("CREATE TABLE codeComplexity ("
	                        "repository	TEXT NOT NULL, "
	                        "fileName NUMERIC NOT NULL, "
	                        "author	TEXT NOT NULL, "
	                        "codeLink TEXT NOT NULL, "
	                        "booleanExpressionComplexity INTEGER, "
	                        "classFanOutComplexity INTEGER, "
	                        "cyclomaticComplexity INTEGER, "
	                        "javaNCSS INTEGER, "
	                        "nPathComplexity INTEGER, "
	                        "classDataAbstractionCoupling INTEGER, "
	                        "javaWarnings INTEGER);"
                        )

    def insertValues(self):
        # self.db.execute(f"INSERT INTO userProfile VALUES('{l}','{n}','{p}')")
        self.db.execute("SELECT* FROM userProfile")
        print(self.db.fetchall())


if __name__ == '__main__':
    create = CreateDB()
    #create.insertValues(l='login1',n='name1',p='profile1')             #Testing

    # create.repositories()
    # create.code_complexity()
    # create.user_profile()
    # create.commit_data()
    # create.pull_data()

    create.conn.commit()
    create.conn.close()
