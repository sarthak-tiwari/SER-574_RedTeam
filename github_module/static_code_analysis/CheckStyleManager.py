# Class to manage interaction with third-party static analyzer
# CheckStyle.
#
# Author: Sarthak Tiwari
# E-Mail: sarthak.tiwari@asu.edu

import subprocess

class CheckStyleManager:

    @staticmethod
    def getStaticComplexityMetrices():

        command = ['java', '-jar', 'checkstyle-8.17-all.jar', '-c',
                   './custom_checks.xml', './DummyTestFiles/Frame_81.java']
        output = subprocess.run(command, capture_output=True, universal_newlines=True).stdout

        metrics = {'BooleanExpressionComplexity':0, 'ClassFanOutComplexity':0, 'CyclomaticComplexity':0,
                   'JavaNCSS':0, 'NPathComplexity':0, 'ClassDataAbstractionCoupling':0}

        for line in output.split('\n'):

            if(line[1:6] == "ERROR"):
                complexityParameter = line[line.rfind('[')+1:line.rfind(']')]
                complexityMeasure = line[line.find(' is ')+4:line.find(' (max allowed is')]
        
                metrics[complexityParameter] = max(metrics[complexityParameter], int(complexityMeasure))

        return metrics

metrics = CheckStyleManager.getStaticComplexityMetrices()
print(metrics)