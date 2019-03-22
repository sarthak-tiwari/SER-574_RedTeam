#!/usr/bin/env python3

from flask import Flask, jsonify, request
import requests
import XMLParser, user_story, user_task_information, userstory_create_date, taskassignedto, task_of_userstory, US_Group1

app = Flask(__name__)


@app.route('/taiga/sprint_story_points', methods=['GET'])
def storyPoints():
    slug = request.args.get('slug')

    return jsonify({'story': US_Group1.processStoryPoints(slug)})


@app.route('/taiga/sprint_date', methods=['GET'])
def dateInformation():
    slug = request.args.get('slug')
    return jsonify({'date_info': US_Group1.processDate(slug)})


@app.route('/taiga/initial_task', methods=['GET'])
def initialTaskInformation():
    slug = request.args.get('slug')
    return jsonify({'task_info': US_Group1.processTaskCreation(slug)})


@app.route('/taiga/sprint_user_story', methods=['GET'])
def sprintUserStoryInformation():
    slug = request.args.get('slug')
    return jsonify({'sprint_user_story_info': US_Group1.processSprintUserStory(slug)})


@app.route('/taiga/wikiPage', methods=['GET'])
def wikiInformation():
    projectSlug = request.args.get('projectslug')
    wikiSlug = request.args.get('wiki')
    return jsonify({'wikiContents': XMLParser.XMLParser(projectSlug,wikiSlug)})


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


if __name__ == '__main__':
    app.run(debug=True)

