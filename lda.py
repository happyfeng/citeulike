#coding:utf-8
from gensim import corpora,models,similarities
import gensim
diction = corpora.Dictionary.load(r'D:\citeulike\dic\new\test.dict')
mm = corpora.MmCorpus(r'D:\citeulike\dic\new\test_tfidf.mm')
#用batch_lda训练
'''
batch_lda=models.ldamodel.LdaModel(corpus=mm,id2word=diction,num_topics=200,
        update_every=0, passes=5)
batch_lda.save('batch_lda_200.lda')
online_lda = gensim.models.ldamodel.LdaModel(corpus=mm,
        id2word=diction,num_topics=150,update_every=1,chunksize=100, passes=1)
online_lda.save('online_lda_150.lda')
'''
#计算每篇文章的相似性，可输出与查询文章相似的num_best篇文章
index = similarities.docsim.Similarity(r'D:\citeulike\dic\new\sim',
                corpus=mm,num_features=1200)
print index[mm]
#i = similarities.docsim.SparseMatrixSimilarity.load(r'D:\citeulike\dic\new\sim.0')
#for j in i:
    #    print j
'''
lda = models.LdaModel.load(r'D:\citeulike\dic\batch_lda_50.lda')
for i in range(50):
    print 'Topic %d :'%i,lda.show_topic(i)
    print '-'*50
diction = gensim.corpora.Dictionary.load('citeulike.dict')
batch_lda = models.LdaModel.load(r'D:\citeulike\dic\batch_lda.lda')

for i in range(100,200):
    txt = open(r'D:\citeulike\temp.dat','r').readlines()[i]
    content_list = txt.split(' ')
    doc_bow = diction.doc2bow(content_list)
    doc_lda = batch_lda[doc_bow]
    print doc_lda
'''
