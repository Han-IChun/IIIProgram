# -*- coding: utf-8 -*-

f=open('../dic/dict.txt.big','r')
speech_dic={}
for line in f.readlines():
    if line.split(' ')[0].strip() not in speech_dic:
        speech_dic[line.split(' ')[0].strip()]=line.split(' ')[2].strip()
f.close()

f=open('article_cut.txt','r')
fid=open('speech.txt','w')
for line in f.readlines():
    if line.strip() in speech_dic:
        sentence='{}\t{}\n'.format(line.strip(),speech_dic[line.strip()])
        fid.write(sentence)
    elif len(line.strip())==0:
        fid.write('\n')
    else:
        sentence='{}\tNA\n'.format(line.strip())
        fid.write(sentence)
fid.close()