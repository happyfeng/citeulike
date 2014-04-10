citeulike
=========

实验处理

（1）：运行lda.py,得到如“online_lda_50.lda” 的文件

gensim包内ladmodel.py源代码568行自己改了id2word[id],topic[id]输出顺序。

（2）：运行topic_sim.py 计算好主题相似性，保存到如“topic_online_lda_150.dump”文件中

（3）：运行 topic2article.py ，要修改代码，只运行get_cp()函数，保存到如“all_online_lda_150.dump”文件中
	便于调用由主题反推文章。
（4）：最后运行topic2article.py 输出给用户推荐的文章


———————————————————————————————————————————————————

topic_sim.py : 余弦相似度计算主题相似性，dump到topic_100.jump文件中。

rank_topic.py : 获取输入文章的主题概率分布，从topic_100.jump导入相似性，最终返回，{文章主题i:{相似主题j:相似度,··		·},{},···}

FeatureSimilarity.py : 对主题进行排序，并与相似性结合，输出最终的主题排序列表list2

rank_word.py : 计算推荐的文章page在给定主题topics下的单词概率和

topic2article.py : 获取推荐的文章列表



待补充
