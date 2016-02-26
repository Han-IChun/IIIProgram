# -*- coding: utf-8 -*-

negative_set=set()
positive_set=set()

negative_write=set()
positive_write=set()

f=open('../dic/negative.txt','r')
for word in f.readlines():
    word=word.strip()
    if word not in negative_set:
        negative_set.add(word)
f.close()


f=open('../dic/positive.txt','r')
for word in f.readlines():
    word=word.strip()
    if word not in positive_set:
        positive_set.add(word)
f.close()

f=open('article_inline.txt','r')


for line in f.readlines():
    line=line.strip().decode('utf-8')
    for word in range(0,len(line)):
        for length in range(1,5):
            if line[word:length].encode('utf-8') in negative_set:
                if line[word:length].encode('utf-8') not in negative_write:
                    negative_write.add(line[word:length].encode('utf-8'))

            if line[word:length].encode('utf-8') in positive_set:
                 if line[word:length].encode('utf-8') not in positive_write:
                    positive_write.add(line[word:length].encode('utf-8'))
f.close()

negative=open('negative_word.txt','w')
for word in negative_write:
    negative.write(word+'\n')
negative.close()

positive=open('positive_word.txt','w')
for word in positive_write:
    positive.write(word+'\n')
positive.close()



