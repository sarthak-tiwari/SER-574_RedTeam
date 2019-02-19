import xmltodict
import taigaWiki
import json


def XMLParser(ProjectSlug, WikiSlug):
    wikiContent = taigaWiki.getWiki(ProjectSlug, WikiSlug)
    xmlParser = xmltodict.parse(wikiContent)
    return json.dumps(xmlParser)
