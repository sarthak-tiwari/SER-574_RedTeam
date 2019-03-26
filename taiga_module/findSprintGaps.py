import requests

projectHTTP = "https://api.taiga.io/api/v1/projects/by_slug?slug="
header = {'Content-Type': 'application/json'}
milestoneHTTP = 'https://api.taiga.io/api/v1/milestones?project='
projectSlug = "cram1206-personalized-travel-planning-platform"


def findSprintGaps(projectSlug):
    project_response = requests.get(projectHTTP + projectSlug, headers=header)
    project = project_response.json()
    milestones_response = requests.get(milestoneHTTP+str(project['id']), headers=header)
    milestone = milestones_response.json()
    sprint_list = []
    sprint_data = {}
    for data in milestone:
        sprint_data["sprint_name"] = data['slug']
        sprint_data["estimated_start"] = data['estimated_start']
        sprint_data["estimated_finish"] = data['estimated_finish']
        sprint_data["created_date"] = data['created_date']
        sprint_list.append(sprint_data)

    return sprint_list

