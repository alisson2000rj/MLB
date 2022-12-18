#!/usr/bin/python
# coding: utf-8
'''
Example of use:
1 - xterm h1 h4
2 - h4: iperf -s -f bits > ./resultado/s4f1.txt
3 - h1: python 3-iperf.py <source-node> <destination-IP> <stream-id/port> 

'''
# library needed to receive arguments
import sys
# library required for running OS commands

# import library that allows execution of OS command
from bib.command import systemCommand

# library needed to execute the sleep function
from time import sleep

import time

from datetime import datetime

def iperf(p1, p2, p3, p4):
    now = datetime.now()
    command = 'echo Inicio: ' + str(now.hour)+ ':' + str(now.minute) + ':' + str(now.second) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 't.txt'
    systemCommand(command)
    
    # number of rounds or series of samples. Eg: 10 rounds of 50 samples
    rodadas = 30
    #rodadas = 3
    
    
    # running time of each round of iperf
    # can be understood as number of samples
    t = 600
    #t = 5
    
    
    # bandwidth configuration when dealing with udp traffic   
    # 450 Mbps
    #b = 450000000 
    # 9,6 Mbps
    b = 9500000
    # delete file with old data
    command = 'rm -rf ./resultado/' + str(p1) + 'p' + str(p3) + '.txt'
    systemCommand(command)
    if (p3 == '4'):
        pass
    elif (p3 == '1'):
        pass
        #sleep(5)
    elif (p3 == '2'):
        pass
        #sleep(10)
    elif (p3 == '3'):
        pass
        #sleep(15)
    
    
    #device created to allow the flows to start together at each round. The device imposes a pause between rounds, waiting for all streams to finish being transmitted before starting a new round. Auxiliary variables "ax" start with value "1", which allows flows to be triggered. Whenever the transmission of a stream is finished "ax" changes its value to "0" and remains like that until all the control variables "ax" receive the value "0". After the end of the transmission of all flows, all control variables valued with "0" automatically received the value "1", which allowed the beginning of a new round.
    for i in range(rodadas):
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
        
        # after the end of a round, each process interrupts the firing of a new flow waiting for all the processes to finish too and signal that they are able to start a new round simultaneously.
        while (a1_valor == 1 or a2_valor == 1 or a3_valor == 1 or a4_valor == 1):
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
            sleep(1)
            
        
        if (p4 == 'tcp'):
            #print("iperf rodada: {}" .format(i+1))
            command = 'iperf -c ' + str(p2) + ' -f bits -p 500' + str(p3) + ' -t ' + str(t) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 't.txt'
            systemCommand(command)
            command = 'echo Rodada: ' + str(i) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 't.txt'
            systemCommand(command)
            #sleep(3)
        elif (p4 == 'udp'):
            #print("iperf rodada: {}" .format(i+1))
            command = 'iperf -c ' + str(p2) + ' -f bits -p 500' + str(p3) + ' -u -b ' + str(b) + ' -t ' + str(t) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 'u.txt'
            systemCommand(command)
            command = 'echo Rodada: ' + str(i) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 'u.txt'
            systemCommand(command)
        
        if (p3 == '1'):
            command = 'echo 1 > ./swap/a1.txt'
            systemCommand(command)
            command = 'echo 1 > ./swap/a3.txt'
            systemCommand(command)
        elif (p3 == '2'):
            command = 'echo 1 > ./swap/a2.txt'
            systemCommand(command)
            command = 'echo 1 > ./swap/a4.txt'
            systemCommand(command)
        elif (p3 == '3'):
            command = 'echo 1 > ./swap/a3.txt'
            systemCommand(command)
        elif (p3 == '4'):
            command = 'echo 1 > ./swap/a4.txt'
            systemCommand(command)
        
    now = datetime.now()
    command = 'echo Fim: ' + str(now.hour)+ ':' + str(now.minute) + ':' + str(now.second) + ' >> ./resultado/' + str(p1) + 'f' + str(p3) + 't.txt'
    systemCommand(command)     
    
    # after the end of all rounds, the process responsible for flow 1 sets the value of b1.txt to "2", that is, it signals that the simulation has reached the end and that limp-regras.py can trigger the alarm email .
    if (p3 == '1'):
        command = 'echo 2 > ./swap/b1.txt'
        systemCommand(command)
        
def main():
    # takes four arguments p1, p2, p3 and p4
    try:
        p1 = str(sys.argv[1])
        p2 = str(sys.argv[2])
        p3 = str(sys.argv[3])
        p4 = str(sys.argv[4])
    except IndexError:
        print("sintaxe: python 3-iperf.py <nó origem> <ip destino> <fluxo> <tcp ou udp>")
        exit(1) 
    iperf(p1, p2, p3, p4)

if __name__ == '__main__':
    main()
