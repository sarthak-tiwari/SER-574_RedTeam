import requests

header = {'Content-Type': 'application/json'}
http = "https://api.taiga.io/api/v1"


'''
@Description - The method returns the response for /sprint_story_points. It provides the
story points details of the sprint to check the total points that has been closed
@Parameters - The project slug name
'''
def processStoryPoints(slug):

    # Requests project details to get the project ID
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    storyPoints = list()

    # Requests that particular projects sprint details
    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    # Iterate through the response to return the sprint story point details.
    for sprint in milestone:
        rsp_dict = {
                    'name': sprint['name'],
                    'total_points': sprint['total_points'],
                    'closed_points': sprint['closed_points']
                    }
        storyPoints += [rsp_dict]

    return storyPoints

'''
@Description - The method returns the response for /sprint_date. It provides the date information of
the project, to check if the user story is completed before the end of the sprint
@Parameters - The project slug name
'''
def processDate(slug):

    # Requests project details to get the project ID
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    us_date = list()

    # Requests that particular projects sprint details
    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    # Iterate through the response to parse the date information.
    for sprint in milestone:
        rsp_dict = {
                    'name': sprint['name'],
                    'user_story': [],
                    'sprint_start': sprint['estimated_start'],
                    'sprint_end': sprint['estimated_finish']

                    }

        # Consolidating all the user story date information within this particular sprint.
        for us in sprint['user_stories']:

            us_dict ={
                'description': us['subject'],
                'created_date': us['created_date'].split('T')[0],
                'finish_date': us['finish_date'].split('T')[0]
            }
            rsp_dict['user_story'] += [us_dict]

        us_date += [rsp_dict]

    return us_date


'''
@Description - The method returns the response for /initial_task. It provides the number of initial tasks
that has been created for user story in a sprint. It helps to check if the tasks were created on the fly
thus not following the agile process.
@Parameters - The project slug name
'''
def processTaskCreation(slug):

    # Requests project details to get the project ID
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    taskCreate = list()

    # Requests that particular projects sprint details
    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    # Iterate through the response to parse the Tasks details.
    for sprint in milestone:
        rsp_dict = {'name': sprint['name']}
        sprint_start = sprint["created_date"].split("T")[0]
        user = []

        # Fetching the task details of each user story within the sprint.
        for us in sprint['user_stories']:
            usId = str(us['id'])
            task_rsp = requests.get(http + "/tasks?user_story="+usId, headers=header)
            task = task_rsp.json()
            task_count = 0

            # Counting the number of tasks created on the first date of the sprint.
            for ts in task:
                if ts['created_date'].split("T")[0] <= sprint_start:
                    task_count += 1

            user += [{"Description": us["subject"],
                    "Initial_task": task_count}]
        rsp_dict['user_stories'] = user
        taskCreate += [rsp_dict]

    return taskCreate

'''
@Description - The method returns the response for /sprint_user_story. It provides the total number of user
stories and the ones that are closed among them.
@Parameters - The project slug name
'''
def processSprintUserStory(slug):

    # Requests project details to get the project ID
    project_response = requests.get(http + "/projects/by_slug?slug="+str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    sprintUserStory = list()

    # Requests that particular projects sprint details
    milestone_rsp = requests.get(http + "/milestones?project="+prjId, headers=header)
    milestone = milestone_rsp.json()

    # Iterate through the response to parse the open user story details.
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


'''
@Description - The method returns the response for /user_task_details. It provides the sprint, user stories and
task description and reference number. The endpoint is used by the gitHub team for further analysis.
@Parameters - The project slug name
'''
def processUserAndTaskDetails(slug):

    # Requests project details to get the project ID
    project_response = requests.get(http + "/projects/by_slug?slug=" + str(slug), headers=header)
    project = project_response.json()
    prjId = str(project['id'])
    taskCreate = list()

    # Requests that particular projects sprint details
    milestone_rsp = requests.get(http + "/milestones?project=" + prjId, headers=header)
    milestone = milestone_rsp.json()

    # Iterate through the response to parse the open user story details.
    for sprint in milestone:
        rsp_dict = {'name': sprint['name']}
        user = []

        # Fetching the task details of each user story within the sprint.
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