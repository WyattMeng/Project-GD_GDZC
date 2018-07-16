# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:02:02 2018

@author: DA05
"""

p = r'a_am_staticdata_20180701_000_000.dat'

#with open(p, 'r', encoding='gb18030', errors='ignore') as f:
#
#    raw = f.read().replace('"', '').replace('|+|', '|') #raw是不分line的,只有一条line
#    inputs = StringIO(raw) #这里一定要用StringIO, 以line操作
#    #fucklines = []
#    i=0
#    for line in inputs:
##        print (line.count('|'))
#        if line.count('|') != 46 and line.count('|')>23:
#            print (i, line.count('|'), line)
#        i+=1


def removeLineBreak(f):
    raw = f.read().replace('"', '').replace('|+|', '|') #raw是不分line的,只有一条line
    inputs = StringIO(raw) #这里一定要用StringIO, 以line操作
    #fucklines = []
    for line in inputs:
        if line.count('|') != 46 and line.count('|')>23:
            #fucklines.append(line[-2:])
            #lastChar = line[-2:] #每行异常line最后一个字: '罐\n'
            raw = raw.replace(line, line.strip('\n')) #一定要赋值给raw!!!!!!!!!
            #print(repr(line[-2:]),repr(line[-2:-1]))
    
    inputs = StringIO(raw) #这里一定要用StringIO, 以line操作
    for line in inputs:
        if line.count('|') != 46 and line.count('|')>23:
            raw = raw.replace(line, line.strip('\n')) #一定要赋值给raw!!!!!!!!!
    return raw

with open(p, 'r', encoding='gb18030', errors='ignore') as f:
    raw = removeLineBreak(f)
    inputs = StringIO(raw)
    
    for line in inputs:
#        print (line.count('|'))
        if line.count('|') != 46 and line.count('|')>23:
            print (i, line.count('|'), line)
        i+=1

