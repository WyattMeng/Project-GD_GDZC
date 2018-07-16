# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 22:35:32 2018

@author: Maddox.Meng
"""
import time


'''Part1: '''
import numpy as np
import numexpr as ne
#a = np.arange(10)
#b = np.arange(0, 20, 2)
#c = ne.evaluate("2*a+3*b")

import pandas as pd
'''Part2'''
#n = 100000000
#df = pd.DataFrame({
#    'a': np.random.randn(n),
#    'b': np.random.randn(n),
#    'c': np.random.randn(n),
#})

##01.NumPy Expression
#start_time = time.time()
#def do_work_numpy(a):
#    return np.sin(a - 1) + 1
#
#result = do_work_numpy(df['a'])
#print("--- %s seconds ---" % (time.time() - start_time))
##--- 3.146001100540161 seconds ---

##02.Applying By Row
#start_time = time.time()
#def do_work_row(row):
#    return math.sin(row['a'] - 1) + 1
#
#result = df.apply(do_work_row, axis=1)
#print("--- %s seconds ---" % (time.time() - start_time))

##03.With numexpr
#import numexpr
#start_time = time.time()
#def do_work_numexpr(a):
#    expr = 'sin(a - 1) + 1'
#    return numexpr.evaluate(expr)
#
#result = do_work_numexpr(df['a'])
#print("--- %s seconds ---" % (time.time() - start_time))
##--- 1.9680955410003662 seconds ---

df2 = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]],index=['row1','row2','row3'],columns=['a','b','c'])

n = 3000000
df2 = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
    'c': np.random.randn(n),
})

#def do_work_numexpr(a):
#    expr = 'a + 100'
#    return ne.evaluate(expr)
#
#df2['d'] = do_work_numexpr(df2['a'])

#def do_work_numexpr(a,b):
#    expr = 'a + b + 100'
#    return ne.evaluate(expr)
#
#df2['d'] = do_work_numexpr(df2['a'], df2['b'])

#def do_work_numexpr(a,b):
#    if a+b>=7:
#        expr = 'a + b + 100'
#        return ne.evaluate(expr)
#    else: return 0
##ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
#df2['d'] = do_work_numexpr(df2['a'], df2['b'])

#def do_work_numexpr(a,b):
#    if ne.evaluate('a+b') >= 7:
#        expr = 'a + b + 100'
#        return ne.evaluate(expr)
#    else: return 0
##ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
#df2['d'] = do_work_numexpr(df2['a'], df2['b'])

#def do_work_numexpr(a,b):
#    if a.any() >= 2:
#        expr = 'a + b + 100'
#        return ne.evaluate(expr)
#    else: return 0
##return self.values.item() -- ValueError: can only convert an array of size 1 to a Python scalar
#df2['d'] = do_work_numexpr(df2['a'], df2['b'])
#'''
start_time = time.time()
def do_work_numexpr(a,b):
    expr = 'a + b + 100'
    return ne.evaluate(expr)

#def do_work_numexpr(df):
#    a = df['a']
#    b = df['b']
#    expr = '%s+%s+100'%(a,b)
#    return ne.evaluate(expr)

#return self.values.item() -- ValueError: can only convert an array of size 1 to a Python scalar
#df3 = df2.copy(deep=True)
df3 = df2[df2['a']>2]
df4 = df2[df2['a']<=2]
df3['d'] = do_work_numexpr(df3['a'], df3['b'])
#df3['d'] = do_work_numexpr(df3)
df4['d'] = 0

df2=pd.concat([df3,df4])
df2.sort_index(inplace=True)
print("--- %s seconds ---" % (time.time() - start_time))
#--- 0.9422969818115234 seconds ---
print(df2)
#'''

#start_time = time.time()
#def do_work_apply(row):
#    if row['a'] > 2:
#        return row['a']+row['b']+100
#    else: return 0
#df2['d'] = df2.apply(lambda row: do_work_apply(row), axis=1)
#print("--- %s seconds ---" % (time.time() - start_time))
##--- 47.50325036048889 seconds ---
##print(df2)

'''*****INCREDIBLE!!!!!!!******'''

