# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:36:28 2017

@author:鲲老头
功能：此程序找到只有浏览记录，没有其他任何记录的用户，过滤掉这些只看不买的用户,并重新
写入一个csv文件
"""


f = open("11.18-11.28_unhandle.csv")
context  = f.readlines()  

browse = []  #分别存放浏览，收藏，加购物车，购买行为,全部数据，只看不买的用户  
collect = []
add_Bcar = []
buy = []
all_data = []
never_buy = []
 
for line in context:
    line = line.replace('\n','')
    array = line.split(',')
    array = (array[0],array[1],array[2],array[3],array[4],array[5])   
    if array[0] == 'user_id':
        continue
    all_data.append(array)
    uid = array[0]
    type = int(array[2]) - 1
    if (type == 0):
        if (uid not in browse):
            browse.append(uid)
        continue
    if (type == 1):
        if (uid not in collect):
            collect.append(uid)
        continue        
    if (type == 2):
        if (uid not in add_Bcar):
            add_Bcar.append(uid)
        continue 
        
    if (type == 3):
        if (uid not in buy):
            buy.append(uid)
            

           
print('有浏览行为的用户:\t', len(browse))
print('有收藏行为的用户:\t', len(collect))
print('有加购物车行为的用户:\t', len(add_Bcar))
print('有购买行为的用户:\t', len(buy))
for line in browse:
    if (line not in collect) & (line not in add_Bcar) & (line not in buy):
        never_buy.append(line)

print('只有浏览，没有收藏、加购物车、购买行为的用户:\t', len(never_buy))

print(len(all_data))





i = 0
while i < len(all_data):
    if all_data[i][0] in never_buy:
        del all_data[i]
        i -= 1
    i += 1


f.close()
print(len(all_data))


wf = open('11.18-11.28_unhandle1.csv','w')
for i in range(len(all_data)):
    item = all_data[i]
    wf.write('%s,%s,%s,%s,%s,%s\n'%(item[0],item[1],item[2],item[3],item[4],item[5]))
wf.close()



        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
