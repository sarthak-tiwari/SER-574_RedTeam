from datetime import date
from taiga_module import wikiTextParser
import re


def sprint_planning(project_slug, wiki_slug):
    wiki_content = wikiTextParser.wikiTextParser(project_slug, wiki_slug)
    planning_analysis = []
    retrospective_analysis = []
    analysis = {}
    meeting_data = {}
    for i in range(1, len(wiki_content)+1):
        meeting_data = wiki_content["MoM-"+str(i)]

        meeting_description = meeting_data["Description"]

        if re.search("Planning", meeting_description[0], re.IGNORECASE):
            planning_analysis.append(meeting_data["Date"])
        if re.search("Retrospective", meeting_description[0], re.IGNORECASE):
            retrospective_analysis.append(meeting_data["Date"])

    analysis["sprint_plan_dates"] = planning_analysis
    analysis["sprint_retrospective_dates"] = retrospective_analysis

    return analysis


def diff_between_two_dates(from_date,to_date):

    from_month = int(from_date[0:10].split("-")[1])
    from_year = int(from_date[0:10].split("-")[0])
    from_day = int(from_date[0:10].split("-")[2])
    to_month = int(to_date[0:10].split("-")[1])
    to_year = int(to_date[0:10].split("-")[0])
    to_day = int(to_date[0:10].split("-")[2])

    start_date = date(from_year, from_month, from_day)
    end_date = date(to_year, to_month, to_day)

    delta = start_date - end_date

    return delta.days
