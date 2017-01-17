# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 19:58:38 2017

@author: 鲲老头
use (uesr_id, item_id, time:25号) to train
"""


import time
import numpy as np
import math

f = open("tianchi_fresh_comp_train_user.csv")
context  = f.readlines()  #把每一行的原始数据放进context中,

 #readlines()自动将文件内容分析成一个行的列表，该列表可以由 Python 的 for. in .处理


train_day_Nov25 = []  #它里面存的都是前7天的所有三元组对象
forecast_Dec_day19 = []

for line in context:    #一个line就是源数据文件中的一行
    line = line.replace('\n','')
    array = line.split(',')        #split返回分割后的字符串列表
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H") #转换成时间格式来表示
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1],f_times) 
    if (int(times.tm_mday) < 25) & (int(times.tm_mon) == 11):
        train_day_Nov25.append(uid)

train_day_Nov25 = list(set(train_day_Nov25))             #去重复
print('training item number:\t', len(train_day_Nov25))




for line in context:    #一个line就是源数据文件中的一行
    line = line.replace('\n','')
    array = line.split(',')        #split返回分割后的字符串列表
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H") #转换成时间格式来表示
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1],f_times) 
    if (int(times.tm_mday) < 19) & (int(times.tm_mday) > 11)  & (int(times.tm_mon) == 12):
        forecast_Dec_day19.append(uid)
        
forecast_Dec_day19 = list(set(forecast_Dec_day19))             #去重复
print('testing item number:\t', len(forecast_Dec_day19))

########################特征和标签的预处理###############################
ui_dict = [{} for i in range(4)] 
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1],f_times)
    type = int(array[2]) - 1  # -1的是因为python下标从0开始
    if uid in ui_dict[type]:        #前7天4种操作的分别统计到ui_dict
        if (int(times.tm_mday)) < 24 & (int(times.tm_mon) == 11) & (int(type) == 0):
            train_day_Nov25.remove(uid)
            continue
        ui_dict[type][uid] += 1
    else:
        ui_dict[type][uid] = 1



########################打标签#######################
ui_buy = {}
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H")
    f_times = time.strftime("%Y-%m-%d %H", times)
    uid = (array[0],array[1],f_times)  #所有对象取出来
    if array[2]  == '4':
        ui_buy[uid] = 1

####################用(X,y)生成特征向量和样本标签
X = np.zeros((len(train_day_Nov25),4))
y = np.zeros((len(train_day_Nov25),))
id = 0
for uid in train_day_Nov25:
    for i in range(4):
        X[id][i] = math.log1p(ui_dict[i][uid] if uid in ui_dict[i] else 0)
    y[id] = 1 if uid in ui_buy else 0
    id += 1



print('--------------------- \n\n')
print('train number = ', len(y), 'positive number = ', sum(y), '\n') 
"""
"""
pX = np.zeros((len(forecast_Dec_day19),4))

id = 0
for uid in forecast_Dec_day19:
    for i in range(4):
        pX[id][i] = math.log1p(ui_dict[i][uid] if uid in ui_dict[i] else 0)
    id += 1

#print('pX = ', pX)


##########################训练模型#########################################
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()  #定义好模型以及超参数，这里使用默认的超参数
model.fit(X,y)
#把上面的刚准备好的训练样本的特征值和训练样本对应的标签塞进去，就能完成模型的训练，得到参数


#################### evaluate   #############################################
py = model.predict_proba(pX)

npy = []
for a in py:
    npy.append(a[1])    ##把属于1的概率全部取出来

py = npy




####  combine
lx = zip(forecast_Dec_day19, py)

###  sort by predict score
lx = sorted(lx, key = lambda x:x[1], reverse = True)



wf = open('ans.csv','w')
wf.write('user_id,item_id\n')
for i in range(len(lx)):
    item = lx[i]
    wf.write('%s,%s\n'%(item[0][0],item[0][1]))


















     
