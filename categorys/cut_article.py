# -*- coding: utf-8 -*-

import jieba


not_dic=set()
f=open('../dic/not_dic.txt','r')
for word in f.readlines():
    not_dic.add(word.strip())
f.close()

f=open('test/asp.txt','r')
fid=open('article_cut_not.txt','w')
for sentence in f.readlines():
    sentence=sentence.decode('utf-8').strip()

    new_sentence_list=[]
    w=0
    while w<len(sentence):
        if sentence[w]==u'不':
            for i in range(1,5):
                for k in range(1,5):
                    if w+i+k<=len(sentence):
                        word=sentence[w]+sentence[w+i:w+i+k]
                        if word.encode('utf-8') in not_dic:
                            new_sentence_list.append(word)
                            w+=i+k
                        if w+i+k<len(sentence):
                            word=sentence[w]+sentence[w+i]+sentence[w+i+k]
                            if word.encode('utf-8') in not_dic:
                                new_sentence_list.append(word)
                                w+=i+k+1
        if w < len(sentence):
            new_sentence_list.append(sentence[w])
            w+=1
        else:
            break
    fid.write(''.join(new_sentence_list).encode('utf-8')+'\n')
fid.close()




jieba.set_dictionary('../dic/dict.txt.big')  #設定繁中字典
jieba.load_userdict('../dic/userdic.txt')  #設定自定義字典
jieba.load_userdict('../dic/antusd.txt')  #設定自定義字典
jieba.load_userdict('../dic/negative.txt')  #設定自定義字典
jieba.load_userdict('../dic/positive.txt')  #設定自定義字典


f=open('article_cut_not.txt','r')
fid=open('article_cut.txt','w')

very_set=set([u'很',u'頗',u'更',u'還',u'的'])

for line in f.readlines():
    cut_list=[]
    final_cut_list=[]
    if len(line.decode('utf-8').strip())>0:
        print line.strip()
        for w in jieba.cut(line.strip(),HMM=False):
            if len(w)>0:
                cut_list.append(w)
    for word in cut_list:
        i=0
        word_list=[]
        #word=word.encode('utf-8')
        while i <len(word):
            very_word=''
            if word[i] in very_set:
                very_word=word[i]
                i+=1
            else:
                word_list.append(word[i])
                i+=1
        if len(word_list)>0:
            final_cut_list.append(''.join(word_list))
        if len(very_word)>0:
            final_cut_list.append(very_word)
    sentence='{}\n\n'.format('\n'.join(final_cut_list).encode('utf-8'))
    fid.write(sentence)
fid.close()
