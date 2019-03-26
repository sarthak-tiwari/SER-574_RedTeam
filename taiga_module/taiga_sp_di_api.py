#!/usr/bin/env python3

import requests
from flask import Flask, jsonify, request

import task_of_userstory
import taskassignedto
import user_story
import user_task_information
import userstory_create_date
import wikiTextParser
import listWikiContent

app = Flask(__name__)
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


@app.route('/taiga/sprint_story_points', methods=['GET'])
def storyPoints():
    slug = request.args.get('slug')

    return jsonify({'story': processStoryPoints(slug)})


@app.route('/taiga/sprint_date', methods=['GET'])
def dateInformation():
    slug = request.args.get('slug')
    return jsonify({'date_info': processDate(slug)})


@app.route('/taiga/wikiPage', methods=['GET'])
def wikiInformation():
    projectSlug = request.args.get('projectslug')
    wikiSlug = request.args.get('wiki')
    return jsonify({'wikiContents': wikiTextParser.wikiTextParser(projectSlug,wikiSlug)})


@app.route('/taiga/user_task', methods=['GET'])
def taskInformation():
    projectSlug = request.args.get('projectslug')
    return jsonify({'role': user_story.project_info_byslug(projectSlug)})


@app.route('/taiga/userTaskInfo', methods=['GET'])
def usertaskInformation():
    projectSlug = request.args.get('projectslug')
    return jsonify({'userTaskInfo': user_task_information.user_task_info(projectSlug)})


@app.route('/taiga/userStoryCreateDate', methods=['GET'])
def userStoryCreateDateInfo():
    projectSlug = request.args.get('projectslug')
    sprintno = request.args.get('sprint')
    return jsonify({'USERSTORY': userstory_create_date.get_userstory_createdate(projectSlug, sprintno)})


@app.route('/taiga/taskAssignedTo', methods=['GET'])
def taskAssignedToInfo():
    projectSlug = request.args.get('projectslug')
    return jsonify({'TASK': taskassignedto.get_task_assignedto(projectSlug)})


@app.route('/taiga/task_of_userstory', methods=['GET'])
def taskOfUserStory():
    projectSlug = request.args.get('projectslug')
    userStoryId = request.args.get('userstory_id')
    return jsonify({'TASK': task_of_userstory.get_task_of_userstory(projectSlug, userStoryId)})


@app.route('/taiga/listwikipages', methods=['GET'])
def listWikiPages():
    projectSlug = request.args.get('projectslug')
    return jsonify({'wikiPages': listWikiContent.getWiki(projectSlug)})


if __name__ == '__main__':
    app.run(debug=True)
