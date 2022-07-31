import os
#print(os.getcwd())

import subprocess
numProcesses = 9
index = 0
processes = []

print('--- opening processes')
for index in range(0,numProcesses):
    cmd = 'python data_organization.py {0} {1}'.format(numProcesses, index)
    print('------ {0}'.format(cmd))
    processes.append(subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE))

print('--- processes running')