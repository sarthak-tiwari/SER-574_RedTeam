import os
import requests
import json
import getpass

from datetime import datetime as dt


http = 'https://api.taiga.io/api/v1/'

headers = {'Content-Type': 'application/json'}

def get_task_assignedto(slug1):

	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	lst = []
	for tasks in sprintTask_data:
	
		assigned_to = tasks["assigned_to_extra_info"]
		dic["subject"] = tasks["subject"]
		if tasks["assigned_to"]:
			dic["assigned_to"] = assigned_to["full_name_display"]
			lst.append(dic)
			dic = {}
		else:
			dic["assigned_to"] = "null"
			lst.append(dic)
			dic = {}
		

	dic = {}
	for i in range(len(lst)):
		dic["Task " + str(i+1)] = lst[i]

	return dic