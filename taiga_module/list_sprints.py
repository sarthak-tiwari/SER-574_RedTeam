import os
import requests
import json

http = 'https://api.taiga.io/api/v1/'

headers = {'Content-Type': 'application/json'}

def get_list_sprints(slug1):

	project_response = requests.get(http + "/projects/by_slug?slug="+str(slug1), headers=headers)
	project = project_response.json()
	prjId = str(project['id'])
	
	milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=headers)
	milestone = milestone_rsp.json()
	sprintVal = []

	for sprint_name in milestone:
		sprintVal.append(
			{
				"Name": sprint_name["name"]
			}
		)
	sprintVal = list(reversed(sprintVal))
	dic = {}
	lst = []
	for sprint in sprintVal:
		dic["name"] = sprint["Name"]
		lst.append(dic)
		dic = {}
		
	dic = {}
	for i in range(len(lst)):
		dic["Sprint " + str(i+1)] = lst[i]

	return dic