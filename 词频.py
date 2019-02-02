# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 16:08:08 2018
@author: Han

"""
##########################################
#功能模块:
#分词
#词频统计
#词云
#词云和底版融合
##########################################


import jieba
import re
from wordcloud import wordcloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
from random import randint

abel_mask = np.array(Image.open("a.jpg"))
image_colors = ImageColorGenerator(abel_mask)

f = open("pos2.txt", "r", encoding="gbk")
 
t = f.read()
f.close()
ls = jieba.lcut(t)

#没有用到
"""
for i in ls:
    if  i.flag==n:
        ls.append(i.word)
"""

#排除没有统计意义的词
excludes = {"总队","委员会","管理局","办公室","管理部","国家","中国","调查","民用","监督管理"}

counts = {}


#归并同义词
for word in ls:
    
    word =re.sub('省','', word)
    word =re.sub('市','', word)
    
    if len(word) == 1:
        continue
    elif word == "广东" or word == "广东省":
        rword = "广东"
    else:
        rword = word

    counts[rword] = counts.get(rword,0) + 1


for word in excludes:
    del counts[word]

items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 

ls2 = []

#词频前100的词输出到文件
output = open("词频100list.txt", "w+")  
for i in range(100):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count), file = output) 
    ls2.append(items[i][0])
output.close


#准备词云input
txt = " ".join(ls2)

#红橘配色
def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = randint(0,48)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

#stopword设置，没有用到
stopWORD =[]

stopWORD.append("国家")
stopWORD.append("中国")

#词云configuration
w = wordcloud.WordCloud( \
    width = 3000, height = 2100,\
    scale =4, background_color = "white",color_func = random_color_func, stopwords = stopWORD,
    mask=abel_mask, max_words=100,
    font_path = "msyh.ttc"    
    )
w.generate(txt)
w.to_file("职位词频2.jpg")

#将底版和词云融合
img1 = Image.open("a.jpg")
img2 = Image.open("职位词频2.jpg")
img_1 = img1.resize(img2.size)
img = Image.blend(img_1, img2, 0.9)
img.save("职位词频3.png")

#w.recolor(color_func=image_colors)




