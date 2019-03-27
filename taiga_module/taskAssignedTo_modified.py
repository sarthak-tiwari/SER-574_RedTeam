import requests
import json
#from jwkest.jwk import SYMKey
#from jwkest.jwe import JWE
from requests.auth import HTTPDigestAuth
headers = {
    'Content-Type': 'application/json',
}
#slug1 = "sarthak-tiwari-ser-574_redteam_team-taiga"

def get_modifiedTaskAssignedTo(slug1,sprint_no):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	ut = []
	utHistory = {}
	assigned_to_modified = {}
	for i in sprintTask_data:
		if (sprint_no == int(i['milestone_slug'][7])):
			ut.append(i['id'])
			assigned_to_modified[i['id']] = i['assigned_to']
	for i in range(len(ut)):
		status_change_dates = {}
		tmpList = []
		test1 = "https://api.taiga.io/api/v1/history/task/" + str(ut[i])
		testUserTask1 = requests.get(test1 , headers=headers)
		testData1 = json.loads(testUserTask1.content)
		for testEntry in testData1:
			for key in testEntry['values_diff']:
				if key == 'assigned_to':
					tmpList.append(testEntry['values_diff'][key])
		dic['assigned_to_modified'] = tmpList
		tl = []
		tl.append(dict([('assigned_to_modified',tmpList)]))
		utHistory[ut[i]] = tl
		tmpList = []
		tl = []
	#print (utHistory)
	return utHistory

#get_modifiedTaskAssignedTo("sarthak-tiwari-ser-574_redteam_team-taiga",2)