# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 19:02:49 2018

@author: Maddox.Meng
"""

import pandas as pd
from io import StringIO
from GDZC_module import cal1
from GDZC_module import cal2
from GDZC_module import cal3
from GDZC_module import cal4
from GDZC_module import category
from GDZC_module import category_sub
from GDZC_module import removeLineBreak
from GDZC_module import removeLineBreak2
import re
import datetime

cols = ['数据期间', '资产号', '资产次级编号', '资产类别', '资产子类', '工厂', '成本中心', '责任成本中心', '使用状态', '产权状态', '折旧码', '科目定位码', '使用期限', '购置年月', '购置日期', '资本化日期', '折旧开始日期', '已使用年限', '停用标志', '报废日期', '当年度报废标志:Y/N', '数量', '数量单位', '年初原值', '当年原值增加', '当年原值减少', '期末原值', '年初减值准备', '当年减值准备计提额', '当年减值准备转移', '期末减值准备', '年初累计折旧', '当年度计提折旧额', '当年度折旧调整', '当年度折旧转移', '期末累计折旧', '期末净值', '供应商', '投资订单', '序列号', '存货号', '设备号', '资产名称', '资产详细描述', '资产主号文本', '使用者', '实物所在地']

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

#dict_subCategs = {"W_土地使用权": W_TD}

plist = [r'a_am_staticdata_20180701_000_000.dat']

#plist = [r'.\固定资产\step 1\数据库\a_am_staticdata_20160701_000_004.dat']


starttime_total = datetime.datetime.now()
#for list in subCategs:
cnt = 1
for k in dict_subCategs: #k = 'G_电子设备'
    
    frames = [] # Frames should be here, not outside the the whole loop!!!
    
    starttime = datetime.datetime.now()
    print ('|--0%d*****%s*****'%(cnt, k))
    print ('|--'+str(dict_subCategs[k]))
    
    i=1
    for p in plist:
        print ('   |--' + p.split('\\')[-1])
        with open(p, 'r', encoding='gb18030', errors='ignore') as f:
            
            #raw = removeLineBreak(f) #相当于f.read(), 替换了", |+|, 还有非末尾换行符
            raw = removeLineBreak2(f) #相当于f.read(), 替换了", |+|, 还有非末尾换行符
            input = StringIO(raw)
            
            print ('      |--01.Read database:')
            df = pd.read_csv(input, sep="|", skiprows=0, names=cols, engine='python')
            
            print ('      |--02.Filter category: %s'%k)

            #df = df.loc[df['资产类别'].isin(list)]
            dff = df.copy(deep=True)
            dff = dff.loc[dff['资产类别'].isin(dict_subCategs[k])]
            
            if dff.empty:
                print ('      |--03.Warning: This data source contains NO %s'%k)
            else:
                print ('      |--03.Calculate columns')
                dff['database'] = i
                #dff[u'当年度计提折旧额-EY'] = dff.apply(lambda row: cal1(row[u'使用期限'],row[u'已使用年限'],row[u'年初原值']), axis=1)
                dff['当年度计提折旧额-EY'] = dff.apply(lambda row: cal1(row), axis=1)
                dff['期末累计折旧-EY']    = dff.apply(lambda row: cal2(row), axis=1)
                dff['期末净值-EY']        = dff.apply(lambda row: cal3(row), axis=1)
                dff['Diff']              = dff.apply(lambda row: cal4(row), axis=1)
                
                dff['EYtype1']= dff.apply(lambda row: category(row[u'资产类别']), axis=1)
                dff['EYtype2']= dff.apply(lambda row: category_sub(row[u'资产类别']), axis=1)
            
            frames.append(dff)           
        i+=1
    
    print ('   |--04.Combine %s dataframe'%len(plist))
    res = pd.concat(frames, sort=False)
    print ('   |--05.Export to: res_detail_%s.csv'%k)
    #res.to_excel(r'.\Result0706\res_detail_%s.xlsx'%(k))
    res.to_csv(r'.\Result0712\res_detail_%s.csv'%(k), encoding='utf_8_sig')
    
    endtime = datetime.datetime.now()
    print ('   |--This category contains %s rows'%(dff.shape[0]))
    print ('   |--This category costs %s seconds'%((endtime - starttime).seconds))
    
    cnt+=1

endtime_total = datetime.datetime.now()

print ('|--Export details Successfully!')
print ('|--Totally costs %s seconds'%((endtime_total - starttime_total).seconds))