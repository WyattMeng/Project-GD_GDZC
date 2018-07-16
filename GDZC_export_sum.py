# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 10:39:49 2018

@author: Maddox.Meng
"""

import pandas as pd
from pandas.compat import StringIO
from GDZC_module import cal1
from GDZC_module import cal2
from GDZC_module import cal3
from GDZC_module import cal4
from GDZC_module import category
from GDZC_module import category_sub
from GDZC_module import removeLineBreak2
import datetime

cols = ['数据期间', '资产号', '资产次级编号', '资产类别', '资产子类', '工厂', '成本中心', '责任成本中心', '使用状态', '产权状态', '折旧码', '科目定位码', '使用期限', '购置年月', '购置日期', '资本化日期', '折旧开始日期', '已使用年限', '停用标志', '报废日期', '当年度报废标志:Y/N', '数量', '数量单位', '年初原值', '当年原值增加', '当年原值减少', '期末原值', '年初减值准备', '当年减值准备计提额', '当年减值准备转移', '期末减值准备', '年初累计折旧', '当年度计提折旧额', '当年度折旧调整', '当年度折旧转移', '期末累计折旧', '期末净值', '供应商', '投资订单', '序列号', '存货号', '设备号', '资产名称', '资产详细描述', '资产主号文本', '使用者', '实物所在地']

plist = [r'a_am_staticdata_20180701_000_000.dat']
#plist = [r'a_am_staticdata_20180701_000_000_tst.dat']

starttime_total = datetime.datetime.now()
framessum = []

i=1
for p in plist:
    print ('|--' + p.split('\\')[-1])
    
    with open(p, 'r', encoding='gb18030', errors='ignore') as f:
        
        print('remove line break')
        raw = removeLineBreak2(f) #相当于f.read(), 替换了", |+|, 还有非末尾换行符
        input = StringIO(raw)
        
        print('read data')
        df = pd.read_csv(input, sep="|", skiprows=0, names=cols, engine='python')

        print('   |--Calculate columns...')
        df['database'] = i
             
        df[u'当年度计提折旧额-EY'] = df.apply(lambda row: cal1(row), axis=1)                       
        #df[u'期末累计折旧-EY']    = df.apply(lambda row: cal2(row), axis=1)
        #df[u'期末净值-EY']        = df.apply(lambda row: cal3(row), axis=1)
        #df[u'Diff']              = df.apply(lambda row: cal4(row), axis=1)
        
        
        #df[u'当年度计提折旧额-EY'] = cal1(df) 
        df['期末累计折旧-EY']    = cal2(df)
#        df['期末净值-EY']        = cal3(df)
#        df['Diff']               = cal4(df)
        
        df['EYtype1']= df.apply(lambda row: category(row[u'资产类别']), axis=1)
        df['EYtype2']= df.apply(lambda row: category_sub(row[u'资产类别']), axis=1)
        
        print('   |--Summarize...')
        '''dfsum = df.groupby(['资产类别']).sum()'''
        dfsum = df.groupby(['database','EYtype1','EYtype2']).sum()
        framessum.append(dfsum)
       
    i+=1
 
#ressum = pd.concat(framessum, sort=False)
ressum = pd.concat(framessum)
#TypeError: concat() got an unexpected keyword argument 'sort'

sumcol = ['年初原值','当年原值增加','当年原值减少',	
          '年初减值准备','当年减值准备计提额','当年减值准备转移',
          '年初累计折旧','当年度计提折旧额','当年度折旧调整','当年度折旧转移',
          '当年度计提折旧额-EY','期末累计折旧-EY']

ressum = ressum[sumcol]
ressum['期末原值'] = ressum.apply(lambda row: row['年初原值'] + row['当年原值增加'] + row['当年原值减少'], axis=1)
ressum['期末减值准备'] = ressum.apply(lambda row: row[u'年初减值准备']+row[u'当年减值准备计提额']+row[u'当年减值准备转移'], axis=1)
ressum['期末累计折旧'] = ressum.apply(lambda row: row[u'年初累计折旧']+row[u'当年度计提折旧额']+row[u'当年度折旧调整']+row[u'当年度折旧转移'], axis=1)
ressum['净值'] = ressum.apply(lambda row: row['期末原值']+row['期末减值准备']+row['期末累计折旧'], axis=1)
ressum['测算净值'] = ressum.apply(lambda row: row['期末原值']+row['期末减值准备']+row['期末累计折旧-EY'], axis=1)    
ressum['Diff'] = ressum.apply(lambda row: row['测算净值']-row['净值'], axis=1)   
        
ressum.to_excel(r'.\Result0712\res_sum_formulaChange02.xlsx')
#ParserError: Expected 47 fields in line 107, saw 48
#ValueError: ("invalid literal for int() with base 10: '1-'", 'occurred at index 9877')
endtime_total = datetime.datetime.now()

print ('|--Export details Successfully!')
print ('|--Totally costs %s seconds'%((endtime_total - starttime_total).seconds))