import xml.etree.ElementTree as xml

filename = "/home/chiranjeevi_ram/Documents/SER574/SER-574_RedTeam/documentation/template.xml"

def createXMLTemplate(location):

    filename = location
    root = xml.Element("mom")
    date = xml.Element("date")
    attendees = xml.Element("attendees")
    agenda = xml.Element("agenda")
    root.append(date)
    root.append(attendees)
    root.append(agenda)

    data = xml.tostring(root)
    template = open(filename, "w")
    template.write(data.decode("utf-8"))

createXMLTemplate(filename)
