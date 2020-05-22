# -*- coding:utf-8 -*-
import jieba
import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import imread
import wordcloud
# 设置词云路径
WC_FONT_PATH = 'C:/Windows/Fonts/simkai.ttf'

def cut_word():
    with open(r'lianxi/result.txt', 'r', encoding='utf8') as file:
        # 读取文件里面的全部内容
        comment_txt = file.read()
        # 使用jieba进行分割
        wordlist = jieba.cut(comment_txt)
        print('***********',wordlist)
        wl = "/".join(wordlist)
        # print(wl)
        return wl

def create_word_cloud():
    # 设置词云形状图片,numpy+PIL方式读取图片
    # 数据清洗词列表
    stop_words = ['就是', '不是', '但是', '还是', '只是', '这样', '这个', '一个', '什么', '电影', '没有']
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小,生成词云对象
    wc = wordcloud.WordCloud(mask=imread('lianxi/background1.png'), background_color=None,stopwords=stop_words, max_words=250, scale=4,mode='RGBA',
                   min_font_size=10,max_font_size=70, random_state=42,font_path="C:\\Windows\\Fonts\\SimHei.TTF")
    # 生成词云
    wc.generate(cut_word())
    img = imread('lianxi/color.jpg')
    cloud_colors = wordcloud.ImageColorGenerator(np.array(img))
    wc.recolor(color_func=cloud_colors)
    plt.figure(figsize=(20, 20))
    plt.rcParams['font.family'] = 'SimHei'
    # 开始画图
    plt.imshow(wc)
    # 为云图去掉坐标轴
    plt.axis("off")
    plt.savefig('dataout/图7豆瓣电影词语云.png')

if __name__ == '__main__':
    create_word_cloud()
