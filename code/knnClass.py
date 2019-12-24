# -*- coding: utf-8 -*-
import pandas as pd

import os


from sklearn import tree
os.environ["PATH"] += os.pathsep +'E:/python/release/bin'
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import matplotlib.pyplot as plt
import pydotplus as py
from sklearn.metrics import accuracy_score, auc, confusion_matrix, f1_score, precision_score, recall_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

plt.rcParams["font.sans-serif"] = ["FangSong"]
plt.rcParams["axes.unicode_minus"] = False
init_data = pd.read_excel('添加后的数据.xls')
# plt.rcParams["font.sans-serif"] = ["FangSong"]
# plt.rcParams["axes.unicode_minus"] = False
data = init_data[-init_data['品牌'].isin(['其他'])]
computerClass=['小米','联想','华硕','戴尔','华为','神舟','惠普','苹果']
shopNum=[]
sum=[]
num=[]
shopNames = list(set(data['店铺']))
for i in range(0,len(shopNames)):
   num.append(0)
for shop in data['店铺']:
   for i in range(0,len(shopNames)):
     if(shop==shopNames[i]):
        num[i]+=1
for shop in data['店铺']:
   for i in range(0,len(shopNames)):
     if(shop==shopNames[i]):
         shopNum.append(num[i])
data['店铺数量']=shopNum
data=data.drop(['电脑','店铺'],axis=1)
data.to_excel('knnClass.xls',sheet_name='dataset',index=None)
def read_data():
   computerData=pd.read_excel('knnClass.xls')
   computerData['品牌']=computerData['品牌'].map({
      '小米':0,'联想':1,'华硕':2,'戴尔':3,'华为':4,'神舟':5,'惠普':6,'苹果':7
   })
   return computerData
#决策树实现分类采用留出法
def get_data_ce():
   df_data=read_data()
   x=df_data[['店铺数量','价格','评论数', '好评数','差评数']]
   y=df_data['品牌']
   #按照8：2的比例随机分为训练集，测试集
   x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.4)
   #初始化决策模型
   de=DecisionTreeClassifier(random_state=2019)
   de.fit(x_train,y_train)
   y_pred=de.predict(x_test)
   print(len(y_pred))
   print('Test set predictions:\n{}'.format(y_pred))
   #用测试集评估模型的好坏
   print('决策树准确率：',de.score(x_test,y_test))
   ####模型评估###
   con_m=confusion_matrix(y_test,y_pred)
   df_con_m=pd.DataFrame(con_m,columns=computerClass,index=computerClass)
   df_con_m.index.name='真实值'
   df_con_m.columns.name='预测值'
   print(df_con_m)
   #获得决策树的预测概率
   y_score=de.predict_proba(x_test)
   print(y_score)

   dot_data=export_graphviz(de, max_depth=5, feature_names=['shopNums','prices','comments', 'GoodComments','poorComments'], class_names=['0','1','2','3','4','5','6','7'], filled=True, rounded=True,  special_characters=True)
   # 通过pydotplus将决策树规则解析为图形
   graph = py.graph_from_dot_data(dot_data)
   # 将决策树规则保存为PDF文件
   graph.write_pdf('tree.pdf')
   # 保存为jpg图片
   graph.write_jpg('juece.jpg')
def knn_class():
   df_data = read_data()
   x = df_data[['店铺数量','价格','评论数', '中评数','好评数','差评数']]
   y = df_data['品牌']
   # 按照8：2的比例随机分为训练集，测试集
   x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.40)
   from sklearn.neighbors import KNeighborsClassifier
   knn = KNeighborsClassifier(n_neighbors=1)
   knn.fit(x_train, y_train)
   y_pred = knn.predict(x_test)
   print('KNN set score:{:.2f}'.format(knn.score(x_test, y_test)))
def class_Log():
   df_data = read_data()
   x = df_data[['店铺数量','价格','评论数', '中评数','好评数','差评数']]
   y = df_data['品牌']
   # 按照6:4的比例随机分为训练集，测试集
   x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.40)
   from sklearn.linear_model import LogisticRegression
   lr = LogisticRegression(penalty='l2', solver="newton-cg", multi_class='multinomial')
   lr.fit(x_train, y_train)
   print('Logistic Regression模型测试集的准确率：%.3f' % lr.score(x_test, y_test))
   from sklearn.naive_bayes import GaussianNB
   clf = GaussianNB()
   clf.fit(x_train, y_train)
   print('GaussianNB模型测试集的准确率：%.3f' % clf.score(x_test, y_test))
if __name__ == '__main__':
   read_data()
   get_data_ce()
   knn_class()
   class_Log()