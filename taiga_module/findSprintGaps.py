import requests
from datetime import date

projectHTTP = "https://api.taiga.io/api/v1/projects/by_slug?slug="
header = {'Content-Type': 'application/json'}
milestoneHTTP = 'https://api.taiga.io/api/v1/milestones?project='


def findSprintGaps(projectSlug):
    project_response = requests.get(projectHTTP + projectSlug, headers=header)
    project = project_response.json()
    milestones_response = requests.get(milestoneHTTP+str(project['id']), headers=header)
    milestone = milestones_response.json()
    sprint_list = []
    sprint_data = {}
    sprint_analysis = {}
    for data in milestone:
        sprint_data["sprint_name"] = data['slug']
        sprint_data["estimated_start"] = data['estimated_start']
        sprint_data["estimated_finish"] = data['estimated_finish']
        sprint_data["created_date"] = data['created_date']
        sprint_data["status"] = ""
        sprint_data["gap"] = ""
        sprint_list.append(sprint_data)
        sprint_data = {}

    for sprintdetail in sprint_list:
        splitdata = sprintdetail.get("created_date")[0:10].split("-")
        createdyear = int(splitdata[0])
        createdmonth = int(splitdata[1])
        createdday = int(splitdata[2])
        splitdata = sprintdetail.get("estimated_start")[0:10].split("-")
        estimatedyear = int(splitdata[0])
        estimatedmonth = int(splitdata[1])
        estimatedday = int(splitdata[2])

        created_date = date(createdyear, createdmonth, createdday)
        estimated_date = date(estimatedyear, estimatedmonth, estimatedday)

        difference = created_date-estimated_date
        if difference.days <= 0:
            status = {"status": "on-time"}
            gap = {"gap": str(difference.days)}
            sprintdetail.update(status)
            sprintdetail.update(gap)

        else:
            status = {"status": "delayed"}
            gap = {"gap": str(difference.days)}
            sprintdetail.update(status)
            sprintdetail.update(gap)

    return sprint_list
