#!/usr/bin/python
# coding: utf-8
import os
# library needed to receive arguments
import sys
# library required for running OS commands

# import library that allows executing commands on the operating system from within python
from bib.command import systemCommand


# library needed to execute the sleep function
from time import sleep

# library needed to execute the sleep function
from bib.aux.correio import envia_mail

from datetime import datetime

def main():
    lst = []
    flag=True
    
    ##### state file creation block ############
    # if state files are deleted this block will create new state files.
    command = 'echo 1 > ./swap/a1.txt'
    systemCommand(command)
    command = 'echo 1 > ./swap/a2.txt'
    systemCommand(command)
    command = 'echo 1 > ./swap/a3.txt'
    systemCommand(command)
    command = 'echo 1 > ./swap/a4.txt'
    systemCommand(command)
    command = 'echo 1 > ./swap/b1.txt'
    systemCommand(command)
    sleep(1)
    ##########################################################
    
    
    while flag:
        a1 = open('./swap/a1.txt', 'r')
        for line in a1:
            a1_valor = int(line.split()[0])
        a1.close()
        
        a2 = open('./swap/a2.txt', 'r')
        for line in a2:
            a2_valor = int(line.split()[0])
        a2.close()
            
        a3 = open('./swap/a3.txt', 'r')
        for line in a3:
            a3_valor = int(line.split()[0])
        a3.close()
            
        a4 = open('./swap/a4.txt', 'r')
        for line in a4:
            a4_valor = int(line.split()[0])
        a4.close()
        
        iperf = 1
        lst = os.popen('ps -aux | grep -v color |  grep iperf\ -c | grep root').read()
        if (lst):
            lst = lst.split()
            if (lst[0] == 'root'):
                iperf = 0
        
        
            
        # for 4 streams
        if (a1_valor == 1 and a2_valor == 1 and a3_valor == 1 and a4_valor == 1 and iperf == 1):
        # for 2 streams
        #if (a1_valor == 1 and a2_valor == 1):
            #print('dentro')
            #lst = os.popen('ps a | grep odl-v1.py | grep -v color').read()
            #lst = lst.split()
            #print(lst)
            #print(lst[0])
            #command = 'kill -9 ' + str(lst[0])
            #systemCommand(command)
            #print('a')
            #command = './2-delete.sh'
            #systemCommand(command)
            #print('b')
            #command = 'python odl-v1.py &'
            #systemCommand(command)
            #print('c')
            sleep(20)
            command = 'echo 0 > ./swap/a1.txt'
            systemCommand(command)
            command = 'echo 0 > ./swap/a2.txt'
            systemCommand(command)
            command = 'echo 0 > ./swap/a3.txt'
            systemCommand(command)
            command = 'echo 0 > ./swap/a4.txt'
            systemCommand(command)
        
        b1 = open('./swap/b1.txt', 'r')
        for line in b1:
            b1_valor = int(line.split()[0])
        b1.close()
        if (b1_valor == 2):
            print("\n {} - {} \n" .format(envia_mail(),datetime.now()))
            command = 'echo 0 > ./swap/b1.txt'
            systemCommand(command)


if __name__ == '__main__':
    try:
        main()
    except(KeyboardInterrupt):
        print('\n Interrupção manual provocada pelo usuário, Ctrl + c. \n')
