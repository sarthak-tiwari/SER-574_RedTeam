import requests


projectSlug = "cram1206-test"
header = {'Content-Type': 'application/json'}
projectHTTP = "https://api.taiga.io/api/v1/projects/by_slug?slug="
wikiHTTP = "https://api.taiga.io/api/v1/wiki"
wikiSlug = "samplewiki"


def getProjectID(projectSlug):
    project_response = requests.get(projectHTTP + projectSlug, headers=header)
    project = project_response.json()
    projectID = project['id']
    return projectID


def getWiki(projectSlug):
    projectID = getProjectID(projectSlug)
    wikiResponse = requests.get(wikiHTTP+"?project="+str(projectID), headers=header)
    wiki = wikiResponse.json()
    counter = 1
    wikilist = {}
    for json in wiki:
        wikilist["wikiPage"+str(counter)]=json["slug"]
        counter = counter+1
    return wikilist
