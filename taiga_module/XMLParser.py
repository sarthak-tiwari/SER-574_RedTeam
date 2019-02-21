import xmltodict
import taigaWiki
import json
#@author Chiranjeevi Ramamurthy
#@description This modules takes XML as input and converts it into Dictionary 

def XMLParser(ProjectSlug, WikiSlug):
    wikiContent = taigaWiki.getWiki(ProjectSlug, WikiSlug)
    xmlParser = xmltodict.parse(wikiContent)
    return xmlParser
