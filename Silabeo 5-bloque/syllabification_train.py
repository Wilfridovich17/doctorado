# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:08:41 2021

@author: Wilfridovich
"""
import syllabification_code as coder
import json

#Training set raw
silabas = {}
for i in range(4):
    silabas_json = open("Silabas/syllables_dataset"+str(i+1)+'.json','r')
    silabas_aux = json.load(silabas_json)
    silabas_json.close()
    for key, value in silabas_aux.items():
        silabas[key] = value


x_train,y_train = coder.generate_readlydata(silabas,2180)
coder.save_nparray('syllabification_xtrain', x_train)
coder.save_nparray('syllabification_ytrain', y_train)

print(coder.codification('transp'))
