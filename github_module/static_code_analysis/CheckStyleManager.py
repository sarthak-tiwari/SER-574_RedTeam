# Class to manage interaction with third-party static analyzer
# CheckStyle.
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

import subprocess

class CheckStyleManager:

    @staticmethod
    def createFile(fileContent, fileName):

        newFile = open('./TestFile/' + fileName, 'w')
        newFile.write(fileContent)


    @staticmethod
    def getStaticComplexityMetrices(fileName):

        command = ['java', '-jar', 'checkstyle-8.17-all.jar', '-c',
                   './custom_checks.xml', './DummyTestFiles/' + str(fileName)]
        output = subprocess.run(command, capture_output=True,
                                universal_newlines=True).stdout

        metrics = {'BooleanExpressionComplexity':0, 'ClassFanOutComplexity':0,
                   'CyclomaticComplexity':0, 'JavaNCSS':0, 'NPathComplexity':0,
                   'ClassDataAbstractionCoupling':0}

        for line in output.splitlines():

            if(line[1:6] == "ERROR"):
                complexityParameter = line[line.rfind('[')+1:line.rfind(']')]
                complexityMeasure = line[line.find(' is ')+4:
                                         line.find(' (max allowed is')]
        
                metrics[complexityParameter] = max(metrics[complexityParameter]
                                                   , int(complexityMeasure))

        return metrics



    @staticmethod
    def getComplexities(repoName, filenames):

        result = []

        for filename in filenames:
            if(filename[filename.rfind('.')+1:] == 'java'):
                metrics = CheckStyleManager.getStaticComplexityMetrices(filename)
                result.append((filename, metrics))

        return result

    @staticmethod
    def getDummyComplexities(filename):

        metrics = {'BooleanExpressionComplexity':2, 'ClassFanOutComplexity':10,
                   'CyclomaticComplexity':3, 'JavaNCSS':50, 'NPathComplexity':3,
                   'ClassDataAbstractionCoupling':6}

        return metrics

# metrices = CheckStyleManager.getComplexities('abc', ['Frame_81.java', 'Panel_59.java'])
# print(metrices)