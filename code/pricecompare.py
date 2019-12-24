# -*- coding: utf-8 -*-
import pandas as pd
from PIL import Image
import numpy as  np
import jieba
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

plt.rcParams["font.sans-serif"] = ["FangSong"]
plt.rcParams["axes.unicode_minus"] = False
colors = ['linen', 'mediumspringgreen', 'royalblue', 'lavender', 'mediumpurple', 'palegreen', 'peachpuff', 'goldenrod']
data = []
computerClass = ['小米', '联想', '华硕', '戴尔', '华为', '神舟', '惠普', '苹果']
# 处理数据
shaidata = pd.read_excel('筛选后的数据.xls')
computerBrand=[]
for i in range(0,len(shaidata['电脑'])):
    if(fuzz.ratio('联想,ThinkPad',shaidata['店铺'][i])>22):
          computerBrand.append('联想')
    else :
        if(fuzz.ratio('小米',shaidata['店铺'][i])>22 ):
          computerBrand.append('小米')
        else:
            if (fuzz.ratio('华硕',shaidata['店铺'][i])>22):
                computerBrand.append('华硕')
            else:
                if (fuzz.ratio('华为，荣耀',shaidata['店铺'][i])>22):
                    computerBrand.append('华为')
                else:
                     if (fuzz.ratio('神舟',shaidata['店铺'][i])>22 ):
                         computerBrand.append('神舟')
                     else:
                         if(fuzz.ratio('戴尔',shaidata['店铺'][i])>22 ):
                             computerBrand.append('戴尔')
                         else:
                             if (fuzz.ratio('Apple',shaidata['店铺'][i])>22 ):
                                 computerBrand.append('苹果')
                             else:
                                 if (fuzz.ratio('惠普',shaidata['店铺'][i])>22 ):
                                     computerBrand.append('惠普')
                                 else:
                                     computerBrand.append('其他')

shaidata['品牌']=computerBrand
shaidata.to_excel('添加后的数据.xls',sheet_name='电脑数据',index=None)
dat = shaidata['价格']

def price_data():
    for i in range(0, 8):
        data.append(0)
    for i in range(0, 8):
        data[i] = pd.read_excel('8种常用品牌电脑分类.xls', sheet_name=computerClass[i])


# 画出密度图
def price_p():
    fig, axes = plt.subplots(4, 2, figsize=(15, 7))
    fig.legend().set_title('京东常用的8种品牌电脑的价格密度图')
    for i in range(0, 8):
        if (i < 4):
            sns.distplot(data[i]['价格'], rug=True, ax=axes[i, 0])
            sns.distplot(data[i]['价格'], hist_kws={'color': colors[i], 'label': computerClass[i]}, ax=axes[i, 0], )
            axes[i, 0].legend(computerClass[i], fontsize='15')
            axes[i, 0].text(x=0, y=0, s=None, color='black', fontsize='20')
        else:
            sns.distplot(data[i]['价格'], rug=True, ax=axes[i % 4, 1])
            sns.distplot(data[i]['价格'], hist_kws={'color': colors[i], 'label': computerClass[i]}, ax=axes[i % 4, 1], )
            axes[i % 4, 1].legend(computerClass[i], fontsize='15')
            axes[i % 4, 1].text(x=0, y=0, s=None, color='black', fontsize='20')
    plt.show()
    fig.savefig('京东常用的8种品牌电脑的价格密度图.png', dpi=600)
# 不同品牌电脑的价格散点图
def price_san(value):
    fig, axes = plt.subplots()
    axes.set_title('基于品牌的'+value+'散点图')
   # sns.stripplot(x='品牌', y='价格', data=shaidata)
    sns.swarmplot(x='品牌', y=value, data=shaidata,  palette="Set2")
    plt.show()
    fig.savefig('基于品牌的'+value+'散点图.png',dpi=600)


# 不同品牌电脑价格的小提琴+散点图
def violin_san(value):
    fig, axes = plt.subplots()
    axes.set_title('基于品牌的'+value+'小提琴+散点图')
    sns.violinplot(x='品牌', y=value, data=shaidata, inner=None)
    sns.swarmplot(x='品牌', y=value, data=shaidata,
                  color="white", edgecolor="gray")
    plt.show()
    fig.savefig('基于品牌的'+value+'小提琴+散点图.png',dpi=600)

if __name__ == '__main__':
    param=['价格','评论数','好评数','差评数']
    price_data()
    price_p()
    for value in param:
         price_san(value)
         violin_san(value)
