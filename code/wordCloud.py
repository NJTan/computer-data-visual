# -*- coding: utf-8 -*-
from PIL import Image
import numpy as  np
import jieba
import pandas as pd
import matplotlib.pyplot as plt
#词云生成工具
from wordcloud import WordCloud
#需要对中文进行处理
import matplotlib.font_manager as fm
#读取并清理数据

data = pd.read_excel("筛选后的数据.xls")
data['电脑'].to_csv('computername.txt', index=False)
def read_txt():
    with open('computername.txt','r',encoding='utf-8') as fd:
        txt=fd.read()
        re_move=['"','?','/','\n','\xa0',',','','"|“|”|</ a>|<a>|★|\'',' ','(',')','@','+','】','【','（','）','-','[',']','|']
        for i in re_move:
            txt=txt.replace(i,"")
        word=jieba.lcut(txt)
        print(word)
    with open('txt_save.txt','w',encoding='utf-8') as file:
      for i in word:
          file.write(str(i)+' ')
#产生词云图片
def img_txt():
    bg = np.array(Image.open('backgroud.png'))
    with open('txt_save.txt','r',encoding='utf-8') as f:
        txt=f.read()
    word=WordCloud(background_color='white',
                       width=800,height=800,
                       font_path='simhei.ttf',
                       mask=bg,).generate(txt)
    word.to_file('ciyun.png')
    plt.imshow(word)
    plt.axis('off')
    plt.show()
if __name__ == '__main__':
    read_txt()
    img_txt()