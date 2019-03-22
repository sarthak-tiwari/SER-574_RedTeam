import requests

#@author Chiranjeevi Ramamurthy
#@description A module that downloads the contents from taiga wikipage

projectSlug = "cram1206-test"
header = {'Content-Type': 'application/json'}
projectHTTP = "https://api.taiga.io/api/v1/projects/by_slug?slug="
wikiHTTP = "https://api.taiga.io/api/v1/wiki/by_slug?slug="
wikiSlug = "samplewiki"

def getProjectID(projectSlug):
    project_response = requests.get(projectHTTP + projectSlug, headers=header)
    project = project_response.json()
    projectID = project['id']
    return projectID


def getWiki(projectSlug,wikiSlug):
    projectID = getProjectID(projectSlug)
    wikiResponse = requests.get(wikiHTTP+wikiSlug+"&project="+str(projectID), headers=header)
    wiki = wikiResponse.json()
    wikiContent = wiki["html"]
    return wikiContent
    