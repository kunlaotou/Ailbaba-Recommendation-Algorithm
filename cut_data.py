# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:43:09 2017
@author:鲲老头
功能:该程序主要是分割n天(自己定义时间区间)的记录，构建一次训练集
"""
import time

f = open("testdata.csv") #读取的文件
context  = f.readlines()  


all_data = []

 
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    array = (array[0],array[1],array[2],array[3],array[4],array[5])   
    if array[0] == 'user_id':
        continue
    times = time.strptime((array[-1]),"%Y-%m-%d %H") #转换成时间格式来表示
    f_times = time.strftime("%Y-%m-%d %H", times)
    if (int(times.tm_mday) >= 7) & (int(times.tm_mday) <= 17) & (int(times.tm_mon) == 12):
        all_data.append(array)
f.close()
print(len(all_data))
all_data = set(all_data)  #去重复
print(len(all_data))

wf = open('testdata1.csv','w') #写入的文件
for line in all_data:
    wf.write('%s,%s,%s,%s,%s,%s\n'%(line[0],line[1],line[2],line[3],line[4],line[5]))
wf.close()

