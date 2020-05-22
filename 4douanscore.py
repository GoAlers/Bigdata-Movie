# -*- coding:utf8 -*-
#首先用于确定编码，加上这句
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
conn = pymysql.connect(host="localhost", user="root", password="123456", db="maoyan", charset="utf8", port=3306)
cursor = conn.cursor()
sql = "select * from movies limit 20"
data = pd.read_sql(sql, conn)
df = data.sort_values(by="score", ascending=1)
a = df[['name', 'score']]

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 6))
xweek = range(0, len(df['name']))
plt.bar(df['name'], df['score'], color='g', width=0.3, alpha=0.6, label=u'截取数据前20')
plt.xticks(xweek, df['name'], rotation=90, fontsize=8)
plt.xlabel(u'电影名称')
plt.ylabel(u'电影评分')
plt.title(u'豆瓣电影高分top20')
plt.legend(loc='upper right')
plt.show()