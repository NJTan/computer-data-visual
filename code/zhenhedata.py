# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import numpy as np
import re
import matplotlib.pyplot as plt
from xlwt import Workbook
from fuzzywuzzy import fuzz
sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})
data = pd.read_excel("京东部分电脑销售以及评论数据.xls")
plt.rcParams["font.sans-serif"] = ["FangSong"]
plt.rcParams["axes.unicode_minus"] = False
#删除为店名为0的整行数据
print(data)
data2 = data[-data.店铺.isin([0])]
def e_value(e_data):
    perce=np.percentile(e_data,(25,50,75),interpolation='midpoint')
    Q1=perce[0]#上四分数
    Q3=perce[2]#下四分数
    IQR=Q3-Q1
    ulim=Q3+1.5*IQR
    llim=Q1-1.5*IQR
    return ulim,llim
# e_price = np.percentile(data2['价格'],(25,50,75), interpolation='midpoint')
# e_comments=np.percentile(data2['中评数'],(25,50,75),interpolation='midpoint')
# e_good=np.percentile(data2['评论数'],(25,50,75),interpolation='midpoint')
# e_general=np.percentile(data2['好评数'],(25,50,75),interpolation='midpoint')
# e_poor=np.percentile(data2['差评数'])
#剔除数据函数
val=''
def del_e_value(x,y,val,dat):
    for value in dat[val]:
        if(y>=value or value>=x):
            dat=dat[-dat[val].isin([value])]
    return dat
e_price_x,e_price_y=e_value(data2['价格'])
print(e_price_y,e_price_x)
nedata1=del_e_value(e_price_x,e_price_y,'价格',data2)
e_com_x,e_com_y=e_value(nedata1['评论数'])
newdata2=del_e_value(e_com_x,e_com_y,'评论数',nedata1)
e_good_x,e_good_y=e_value(newdata2['好评数'])
newdata3=del_e_value(e_good_x,e_good_y,'好评数',newdata2)
e_zong_x,e_zong_y=e_value(newdata3['中评数'])
newdata3=del_e_value(e_zong_x,e_zong_y,'中评数',newdata3)
e_poor_x,e_poor_y=e_value(newdata3['差评数'])
data2=del_e_value(e_poor_x,e_poor_y,'差评数',newdata3)

print(len(data2))
#sns.boxplot(data=data2['价格'],axis=1)
data3=data2.drop(['价格','中评数','差评数','评论数'],axis=1)
# data4=data2.drop(['评论数','好评数'],axis=1)
#data3=data2.drop(['评论数','好评数'],axis=1)


#获取指定的列
shops=data2["店铺"]
num=[] #店铺的数量
print(shops)
classes=[]#电脑店铺的分类
computerClass=['小米','联想','华硕','戴尔','华为','神舟','惠普','苹果']#常用8种电脑的分类，将电脑的价格进行分类，然后画饼图，确定那种电脑的数量。
shopNames = list(set(shops))
goodComputer=[]
j=0
a='小米'
b='联想,ThinkPad'
c='华硕'
d='戴尔'
e='华为,荣耀'
f='神舟'
h='惠普'
g='Apple'
pipei=np.array([a,b,c,d,e,f,h,g])
sum=[]
for i in range(0,8):
    sum.append(0)
    goodComputer.append(0)
for i in range(0,len(shopNames)):
    num.append(0)
    classes.append(0)
for shop in shops:
    for i in range(0,len(shopNames)):
        if(shop==shopNames[i]):
            num[i]+=1
i = 0
for i in range(0,len(shopNames)):
    print(num[i])
for i in range(0,len(shopNames)):
    data2.店铺.isin([shopNames[i]])
    classes[i]=data2[data2.店铺.isin([shopNames[i]])]
for i in range(0,8):
    if(i!=1 or i!=4):
       goodComputer[i]=data2.loc[data2['店铺'].str.contains(pipei[i])]

