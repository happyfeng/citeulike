#coding:utf-8

def get_rate(path):
    ##输出每篇文章被引用的概率
    content = open(r'D:\citeulike\items.dat','r')
    rate_content = open(path,'a')
    content_list = content.readlines()
    #print content_list
    for i in content_list:
        num = i.split(' ')
        rate = 1 - int(num[0])/5551.0 
        rate_content.write(str(rate)+ '\n')
    content.close()
    rate_content.close()
get_rate(r'D:\citeulike\rate.dat')
