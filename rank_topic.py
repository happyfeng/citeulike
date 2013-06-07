#coding:utf-8
import gensim
import stopword
import pickle

txt = open(r'D:\citeulike\items.dat', 'r').readlines()
def input_article(article):
    content = open(r'D:\citeulike\raw-data.csv','r').readlines()
    for one in content:
        content_one = one.split(',')[3][1:-1] #提取文章标题并去掉""
        if article == content_one:
            #输出摘要，并处理得到主题
            temp = one.split(',')[4:]
            abstracts = ''.join(temp)
    try:
        return abstracts
    except:
        print u'不存在该篇文章'
        exit()

def get_topic(texts,lda):
    #获取输入文章的主题概率分布
    dict_sim1 = {}
    sim = pickle.load(open(r'D:\citeulike\dic\topic_'+lda[:-4]+'.dump','r'))
    diction = gensim.corpora.Dictionary.load('citeulike.dict')
    batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic'+'\\'+lda)
    text = input_article(texts)
    text_list = stopword.get_txt(text)
    doc_bow = diction.doc2bow(text_list)
    doc_lda = batch_lda[doc_bow]
    #print doc_lda
    #元组不可变，更改为列表
    tp_batch = []
    for yuanzu in doc_lda:
        tp_batch.append(list(yuanzu))
    #归一化
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
            if tp_id in dict_sim2.keys():
                dict_sim2[tp_id] += 1.0
            else:
                dict_sim2[tp_id] = 1.0  #加入文章的主题，概率设为10
            dict_sim1[tp_id] = dict_sim2    
    #最终返回字典形式，{文章主题i:{相似主题j:相似度,···},{},···}
    #print dict_sim1
    return dict_sim1

def seen(users, re_doc):
    #对于输出的推荐文章，判断用户是否看过，并计算概率来衡量新奇性
    
    user_seen = txt[re_doc].split()[1:] 
    if users in user_seen:
        rate_unseen = 0
    else:
        rate_unseen = 1
    num = txt[re_doc].split()[0] 
    rate_art = 1 - int(num)/5551.0
    rate_nov = rate_art * rate_unseen
    #print rate_nov
    return rate_nov
if __name__ == '__main__':

    get_topic("The metabolic world of Escherichia coli is not small") 
    #seen("215",3)