goodComputer[1]=data2.loc[data2['店铺'].str.contains('联想')]
goodComputer[1]=goodComputer[1].append(data2.loc[data2['店铺'].str.contains('ThinkPad')])
goodComputer[4]=data2.loc[data2['店铺'].str.contains('华为')]
goodComputer[4]=goodComputer[4].append(data2.loc[data2['店铺'].str.contains('荣耀')])
for j in range(0,len(shopNames)):
        #print(shopNames[j])
        if ((fuzz.ratio(a, shopNames[j])) >= 22):
           sum[0]+=num[j]
        if ((fuzz.ratio(b, shopNames[j])) >= 22):
            sum[1] += num[j]
        if ((fuzz.ratio(c, shopNames[j])) >= 22):
            sum[2] += num[j]
        if ((fuzz.ratio(d, shopNames[j])) >= 22):
            sum[3] += num[j]
        if ((fuzz.ratio(e, shopNames[j])) >= 22):
            sum[4]+=num[j]
        if ((fuzz.ratio(f, shopNames[j])) >=22):
            sum[5] += num[j]
        if ((fuzz.ratio(e, shopNames[j])) >=22):
            sum[6] += num[j]
        if ((fuzz.ratio(f, shopNames[j])) >=22):
            sum[7] += num[j]
for i in range(0,8):
    print("各种品牌电脑",goodComputer[i])
# print(len(computerClass))
# print(len(shopNames))
#computer8大分类的数据
computerName=[]



#b='小米官方旗舰店'
#print(fuzz.ratio(a,b))
print(len(classes[0]))
#将不同的店家进行分类，以便获得不同的店家的数据可视化
writer=pd.ExcelWriter(r"8种常用品牌电脑分类.xls")
for i in range(len(computerClass)):
    goodComputer[i].to_excel(writer, sheet_name=str(computerClass[i]), index=False)  # 注意加上index=FALSE 去掉index列
writer.save()
#筛选后的数据
print(shops)
writer = pd.ExcelWriter(r"筛选后的数据.xls");
data2.to_excel(writer,sheet_name="筛选后的数据",index=0)
writer.save()

#画饼图，表示不同品牌手机的数量
def age_pie():
    plt.rcParams['font.family']='SimHei'
    labels=computerClass
    sizes=sum
    explode=(0,0.1,0,0,0,0,0,0)
    colors=['tomato', 'lightskyblue', 'goldenrod', 'green','mediumaquamarine','turquoise','goldenrod','rosybrown']
    plt.figure(figsize=(10,6))
    plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=False,pctdistance=0.8,\
            startangle=180,textprops={'fontsize':16,'color':'slategrey'})
    plt.title("京东常用的8种品牌电脑的店铺数量分布图")
    plt.axis('equal')
    plt.legend(loc='upper right')
    plt.savefig('京东常用的8种品牌电脑的店铺数量分布图.png', dpi=600)
    plt.show()
    dataType=[]
def box_fig(dat,dataType,color):
    plt.close()
    data=dat.drop(dataType,axis=1)
    plt.rcParams['font.family'] = 'SimHei'
    sns.boxplot(sym='o',
    data=data,
    whis=1.5,
    meanline=False,
    showmeans=True,
    showbox=True,
    showfliers=True,
    notch=False,
    color=color,
    )
    plt.title("箱型图")
    plt.savefig('京东电脑差评与中评盒图.png', dpi=600)
    plt.show()



    # 好评数颜色
if __name__ == '__main__':
    c = sns.xkcd_rgb['hot purple']
   # colors[0]=c
    #价格、差评和中评数
    age_pie()
    box_fig(data2,['价格','好评数','中评数','差评数'],c)
    box_fig(data2,['评论数','中评数','差评数'],'lightsalmon')
    box_fig(data2,['价格','评论数','好评数'],'palegreen')
   #条形图
  # sns.countplot(y='price',hue='品牌')

