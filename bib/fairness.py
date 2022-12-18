#!/usr/bin/python
# coding: utf-8

def justica(lista):
    a = sum(lista)**2
    b = sum([x**2 for x in lista])*len(lista)
    return (a/float(b))


