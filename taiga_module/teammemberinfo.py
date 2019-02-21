import requests
import json

header = {
    'Content-Type': 'application/json',
}

user_name = raw_input("username : ")
password = raw_input("password : ")


data = {"password": password, 
		"type": "normal",        
		"username": user_name }

API= 'https://api.taiga.io/api/v1/'
response = requests.post(API+'auth', headers=header, data=json.dumps(data))
data=json.loads(response.content)

print("Token - " + data['auth_token'])

project_name = raw_input("Enter project name : ")

response = requests.get(API+'projects/by_slug?slug=' +project_name, headers=header, data=json.dumps(data))
data = json.loads(response.content)

for pdata in data['members']:
	 
	print ("Member's Name - " + pdata['full_name_display'])
	print ("email - " + pdata['email'])
	print ("Pid - " + pdata['id'])
	print ("Role - " + pdata['role_name'])
	print ("Username - " + pdata['username'])
	print ("__________________________________________________")
	
projec_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
response_milestone = requests.get(projec_milestone, headers=headers, data=json.dumps(data))
milestone_data = json.loads(response_milestone.content)

sprintdata = raw_input("Choose a sprint, type in the number the number mentioned for the sprint: ")


sprint_data = milestone_data[int(sprintdata)]
print(sprint_data['name'])
print("User story info for " + sprint_data['name'])

us = []

for i in sprint_data['user_stories']:
	#print i
	print "US name:      " + i['subject']
	print "US storyPoints:      " + i['total_points']
	us.append(i['id'])
	response_usid = requests.get("https://api.taiga.io/api/v1/history/userstory/" + str(i['id']), headers=headers, data = json.dumps(data))
	us_data = json.loads(response_usid.content)
	
response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers, data=json.dumps(data))
sprintTask_data = json.loads(response_sprintTask.content)

task_per_user = []
for i in sprintTask_data:
	if i['user_story'] in us:
		extra = i['assigned_to_extra_info']
		print(i['subject'] + " is assigned to: " + extra['full_name_display'])
		task_per_user.append(extra['full_name_display'])

