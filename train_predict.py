# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:14:38 2017

@author: Administrator
功能:该程序的主要用于对模型的训练,预测
"""
import time
import numpy as np
import math



trainset= []
f = open("testdata.csv")
context  = f.readlines()

ui_buy = {}
for line in context:    
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1]) 
    if((int(times.tm_mday) < 30) & (int(times.tm_mon) == 11)) :
        trainset.append(uid)
    else:
        if (array[2]  == '4'):             #训练集打标签预处理
            ui_buy[uid] = 1 
   
trainset = list(set(trainset))
print('U-I:\t',len(trainset))
########################训练集特征预处理###############################
ui_dict = [{} for i in range(4)] 
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")#字符串转时间格式
    f_times = time.strftime("%Y-%m-%d %H", times)#时间转字符串
    uid = (array[0],array[1])
    type = int(array[2]) - 1 
    if((int(times.tm_mday) < 30) & (int(times.tm_mon) == 11)) :
        if uid in ui_dict[type]:
            ui_dict[type][uid] += 1
        else:
            ui_dict[type][uid] = 1
f.close()  

#######################对测试集/预测集合的预处理################################
f = open("tianchi_fresh_comp_train_user4.csv")
context  = f.readlines()
predictset = []
for line in context:    
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1]) 
    predictset.append(uid)
predictset = list(set(predictset))
  
pre_ui_dict = [{} for i in range(4)] 
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")#字符串转时间格式
    f_times = time.strftime("%Y-%m-%d %H", times)#时间转字符串
    uid = (array[0],array[1])
    type = int(array[2]) - 1 
    if uid in pre_ui_dict[type]:
        pre_ui_dict[type][uid] += 1
    else:
        pre_ui_dict[type][uid] = 1

f.close()

####################用(X,y)训练集/预测集生成特征向量和样本标签#######################
X = np.zeros((len(trainset),4))
y = np.zeros((len(trainset),))
id = 0
for uid in trainset:
    for i in range(4):
        X[id][i] = math.log1p(ui_dict[i][uid] if uid in ui_dict[i] else 0)
    y[id] = 1 if uid in ui_buy else 0
    id += 1
print('x=',X)
print('y=',y)
print('train number = ', len(y), 'positive number = ', sum(y), '\n') 

pX = np.zeros((len(predictset),4)) #测试/预测特征向量
id = 0
for uid in predictset:
    for i in range(4):
        pX[id][i] = math.log1p(pre_ui_dict[i][uid] if uid in pre_ui_dict[i] else 0)
    id += 1
print('px=',pX)

##########################训练模型#########################################
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()  #定义好模型以及超参数，这里使用默认的超参数
model.fit(X,y)
#把上面的刚准备好的训练样本的特征值和训练样本对应的标签塞进去，就能完成模型的训练，得到参数


#################### 预测   #############################################

py = model.predict_proba(pX)


npy = []
for a in py:
    npy.append(a[1])    ##把属于1的概率全部取出来
py = npy



####  把测试/预测集一一对应打包，排序
lx = list(zip(predictset, py))
###  sort by predict score
lx = sorted(lx, key = lambda x:x[1], reverse = True)



wf = open('ans_unhandle.csv','w')
wf.write('user_id,item_id\n')
for i in range(len(lx)):
    item = lx[i]
    wf.write('%s,%s\n'%(item[0][0],item[0][1]))









