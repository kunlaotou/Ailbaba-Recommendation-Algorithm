# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:56:41 2017

@author: Administrator
功能:该程序的主要是找出浏览数和购买数比例过大的用户，并按从大到小输出
"""

import time




f = open("testdata.csv")
context  = f.readlines() 

users = []
user_dict = [ {} for i in range(4) ]

for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    array = (array[0],array[1],array[2],array[3],array[4],array[5])   
    if array[0] == 'user_id':
        continue
    uid = array[0]
    type = int(array[2]) - 1
    if (uid not in users):
        users.append(uid)
    if uid in user_dict[type]: 
        user_dict[type][uid] += 1
    else:
        user_dict[type][uid] = 1
f.close()
print('用户个数:\t',len(users))

rate_dict = {}
for line in user_dict[0]:
    #print(user_dict[0][line]) value
    #print(line) key
    for lines in user_dict[3]:
        if(lines == line):
            rate_dict[line] = (user_dict[0][line])/(user_dict[3][lines])
            
rate_dict_after = sorted(rate_dict.items(), key = lambda item:item[1],reverse = True)
print(rate_dict_after)   


