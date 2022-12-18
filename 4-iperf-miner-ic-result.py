#!/usr/bin/python
# coding: utf-8

'''
file output:
     x-iperf-rslt.txt = volume bandwidth jitter lost-packets-total-packets
     IC_iperf_loss_rslt.txt = host lost-packages min max error percent
'''

# library needed to receive arguments
import sys
# library required for running OS commands
from bib.ic import mean_confidence_interval
# import library that allows execution of OS command
from bib.command import systemCommand

# import library that provides metric class
from bib.metrica import metrica

# import numpy math library  
import numpy as np 

   
    
def calc_ic(p1, m, udp_flag):
    # list that will receive result
    rslt_vol = []
    rslt_band = []
    rslt_jitter = []
    rslt_loss = []
    rslt_pkt_percent = []
    
    media_vol, min_vol, max_vol, erro_vol = mean_confidence_interval(m.getLstDados())
    media_band, min_band, max_band, erro_band = mean_confidence_interval(m.getLstVazao())
    
    if (udp_flag and p1[0] == 's'):
        media_jitter, min_jitter, max_jitter, erro_jitter = mean_confidence_interval(m.getLstJitter())
        media_loss1, min_loss1, max_loss1, erro_loss1 = mean_confidence_interval(m.getLstLoss1())
        media_pkt_percent, min_pkt_percent, max_pkt_percent, erro_pkt_percent = mean_confidence_interval(m.getLstPer())
        media_loss2 = np.mean(m.getLstLoss2())  
    
    rslt_vol.append(str(p1) + ' ' + str(media_vol) + ' ' + str(min_vol) + ' ' + str(max_vol) + ' ' + str(erro_vol) + '\n')
    rslt_band.append(str(p1) + ' ' + str(media_band) + ' ' + str(min_band) + ' ' + str(max_band) + ' ' + str(erro_band) + '\n')
    
    if (udp_flag and p1[0] == 's'):
        rslt_jitter.append(str(p1) + ' ' + str(media_jitter) + ' ' + str(min_jitter) + ' ' + str(max_jitter) + ' ' + str(erro_jitter) + '\n')
        rslt_loss.append(str(p1) + ' ' + str(media_loss1) + ' ' + str(min_loss1) + ' ' + str(max_loss1) + ' ' + str(erro_loss1) + ' ' + str(media_pkt_percent) + ' ' + str(media_loss2) +'\n')
    
    # output: average minimum maximum error
    arq1 = open('./resultado/IC_iperf_vol_rslt.txt', 'a')
    arq1.writelines(rslt_vol)
    arq1.close()
    
    arq2 = open('./resultado/IC_iperf_band_rslt.txt', 'a')
    arq2.writelines(rslt_band)
    arq2.close()
    
    if (udp_flag):
        arq3 = open('./resultado/IC_iperf_jitter_rslt.txt', 'a')
        arq3.writelines(rslt_jitter)
        arq3.close()
        arq4 = open('./resultado/IC_iperf_loss_rslt.txt', 'a')
        arq4.writelines(rslt_loss)
        arq4.close()
        
    if (udp_flag and p1[0] == 's'):
        rslt_pkt_percent.append(str(p1) + ' ' + str(media_pkt_percent) + ' ' + str(min_pkt_percent) + ' ' + str(max_pkt_percent) + ' ' + str(erro_pkt_percent) + '\n')
        arq5 = open('./resultado/IC_iperf_loss_percet_rslt.txt', 'a')
        arq5.writelines(rslt_pkt_percent)
        arq5.close()
        
        
        
def miner(p1):
    
    # instantiate the metric class to a local object m
    m = metrica()
    
    # variable used as a flag to signal the use of UDP
    udp_flag = 0
    # open file for data analysis
    arquivo = open('./resultado/' + str(p1) + '.txt','r')
    
    # delete old analysis results file
    command = 'rm -rf ./resultado/' + str(p1) + '-iperf-rslt.txt'
    systemCommand(command)
    
    # create a file for writing the analysis result
    arquivoEscrita = open('./resultado/' + str(p1) + '-iperf-rslt.txt','a')
    
    arquivo.readline()
    
    if 'UDP' in arquivo.readline():
        udp_flag = 1
        
    # loop through each line of the open file
    for line in arquivo:
        # split the file line by line
        linhaTratada = line.split()
        
        if '[SUM]' != linhaTratada[0]:
                i = 0
                for item in linhaTratada:
                    # if TCP
                    if (not udp_flag): 
                        if item == 'bits/sec':
                            m.setLstVazao(linhaTratada[i-1])
                            m.setLstDados(linhaTratada[i-3])
                            arquivoEscrita.write(str(m.getLstDados()[-1]) + " " + str(m.getLstVazao()[-1]) + "\n")
                            
                    # If it's UDP
                    else:
                        
                        if p1[0] == 'h':
                            if item == 'bits/sec' and len(linhaTratada)-1 == i:
                                #print(len(linhaTratada)-1)
                                #print(i)
                                m.setLstVazao(linhaTratada[i-1])
                                m.setLstDados(linhaTratada[i-3])
                                arquivoEscrita.write(str(m.getLstDados()[-1]) + " " + str(m.getLstVazao()[-1]) + "\n")
                        else:
                            if item == 'ms':
                                m.setLstVazao(linhaTratada[i-3])
                                m.setLstDados(linhaTratada[i-5])
                                m.setLstJitter(linhaTratada[i-1])
                                m.setLstLoss1(line.split('ms')[1].split('(')[0].replace(' ','').split('/')[0])
                                m.setLstLoss2(line.split('ms')[1].split('(')[0].replace(' ','').split('/')[1])
                                #m.setLstPer(line.split('(')[1].split('%')[0])
                                m.setLstPer(  float(line.split('ms')[1].split('(')[0].replace(' ','').split('/')[0]) /  float(line.split('ms')[1].split('(')[0].replace(' ','').split('/')[1]) )
                                arquivoEscrita.write(str(m.getLstDados()[-1]) + " " + str (m.getLstVazao()[-1]) + " " + str(m.getLstJitter()[-1]) + " " + str(m.getLstLoss1()[-1]) + " " + str(m.getLstLoss2()[-1]) + " " + str(m.getLstPer()[-1]) + "\n")
                            
                    i+=1
    
    # close open files    
    arquivo.close()
    arquivoEscrita.close()
    calc_ic(p1, m, udp_flag)
    
    
def main():
    try:
        p1 = str(sys.argv[1])
        miner(p1) 
        
    except IndexError:
        print("ERROR!!! sintaxe: python 4-iperf-miner-result.py <nó/fluxo>")
        exit(1)
    else:
        print('Mineração de {} Concluída com Sucesso!'.format(p1))
    #finally:
        #calc_ic(p1)

if __name__ == '__main__':
    main()

