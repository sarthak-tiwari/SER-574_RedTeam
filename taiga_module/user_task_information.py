import requests
import json
#from jwkest.jwk import SYMKey
#from jwkest.jwe import JWE

def project_info_byslug(headers,data):
	projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
	project_slug = raw_input("Enter the project slug : ")
	response_project_data = requests.get(projectinfo+project_slug, headers=headers, data=json.dumps(data))
	project_data = json.loads(response_project_data.content)

	project_id = project_data['epic_statuses'][0]['project_id']
	dic = {}
	lst = []
	for i in project_data['members']:
		dic["full_name_display"] = i['full_name_display']
		dic["role_name"] = i['role_name']
		lst.append(dic)
		dic = {}

	dic = {}
	for i in range(len(lst)):
		dic["user " + str(i+1)] = lst[i]

	return json.dumps(dic),project_id


headers = {
    'Content-Type': 'application/json',
}

username1 = raw_input("Enter Username : ")
password1 = raw_input("Enter Password : ")


data = {"password": password1, 
		"type": "normal",        
		"username": username1 }


response = requests.post('https://api.taiga.io/api/v1/auth', headers=headers, data=json.dumps(data))
data=json.loads(response.content)
print("Auth Token : " + data['auth_token'])

projectInfo_bySlug,project_id =  project_info_byslug(headers,data)
print projectInfo_bySlug

def user_story_info(project_id,headers,data):

	projec_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
	response_milestone = requests.get(projec_milestone, headers=headers, data=json.dumps(data))
	milestone_data = json.loads(response_milestone.content)
	dic = {}
	lst = []

	sprintno = 0
	for i in milestone_data:
		print("Sprint info -")
		print(str(sprintno) + " : " + i['name'])
		print("    Created:    " + i['created_date'])
		print("    Start Date:     " + i['estimated_start'])
		print("    End Date:      " + i['estimated_finish'])
		print("    Sprint Points    " + str(i['total_points']))
		print("    Closed Points    " + str(i['closed_points']))
		sprintno += 1
	sprintdata = raw_input("Choose a sprint, type in the number the number mentioned for the sprint: ")


	sprint_data = milestone_data[int(sprintdata)]

	us = []
	for i in sprint_data['user_stories']:
		us.append(i['id'])
		dic['US_name'] = i['subject']
		dic['US_created_date'] = i['created_date']
		dic['US_finish_date'] = i['finish_date']
		response_usid = requests.get("https://api.taiga.io/api/v1/history/userstory/" + str(i['id']), headers=headers, data = json.dumps(data))
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

	return json.dumps(dic),us

us_info,us = user_story_info(project_id,headers,data)
print us_info
print "----------"


def user_task_info(headers,data,us):
	response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers, data=json.dumps(data))
	sprintTask_data = json.loads(response_sprintTask.content)
	dic = {}
	lst = []
	task_per_user = []
	for i in sprintTask_data:
		if i['user_story'] in us:
			extra = i['assigned_to_extra_info']
			task_per_user.append(extra['full_name_display'])
			dic['user_task'] = i['subject']
			dic['user_task_created_at'] = i['created_date']
			lst.append(dic)
			dic = {}

	dic = {}
	for i in range(len(lst)):
		dic['User_task ' + str(i+1)] = lst[i]

	return json.dumps(dic)

userTask_info = user_task_info(headers,data,us)
print userTask_info

