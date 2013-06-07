# coding:utf-8
# 获取citeulike语料库
from gensim import corpora, models,similarities
import re


def get_cp(files):
    content3 = []
    content = open(files, 'r')
    txt = content.readlines()
    stopword = open('stopword_en.dat', 'r')
    sw = stopword.readlines()
    stoplist = []
    for w in sw:
        stoplist.append(w.rstrip())
    for txt2 in txt:
        # 只保留英文，去掉符号和数字
        content2 = re.sub('[^a-zA-Z]', ' ', txt2)
        content3.append(content2)
    text = [[word for word in texts.split() if word not in stoplist]for texts
            in content3]
    stopword.close()
    content.close()
    dictionary = corpora.Dictionary(text)
    #dictionary.save(r'D:\citeulike\dic\new\test.dict')
    #print 'finish saveing dict'
    corpus = [dictionary.doc2bow(texts) for texts in text]
    #corpora.MmCorpus.serialize(r'D:\citeulike\dic\new\test.mm', corpus)
    #tfidf = models.TfidfModel(corpus)
    #corpus_tfidf = tfidf[corpus]
    #corpora.MmCorpus.serialize(r'D:\citeulike\dic\new\test_tfidf.mm', corpus_tfidf)
    
    index = similarities.docsim.Similarity(r'D:\citeulike\dic\new\sim',
                corpus,num_features=10000)
    i = index[corpus][0]
    return i
    
    
if __name__ == '__main__':

    get_cp(r'D:\citeulike\dic\rec_text.dat')

