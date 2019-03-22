import requests
import json
#from jwkest.jwk import SYMKey
#from jwkest.jwe import JWE
from requests.auth import HTTPDigestAuth
headers = {
    'Content-Type': 'application/json',
}
slug1 = "sarthak-tiwari-ser-574_redteam_team-taiga"

def user_story_info(slug1,sprint_no):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)
	project_id = project_data['epic_statuses'][0]['project_id']
	project_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
	response_milestone = requests.get(project_milestone, headers=headers)
	milestone_data = json.loads(response_milestone.content)
	dic = {}
	lst = []
	sprint_no = len(milestone_data) - sprint_no
	sprint_data = milestone_data[sprint_no]

	us = []
	for i in sprint_data['user_stories']:
		us.append(i['id'])
		dic['US_name'] = i['subject']
		dic['US_created_date'] = i['created_date']
		dic['US_finish_date'] = i['finish_date']
		response_usid = requests.get("https://api.taiga.io/api/v1/history/userstory/" + str(i['id']), headers=headers)
		us_data = json.loads(response_usid.content)
		for j in us_data:
			diff = j['diff']
			ms = 'milestone'
			if ms in diff:
				diff2 = diff['milestone']
				if diff2[1] == i['milestone']:
					dic['US_movedToSprintDate'] = j['created_at']
		lst.append(dic)
		dic = {}

	dic = {}
	for i in range(len(lst)):
		dic['US ' + str(i+1)] = lst[i]

	return dic


def user_task_info(slug1,sprint_no):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	response_project_data = requests.get(projectinfo+slug1, headers=headers)
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers)
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	lst = []
	ut = []
	for i in sprintTask_data:
		ut.append(i['id'])
		extra = i['assigned_to_extra_info']
		dic['user_task'] = i['subject']
		dic['user_task_created_at'] = i['created_date']
		lst.append(dic)
		dic = {}

	dic = {}
	for i in range(len(lst)):
		dic['User_task ' + str(i+1)] = lst[i]

	project_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
	response_milestone = requests.get(project_milestone, headers=headers)
	milestone_data = json.loads(response_milestone.content)
	sprint_no = len(milestone_data) - sprint_no
	#sprint_data = milestone_data[sprint_no]
	#print sprint_data


	#print(dic)
	print "UT info"
	for i in range(len(ut)):
		test = "https://api.taiga.io/api/v1/tasks/" + str(ut[i])
		testUserTask = requests.get(test , headers=headers)
		testData = json.loads(testUserTask.content)
		#print testData
		if (sprint_no == testData['milestone_slug'][8]):
			test = "https://api.taiga.io/api/v1/history/task/" + str(ut[i])
			testUserTask = requests.get(test , headers=headers)
			testData = json.loads(testUserTask.content)
			print testData
			print '-----'

	return dic

#print user_story_info(slug1,2)
# user_task_info("sarthak-tiwari-ser-574_redteam_team-taiga",2)