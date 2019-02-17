#!/usr/bin/env python3

from flask import Flask, jsonify
import requests

app = Flask(__name__)
header = {'Content-Type': 'application/json'}
http = "https://api.taiga.io/api/v1"

'''tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]'''

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


@app.route('/taiga/sprint_story_points', methods=['GET'])
def storyPoints():

    return jsonify({'story': processStoryPoints('sarthak-tiwari-ser-574_redteam_team-taiga')})

if __name__ == '__main__':
    app.run(debug=True)
