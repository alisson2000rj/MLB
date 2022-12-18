#!/usr/bin/python
# coding: utf-8

# library needed to receive arguments
import sys
# library required for running OS commands
from bib.ic import mean_confidence_interval
# import library that allows execution of OS command
from bib.command import systemCommand

import numpy as np

data = []
    
def calc_ic(p1, data2, flag):
    # list that will receive result
    rslt_vol = []
    rslt_band = []
    rslt_pkt_loss = []
    #amostra = []
    volume = []
    banda = []
    pkt_loss = []
    pkt_total = []
    
    
    
    for line in data2:
        # split by space line by line of the file
        #linhaTratada = line.split(" ")
        #print(line)
        
        volume.append(line[0])
        banda.append(line[1])
        if (flag == 'u'):
            pkt_loss.append(line[3])
            pkt_total.append(line[4])
            #print(pkt_loss)
            #print(pkt_total)
        
        
    #vol = sorted(volume)
    #band = sorted(banda)
    
    media_vol, min_vol, max_vol, erro_vol = mean_confidence_interval(volume)
    media_band, min_band, max_band, erro_band = mean_confidence_interval(banda)
    
    
    if (flag == 'u'):
        media_pkt_loss, min_pkt_loss, max_pkt_loss, erro_pkt_loss = mean_confidence_interval(pkt_loss)
        percent = round((np.mean(pkt_loss) / np.mean(pkt_total) * 100), 2)
        
    
	# output: average minimum maximum error
    rslt_vol.append(str(p1) + ' ' + str(media_vol) + ' ' + str(min_vol) + ' ' + str(max_vol) + ' ' + str(erro_vol) + '\n')
    arq1 = open('./resultado/IC_iperf_vol_rslt.txt', 'a')
    arq1.writelines(rslt_vol)
    arq1.close()
    
    rslt_band.append(str(p1) + ' ' + str(media_band) + ' ' + str(min_band) + ' ' + str(max_band) + ' ' + str(erro_band) + '\n')
    arq2 = open('./resultado/IC_iperf_band_rslt.txt', 'a')
    arq2.writelines(rslt_band)
    arq2.close()
    
    if (flag == 'u'):
        rslt_pkt_loss.append(str(p1) + ' ' + str(media_pkt_loss) + ' ' + str(min_pkt_loss) + ' ' + str(max_pkt_loss) + ' ' + str(erro_pkt_loss) + ' ' + str(percent) + '\n')
        arq3 = open('./resultado/IC_iperf_loss_rslt.txt', 'a')
        
        #print(rslt_pkt_loss)
        arq3.writelines(rslt_pkt_loss)
        arq3.close()
    
def soma_miner(x1):
    p1 = x1
    p1Tratado = p1.split(",")
    data1 = []
    data2 = []
    data3 = []
    linhaTratada1 = ''
    flag = p1Tratado[0][-1]
    
    # initialize the data2 matrix that will receive the sum of the data from the servers
    # its value depends on the number of columns of the file to be analyzed
    # the ncol variable value must follow the number of columns in the file
    ncol = 6
    for x in range(10):
        #data2.append([0,0,0,0,0,0])
        data2.append([0 for x in range(ncol)])
    
    # reads the data from each server, then sums it up and stores it in data2
    for x in p1Tratado:
        # open file for data analysis
        arquivo1 = open('./resultado/' + str(x) + '-iperf-rslt.txt','r')
        data1 = []
        
        # load data from each server (in turn) into data1
        for line1 in arquivo1:
            
            # split by space line by line of the file
            linhaTratada1 = [float(x) for x in line1.split()]
            data1.append(linhaTratada1)
            
        for i in range(len(data1)):
            for j in range(len(linhaTratada1)):
                data2[i][j] += data1[i][j]
                
        arquivo1.close()
        
    for i in range(len(data2)):
        data3.append(str(data2[i][0]) + ' ' + str(data2[i][1]) + ' ' + str(data2[i][3]) + ' ' + str(data2[i][4]) + ' ' +'\n')
    
    # delete old analysis results file
    command = 'rm -rf ./resultado/tserv_iperf_rslt.txt'
    systemCommand(command)
    arq3 = open('./resultado/tserv_iperf_rslt.txt', 'a')
    arq3.writelines(data3)
    arq3.close()
    
    #print(data2)
    
    calc_ic('TServ', data2, flag)
    
def main():
    try:
        p1 = str(sys.argv[1])
        #p2 = str(sys.argv[2])
        #print(p1)
        soma_miner(p1)
         
    except IndexError:
        print("sintaxe: python 5-iperf-soma-server.py <server 1>,<server 2>, ...")
        exit(1)
    else:
        print('Somatório de {} Concluído com Sucesso!'.format(p1))
   

if __name__ == '__main__':
    main()

