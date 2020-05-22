import numpy as np
import pandas as pd
import jieba
import wordcloud
from scipy.misc import imread
import matplotlib.pyplot as plt
from pylab import mpl
import seaborn as sns  # 导入seaborn

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus']
# 设置风格
import matplotlib.style as psl
psl.use('bmh')

import warnings
warnings.filterwarnings('ignore') 

data = pd.read_csv('lianxi/中国票房数据.csv',engine='python')
data.head()

# 词频分析
stop_word = pd.read_csv('lianxi/tyc.txt', encoding='utf-8')
stop_word.columns = ['key', '']
stop_list = stop_word['key'].tolist()
print(stop_list[:5])

#停用词读取

def txt_cut(f):
    return [w for w in jieba.cut(f) if w not in stop_list]  # 创建函数
word_list = []
for line in data[data['电影名'].notnull()]['电影名'].tolist():
    for word in txt_cut(line):
        word_list.append(word)
print(word_list[:5])
#分词

word_count = pd.Series(word_list).value_counts().sort_values(ascending=False)[0:20]
# print(word_count)
# 分析词频
# 出图
fig = plt.figure(figsize=(12,5))
x = word_count.index.tolist()
y = word_count.values.tolist()
#sns.barplot(x, y, palette="BuPu_r")
sns.barplot(x, y, palette="Set3")
plt.title('电影数据词频Top20')
plt.ylabel('count')
sns.despine(bottom=True)
plt.savefig('dataout/图9词频分析.png')



