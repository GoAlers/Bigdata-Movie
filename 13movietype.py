# -*- coding: utf-8 -*
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import MultipleLocator

data = pd.read_csv('lianxi/film-csv.txt',encoding = 'utf-8',delimiter = ';') #读取文件
# print ans0400
#数据清洗
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
ax0 = f.add_subplot(1,1,1)
plt.rcParams['font.sans-serif']=['simhei']   #绘图中文设置
plt.rcParams['axes.unicode_minus'] = False

lst = []
lsb = []
for i in range(len(data)):   #按照电影类型进行切分出票房
    for j in tt:
        if j in data[u'影片类型'][i]:
            lst.append(j.replace(u' ',u''))
            lsb.append(data[u'票房/万'][i])

lst = pd.DataFrame(lst,columns=[u'影片类型'])   #转成Dataframe类型
lsb = pd.DataFrame(lsb,columns=[u'票房'])
x_major_locator=MultipleLocator(0.05)
#x轴刻度间隔设置为1，并存在变量里
ax0.xaxis.set_major_locator(x_major_locator)
dftb = pd.concat([lst,lsb],axis = 1)    #将电影类型和票房进行合并
dftb = dftb.groupby(u'影片类型').sum().sort_values(u'票房')   #分组求和按票房排序
dftb.plot(kind = 'bar',title = u'各种类型片票房收入比较',ax = ax0) #绘图
plt.xlabel('影片类型',fontsize=14)
plt.legend()
plt.show()

