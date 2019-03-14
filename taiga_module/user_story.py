import requests
import json

headers = {'Content-Type': 'application/json'}
project = {"project_id":  ""}


def project_info_byslug(project_slug):
    print("In")
    print(project_slug)
    response_project_data = requests.get("https://api.taiga.io/api/v1/projects/by_slug?slug="+str(project_slug),
                                         headers=headers)
    project_data = response_project_data.json()

    project["project_id"] = project_data['epic_statuses'][0]['project_id']
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

    return json.dumps(dic)

#print(project_info_byslug("svanter1-virat"))
