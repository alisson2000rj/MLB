#!/usr/bin/python
# coding: utf-8


'''
runs inside node on mininet e.g. h1
syntax: 10-icmp.py <no source> <destination ip>

output formats for gnuplot
http://gnuplot.sourceforge.net/docs_4.2/node184.html

'''
# library needed to receive arguments
import sys

# library needed to calculate confidence interval
from bib.ic import mean_confidence_interval

# import library that allows execution of OS command
from bib.command import systemCommand

def mineracao(p1):
    #Reading the ping file and manipulating its string to get the average ping value
    arquivo = open('./resultado/'+ str(p1) + '-icmp.txt','r')
    
    # delete old analysis results file
    command = 'rm -rf ./resultado/' + str(p1) + '-icmp-rslt.txt'
    systemCommand(command)
    
    # create file for writing analysis result
    arquivoEscrita = open('./resultado/' + str(p1) + '_icmp-rslt.txt','a')
    transmitido = ''
    recebido = ''
    
    # Loop scans the lines of the file
    for line in arquivo:
        #Returns a list with each column of the row
        # The split function returns a list with each column according to the character that was defined
        # In this case, it's a blank space, but it could be a comma, colon, anything
        linhaTratada = line.split()
        i = 0
        # loop scans the words of each line of the file
        for item in linhaTratada:
            #print(item)
            if (item == 'transmitted,'):
                #print(linhaTratada)
                transmitido = linhaTratada[i-2]
                #print(transmitido)
                recebido = int(linhaTratada[i+1])
                #print(recebido)
                loss = linhaTratada[i+3].split('%')[0]
                #print(loss)
            i+= 1
        if(linhaTratada and linhaTratada[0] == "rtt"):
            #print(linhaTratada)
            ## By analyzing the ping, the measurement is in column 3
            #Separate the value of this line, which is divided by /
            sublinhaTratada = linhaTratada[3].split("/")
            # Within this column, the average value is in subcolumn 1 separated by /
            arquivoEscrita.write(str(sublinhaTratada[1]) + ' ' + str(transmitido) + ' ' + str(recebido) + ' ' + str(loss) + "\n")
    arquivo.close()
    arquivoEscrita.close()

def calc_ic(p1):
    # declaration of the list structures that will be used
    rtt = []
    transmitido = []
    recebido = []
    rslt_icmp = []
    
    # open file
    arquivo = open('./resultado/' + str(p1) + '_icmp-rslt.txt', 'r')

    ## load the contents of the file into the "data" list, removing the special line skip character
    for x in arquivo: 
        rtt.append(float(x.split()[0]))
        transmitido.append(int(x.split()[1]))
        recebido.append(int(x.split()[2]))
    
    # close file
    arquivo.close()
    
    # call function that calculates IC and returns values into variables
    media_vol, min_vol, max_vol, erro_vol = mean_confidence_interval(rtt)
    # load value into the list
    rslt_icmp.append(str(p1) + ' ' + str(media_vol) + ' ' + str(min_vol) + ' ' + str(max_vol) + ' ' + str(erro_vol) + '\n')
    # open file that will receive final result
    arq1 = open('./resultado/IC_rslt_icmp.txt', 'a')
    # write data to file
    arq1.writelines(rslt_icmp)
    # close file
    arq1.close()

def main():
    # receive two parameters p1 and p2
    try:
        p1 = str(sys.argv[1])
        mineracao(p1)
        calc_ic(p1)
    except IndexError:
        print("ERROR!!! sintaxe: python 8-icmp.py <nó origem>")
        exit(1)
    else:
        print('Mineração concluída com Sucesso!')
    
    

if __name__ == '__main__':
    main()
