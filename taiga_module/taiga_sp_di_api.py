#!/usr/bin/env python3

from flask import Flask, jsonify, request
import requests
import XMLParser

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
    return jsonify({'wikiContents': XMLParser.XMLParser(projectSlug,wikiSlug)})

if __name__ == '__main__':
    app.run(debug=True)
