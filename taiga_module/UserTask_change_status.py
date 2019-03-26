import requests
import json

from requests.auth import HTTPDigestAuth
headers = {
    'Content-Type': 'application/json',
}

def user_task_info(slug1,sprint_no):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	ut = []
	utStatus = {}
	utChangeDate = {}
	for i in sprintTask_data:
		if (sprint_no == int(i['milestone_slug'][7])):
			ut.append(i['id'])
			utChangeDate[i['id']] = i['created_date']
	print "User task status info"
	for i in range(len(ut)):
		status_change_dates = {}
		tempList = []
		test1 = "https://api.taiga.io/api/v1/history/task/" + str(ut[i])
		testUserTask1 = requests.get(test1 , headers=headers)
		testData1 = json.loads(testUserTask1.content)
		for testEntry in testData1:
			for key in testEntry['values_diff']:
				if key == 'status':
					tempList.append(testEntry['values_diff'][key])
					tempList.append(testEntry['created_at'])
		dic['status_change'] = tempList
		tl = []
		tl.append(dict([("created_date", utChangeDate[ut[i]])]))
		tl.append(dict([('status_change',tempList)]))
		utStatus[ut[i]] = tl
		tempList = []
		tl = []
	return utStatus

print (user_task_info("sarthak-tiwari-ser-574_redteam_team-taiga",2))
