#coding:utf-8
def get_txt(texts):
    # È¥Í£ÓÃ´Ê
    stopword = open(r'D:\citeulike\stopword_en.dat', 'r')
    sw = stopword.readlines()
    stoplist = []
    for w in sw:
        stoplist.append(w.rstrip())
    text = []
    for word in texts.split(' '):
        if word not in stoplist and len(word) > 1:
            text.append(word)
    return text
