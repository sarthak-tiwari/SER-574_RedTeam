import os
import requests
import json
import getpass

from datetime import datetime as dt


http = 'https://api.taiga.io/api/v1/'

headers = {'Content-Type': 'application/json'}

def get_task_finishdate(slug1, userstory_no):

	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	lst = []
	for tasks in sprintTask_data:
	
		userstory_id = tasks["user_story_extra_info"]
		userstory = userstory_id["id"]
		us = int(userstory_no)
		if userstory == us:
			finish = dt.strptime(tasks["finished_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
			finish = dt.strftime(finish, "%b %d %Y")
			dic["finished date"] = finish
			dic["name"] = tasks["subject"]
			lst.append(dic)
			dic = {}

	dic = {}
	for i in range(len(lst)):
		dic["Task " + str(i+1)] = lst[i]

	return dic