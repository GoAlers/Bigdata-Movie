#encoding:utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression

#绘图部分
data = pd.read_csv('lianxi/film-csv.txt',encoding = 'utf-8',delimiter = ';') #读取文件
data = data.iloc[:,:-1]   #去除文件中的非法数据
data = data.drop(0).drop_duplicates().reset_index().drop('index',axis = 1)    #由于第一行为空数据 去除 并去重 重置索引
# print data

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

#评分预测
id = [1050,1114,1048,1488,1102] #五个用户id
data1 = pd.read_csv('lianxi/score.log',delimiter=',',encoding = 'utf-8',header=0,names = [u'电影名称',u'userid',u'score'])
data1 = data1[data1[u'userid'].isin(id)]   #去除五个用户 相关数据

data1[u'电影名称'] = data1[u'电影名称'].str.strip()   #去除电影名称的空格
all = []#用来存预测结果
for k in range(len(id)):        #循环五次 建模 进行预测
    dfp1 = data1[data1[u'userid']==id[k]].reset_index().drop('index',axis = 1)
    datamerge = pd.merge(data,dfp1,on=u'电影名称')    #用merge 将电影详细信息 与新用户评分合并
    lst = []
    lsd = []
    lsr = []
    for i in range(len(datamerge)):  #切分出电影类型 和导演 以及对应的票房
        for j in tt:
            if j in datamerge[u'影片类型'][i]:
                d = re.split(u'，|、|/| ',datamerge[u'导演'][i])
                for k in d:
                    lsd.append(k.replace(u' ', u''))
                    lst.append(j.replace(u' ', u''))
                    lsr.append(datamerge[u'score'][i])
    lsd1 = list(set(lsd))
    for i in range(len(lsd1)):  #将电影类型和票房转成 连续量 以便机器训练
        for j in range(len(lsd)):
            if lsd1[i] == lsd[j]:
                lsd[j] = i + 1
    for i in range(len(tt)):
        for j in range(len(lst)):
            if tt[i] == lst[j]:
                lst[j] = i + 1
    lsd = pd.DataFrame(lsd, columns=[u'导演'])
    lst = pd.DataFrame(lst, columns=[u'影片类型'])
    lsr = pd.DataFrame(lsr, columns=[u'评分'])

    a = pd.concat([lsd, lst, lsr], axis=1)
    trainx = a.iloc[:, 0:2]  # 电影类型和 导演 作为特征量
    trainy = a.iloc[:, 2:3]  # 评分作为样本值
    l = LinearRegression()  # 建模
    l.fit(trainx, trainy)  # 训练

    anstest = pd.DataFrame([[5,10]],columns=[u'导演',u'影片类型'])
    ans = l.predict(anstest)#预测
    all.append(ans[0][0]) #得出结果
print (u'评分最大值是'+'%.2f'%max(all)) #输出
print (u'评分最小值是'+'%.2f'%min(all))
print (u'评分中位数值是'+'%.2f'%np.median(all))
print (u'评分平均值是'+'%.2f'%np.mean(all))


