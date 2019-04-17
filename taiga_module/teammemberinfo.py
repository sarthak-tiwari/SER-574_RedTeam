import requests
import json

headers = {
    'Content-Type': 'application/json',
}
slug1 = "sarthak-tiwari-ser-574_redteam_team-taiga"


def members_info(slug1):
    projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
    response_project_data = requests.get(projectinfo + slug1, headers=headers)
    project_data = json.loads(response_project_data.content)

    dic = {}
    lst = []
    for pdata in project_data['members']:
        dic['full_name_display'] = pdata['full_name_display']
        dic['id'] = pdata['id']
        dic['role_name'] = pdata['role_name']
        dic['username'] = pdata['username']
        lst.append(dic)
        dic = {}

    dic = {}
    for i in range(len(lst)):
        dic['User_details ' + str(i + 1)] = lst[i]

    return dic


def user_story_points_info(slug1, sprint_no):
    projectinfo = "https://api.taiga.io/api/v1/projects/by_slug?slug="
    response_project_data = requests.get(projectinfo + slug1, headers=headers)
    project_data = json.loads(response_project_data.content)
    project_id = project_data['epic_statuses'][0]['project_id']
    projec_milestone = "https://api.taiga.io/api/v1/milestones?project=" + str(project_id)
    response_milestone = requests.get(projec_milestone, headers=headers)
    milestone_data = json.loads(response_milestone.content)
    dic = {}
    lst = []
    sprint_data = milestone_data[sprint_no]
    us = []
    for i in sprint_data['user_stories']:
        us.append(i['id'])
        dic['US_name'] = i['subject']
        dic['US_points'] = i['total_points']
        response_usid = requests.get("https://api.taiga.io/api/v1/history/userstory/" + str(i['id']), headers=headers)
        us_data = json.loads(response_usid.content)
        lst.append(dic)
        dic = {}

    dic = {}
    for i in range(len(lst)):
        dic['US ' + str(i + 1)] = lst[i]
        
    return dic
