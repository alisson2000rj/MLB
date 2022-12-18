#!/usr/bin/python
# coding: utf-8
'''
exemplo:
command = 'ls -l'
systemCommand(command)

'''

# library required for running OS commands
from subprocess import Popen, PIPE

def systemCommand(cmd):
    terminalProcess = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    terminalOutput, stderr = terminalProcess.communicate()
