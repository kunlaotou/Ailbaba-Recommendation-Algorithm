# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 18:48:49 2017

@author: Administrator
要提交的数据和item子集做一个取交集,然后输出满足 预测的商品在商品子集表中  的数据
"""
import sys

g = open("tianchi_fresh_comp_train_item.csv")
offer_data  = g.readlines() 
offer_set = []
for line in offer_data:
    line = line.replace('\n','')
    array = line.split(',')        #split返回分割后的字符串列表
    item_context = array[0]
    if array[0] == 'item_id':
        continue
    offer_set.append(item_context)
offer_set = set(offer_set)  
print('tianchi_fresh_comp_train_item文件的item个数:\t',len(offer_set))
g.close()





f = open("ans.csv")
result_data  = f.readlines() 

result_set = []
orig_set = []
for line in result_data:
    line = line.replace('\n','')
    array = line.split(',')        #split返回分割后的字符串列表
    context = array[1]
    uid = (array[0],array[1])
    if array[0] == 'user_id':
        continue
    result_set.append(context)
    orig_set.append(uid)
len_orig_set = len(orig_set)
result_data = len(result_data)
result_set = set(result_set)  
print("预测文件的item个数:\t",len(result_set))
inter = result_set & offer_set
print("俩个文件取交集的个数:\t",len(inter))
f.close()


fin_f = open('ans_test.csv','w')
fin_f.write('user_id,item_id\n')
i = 0
f = open("ans.csv")
result_data  = f.readlines() 
for line in result_data:
    line = line.replace('\n','')
    array = line.split(',')
    context = array[1]
    if array[0] == 'user_id':
        continue
    if context in inter:
        item = orig_set[i]
        fin_f.write('%s,%s\n'%(item[0],item[1]))
    i += 1

f.close()