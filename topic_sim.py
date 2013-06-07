# coding:utf-8
from math import sqrt
import gensim
import pickle
# import numpy as np
# 通过余弦相似度计算各主题间的相似性


def scalar(collection):
    total = 0
    for coin, count in collection.items():
        total += count * count
    return sqrt(total)


def similarity(A, B):
    # 余弦相似度计算
    total = 0
    for kind in A:
        if kind in B:
            total += A[kind] * B[kind]
    return float(total) / (scalar(A) * scalar(B))
if __name__ == '__main__':
    diction = gensim.corpora.Dictionary.load('citeulike.dict')
    batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic\online_lda_50.lda')
    list2 = []
    for i in range(50):
        list1 = []
        for j in range(50):
            topic1 = batch_lda.show_topic(i, topn=500000)
            # ladmodel.py源代码569行自己改了输出顺序
            topic2 = batch_lda.show_topic(j, topn=500000)
            sim = similarity(dict(topic1), dict(topic2))
            list1.append(sim)
        list2.append(list1)

    pickle.dump(list2, open(r'D:\citeulike\dic\topic_online_50.jump', 'w'))
    '''
    i = pickle.load(open(r'D:\citeulike\dic\topic_100.jump','r'))
    j = np.array(i)
    print j
    '''
