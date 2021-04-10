# -*- coding: utf-8 -*-
"""
RAE simple Scrapping

Autor: Wilfrido J. Paredes Garcia

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions

import time

import re

import json

crea_json = open("crea.json",'r')
crea = json.load(crea_json)
crea_json.close()

def tulengua_access():
    website = 'https://tulengua.es/silabas/'
    options = EdgeOptions()
    options.use_chromium = True
    browser = Edge(executable_path='D:/Documents/Python Scripts/silabeo/Web Driver/msedgedriver.exe', options = options)

    browser.get(website)

    return browser


def word_syllabification(browser,word):
    #El input de busqueda está bajo el ID 'edit-termino2' pero podría cambiar con el tiempo
    finder = browser.find_element(By.ID, "MainContent_inputPalabra")
    finder.send_keys(word+Keys.ENTER)
    #Ya no es necesario mantener el elemento
    del finder
    
    return browser


def syllables(word,browser=None):
    if browser == None:
        browser = tulengua_access()
    else:
        browser.get('https://tulengua.es/silabas/')
    browser = word_syllabification(browser, word)
    result_short = []
    while len(result_short) < 1:
        time.sleep(2)
        result_raw = browser.page_source
        result_short = re.findall(r'divide\sen\s[0-9]+\ssílabas:\s[^.]+', result_raw, flags=re.M)
    
    x = re.findall(r'divide\sen\s[0-9]+\ssílabas:\s[^.]+', result_short[0], flags=re.M)[0]
    x = re.findall(r':.*', x)[0]
    x = re.sub(r'</?b>', '', x)
    x = re.sub(r'[:\s]+', '', x)
    x = x.split('-')
    
    return x, browser

syllables_dic = {}
counter = 0
navigation = None
words = list(crea.keys())
for w in range(counter,len(crea.keys())):
    if len(syllables_dic)>273:
        break
    try:
        if len(words[w]) > 5:
            results, navigation = syllables(words[w],navigation)
            syllables_dic[w] = results
        counter += 1
    except:
        navigation.quit()
        navigation = None
        w = counter
        time.sleep(60)
    
f = open('syllables_dataset.json','w+')
json.dump(syllables_dic,f)
f.close()


  