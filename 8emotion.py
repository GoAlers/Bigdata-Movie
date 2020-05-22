# -*- coding:utf-8 -*-

import jieba
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from snownlp import SnowNLP
from scipy.misc import imread
import wordcloud
# 设置词云路径

def data_show():
    f = open(r'lianxi/result.txt', 'r', encoding='utf-8')
    list = f.readlines()
    sentimentslist = []
    for i in list:
        s = SnowNLP(i)
        sentimentslist.append(s.sentiments)
    print(sentimentslist)
    # print(len(sentimentslist))
    plt.style.use("ggplot")
    plt.rcParams['font.family'] = 'SimHei'
    plt.hist(sentimentslist, bins=10,color='b')
    plt.xlabel('情感概率')
    plt.ylabel('数量')
    plt.title('《囧妈》短评情感分析')
    plt.savefig('dataout/8情感分析.png')

if __name__ == '__main__':
    # create_word_cloud()
    data_show()