import os
import requests
import json
import getpass

from datetime import datetime as dt


def separator():
    for i in range(130):
        print("_", end="")
    print("\n")


separator()
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

separator()

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

separator()

print("Members are:\n")
for members in test["members"]:
    print("Name: {}".format(members["full_name_display"]))
    print("Role: {}\n".format(members["role_name"]))

separator()

try:
    res = requests.get(http + "milestones", headers = header, params = {"project": id})
    sprint = res.json()

    sprintVal = []

    for sprint_name in sprint:
        sprintVal.append(
            {
                "Name": sprint_name["name"],
                "Date of creation": sprint_name["created_date"],
                "Start date": sprint_name["estimated_start"],
                "Finish date": sprint_name["estimated_finish"],
                "Total points": sprint_name["total_points"],
                "Closed points": sprint_name["closed_points"],
            }
        )

except:
    with open("sprints_dump.json", "w") as outfile:
        json.dump(sprint, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

sprintVal = list(reversed(sprintVal))

print("Sprints are:\n")

for sprints in sprintVal:
    print("Title: {}".format(sprints["Name"]))


separator()
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
		
separator()

try:
    res = requests.get(http + "tasks", headers = header, params = {"milestone": id})
    task = res.json()

except:
    with open("task_dump.json", "w") as outfile:
        json.dump(userStories, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

print("Tasks are:\n")

name = {}
count = {}

for tasks in task:
    assigned_to = tasks["assigned_to_extra_info"]
    print("Task: {}".format(tasks["subject"]))
    if tasks["assigned_to"]:
        print("Assigned to: {}\n".format(assigned_to["full_name_display"]))
        count[tasks["assigned_to"]] = 0
        name[tasks["assigned_to"]] = assigned_to["full_name_display"]
    else:
        print("Assigned to: None\n")