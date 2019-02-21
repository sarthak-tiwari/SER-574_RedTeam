import os
import requests
import json
import getpass

http = 'https://api.taiga.io/api/v1/'

def get_task_assignedto(headers,data,userStories):
	
	dic = {}
	lst = []
	for tasks in task:
	
		assigned_to = tasks["assigned_to_extra_info"]
		dic["subject"] = tasks["subject"]
		if tasks["assigned_to"]:
			dic["assigned_to"] = assigned_to["full_name_display"]
			lst.append(dic)
			dic = {}
		else:
			dic["assigned_to"] = null
			lst.append(dic)
			dic = {}
		

	dic = {}
	for i in range(len(lst)):
		dic["Task " + str(i+1)] = lst[i]

	return json.dumps(dic)

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
		
projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
slug = input("Enter the project slug : ")
res = requests.get(http +"projects/by_slug",headers = header, params={"slug": slug})
test = res.json()

if test["name"]:
	name = test["name"]
	test_id = test["id"]
		
print("Project Name: {}\n".format(name))
	
res = requests.get(http + "milestones", headers = header, params = {"project": test_id})
sprint = res.json()
	
sprintVal = []
	
for sprint_name in sprint:
	sprintVal.append(
		{
			"Name": sprint_name["name"]
		}
	)
		
sprintVal = list(reversed(sprintVal))

print("Sprints are:\n")
	
for sprints in sprintVal:
	print("Title: {}".format(sprints["Name"]))
		
sprintNo = int(input("Enter sprint number: "))
if sprintNo <= 1 and sprintNo >= len(sprintVal):
	print("Sprint does not exsist\n")
		
		
sprintNo = len(sprintVal) - sprintNo

sprintId = sprint[sprintNo]
sprint_id = sprintId["id"]



res = requests.get(http + "tasks", headers = header, params = {"milestone": sprint_id})
task = res.json()


		
task_member = get_task_assignedto(header,data,task)
print (task_member)
		