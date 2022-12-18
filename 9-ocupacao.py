#!/usr/bin/python
# coding: utf-8

'''
file output:
    x-iperf-rslt.txt = volume band jitter packet-lost total-packets
    IC_iperf_loss_rslt.txt = host lost-packages min max error percentage
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

   
    
def calc_ic(p1, m):
    # list that will receive result
    rslt_band = []
    
    media_band, min_band, max_band, erro_band = mean_confidence_interval(m.getLstVazao())
    
    rslt_band.append(str(p1) + ' ' + str(media_band) + ' ' + str(min_band) + ' ' + str(max_band) + ' ' + str(erro_band) + '\n')
    
    arq2 = open('./resultado/ocupacao_band_rslt.txt', 'a')
    arq2.writelines(rslt_band)
    arq2.close()
    
    
        
        
def miner(p1):
    
    # instantiate the metric class to a local object m
    m = metrica()
    
    # open file for data analysis
    arquivo = open('./resultado/' + str(p1) + '-iperf-rslt.txt','r')
    
    # loop through each line of the open file
    for line in arquivo:
        # split the file line by line
        linhaTratada = line.split()
        m.setLstVazao(linhaTratada[-1])
                   
    # close open files  
    arquivo.close()
    calc_ic(p1, m)
    
    
def main():
    try:
        p1 = str(sys.argv[1])
        miner(p1) 
        
    except IndexError:
        print("ERROR!!! sintaxe: python 4-iperf-miner-result.py <nó/fluxo>")
        exit(1)
    else:
        print('Mineração de {} Concluída com Sucesso!'.format(p1))
    

if __name__ == '__main__':
    main()

