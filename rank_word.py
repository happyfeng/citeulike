# coding:utf-8
# 计算每篇文章top-n主题下的所有单词概率总和
import gensim
import stopword
import FeatureSimilarity

txt = open(r'D:\citeulike\temp.dat', 'r').readlines()
diction = gensim.corpora.Dictionary.load('citeulike.dict')
batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic\batch_lda_100.lda')
topics = FeatureSimilarity.rank_tp()
def word(page):
    #计算推荐的文章page在给定主题topics下的单词概率和
    topic_rate_new = 0
    content_list = stopword.get_txt(txt[page])
    doc_bow = diction.doc2bow(content_list)
    doc_lda = batch_lda[doc_bow]
    for j in range(len(doc_lda)):
        dic = {}
        word_rate = 0
        tp_id = doc_lda[j][0]
        if tp_id in topics:
            word_list = batch_lda.show_topic(tp_id, 500000)
            dic = dict(word_list)  # 将showtopic的[(a,b),(),()]形式转换成字典
            for w in list(set(content_list)):
                # print dic[w]
                word_rate += dic[w]  # 计算总的主题下单词概率
            # 乘以该主题的概率并除以文章内单词总个数，防止有些文章词很多，值也就很大
            topic_rate = doc_lda[j][1] * word_rate / len(set(content_list))
            topic_rate_new += topic_rate
    #print topic_rate_new
    return topic_rate_new
    '''
        # 计算每篇文章top-n主题下的单词概率总和
        for m in range(len(tP_batch_new)):
            dic = {}
            word_rate = 0
            tp_id = tP_batch_new[m][1]
<<<<<<< HEAD
            #ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序
            word_list = batch_lda.show_topic(tp_id,500000)
            dic = dict(word_list)  #将showtopic的[(a,b),(),()]形式转换成字典
=======
            # ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序
            word_list = batch_lda.show_topic(tp_id, 500000)
            dic = dict(word_list)  # 将showtopic的[(a,b),(),()]形式转换成字典
>>>>>>> citeulike
            for w in list(set(content_list)):
                # print dic[w]
                word_rate += dic[w]  # 计算总的主题下单词概率
            # 乘以该主题的概率并除以文章内单词总个数，防止有些文章词很多，值也就很大
            topic_rate = tP_batch_new[m][0] * word_rate / len(set(content_list))
            topic_rate_new += topic_rate
        print topic_rate_new
        # 写入文件
        file_rate.write(str(topic_rate_new) + '\n')
    file_rate.close()
    '''
if __name__ == '__main__':
    word(3)
