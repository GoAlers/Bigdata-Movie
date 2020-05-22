# -*- coding: utf-8 -*
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import MultipleLocator
#绘图部分
data = pd.read_csv(r'lianxi/film-csv.txt',encoding = 'utf-8',delimiter = ';') #读取文件
data = data.iloc[:,:-1]   #去除文件中的非法数据
data = data.drop(0).drop_duplicates().reset_index().drop('index',axis = 1)    #由于第一行为空数据 去除 并去重 重置索引

t = []  #将电影类型按多种分割符切分
for i in range(len(data)):
    a = re.split(u' / |/|，|、| | ',data[u'影片类型'][i])
    for j in a:
        t.append(j)
t = set(t)  #将重复的类型去掉
tt = []
for i in t: #将不规范的类型去除 得出所有存在的类型
    if (len(i)<=2)|(i==u'合家欢'):
        tt.append(i)

f = plt.figure(figsize=(10,5))
ax2 = f.add_subplot(1,1,1)
plt.rcParams['font.sans-serif']=['simhei']   #绘图中文设置
plt.rcParams['axes.unicode_minus'] = False

lst = []
lsd = []
for i in range(len(data)):
    for j in tt:
        if j in data[u'影片类型'][i]:#按照导演进行切分出电影类型
            d = re.split(u'，|、|/| ',data[u'导演'][i])
            for k in d:
                lsd.append(k.replace(u' ',u''))
                lst.append(j.replace(u' ',u''))

lsd1 = list(set(lsd))
dict_t = {}
dict_d = {}
for i in range(len(lsd1)):  #将导演和电影类型转成连续量 进行绘图
    for j in range(len(lsd)):
        if lsd1[i] == lsd[j]:
            dict_d[i+1] = lsd[j]
            lsd[j] = i+1
for i in range(len(tt)):
    for j in range(len(lst)):
        if tt[i] == lst[j]:
            dict_t[i + 1] = lst[j]
            lst[j] = i+1
lsd = pd.DataFrame(lsd,columns=[u'导演']) #转成Dataframe类型
lst = pd.DataFrame(lst,columns=[u'影片类型'])
dftd = pd.concat([lsd,lst],axis = 1)
for i in range(len(dftd)):
    ax2.scatter(dftd[u'导演'][i], dftd[u'影片类型'][i])   #循环绘图

xl = '' #x轴 y轴给予提示
yl = ''
for i in range(1,4):
    xl+= 'i'+u'是'+dict_d[i]+u','
    yl+= 'i'+ u'是' + dict_t[i] + u','
ax2.set_xlabel(xl[:-1])
ax2.set_ylabel(yl[:-1])
ax2.set_title(u'导演执导过的影片类型')
plt.show()



