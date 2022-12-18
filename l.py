import os
# import library that allows executing commands on the operating system from within python
from bib.command import systemCommand

lst = os.popen('ps a | grep odl-v1.py | grep -v color').read()
lst = lst.split()
print(lst)
print(lst[0])
command = 'kill -9 ' + str(lst[0])
systemCommand(command)
command = 'python odl-v1.py &'
systemCommand(command)

