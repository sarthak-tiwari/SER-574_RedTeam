import os
import requests
import json
import getpass

from datetime import datetime as dt

http = 'https://api.taiga.io/api/v1/'
header = {'Content-Type': 'application/json'}

def get_wrong_userstories(slug1,sprint_no):
	sprint_no = int(sprint_no)	
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	res = requests.get(http +"projects/by_slug",headers = header, params={"slug": slug1})
	test = res.json()

	if test["name"]:
		name = test["name"]
		test_id = test["id"]
		
	res = requests.get(http + "milestones", headers = header, params = {"project": test_id})
	sprint = res.json()
	sprintId = sprint[sprint_no]
	sprint_id = sprintId["id"]
		
	res = requests.get(http + "userstories", headers = header, params = {"milestone": sprint_id})
	userStories = res.json()
	
	dic = {}
	lst = []
	us_lst = {}
	i = 1
	
	for user_story in userStories:
		dic["id"] = user_story["id"]
		dic["name"] = user_story["subject"]
		us_lst[i] = user_story["subject"]
		i = i + 1
		lst.append(dic)
		dic = {}

	dic = {}
	for i in range(len(lst)):
		dic["User Story " + str(i+1)] = lst[i]

	lst = []
	strC = "as a user"
	for i in range(1,len(us_lst)+1):
		if strC != us_lst[i][0:9].lower():
			lst.append(i)

	return lst
