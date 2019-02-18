import requests
import json
#from jwkest.jwk import SYMKey
#from jwkest.jwe import JWE

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
#print(data)
print("Auth Token : " + data['auth_token'])
"""key = "this is the secret key"

sym_key = SYMKey(key=key, alg="A128KW")
token=JWE().decrypt(data['auth_token'], keys=[sym_key])
print(token)"""

projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="

project_slug = raw_input("Enter the project slug : ")
memberno = 1
response_project_data = requests.get(projectinfo+project_slug, headers=headers, data=json.dumps(data))
project_data = json.loads(response_project_data.content)

project_id = project_data['epic_statuses'][0]['project_id']
#print project_id
print "Member Info : "
for i in project_data['members']:
	 
	print "Name:       " + i['full_name_display']
	print "  Role          " + i['role_name']


projec_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
#projec_milestone = "https://api.taiga.io/api/v1/projects/by_slug?slug="
response_milestone = requests.get(projec_milestone, headers=headers, data=json.dumps(data))
milestone_data = json.loads(response_milestone.content)
#id = milestone_data['id']
#print milestone_data
#projec_milestone = "https://api.taiga.io/api/v1/milestones"
#response_milestone = requests.get(projec_milestone+project_slug, headers=headers, params = {"project" : id}, data=json.dumps(data))
#print response_milestone
#milestone_data = json.loads(response_milestone.content)
#mdata = response_milestone.json()
#print mdata

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
print(sprint_data['name'])
print("User story info for " + sprint_data['name'])

us = []

for i in sprint_data['user_stories']:
	#print i
	print "US name:      " + i['subject']
	print "US Created:     " + str(i['created_date'])
	print "US Finished:    " + str(i['is_closed'])
	us.append(i['id'])
	response_usid = requests.get("https://api.taiga.io/api/v1/history/userstory/" + str(i['id']), headers=headers, data = json.dumps(data))
	us_data = json.loads(response_usid.content)
	for j in us_data:
		diff = j['diff']
		ms = 'milestone'
		if ms in diff:
			diff2 = diff['milestone']
			if diff2[1] == i['milestone']:
				print("         Added in sprint on : " + str(j['created_at']))

response_sprintTask = requests.get("http://api.taiga.io/api/v1/tasks?project=" + str(project_id) , headers=headers, data=json.dumps(data))
sprintTask_data = json.loads(response_sprintTask.content)

task_per_user = []
for i in sprintTask_data:
	if i['user_story'] in us:
		extra = i['assigned_to_extra_info']
		print(i['subject'] + " is assigned to: " + extra['full_name_display'])
		print("User Task Created:" + i['created_date'] )
		task_per_user.append(extra['full_name_display'])

user_unique = []

for i in task_per_user:
	if i not in user_unique:
		user_unique.append(i)


for i in user_unique:
	print "User " + i + " has " + str(task_per_user.count(i)) + " tasks."

rget = requests.get("http://api.taiga.io/api/v1/userstories/project=" + str(project_id), headers=headers, data = json.dumps(data))
rdata = json.loads(rget.content)

print rdata



