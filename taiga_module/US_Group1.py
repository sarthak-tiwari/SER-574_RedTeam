from flask import Flask, jsonify, request
import requests

header = {'Content-Type': 'application/json'}
http = "https://api.taiga.io/api/v1"


def processStoryPoints(slug):
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    storyPoints = list()

    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    for sprint in milestone:
        rsp_dict = {
                    'name': sprint['name'],
                    'total_points': sprint['total_points'],
                    'closed_points': sprint['closed_points']
                    }
        storyPoints += [rsp_dict]

    return storyPoints


def processDate(slug):
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    us_date = list()

    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    for sprint in milestone:
        rsp_dict = {
                    'name': sprint['name'],
                    'user_story': [],
                    'sprint_start': sprint['estimated_start'],
                    'sprint_end': sprint['estimated_finish']

                    }
        for us in sprint['user_stories']:

            us_dict ={
                'description': us['subject'],
                'created_date': us['created_date'].split('T')[0],
                'finish_date': us['finish_date'].split('T')[0]
            }
            rsp_dict['user_story'] += [us_dict]

        us_date += [rsp_dict]

    return us_date


def processTaskCreation(slug):
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    taskCreate = list()

    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    for sprint in milestone:
        rsp_dict = {'name': sprint['name']}
        sprint_start = sprint["created_date"].split("T")[0]
        user = []

        for us in sprint['user_stories']:
            usId = str(us['id'])
            task_rsp = requests.get(http + "/tasks?user_story="+usId, headers=header)
            task = task_rsp.json()
            task_count = 0
            for ts in task:
                if ts['created_date'].split("T")[0] <= sprint_start:
                    task_count += 1

            '''user["user_story"+str(cnt)] = {"Description": us["subject"],
                                           "Initial_task":  task_count}
            cnt += 1'''

            user += [{"Description": us["subject"],
                    "Initial_task": task_count}]
        rsp_dict['user_stories'] = user
        taskCreate += [rsp_dict]

    return taskCreate


def processSprintUserStory(slug):
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    sprintUserStory = list()

    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    for sprint in milestone:
        totalUS = 0
        openUS = 0
        closeUS = 0
        rsp_dict = {
                    'name': sprint['name']
                    }
        for us in sprint['user_stories']:
            totalUS += 1
            if us['finish_date'] is None:
                openUS += 1
            else:
                if sprint['estimated_finish'] >= us['finish_date'].split("T")[0]:
                    closeUS += 1
                else:
                    openUS += 1

        rsp_dict['no_of_user_stories'] = totalUS
        rsp_dict['open_user_stories'] = openUS
        rsp_dict['closed_user_stories'] = closeUS
        sprintUserStory += [rsp_dict]

    return sprintUserStory


def processUserAndTaskDetails(slug):
    project_response = requests.get(http + "/projects/by_slug?slug=" + str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    taskCreate = list()

    milestone_rsp = requests.get(http + "/milestones?project=" + prjId, headers=header)
    milestone = milestone_rsp.json()

    for sprint in milestone:
        rsp_dict = {'name': sprint['name']}
        user = []

        for us in sprint['user_stories']:
            usId = str(us['id'])
            task_rsp = requests.get(http + "/tasks?user_story=" + usId, headers=header)
            task = task_rsp.json()

            tempUser = {"Description": us["subject"],
                      "Ref_Num": us["ref"],
                      "Create_Date": us["created_date"].split("T")[0],
                      "Complete_Date": None,
                      "Tasks": None}

            if us["finish_date"]:
                tempUser["Complete_Date"] = us["finish_date"].split("T")[0]

            tasks = []
            for ts in task:
                tempTask = {"Description": ts["subject"],
                          "Ref_Num": ts["ref"],
                          "Create_Date": ts["created_date"].split("T")[0],
                          "Complete_Date": None,
                }

                if ts["finished_date"]:
                    tempTask["Complete_Date"] = ts["finished_date"].split("T")[0]

                tasks += [tempTask]

            tempUser["Tasks"] = tasks
            user += [tempUser]
        rsp_dict['user_stories'] = user
        taskCreate += [rsp_dict]

    return taskCreate