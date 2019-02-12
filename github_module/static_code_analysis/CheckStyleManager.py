# Class to manage interaction with third-party static analyzer
# CheckStyle.
#
# Author: Sarthak Tiwari
# EMail: sarthak.tiwari@asu.edu

import subprocess

command = ['java', '-jar', 'checkstyle-8.17-all.jar', '-c',
           './custom_checks.xml', './DummyTestFiles/Frame_81.java']
output = subprocess.run(command, capture_output=True, universal_newlines=True).stdout

for line in output.split('\n'):

    if(line[1:6] == "ERROR"):
        complexityParameter = line[line[8:].find('[')+9:line[8:].find(']')+8]
        complexityMeasure = line[line.find(' is ')+4:line.find(' (max allowed is')]
        print(complexityParameter + ": " + complexityMeasure)