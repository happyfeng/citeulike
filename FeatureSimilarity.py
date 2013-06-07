# -*- coding: utf-8 -*-

import numpy as np
import sys
import rank_topic
import gensim
import operator
import pickle


class FeatureSimilarity:
    def __init__(self):
        pass

    def computeEuclidean(self, tt1, tt2):
        norm1 = np.dot(tt1, tt1)
        norm2 = np.dot(tt2, tt2)
        dots = np.dot(tt1, tt2)
        euclidean_distance = np.sqrt(norm1 + norm2 - 2 * dots)
        return euclidean_distance

    def computeSpecialEuclidean(self, tt1, tt2):
        norm1 = np.dot(tt1, tt1)
        norm2 = np.dot(tt2, tt2)
        dots = np.dot(tt1, tt2)
        specialeuclidean_distance = (1 - dots / (np.sqrt(norm1 * norm2) + sys.float_info.min))
        return specialeuclidean_distance

    def computeCorrelation(self, tt1, tt2):
        # it seems like tt1 and tt2 should have the same dimension, which is
        # true, casue they are each a distribution of vocabulary
        # the result is a square matrix in the shape of
        # (num_of_topic * num_of_topic)

        # length of the topic distribution
        dot = np.dot(tt1, tt2)
        sysmin = sys.float_info.min
        v1mean = np.sum(tt1)
        v2mean = np.sum(tt2)
        v1square = np.sum(tt1[i] * tt1[i] for i in range(len(tt1)))
        v2square = np.sum(tt2[i] * tt2[i] for i in range(len(tt2)))

        correlation_distance = 1 - np.fabs((self.topic_num * dot - v1mean * v2mean) / (np.sqrt(self.topic_num * v1square - v1mean * v1mean) + sysmin) / (np.sqrt(self.topic_num * v2square - v2mean * v2mean) + sysmin))
        return correlation_distance

    def computeSquareLossofPCA(self, tt1, tt2):
        dots = np.dot(tt1, tt2)
        sysmin = sys.float_info.min
        v1mean = np.sum(tt1)
        v2mean = np.sum(tt2)
        v1square = np.sum(tt1[i] * tt1[i] for i in range(self.topic_num))
        v2square = np.sum(tt2[i] * tt2[i] for i in range(self.topic_num))
        rho = ((self.topic_num * dots - v1mean * v2mean) / (np.sqrt(self.topic_num * v1square - v1mean * v1mean) + sysmin) / (np.sqrt(self.topic_num * v2square - v2mean * v2mean) + sysmin))
        v1mean /= self.topic_num
        v2mean /= self.topic_num
        v1var = np.sum((tt1[i] - v1mean) * (tt1[i] - v1mean) for i in range(self.topic_num)) / self.topic_num
        v2var = np.sum((tt2[i] - v2mean) * (tt2[i] - v2mean) for i in range(self.topic_num)) / self.topic_num
        squareLossofPCA_distance = v1var + v2var - np.sqrt((v1var + v2var) * (v1var + v2var) - 4 * v1var * v2var * (1 - rho * rho))
        return squareLossofPCA_distance

    def computePairwiseSimilarity(self, fmat, d_string):
        # d_string is string, distance type

        # initialize distance matrix
        # m is the topic number, n is the topis distribution length
        m, n = np.shape(fmat)
        self.topic_num = m
        self.topic_length = n
        fdistances = np.zeros([m, m])

        for i in range(m):
            for j in range(i+1, m):
                tt1 = fmat[i]
                tt2 = fmat[j]
                if (d_string.lower() == "euclidean"):
                    distances = self.computeEuclidean(tt1, tt2)
                elif (d_string.lower() == "special"):
                    distances = self.computeSpecialEuclidean(tt1, tt2)
                elif (d_string.lower() == "correlation"):
                    distances = self.computeCorrelation(tt1, tt2)
                elif (d_string.lower() == "maxinfocompress"):
                    distances = self.computeSquareLossofPCA(tt1, tt2)
                else:
                    print 'your input is: ', d_string.lower()
                    print
                    print 'No found simiarity type, or you spell it wrong.'
                fdistances[i][j] = distances
                fdistances[j][i] = distances
        return fdistances

    def rankFeatures(self, fmat, d_string):
        '''
        The basic idea is that based on the computed distance (implemented
        above, four kinds), a diagional matrix can be formed.

        Find out the smallest number from distance matrix, then the closest
        two topics can be decided, let's say the distance is s_ij, then
        topic j get the hightest rank, then, the process goes on till the last
        topic is popped.

        '''
        # initialize distance matrix
        # m is the topic number, n is the topis distribution length
        m, n = np.shape(fmat)
        self.topic_num = m
        self.topic_length = n
        fdistances = np.zeros([m, m])
        fdistances = self.computePairwiseSimilarity(fmat, d_string)
        # copy the distance matrix, in case it would be messed up
        processed_fdistance = fdistances.copy()
        # make this matrix into upper triangle matrix
        for i in range(1, m):
            for j in range(i):
                processed_fdistance[i][j] = 0
        #print 'diagional distanc'
        #print processed_fdistance
        rank_list = []  # empty list for final rank list
        while len(rank_list) < self.topic_num:
            # yes, here is argmax
            i, j = np.unravel_index(processed_fdistance.argmax(), processed_fdistance.shape)
            rank_list.append(j)
            for ii in range(self.topic_num):
                processed_fdistance[ii][j] = 0
        # reverse the list, since above is argmax
        result = rank_list[::-1]
        return result

def rank_tp(titles,lda):
    batch_lda = gensim.models.LdaModel.load(r'D:\citeulike\dic'+'\\'+lda)
    tp = rank_topic.get_topic(titles,lda)
    #print tp
    lists = []
    dic = {} #将tp字典值合并
    for i in tp.values():
        for j in i.keys():
            lists.append(j)
            if j not in dic.keys():
                dic[j] = i[j]
            else:
                dic[j] += i[j]
    ay = []
    topic_list = list(set(lists))
    #print topic_list
    for m in topic_list:
        #ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序
        word_list = batch_lda.show_topic(m,topn=500000)
        to_dic = dict(word_list)
        ay.append(to_dic.values())
    t = np.array(ay)
    
    pickle.dump(t,open('juzhen.dump','wb'))
    #cPickle.dump(ay,open('juzhen4.dump','wb'))
    ff = FeatureSimilarity()
    # test2 = ff.computePairwiseSimilarity(ls, "Euclidean")
    # print test2
    indices = ff.rankFeatures(t, "euclidean")
    #print indices
    rank_topics = []
    for n in indices:
        rank_topics.append(topic_list[n])
    # rank_topics 排序好的主题
    #return rank_topics
    #print rank_topics
    
    #将相似度的值与排序好的主题结合
    value = np.arange(1,0,-0.1)
    for t in dic.keys():
        x = rank_topics.index(t)
        dic[t] = dic[t]*value[x]
    dic2 = sorted(dic.iteritems(),key=operator.itemgetter(1),reverse=True)
    list2 = []
    for i in dic2:
        list2.append(i[0])
    #print list2
    return list2    
if __name__ == '__main__':
    rank_tp('Exploring complex networks','batch_lda_100.lda')
