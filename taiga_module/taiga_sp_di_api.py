#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS

from taiga_module import US_Group1
from taiga_module import ut_History_Info
from taiga_module import findSprintGaps
from taiga_module import listWikiContent
from taiga_module import list_sprints
from taiga_module import list_userstories
from taiga_module import sprintplanningAnalysis
from taiga_module import taskAssignedTo_modified
from taiga_module import task_finishdate
from taiga_module import task_of_userstory
from taiga_module import taskassignedto
from taiga_module import user_story
from taiga_module import user_task_information
from taiga_module import userstory_create_date
from taiga_module import wikiTextParser

from taiga_module import sprintplanningAnalysis
from taiga_module import ut_History_Info, taskAssignedTo_modified
from taiga_module import teammemberinfo
from taiga_module import UserTask_change_status


app = Flask(__name__)
CORS(app)


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


@app.route('/taiga/user_task_details', methods=['GET'])
def sprintUserTaskDetails():
    slug = request.args.get('slug')
    return jsonify({'sprint_user_task_details': US_Group1.processUserAndTaskDetails(slug)})


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

  
@app.route('/taiga/list_of_sprints', methods=['GET'])
def listOfSprints():
    projectSlug = request.args.get('projectslug')
    return jsonify({'SPRINTS': list_sprints.get_list_sprints(projectSlug)})


@app.route('/taiga/list_of_userstories', methods=['GET'])
def listOfUserstories():
    projectSlug = request.args.get('projectslug')
    sprintno = request.args.get('sprint')
    return jsonify({'USERSTORY': list_userstories.get_list_userstories(projectSlug, sprintno)})


@app.route('/taiga/taskFinishdate', methods=['GET'])
def taskFinishdate():
    projectSlug = request.args.get('projectslug')
    userStoryId = request.args.get('userstory_id')
    return jsonify({'TASK': task_finishdate.get_task_finishdate(projectSlug, userStoryId)})
	
@app.route('/taiga/taskAssignedTo_modified', methods=['GET'])
def assignedToModified():
    projectSlug = request.args.get('projectslug')
    sprintno = request.args.get('sprint')
    return jsonify({'assignedToModified': taskAssignedTo_modified.get_modifiedTaskAssignedTo(projectSlug, sprintno)})

@app.route('/taiga/historyOfTasks', methods=['GET'])
def historyOfTasks():
    projectSlug = request.args.get('projectslug')
    sprintno = request.args.get('sprint')
    return jsonify({'historyOfTasks':ut_History_Info.user_task_info(projectSlug, sprintno)})


@app.route('/taiga/listSprintDetails', methods=['GET'])
def listSprintDetails():
    projectSlug = request.args.get('projectslug')
    return jsonify({'sprintDetails': findSprintGaps.findSprintGaps(projectSlug)})


@app.route('/taiga/planning-retrospective-analysis', methods=['GET'])
def plan_retro_details():
    projectSlug = request.args.get('projectslug')
    wiki_slug = request.args.get('wikislug')
    return jsonify({'project_details': sprintplanningAnalysis.sprint_planning(projectSlug,wiki_slug)})

@app.route('/taiga/teammemberinfo', methods=['GET'])
def teammemberinfo():
    projectSlug = request.args.get('projectslug')
    return jsonify({'TeamMemberInfo': teammemberinfo.members_info(projectSlug)})

@app.route('/taiga/memberuserstorypointsinfo', methods=['GET'])
def memberuserstorypointsinfo():
    projectSlug = request.args.get('projectslug')
    return jsonify({'TeamMemberInfo': teammemberinfo.user_story_points_info(projectSlug)})

@app.route('/taiga/UserTaskchangestatus', methods=['GET'])
def UserTaskchangestatus():
    projectSlug = request.args.get('projectslug')
    sprintno = request.args.get('sprint')
    return jsonify({'historyOfTasks':UserTask_change_status.UserTaskchangestatus(projectSlug, sprintno)})


if __name__ == '__main__':
    app.run(debug=True)

