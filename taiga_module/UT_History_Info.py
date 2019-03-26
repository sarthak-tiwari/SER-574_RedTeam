import requests
import json
#from jwkest.jwk import SYMKey
#from jwkest.jwe import JWE
from requests.auth import HTTPDigestAuth
headers = {
    'Content-Type': 'application/json',
}
#slug1 = "sarthak-tiwari-ser-574_redteam_team-taiga"

def user_task_info(slug1,sprint_no):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	print sprintTask_data
	dic = {}
	ut = []
	utHistory = {}
	utCreate_date = {}
	for i in sprintTask_data:
		if (sprint_no == int(i['milestone_slug'][7])):
			ut.append(i['id'])
			utCreate_date[i['id']] = i['created_date']
	for i in range(len(ut)):
		status_change_dates = {}
		tmpList = []
		test1 = "https://api.taiga.io/api/v1/history/task/" + str(ut[i])
		testUserTask1 = requests.get(test1 , headers=headers)
		testData1 = json.loads(testUserTask1.content)
		for testEntry in testData1:
			for key in testEntry['values_diff']:
				if key == 'status':
					tmpList.append(testEntry['values_diff'][key])
					tmpList.append(testEntry['created_at'])
		dic['status_change'] = tmpList
		tl = []
		tl.append(dict([("created_date", utCreate_date[ut[i]])]))
		tl.append(dict([('status_change',tmpList)]))
		utHistory[ut[i]] = tl
		tmpList = []
		tl = []
		print json.dumps(utHistory, indent=4)

	return utHistory

#print user_story_info(slug1,2)
#user_task_info("sarthak-tiwari-ser-574_redteam_team-taiga",2)