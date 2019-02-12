import os
import requests
import json
import getpass
from datetime import datetime as dt

http = 'https://api.taiga.io/api/v1/'

header = {'Content-Type': 'application/json'}

while True:
    try:
        username = input("Enter username: ")

        password = getpass.getpass("Password: ")

        data = {"password": password, "type": "normal", "username": username}

        res = requests.post(http + "auth", headers = header, data = json.dumps(data))
        test = res.json()

        token = test["auth_token"]
        break

    except:
        print("Invalid username or password\n")
		
while True:
    try:
        slug = input("Enter slug: \n")

        res = requests.get(http +"projects/by_slug",headers = header, params={"slug": slug})
        test = res.json()

        if test["name"]:
            name = test["name"]
            id = test["id"]
        break

    except:
        with open("project_dump.json", "w") as outfile:
            json.dump(test, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
        print("Invalid slug\n")
		
print("Project Name: {}\n".format(name))

try:
    res = requests.get(http + "milestones", headers = header, params = {"project": id})
    sprint = res.json()

    sprintVal = []

    for sprint_name in sprint:
        sprintVal.append(
            {
                "Name": sprint_name["name"]
            }
        )

except:
    with open("sprints_dump.json", "w") as outfile:
        json.dump(sprint, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
		
sprintVal = list(reversed(sprintVal))

print("Sprints are:\n")

for sprints in sprintVal:
    print("Title: {}".format(sprints["Name"]))
   
while True:
    try:
        sprintNo = int(input("Enter sprint number: "))
        if sprintNo >= 1 and sprintNo <= len(sprintVal):
            break
        else:
            print("Sprint does not exsist\n")
    except:
        print("Sprint does not exsist\n")
		

sprintNo = len(sprintVal) - sprintNo

sprintId = sprint[sprintNo]
id = sprintId["id"]

try:
    res = requests.get(http + "userstories", headers = header, params = {"milestone": id})
    userStories = res.json()

    print("\nUser Stories are:\n")

    for user_story in userStories:
        print("Subject: {}".format(user_story["subject"]))
              
except:
    with open("us_dump.json", "w") as outfile:
        json.dump(userStories, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
