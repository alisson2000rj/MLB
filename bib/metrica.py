#!/usr/bin/python
# coding: utf-8

class metrica:
    def __init__(self):
        self.__lstvazao = []
        self.__lstdados = []
        self.__lstjitter = []
        self.__lstloss1 = []
        self.__lstloss2 = []
        self.__lstper = []
    
    def setLstVazao(self, vazao):
        self.__lstvazao.append(int(vazao))
    
    def setLstDados(self, dados):
        self.__lstdados.append(int(dados))
    
    def setLstJitter(self, jitter):
        self.__lstjitter.append(float(jitter))
    
    def setLstLoss1(self, loss1):
        self.__lstloss1.append(int(loss1))
        
    def setLstLoss2(self, loss2):
        self.__lstloss2.append(int(loss2))
        
    def setLstPer(self, per):
        self.__lstper.append(float(per))
        
    
    
    def getLstVazao(self):
        return self.__lstvazao
    
    def getLstDados(self):
        return self.__lstdados
    
    def getLstJitter(self):
        return self.__lstjitter
    
    def getLstLoss1(self):
        return self.__lstloss1
    
    def getLstLoss2(self):
        return self.__lstloss2
    
    def getLstPer(self):
        return self.__lstper
  
  
    
    def setDados(self, dados):
        self.__lstdados = dados
        
    def setVazao(self, vazao):
        self.__lstvazao = vazao
    
    def setJitter(self, jitter):
        self.__lstjitter = jitter
    
    def setLoss1(self, loss1):
        self.__lstloss1 = loss1
    
    def setLoss2(self, loss2):
        self.__lstloss2 = loss2
    
    def setPer(self, per):
        self.__lstper = per
