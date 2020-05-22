# -*- coding: utf-8 -*
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
#读入数据
df=pd.read_csv('lianxi/movie.csv',encoding='utf-8')
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
data_week = pd.read_csv(r'lianxi/movie.csv',nrows=50)['总票房（万）'].T.values
plt.figure(figsize=(10, 6))
xweek=range(0,len(data_week))
# xweek1=[i+0.3 for i in xweek]
plt.bar(xweek,data_week,color='g',width = 0.3,alpha=0.6,label=u'总票房')
plt.xticks(range(0,50),df['name'],rotation=90,fontsize=8)
plt.xlabel(u'电影名称')
plt.ylabel(u'票房收入')
plt.title(u'2009-2019中国电影票房综合排名')
plt.legend(loc='upper right')
plt.show()