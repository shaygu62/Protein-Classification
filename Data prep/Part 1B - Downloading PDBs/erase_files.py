# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:30:30 2019

@author: owner
"""

import os

mydir =  "D:\\3D structural data\\project\\families"
families_list = os.listdir(mydir)
word_to_leave = 'Copy' # in our case we would leave all files containing 'chain'
for f in families_list:
    proteins_list = os.listdir(mydir+'\\'+f)
    for p in proteins_list:
        if not word_to_leave in p:
            os.remove(os.path.join(mydir, f, p))
