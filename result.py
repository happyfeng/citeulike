#coding:utf-8
import os
import pickle
'''
filelist = os.listdir(r'D:\citeulike\dic\result\cos')
lists = []
dic = {}
for j in range(20):
    content = open(r'D:\citeulike\dic\result\cos'+'\\'+filelist[j],'r')
    for i in content.readlines():
        k = i.rstrip().split(',')[0][2:-2]
        if k in dic.keys():

            dic[k] = float(dic[k]) +float(i.rstrip().split(',')[1][1:-1])
        else:
            dic[k] = float(i.rstrip().split(',')[1][1:-1])
    content.close()

print len(dic)
print dic
pickle.dump(dic,open(r'D:\citeulike\dic\result\cos.dump','wb'))
'''
filelist = os.listdir(r'D:\citeulike\dic\result\div')
lists = []
dic = {}
for j in range(20):
    content = open(r'D:\citeulike\dic\result\div'+'\\'+filelist[j],'r')
    for i in content.readlines():
        k = i.rstrip().split(',')[0][2:-2]
        if k in dic.keys():

            dic[k] = float(dic[k]) +float(i.rstrip().split(',')[1][1:-1])
        else:
            dic[k] = float(i.rstrip().split(',')[1][1:-1])
    content.close()

print len(dic)
print dic
pickle.dump(dic,open(r'D:\citeulike\dic\result\div.dump','wb'))
