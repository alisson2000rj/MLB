#!/usr/bin/python
# coding: utf-8

# library needed to receive arguments
import sys

# import library that allows measuring justice between flows
from bib.fairness import justica

# library required for running OS commands
from bib.ic import mean_confidence_interval

def miner(p1):
    p1Tratado = p1.split(",")
    lista = [[] for _ in range(len(p1Tratado))]
    lista3 = []
    
    for i in range(0, len(p1Tratado)):
        # open the file with the analysis result
        arquivo = open('./resultado/'+ str(p1Tratado[i]) + '-iperf-rslt.txt','r')
        for linha in arquivo:
            # split the file line by line
            linhaTratada = linha.split()
            lista[i].append(int(linhaTratada[1]))
    
    for i in range(0, len(lista[0])):
        lista2 = []
        for j in range(0, len(p1Tratado)):
            lista2.append(lista[j][i]) 
            
        lista3.append(justica(lista2))
    
    return(lista3)
    
def main():
    try:
        p1 = str(sys.argv[1])
        rslt_justica = []
        media_justica, min_justica, max_justica, erro_justica = mean_confidence_interval(miner(p1))
        rslt_justica.append(str(p1) + ' ' + str(media_justica) + ' ' + str(min_justica) + ' ' + str(max_justica) + ' ' + str(erro_justica) + '\n')
        arq1 = open('./resultado/IC_justica_rslt.txt', 'a')
        arq1.writelines(rslt_justica)
        arq1.close()
        
    except IndexError:
        print("sintaxe: python a.py <server 1>,<server 2>, ...")
        exit(1)
    else:
        print('#Calculo justica com IC {} Concluído com Sucesso!'.format(p1))
   
if __name__ == '__main__':
    main()
