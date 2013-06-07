#coding:utf-8
import gensim
import pickle
import stopword
import rank_topic
import os
import get_corpus

article = "Exploring complex networks"
article_no = 2 
to = open(r'D:\citeulike\raw-data.csv', 'r').readlines()
cos = open(r'D:\citeulike\dic'+'\\cos_'+article+'.dat', 'a')
div = open(r'D:\citeulike\dic'+'\\div_'+article+'.dat', 'a')
sim = pickle.load(open(r'topic_online_lda_100.dump','r'))
diction = gensim.corpora.Dictionary.load('citeulike.dict')
batch_lda = gensim.models.LdaModel.load('online_lda_100.lda')
content = open(r'D:\citeulike\dic\temp.dat', 'r').readlines()
def get_tp(nom):
    text_list = stopword.get_txt(content[nom])
    doc_bow = diction.doc2bow(text_list)
    doc_lda = batch_lda[doc_bow]
    tp_batch = []
    for yuanzu in doc_lda:
        tp_batch.append(list(yuanzu))
#归一化
    dict_sim1 = {}
    sum0 = 0
    t = 0
    for m in range(len(doc_lda)):
        if tp_batch[m][1] > 0.1:
            t += 1
            sum0 += tp_batch[m][1]
    for n in range(len(doc_lda)):
        if tp_batch[n][1] > 0.1:
            tp_batch[n][1] = tp_batch[n][1]/sum0
    for (tp_id,rate) in tp_batch:
        if rate >0.1:
            dict_sim2 = {}
            wordsNum = int(round((10-t)*rate))
            #print tp_id
            #print wordsNum
            #从相似性矩阵中获取wordnum个最相似的主题
            sim_1 = sorted(sim[tp_id],reverse=True)
            sim_2 = sim_1[1:wordsNum+1]
            #print sim_2
            for i in sim_2:
                dict_sim2[sim[tp_id].index(i)] = i #index获取列表中对应元素的下标
            '''
            if tp_id in dict_sim2.keys():
                dict_sim2[tp_id] += 1.0
            else:
                dict_sim2[tp_id] = 1.0  #加入文章的主题，概率设为1
            '''
            dict_sim1[tp_id] = dict_sim2
    tp_list = []
    for i in dict_sim1.values():
        for j in i.keys():
            tp_list.append(j)
    tp_list2 = list(set(tp_list))

    tp = pickle.load(open(r'D:\citeulike\dic\all_online_lda_100.dump', 'r'))
#def to_article(rank):
# 遍历每篇文章，通过排序后主题计算与该主题最相关的文章
    rank_list = []
    for m in range(len(tp)):
        rate2 = 0
        t = 0
        nov_rate = rank_topic.seen('1', m)  # 乘以新奇性
        for n in tp_list2:
            if n in tp[m].keys():
                # 计算排序主题与主题概率的乘积，方便选取最相似的文章
                rate = tp[m][n]
                t = t + 1
            else:
                rate = 0
            rate2 += rate
        if t != 0:
            # 乘以文章新奇性概率，除以文章中主题出现在rank中的个数，防止主题过多，结果越大
            sum_rate = rate2 * nov_rate / t
        else:
            sum_rate = rate2 * nov_rate
        rank_list.append(sum_rate)  # 按文章顺序排列的相似性值
    return rank_list

def txt_list(txts, N):
    # 获取推荐的文章列表
    
    rank_list2 = get_tp(txts)
    texts = sorted(rank_list2, reverse=True)[0:N + 1]
    rec_list = []
    for i in texts:
        rec_list.append(rank_list2.index(i))
    return rec_list
if __name__ == '__main__':
    #tt = open(r'D:\citeulike\dic\result\no_rank.dat','a')
    for d in [5,10,15,20]:
        rec_txt = []
        x = txt_list(article_no, d)
        # 在推荐列表中去掉给出的文章
        for i in x:
            title = to[i].split(',')[3][1:-1]
            if article != title:
                rec_txt.append(i)
                print title
                #tt.write(to[i]+'\n')
        # 先判断是否存在该文件
        if os.path.exists(r'D:\citeulike\dic\rec_text2.dat'):
            os.remove(r'D:\citeulike\dic\rec_text2.dat')
        contents = open(r'D:\citeulike\dic\rec_text2.dat', 'a')

        contents.write(to[article_no])  # 将给出的文章写入第1行
        for m in rec_txt[0:d]:
            contents.write(to[m])
        contents.close()
        # 计算评价推荐文章的相似性
        sim_value = get_corpus.get_cp(r'D:\citeulike\dic\rec_text2.dat')
        sums = 0
        for i in sim_value[1:]:
            sums += i
        cos_sum = sums / len(sim_value)  # 最终余弦相似度结果
        cos_print = 'o_00_n_%d_cos:' % d, cos_sum
        cos.write(str(cos_print) + '\n')
        print cos_print
        g = 0.0
        s = 0.0
        for j in rec_txt[0:d]:
            title = to[j].split(',')[3][1:-1]
            try:
                sub_rec = txt_list(j, d)
                for i in sub_rec:
                    if i in rec_txt[0:d]:
                        g += 1
            except:
                continue
        s = g / (d * d)
        div_print = 'o_00_n_%d_div:' %d, s
        div.write(str(div_print) + '\n')
        print div_print
