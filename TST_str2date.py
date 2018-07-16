# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 18:10:47 2018

@author: Maddox.Meng
"""

#df2 = pd.DataFrame([[20180101,2,3],[4,5,6],[7,8,9]],index=['row1','row2','row3'],columns=['a','b','c']


df2[df['起息日']] = df[df['起息日']].astype(datetime.date)
print(df2)
