# -*- coding: utf-8 -*-

import jieba

jieba.set_dictionary('../dic/dict.txt.big')  #設定繁中字典
jieba.load_userdict('../dic/user_dict.txt')  #設定自定義字典
jieba.load_userdict('../dic/opinion_dic.txt')  #設定自定義字典

f=open('text/asp.txt','r')

for line in f.readlines():
    list=[]
    for w in jieba.cut(line.split('\t')[0].strip(),HMM=False):
        list.append(w)
    print '\t'.join(list)+'\n'
f.close()