import os
import requests
import json

http = 'https://api.taiga.io/api/v1/'

headers = {'Content-Type': 'application/json'}

def list_sprints(slug1):

	project_response = requests.get(http + "/projects/by_slug?slug="+str(slug1), headers=header)
	project = project_response.json()
	prjId = str(project['id'])
	
	milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
	milestone = milestone_rsp.json()
	dic = {}
	lst = []
	for sprint in milestone:
		dic["name"] = sprint["name"]
		lst.append(dic)
		dic = {}
		
	dic = {}
	for i in range(len(lst)):
		dic["Sprint " + str(i+1)] = lst[i]

	print(dic)
	return dic