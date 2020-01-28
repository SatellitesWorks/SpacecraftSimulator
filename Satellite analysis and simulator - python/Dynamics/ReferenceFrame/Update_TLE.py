# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:14:52 2018

@author: EAOS
"""

#from urllib3 import ProxyManager, make_headers
import requests


def get_UpdateTLE(NumbNorad, Filename):  
    
    url = 'https://www.celestrak.com/cgi-bin/TLE.pl?CATNR='+NumbNorad
    R = requests.get(url)
    
    ini = R.text.find('<pre>') + 7
    fin = R.text.find('</pre>') - 2
    Text = R.text
    data = ['','','']
    i = 0;
    for l in range(ini, fin):
        if Text[l] == '\n':
            i += 1
        else:
            data[i] += Text[l] 
            
    esp = data[0].find(' ')       
    
    Nombre = data[0][0:esp]
    data[0] = Nombre
    
    archivo = open (Filename + '.txt','w')
    archivo.write(data[0]+'\n')
    archivo.write(data[1]+'\n')
    archivo.write(data[2])
    archivo.close()        
    
    print("Ready: TLE updated")