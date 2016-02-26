# -*- coding: utf-8 -*-

import categorys_pmi
import jieba

dic=categorys_pmi.category_pmi('label_num2_final.xml','camera','software','shap','audio','smooth','battery','brand','screen','hardware','price','other')


jieba.set_dictionary('../dic/dict.txt.big')  #設定繁中字典
jieba.load_userdict('../dic/userdic.txt')  #設定自定義字典
jieba.load_userdict('../dic/antusd.txt')  #設定自定義字典
jieba.load_userdict('../dic/negative.txt')  #設定自定義字典
jieba.load_userdict('../dic/positive.txt')  #設定自定義字典

stopword_set=set()  #設一個空的set 裝 stopword
f=open('../dic/stopword.txt','r')  #開啟stopword txt檔
for i in f.readlines(): #將stop word 一行一行讀出來
    stopword_set.add(i.strip()) #將stop word 加到stopword set 裡面
f.close()


f=open('asp.txt','r')
fid=open('text.txt','w')
for line in f.readlines():
    list=[]
    dic_predic={}
    for w in jieba.cut(line,HMM=False):
        if w not in stopword_set:
            list.append(w)
    for ele in list:
        if ele in dic:
            max_pmi=dic[ele][dic[ele].keys()[0]]
            category=dic[ele].keys()[0]
            for k in dic[ele]:
                if dic[ele][k]>max_pmi:
                    max_pmi=dic[ele][k]
                    category=k
            if category not in dic_predic:
                dic_predic[category] =1
            else:
                dic_predic[category] +=1

            content='{}\t{}\t{}\n'.format(ele.encode('utf-8'),category.encode('utf-8'),max_pmi)
            fid.write(content)
    predic_category=''
    count=0
    for j in dic_predic:
        count=dic_predic[dic_predic.keys()[0]]
        predic_category=j
        if dic_predic[j]>count:
            count=dic_predic[j]
            predic_category=j
    predic='{}\t{}\n'.format(predic_category,count)
    fid.write(predic)
    fid.write('----------------------------------------\n')
fid.close()
f.close()