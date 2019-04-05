import requests
import json
from datetime import date

from requests.auth import HTTPDigestAuth
headers = {
    'Content-Type': 'application/json',
}

def UserTaskchangestatus(slug1,sprint_no):
	sprint_no = int(sprint_no)
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	ut = []
	t = []
	utcd=[]
	utStatus = {}
	utChangeDate = {}
	status_change_dates1 = {}
	for i in sprintTask_data:
		if (sprint_no == int(i['milestone_slug'][7])):
			ut.append(i['id'])
			utChangeDate[i['id']] = i['created_date']

	for i in range(len(ut)):
		cd=[]
		cd.append(utChangeDate[ut[i]])
		status_change_dates = {}
		tempList = []
		tempList1 = []
		test1 = "https://api.taiga.io/api/v1/history/task/" + str(ut[i])
		testUserTask1 = requests.get(test1 , headers=headers)
		testData1 = json.loads(testUserTask1.content)
		for testEntry in testData1:
			for key in testEntry['values_diff']:
				if key == 'status':
					tempList.append(testEntry['values_diff'][key])
					tempList.append(testEntry['created_at'])
					cd.append(testEntry['created_at'])
					
		dic['status_change'] = tempList
		for i in range(len(cd)):
			tempList1 = []
			temp=cd[i]
			status_change_dates1[i]= temp[0:10]
		cd= status_change_dates1.values()

		for i in range(len(cd)-1):
				status_change_dates1 = {}
				
				date_string = cd[i]
				date_string2 = cd[i+1]
				now = date(*map(int, date_string.split('-')))
				now2 = date(*map(int, date_string2.split('-')))
				delta1 = now2 - now
				tempList1.append(delta1.days)
				
		tl = []
		tl.append(dict([("created_date", utChangeDate[ut[i]])]))
		tl.append(dict([('status_change',tempList)]))
		tl.append(dict([('days',tempList1)]))

		utStatus[ut[i]] = tl
		tempList = []
		tl = []

	return utStatus


