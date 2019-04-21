# Class to manage interaction with third-party static analyzer
# CheckStyle.
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

import subprocess
import http
import requests
import os
from pathlib import Path


class CheckStyleManager:

    # Fetches file from GitHub and create a copy of it in local folder for analysis
    @staticmethod
    def fetchAndCreateFile(fileLink):

        fileName = fileLink[fileLink.rfind('/')+1:]
        fileContent = requests.get(fileLink).text
        with open(str(Path(__file__).parent.resolve()) + '/TestFile/' + fileName, 'w+') as newFile:
            newFile.write(fileContent)

    # method to calculate complexity of the file specified once fetched
    @staticmethod
    def getStaticComplexityMetrices(fileName):

        path = str(Path(__file__).parent.resolve())

        command = ['java', '-jar', path + '/checkstyle-8.17-all.jar', '-c',
                   path + '/custom_checks.xml', path + '/TestFile/' + str(fileName)]
        output = subprocess.run(command, capture_output=True,
                                universal_newlines=True).stdout

        metrics = {'BooleanExpressionComplexity': 0, 'ClassFanOutComplexity': 0,
                   'CyclomaticComplexity': 0, 'JavaNCSS': 0, 'NPathComplexity': 0,
                   'ClassDataAbstractionCoupling': 0}

        for line in output.splitlines():

            if(line[1:6] == "ERROR"):
                complexityParameter = line[line.rfind('[')+1:line.rfind(']')]
                complexityMeasure = line[line.find(' is ')+4:
                                         line.find(' (max allowed is')]

                metrics[complexityParameter] = max(
                    metrics[complexityParameter], int(complexityMeasure))

        return metrics

    # Method to calculate the count of java format warnings generated for that file
    @staticmethod
    def getJavaWarningCount(fileName):

        path = str(Path(__file__).parent.resolve())

        command = ['java', '-jar', path + '/checkstyle-8.17-all.jar', '-c',
                   path + '/sun_checks.xml', path + '/TestFile/' + str(fileName)]
        output = subprocess.run(command, capture_output=True,
                                universal_newlines=True).stdout

        countLine = output.splitlines()[len(output.splitlines())-1]
        count = countLine[countLine.find('with ')+5:countLine.find(' error')]

        return count

    # Driver method which syncs all the other methods
    @staticmethod
    def getComplexity(fileLink):

        path = str(Path(__file__).parent.resolve())

        fileName = fileLink[fileLink.rfind('/')+1:]

        CheckStyleManager.fetchAndCreateFile(fileLink)

        metrics = CheckStyleManager.getStaticComplexityMetrices(fileName)
        metrics['JavaWarnings'] = CheckStyleManager.getJavaWarningCount(
            fileName)

        os.remove(path + '/TestFile/' + fileName)

        return metrics

    # Method that returns the baseline values for all the metrices
    @staticmethod
    def getBaselineForComplexities():

        metrics = {'booleanExpressionComplexity': 3, 'classFanOutComplexity': 20,
                   'cyclomaticComplexity': 10, 'javaNCSS': 50, 'nPathComplexity': 200,
                   'classDataAbstractionCoupling': 7}

        return metrics
