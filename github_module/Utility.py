from datetime import datetime
import datetime
import http
import json
import requests
import Constants

""" This file implements functions serving as helper functions """
__author__ = 'Sarthak Tiwari'


def fetchDataFromTaigaAPI(taigaSlug):

    result = []

    jsonData = requests.get(Constants.BASE_API_URL+ '/taiga/user_task_details?slug=' + taigaSlug).json().get('sprint_user_task_details')

    for sprint in jsonData:
        for userStory in sprint.get('user_stories'):

            userStoryDetail = {}
            userStoryDetail['number'] = userStory.get('Ref_Num')
            userStoryDetail['subject'] = userStory.get('Description')
            userStoryDetail['start_date'] = datetime.datetime.strptime(userStory.get('Create_Date'), '%Y-%m-%d').strftime('%Y%m%d')
            if (userStory.get('Complete_Date') is None):
                userStoryDetail['end_date'] = None
            else:
                userStoryDetail['end_date'] = datetime.datetime.strptime(userStory.get('Complete_Date'), '%Y-%m-%d').strftime('%Y%m%d')
            userStoryDetail['commit_count'] = 0
            userStoryDetail['first_commit_date'] = 0
            userStoryDetail['last_commit_date'] = 0
            userStoryDetail['late_start_days'] = 0
            userStoryDetail['early_start_days'] = 0
            userStoryDetail['early_finish_days'] = 0
            userStoryDetail['late_finish_days'] = 0
            
            taskNumbers = []
            for task in userStory.get('Tasks'):
                taskNumbers.append(task.get('Ref_Num'))

            userStoryDetail['taskNumbers'] = taskNumbers

            result.append(userStoryDetail)
    
    return result
