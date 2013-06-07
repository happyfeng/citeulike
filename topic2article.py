# coding:utf-8
import pickle
import gensim
import stopword
import FeatureSimilarity
import numpy as np
import rank_topic
import get_corpus
import os

article = "Exploring complex networks"
article_no = 2
t = open(r'D:\citeulike\raw-data.csv','r').readlines()
cos = open(r'D:\citeulike\dic'+'\\cos_'+article+'.dat','a')
div = open(r'D:\citeulike\dic'+'\\div_'+article+'.dat','a')

def get_tp():
    # 获取16000篇文章的每篇文章概率主题分布，保存便于调用。
    topic_list = []
    diction = gensim.corpora.Dictionary.load('citeulike.dict')
    batch_lda = gensim.models.LdaModel.load('online_lda_100.lda')
    content = open(r'D:\citeulike\dic\temp.dat', 'r').readlines()
    for i in content:
        text_list = stopword.get_txt(i)
        doc_bow = diction.doc2bow(text_list)
        doc_lda = batch_lda[doc_bow]
        topic_list.append(dict(doc_lda))  # 以字典的形式存储，方便获取
    pickle.dump(topic_list, open(r'D:\citeulike\dic\all_onlinetopic_100.dump', 'w'))

def to_article(rank,lda):
    #rank   排序后的主题列表
    value = np.arange(1,0,-0.1)  # 主题对应的分值 np.arange(1,0,-0.1)
    tp = pickle.load(open(r'D:\citeulike\dic\all_'+lda[:-4]+'.dump', 'r'))
    # 遍历每篇文章，通过排序后主题计算与该主题最相关的文章
    rank_list = []
    for m in range(len(tp)):
        rate2 = 0
        t = 0
        nov_rate = rank_topic.seen('1', m) #乘以新奇性
        for n in rank:
            if n in tp[m].keys():
                j = rank.index(n)
                # 计算排序主题与主题概率的乘积，方便选取最相似的文章
                rate = value[j] * tp[m][n]
                t = t +1
            else:
                rate = 0
            rate2 += rate
        if t != 0:
            #乘以文章新奇性概率，除以文章中主题出现在rank中的个数，防止主题过多，结果越大
            sum_rate = rate2*nov_rate / t
        else:
            sum_rate =rate2*nov_rate
        rank_list.append(sum_rate)  # 按文章顺序排列的相似性值
    return rank_list
    

def txt_list(txts,N,lda):
    #获取推荐的文章列表
    
    a = FeatureSimilarity.rank_tp(txts,lda) 
    b = to_article(a,lda)
    texts = sorted(b,reverse = True)[0:N+1]
    rec_list = []
    for i in texts:
        rec_list.append(b.index(i))
    #print rec_list
    #for j in rec_list:
        #title = t[j].split(',')[3][1:-1]
    return rec_list #推荐的文章列表

if __name__ == '__main__':
    
    #tt = open(r'D:\citeulike\dic\result\rank.dat','a')
    for c in ['online_lda_50.lda','batch_lda_50.lda','batch_lda_100.lda','online_lda_100.lda']:
        for d in [5,10,15,20]:
            rec_txt = []
            x = txt_list(article,d,c)
            #在推荐列表中去掉给出的文章
            for i in x:
                title = t[i].split(',')[3][1:-1]
                if article != title:
                    rec_txt.append(i)
                    #tt.write(t[i]+'\n')
            #先判断是否存在该文件
            if os.path.exists(r'D:\citeulike\dic\rec_text.dat'):
                os.remove(r'D:\citeulike\dic\rec_text.dat')
            contents = open(r'D:\citeulike\dic\rec_text.dat','a')

            contents.write(t[article_no]) #将给出的文章写入第1行
            for m in rec_txt[0:d]:
                contents.write(t[m])
            contents.close()
            #计算评价推荐文章的相似性 
            sim_value = get_corpus.get_cp(r'D:\citeulike\dic\rec_text.dat') 
            sums = 0
            for i in sim_value[1:]:
                sums += i
            cos_sum = sums/(len(sim_value)-1) #最终余弦相似度结果
            cos_print = '%s_%s_y_%d_cos:'%(c[:1],c[-6:-4],d) ,cos_sum 
            cos.write(str(cos_print)+'\n')
            print cos_print
            g = 0.0
            s = 0.0
            for j in rec_txt[0:d]:
                title = t[j].split(',')[3][1:-1]
                try:
                    sub_rec = txt_list(title,d,c)
                    for i in sub_rec:
                        if i in rec_txt[0:d]:
                            g += 1
                except:
                    continue
            s = g/(d*d)
            div_print = '%s_%s_y_%d_div:'%(c[:1],c[-6:-4],d) ,s
            div.write(str(div_print)+'\n')
            print div_print
            #print '第%d篇文章包含原来推荐的个数:'%(j+1),g
