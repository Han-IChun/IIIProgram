# -*- coding: utf-8 -*-

import os

total_dic_word=set()

dic_name=('../dic/dict.txt.big','../dic/userdic.txt','../dic/antusd.txt','../dic/negative.txt','../dic/positive.txt')

for name in dic_name:
    f=open(name,'r')
    if name =='../dic/dict.txt.big':
        for word in f.readlines():
            if word.split(' ')[0] not in total_dic_word:
                total_dic_word.add(word.split(' ')[0])
    else:
        for word in f.readlines():
            if word not in total_dic_word:
                total_dic_word.add(word)
    f.close()

fid=open('article_inline.txt','w')
for file in os.listdir('../mobil01/data/mobile_content/Acer(Android)'):
    filename=file.decode('cp950')
    f=open('../mobil01/data/mobile_content/Acer(Android)/'+filename,'r')
    for w in f.readlines(): #readlines將整篇文存成一個list，一行為一個list元素
        if len(w)>1:    #去掉沒內容的行([])
            fid.write(''.join(w.split()).strip()+'\n')

fid.close()

dic={}
f=open('article_inline.txt','r')
for line in f.readlines():
    for i in range(0,len(line.decode('utf-8'))):
        word=line.decode('utf-8')[i]
        if word==u'不':
            if word.strip() != line.decode('utf-8')[i:i+2].strip():
                if word.strip() not in dic:
                    dic[word.strip()]=1
                else:
                    dic[word.strip()]+=1
            if line.decode('utf-8')[i:i+2].strip() !=line.decode('utf-8')[i:i+3].strip():
                if line.decode('utf-8')[i:i+2].strip() not in dic:
                    dic[line.decode('utf-8')[i:i+2].strip()]=1
                else:
                    dic[line.decode('utf-8')[i:i+2].strip()]+=1
            if line.decode('utf-8')[i:i+3].strip() !=line.decode('utf-8')[i:i+4].strip():
                if line.decode('utf-8')[i:i+3].strip() not in dic:
                    dic[line.decode('utf-8')[i:i+3].strip()]=1
                else:
                    dic[line.decode('utf-8')[i:i+3].strip()]+=1

            if line.decode('utf-8')[i:i+4].strip() not in dic:
                dic[line.decode('utf-8')[i:i+4].strip()]=1
            else:
                dic[line.decode('utf-8')[i:i+4].strip()]+=1
f.close()

f=open('negative_word.txt','w')
for ele in dic:
    if ele[1:].encode('utf-8') in total_dic_word:
        print ele
        content='{}\t{}\n'.format(ele.encode('utf-8'),dic[ele])
        f.write(content)
f.close()


