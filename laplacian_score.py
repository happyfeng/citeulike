# -*- coding: UTF-8 -*-

import numpy as np
import sys
import gensim
from rank_word import get_txt

class lp_score():
    """docstring for laplacian_score"""

    def __init__(self, k, sigma):
        # self.fmat = covariance matrix which is the feature
        # self.fmat = np.zeros([self.k, self.k])
        self.fmat = sigma
        self.laplacian = np.zeros([k, k])
        self.sum_row = []
        self.lscore = np.zeros(k)
        # python only provide maxint, according to doc
        # minint = -maxint-1
        # 13.04.19 seems like min_value and max_value are useless
        self.MIN_VALUE = -sys.maxint-1
        self.MAX_VALUE = sys.maxint

    def compute_laplacian(self,k, numk):
        print 'compute laplacian'
        # numK : nearest neighbor number
        col_norm = np.ones(k)
        col_norm = [np.dot(self.fmat[i], self.fmat[i]) for i in range(k)]
        print col_norm
        mid_values = np.zeros(k)
        for i in range(k):
            # print 'fmat[i]', self.fmat[i]
            # print
            euclidean_dis = np.zeros(k)
            for j in range(k):
                dot_prod = np.dot(self.fmat[i], self.fmat[j])
                euclidean_dis[j] = col_norm[i] + col_norm[j] - 2 * dot_prod
                # print
                # print 'euclidean_dis[j]', euclidean_dis[j]
            # sorted
            print 'sorted indices '
            # indices = np.argsort(euclidean_dis)
            values = np.sort(euclidean_dis)
            self.laplacian[i] = values
            # for j in range(len(indices)):
            #     self.laplacian[i][indices[j]] = euclidean_dis[indices[j]]
            # topic number has to be even number, in case the index -1 is not even

            mid = int(k / 2)
            print values[mid]
            mid_values[i] = values[mid]
            print 'mid values[i]', mid_values[i]

        # set symmetric
        for i in range(k):
            for j in range(k):
                temp1 = self.laplacian[i][j]
                temp2 = self.laplacian[j][i]
                if temp1 != 0.0 and temp1 != temp2:
                    self.laplacian[j][i] = temp1

        # compute D, first part of step 3 in paper
        self.sum_row = np.zeros(k)
        for i in range(k):
            for j in range(k):
                if self.laplacian[i][j] != 0.0:
                    aa = -self.laplacian[i][j]
                    bb = mid_values[i] + self.MIN_VALUE
                    value = np.exp(aa / (2 * bb * bb))
                    # sum_row[i] is D_ii
                    self.sum_row[i] += value
                    self.laplacian[i][j] = value
        # compute D-S = L, second part of step 3
        for i in range(k):
            value = self.laplacian[i][i]
            self.laplacian[i][i] = self.sum_row[i] - value
            for j in range(i + 1, k):
                if self.laplacian[i][j] != 0.0:
                    value = self.laplacian[i][j]
                    self.laplacian[i][j] = -value
                    self.laplacian[j][i] = -value

    def laplacian_score(self,k, numk):
        print 'computer laplacian score'
        self.compute_laplacian(k,numk)
        # diag_sum = np.zeros(numk)
        # for i in range(self.k):
        #     diag_sum[i][i] = self.sum_row[i]
        for i in range(k):
            col_vector = self.fmat[i]
            print 'length of col_vector: ', len(col_vector)
            print col_vector
            tt = self.sum_row[i] * np.ones(k)
            print tt
            temp1 = np.dot(col_vector, tt)
            # temp2 = np.dot(np.ones(self.k), np.ones(self.k))
            col_vector -= temp1 / k

            temp3 = np.dot(col_vector, np.dot(self.laplacian, col_vector))
            temp4 = np.dot(col_vector, np.dot(self.sum_row[i], col_vector))
            self.lscore[i] = temp3 / (temp4 + self.MIN_VALUE)
        sorted_indices = np.argsort(self.lscore)
        print 'sorted indices is ', sorted_indices
        return sorted_indices
   
if __name__ == '__main__':
    print 'This program is running by itself'
    lists = []
    diction = gensim.corpora.Dictionary.load('citeulike.dict')
    batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic\batch_lda_50.lda')
    txt = open(r'D:\citeulike\temp.dat','r').readline()
    content_list = get_txt(txt)
    doc_bow = diction.doc2bow(content_list)
    doc_lda = batch_lda[doc_bow]
    print len(doc_lda)
    for j in range(len(doc_lda)):
        dic = {}
        tp_id = doc_lda[j][0]
		#ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序
        word_list = batch_lda.show_topic(tp_id,topn=len(doc_lda))
        print word_list
        dic = dict(word_list)
        print dic
        lists.append(dic.values())
    sigma = np.array(lists)


    #sigma = [[np.random.randint(100) + 0.1 for i in range(10)] for y in range(10)]
    #print 'sigma[3] is:', sigma[3]
    # guarantee symetric
    for i in range(len(doc_lda)):
        for j in range(len(doc_lda)):
            temp1 = sigma[i][j]
            temp2 = sigma[j][i]
            if temp1 != temp2:
                sigma[j][i] = sigma[i][j]
    l_score = []
    ll = lp_score(len(doc_lda), sigma)
    l_score = ll.laplacian_score(len(doc_lda),len(doc_lda))
    print 'lscore is:', l_score
else:
    print 'I am being imported from another module'
