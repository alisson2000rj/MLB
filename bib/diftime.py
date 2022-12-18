#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################################
# File        : diftime.py
# Course	  : Master's Degree in Electronic Engineering
# Student	  : Alisson Cavalcante e Silva
# discipline  : Dissertation
# Teacher     : Marcelo Rubinstein
# Date        : 12/08/2019
# Description : Classe em python para calcular hora
############################################################################################



class DiferencaTempo:
    def __init__(self, tempo2, tempo1):
        self.diff = tempo2 - tempo1

    def getSegundos(self):
        return '{:0.3f}'.format(self.diff)
        #return self.diff
        
    def getMilisegundos(self):
        return '{:0.0f}'.format(self.diff*1000)
        #return self.diff*1000
        
 
