import xml.etree.ElementTree as ET
XMLFileLocation = "/home/chiranjeevi_ram/Documents/SER574/SER-574_RedTeam/documentation/sampleXML.xml"
def XMLParser(XMLFileLocation):
    tree = ET.parse(XMLFileLocation)
    root = tree.getroot()
    for elem in root:
        print(elem.text)

XMLParser(XMLFileLocation)