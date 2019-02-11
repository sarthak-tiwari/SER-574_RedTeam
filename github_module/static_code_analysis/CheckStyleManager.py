import subprocess

p1 = subprocess.run(['java', '-jar', 'checkstyle-8.17-all.jar', '-c', './custom_checks.xml', './DummyTestFiles/Frame_81.java'],
                    capture_output=True, universal_newlines=True)

output = p1.stdout
i = 0
for line in output.split('\n'):
    print(str(i) + ":\t " + line)
    i += 1