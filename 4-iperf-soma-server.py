#!/usr/bin/python
# coding: utf-8

# library needed to receive arguments
import sys
# library required for running OS commands
from bib.ic import mean_confidence_interval
# import library that allows execution of OS command
from bib.command import systemCommand

# import library that provides metric class
from bib.metrica import metrica

import numpy as np

def calc_ic(p1, m, flag):
    # list that will receive result
    rslt_vol = []
    rslt_band = []
    rslt_pkt_loss = []
    rslt_pkt_percent = []
        
    media_vol, min_vol, max_vol, erro_vol = mean_confidence_interval(m.getLstDados())
    media_band, min_band, max_band, erro_band = mean_confidence_interval(m.getLstVazao())
    
    if (flag == 'u'):
        media_pkt_loss1, min_pkt_loss1, max_pkt_loss1, erro_pkt_loss1 = mean_confidence_interval(m.getLstLoss1())
        media_pkt_percent, min_pkt_percent, max_pkt_percent, erro_pkt_percent = mean_confidence_interval(m.getLstPer())
        #percent = round((np.mean(m.getLstLoss1()) / np.mean(m.getLstLoss2()) * 100), 4)
        #percent = np.mean(m.getLstPer())
        media_pkt_loss2 = np.mean(m.getLstLoss2())        
        
    

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
        
        rslt_pkt_loss.append(str(p1) + ' ' + str(media_pkt_loss1) + ' ' + str(min_pkt_loss1) + ' ' + str(max_pkt_loss1) + ' ' + str(erro_pkt_loss1) + ' ' + str(media_pkt_percent) + ' ' + str(media_pkt_loss2)+ '\n')
        arq3 = open('./resultado/IC_iperf_loss_rslt.txt', 'a')
        arq3.writelines(rslt_pkt_loss)
        arq3.close()
        
    
        rslt_pkt_percent.append(str(p1) + ' ' + str(media_pkt_percent) + ' ' + str(min_pkt_percent) + ' ' + str(max_pkt_percent) + ' ' + str(erro_pkt_percent) + '\n')
        arq5 = open('./resultado/IC_iperf_loss_percet_rslt.txt', 'a')
        arq5.writelines(rslt_pkt_percent)
        arq5.close()
        
        
        
    
def soma_miner(p1):
    p1Tratado = p1.split(",")
    data3 = []
    linhaTratada1 = ''
    flag = p1Tratado[0][-1]
    
    m = metrica()
  
    # number of rounds or series of samples. Eg: 10 rounds of 50 samples
    rodadas = sum(1 for line in open('./resultado/' + str(p1Tratado[0]) + '-iperf-rslt.txt','r'))
    
    #print(rodadas)
    
    for i in range(rodadas):
        m.setLstDados(0)
        m.setLstVazao(0)
        m.setLstJitter(0)
        m.setLstLoss1(0)
        m.setLstLoss2(0)
        m.setLstPer(0)
    
    for arq in p1Tratado:
        # open file for data analysis
        arquivo1 = open('./resultado/' + str(arq) + '-iperf-rslt.txt','r')
        
        
        dados = []
        vazao = []
        jitter = []
        loss1 = []
        loss2 = []
        per = []
        # load data from each server (in turn) 
        for line in arquivo1:
            
            linhaTratada = line.split()
            dados.append(int(linhaTratada[0]))
            vazao.append(int(linhaTratada[1]))
            
            if arq[-1] == 'u':
                jitter.append(float(linhaTratada[2]))
                loss1.append(int(linhaTratada[3]))
                loss2.append(int(linhaTratada[4]))
                per.append(float(linhaTratada[5]))
            
        m.setDados([x+y for x, y in zip(m.getLstDados(), dados)])
        m.setVazao([x+y for x, y in zip(m.getLstVazao(), vazao)])
        if arq[-1] == 'u':
            m.setJitter([x+y for x, y in zip(m.getLstJitter(), jitter)])
            m.setLoss1([x+y for x, y in zip(m.getLstLoss1(), loss1)])
            m.setLoss2([x+y for x, y in zip(m.getLstLoss2(), loss2)])
            m.setPer([x+y for x, y in zip(m.getLstPer(), per)])
        
        
        arquivo1.close()
    
    # Necessary to take the average of the percentage of packet losses after the sum of the servers. 
    m.setPer([x/len(p1Tratado) for x in m.getLstPer()])
    
    for i in range(rodadas):
        if (flag == 't'):
            data3.append(str(m.getLstDados()[i]) + ' ' + str(m.getLstVazao()[i]) + '\n')
        elif(flag == 'u'):
            data3.append(str(m.getLstDados()[i]) + ' ' + str(m.getLstVazao()[i]) + ' ' + str(m.getLstLoss1()[i]) + ' ' + str(m.getLstLoss2()[i]) + ' ' + str((float(m.getLstLoss1()[i])/float(m.getLstLoss2()[i]))) +'\n')
        
        
    # delete old analysis results file
    command = 'rm -rf ./resultado/tserv_iperf_rslt.txt'
    systemCommand(command)
    arq3 = open('./resultado/tserv_iperf_rslt.txt', 'a')
    arq3.writelines(data3)
    arq3.close()
    calc_ic('TServ', m, flag)
    
def main():
    try:
        p1 = str(sys.argv[1])
        soma_miner(p1)
         
    except IndexError:
        print("sintaxe: python 5-iperf-soma-server.py <server 1>,<server 2>, ...")
        exit(1)
    else:
        print('\n#Somatório de {} Concluído com Sucesso!'.format(p1))
   

if __name__ == '__main__':
    main()

