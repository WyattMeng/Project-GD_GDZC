# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 17:43:18 2018

@author: Maddox.Meng
"""

import pandas as pd
import re
import numpy as np
import numexpr as ne

#当年度计提折旧额-EY
#def cal1(p1,p2,p3):
#    #TypeError: ("'<' not supported between instances of 'int' and 'str'", 'occurred at index 144')
#    #ValueError: ('cannot convert float NaN to integer', 'occurred at index 28119')
#    #df.iloc[28119,:]
#    '''因为有讨厌的换行符'''
#    if isinstance(p2, int) is True:
#        if int(p1)<int(p2):#使用期限<已使用年限:
#            return 0
#        #ZeroDivisionError: ('float division by zero', 'occurred at index 27555')
#        elif int(p1)>=int(p2) and int(p1) != 0:
#            return -p3/p1*12/366*182 #-(年初原值)/使用期限*12/366*182  
#        #IndentationError: unindent does not match any outer indentation level
#        elif int(p1)>=int(p2) and int(p1) == 0:
#            return 0
#    else:
#        p2=re.findall(r"\d",p2)[0]
#        if int(p1)<int(p2):#使用期限<已使用年限:
#            return 0
#        #ZeroDivisionError: ('float division by zero', 'occurred at index 27555')
#        elif int(p1)>=int(p2) and int(p1) != 0:
#            return -p3/p1*12/366*182 #-(年初原值)/使用期限*12/366*182  
#        #IndentationError: unindent does not match any outer indentation level
#        elif int(p1)>=int(p2) and int(p1) == 0:
#            return 0
'''Abigail An核对发现这列有差异, 原来是她们已经修改了计算公式, 如下'''



''' ****Indicator****
def do_work_numexpr(a,b):
    expr = 'a + b + 100'
    return ne.evaluate(expr)
df2['d'] = do_work_numexpr(df2['a'], df2['b'])
'''

##当年度计提折旧额-EY
#def cal1(row):
#    #=IF((Y3+AG3)>0,-Y3/N3*6,0)
#    Y = row['年初原值']
#    AG= row['年初累计折旧']
#    N = row['使用期限']
#    if Y+AG>0 and N != 0:
#        return -Y/N*6
#        #return ne.evaluate('-Y/N*6')
#    else: return 0

##当年度计提折旧额-EY
#def cal1(df):
#    #=IF((Y3+AG3)>0,-Y3/N3*6,0)
#    Y = df['年初原值']
#    AG= df['年初累计折旧']
#    N = df['使用期限']
#    if Y+AG>0 and N != 0:
#        return -Y/N*6
#        #return ne.evaluate('-Y/N*6')
#    else: return 0
##ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    
#当年度计提折旧额-EY
def cal1(row):
    #=IF((Y3+AG3)>0,-Y3/N3*6,0)
    q = row['已使用年限']
    l = row['使用期限']
    v = row['年初原值']
    x = row['当年原值减少']
    w = row['当年原值增加']
    if l==0:
        return 0
    else:
        if q>l or (q <= l and v+w+x==0):
            return 0
        elif q<=l and v+w+x!=0 and q>=6:
            return -v/l*6
        else:
            return -w/l*q

def cal1_0(df):
    Y = df['年初原值']
    N = df['使用期限']    
    return ne.evaluate('-Y/N*6')

#def cal2(row):    
#    return row[u'年初累计折旧'] + row[u'当年度计提折旧额-EY'] + row[u'当年度折旧调整']+row[u'当年度折旧转移']

def cal2(df):
    a=df['年初累计折旧']
    b=df['当年度计提折旧额-EY']
    c=df['当年度折旧调整']
    d=df['当年度折旧转移']
    expr = 'a + b + c + d'
    return ne.evaluate(expr)    

#def cal3(row):    
#    return row[u'期末原值'] + row[u'期末减值准备'] + row[u'期末累计折旧-EY']
def cal3(df):
    a = df['期末原值'] 
    b = df['期末减值准备'] 
    c = df['期末累计折旧-EY']
    expr = 'a + b + c'
    return ne.evaluate(expr)     

#def cal4(row):    
#    return row[u'期末净值-EY'] - row[u'期末净值']
def cal4(df):  
    a = df['期末净值-EY'] 
    b = df['期末净值']
    expr = 'a - b'
    return ne.evaluate(expr)   


#固定资产
G_DZ = ['Z104', 'Z105', 'Z106', 'Z107', 'Z117', 'Z118'] #G_DZ_电子设备
G_FW = ['Z101','Z102','Z103','Z114','Z204'] #G_FW_房屋及建筑物
G_ZJ = ['Z401', 'Z402', 'Z499'] #G_ZJ_在建工程
G_QT = ['Z108', 'Z109', 'Z110', 'Z111', 'Z112', 'Z116', 'Z119', 'Z120', 'Z121'] #G_QT_其他
#无形资产
W_JS = ['Z202','Z502'] #W_JS_计算机软件
W_TD = ['Z201'] #W_TD_土地使用权
W_QT = ['Z299'] #W_QT_其他
#长期待摊费用
C_JY = ['Z301'] #C_JY_经营租入固定资产改良支出
C_GG = ['Z303'] #C_GG_广告费
C_ZL = ['Z302'] #C_ZL_租赁费
C_QT = ['Z399'] #C_QT_其他

G = G_DZ + G_FW + G_ZJ + G_QT
W = W_JS + W_TD + W_QT
C = C_JY + C_GG + C_ZL + C_QT

subCategs = [G_DZ, G_FW, G_ZJ, G_QT, W_JS, W_TD, W_QT, C_JY, C_GG, C_ZL, C_QT]
dict_subCategs = {'G_电子设备':G_DZ, 
                  "G_房屋及建筑物":G_FW, 
                  "G_在建工程": G_ZJ, 
                  "G_其他固定资产": G_QT, 
                  "W_计算机软件": W_JS, 
                  "W_土地使用权": W_TD, 
                  "W_其他无形资产": W_QT, 
                  "C_经营租入固定资产改良支出": C_JY, 
                  "C_广告费": C_GG, 
                  "C_租赁费": C_ZL, 
                  "C_其他长期待摊费用": C_QT}

def category(p):
    if p in G:
        return 'G'
    elif p in W:
        return "W"
    elif p in C:
        return "C"
        
def category_sub(p):
    if p in G_DZ:
        return 'G_电子设备'
    elif p in G_FW:
        return "G_房屋及建筑物"
    elif p in G_QT:
        return "G_其他固定资产"
    elif p in G_ZJ:
        return "G_在建工程"
    elif p in W_JS:
        return "W_计算机软件"
    elif p in W_TD:
        return "W_土地使用权"
    elif p in W_QT:
        return "W_其他无形资产"
    elif p in C_JY:
        return "C_经营租入固定资产改良支出"
    elif p in C_GG:
        return "C_广告费"
    elif p in C_QT:
        return "C_其他长期待摊费用"
    elif p in C_ZL:
        return "C_租赁费"

from io import StringIO
def removeLineBreak(f):
    raw = f.read().replace('"', '').replace('|+|', '|') #raw是不分line的,只有一条line
    inputs = StringIO(raw) #这里一定要用StringIO, 以line操作
    #fucklines = []
    for line in inputs:
        if line.count('|') != 46 and line.count('|')>23:
            #fucklines.append(line[-2:])
            lastChar = line[-2:] #每行异常line最后一个字: '罐\n'
            raw = raw.replace(lastChar, lastChar.strip('\n')) #一定要赋值给raw!!!!!!!!!
            #print(repr(line[-2:]),repr(line[-2:-1]))
    return raw

def removeLineBreak2(f):
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