# -*- coding: utf-8 -*-
"""
Syllabification code

@author: Wilfridovich
"""

import re 
import numpy as np

letter_dic = {'h':0., 'p':1.,'b':1., 'v':1., 't':1.,'d':1., 'k':2.,'ga':2., 'f':3., 's':4., 'z':4., 'y':4.,  'j':5.,'ge':5.,'x':5.,'m':7.,'n':8.,'ñ':8.,'l':9.,'r':10.,'a':11.,'e':11.,'o':11.,'á':11.,'é':11.,'í':11.0,'ó':11.0,'ú':11.0,'i':12.,'u':12.,'w':13.}
double_letter_dic = {'ch':6.0, 'll':4.0, 'rr':10.0, 'qu':2.0, 'gü':13.0,'br':14.0,'cr':14.0,'dr':14.0, 'fr':14.0,'gr':14.0,'tr':14.,'bl':15.0,'cl':15.,'fl':15.0, 'gl':15.0,'tl':15.0}

def g_work(c_1,c_2='s'):
    if re.match('[aouáóú]',c_1) != None:
        if re.match('[eiéí]',c_2) != None:
            return 'ga',1
        else:
            return 'ga',0
    else:
        return 'ge',0
        
def c_work(c_1):
    if re.match('[eiéí]',c_1) != None:
        return 's'
    else:
        return 'k'
            
   
def codification(block):
    code_block = []
    it = iter(range(len(block)))
    for i in it:
        try:
            little_block = block[i:(i+2)]
        except:
            little_block = block[i:(i+1)]
        if len(little_block) < 2:
            little_block += '-'
        if little_block in double_letter_dic:
            code_block.append(double_letter_dic[little_block])
            i = next(it)
        else:
            character_1 = little_block[0]
            character_2 = little_block[1]
            if character_1 == 'g':
                try:
                    character_3 = block[i+2]
                except:
                    character_3 = 's'
                aux_a, aux_counter = g_work(character_2, character_3)
                if aux_counter > 0:
                    i = next(it)
                code_block.append(letter_dic[aux_a])
            elif character_1 == 'c':
                aux_a = c_work(character_2)
                code_block.append(letter_dic[aux_a])
            else:
                code_block.append(letter_dic[character_1])
    
    if len(code_block) > 5:
        return code_block[0:6]
    else:
        return code_block + [0 for i in range(6-len(code_block))]
                

def generate_readlydata(dictionary, size=0, mode='create'):
    counter = 0
    if mode == 'count':
        for w in list(dictionary.values()):
            for i in range(len(w)-1):
                counter += 1
        return counter,0
    else:
        y = np.zeros([size,5])
        x = np.zeros([size,6])
        for w in list(dictionary.values()):
            for i in range(len(w)-1):
                blocks = codification(w[i]+w[i+1])
                x[counter,:] = np.array(blocks)/15.0 
                y[counter,len(w[i])-1] = 1 
                counter += 1
        return x,y
        

def save_nparray(file_name,arr):
    f = open(file_name+'.np','wb')
    np.save(f,arr)
    f.close()