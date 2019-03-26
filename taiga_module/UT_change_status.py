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
  return utChangeDate

print (user_task_info("sarthak-tiwari-ser-574_redteam_team-taiga",2))
