# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import lxml.etree as etree
import jieba

from bs4 import BeautifulSoup as bs
f=open('label_num2_final.xml','r')
soup=bs(f.read(),'xml')
f.close()

not_dic=set()
f=open('../dic/not_dic.txt','r')
for word in f.readlines():
    not_dic.add(word.strip())
f.close()
final_dic={}

jieba.set_dictionary('../dic/dict.txt.big')  #設定繁中字典
jieba.load_userdict('../dic/userdic.txt')  #設定自定義字典
jieba.load_userdict('../dic/antusd.txt')  #設定自定義字典
jieba.load_userdict('../dic/negative.txt')  #設定自定義字典
jieba.load_userdict('../dic/positive.txt')  #設定自定義字典


stopword_set=set()  #設一個空的set 裝 stopword
f=open('../dic/stopword.txt','r') #開啟stopword txt檔
for i in f.readlines(): #將stop word 一行一行讀出來
    stopword_set.add(i.strip()) #將stop wor 加到stopword set 裡面
f.close()

very_set=set([u'很',u'頗',u'更',u'還',u'的'])

for ele in range(0,len(soup.select('sentence'))):
    reviewID=soup.select('sentence')[ele]['reviewID']
    number=soup.select('sentence')[ele]['number']

    if len(soup.select('sentence')[ele].select('text')[0].text)>0:
        content=''.join(soup.select('sentence')[ele].select('text')[0].text.split())

        sentence=content.strip()

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

        text_dic={}
        cut_list=[]
        final_cut_list=[]
        for w in jieba.cut(''.join(new_sentence_list),HMM=False):     #將要處理的文章放到text裡整理過用jieba斷詞
            cut_list.append(w)
        for word in cut_list:
            i=0
            word_list=[]
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

        text_dic[content]=('\t'.join(final_cut_list))
        final_dic[reviewID]=text_dic.copy()





sentences=ET.Element('sentences')
for ele in range(0,len(soup.select('sentence'))):
    print ele
    sentence=ET.SubElement(sentences,'sentence')
    reviewID=soup.select('sentence')[ele]['reviewID']
    number=soup.select('sentence')[ele]['number']

    sentence.attrib={'reviewID':reviewID,'number':number,'polarity':''}
    text=ET.SubElement(sentence,'text')
    text.text=final_dic[reviewID].keys()[0]

    aspectTerms=ET.SubElement(sentence,'aspectTerms')
    aspectTerm=ET.SubElement(aspectTerms,'aspectTerm')
    aspectTerm.attrib={'term':'','polarity':'','opinion':''}

    aspectCategories=ET.SubElement(sentence,'aspectCategories')
    asp_dic={}
    for i in soup.select('sentence')[ele].select('aspectCategory'):
        asp_dic[i['category']]=i['polarity']

    for j in asp_dic:
        aspectCategory=ET.SubElement(aspectCategories,'aspectCategory')
        aspectCategory.attrib={'category':j,'polarity':asp_dic[j]}


    jieba=ET.SubElement(sentence,'jieba')
    jieba.text=(final_dic[reviewID].values()[0])


tree=ET.ElementTree(sentences)
ET.ElementTree(sentences).write('test.xml',encoding="UTF-8",xml_declaration=True)

x = etree.parse('test.xml')

f=open('test1.xml','w')
f.write(etree.tostring(x,encoding="UTF-8",pretty_print = True))
f.close()



'''
    jieba.set_dictionary('dic/dict.txt.big')  #設定繁中字典
    jieba.load_userdict('dic/userdic.txt')  #設定自定義字典
    jieba.load_userdict('dic/antusd.txt')  #設定自定義字典
    jieba.load_userdict('dic/negative.txt')  #設定自定義字典
    jieba.load_userdict('dic/positive.txt')  #設定自定義字典


        cut=article_cut[i].strip().decode('utf-8')
        sentences=ET.Element('sentences')

        sentence=ET.SubElement(sentences,'sentences')
        sentence.attrib={'reviewID':str(i+1),'number':'1','opinion ':''}

        text=ET.SubElement(sentence,'text')
        text.text=(content)

        aspectCategories=ET.SubElement(sentence,'aspectCategories')
        aspectCategory=ET.SubElement(aspectCategories,'aspectCategory')
        aspectCategory.attrib={'category':'','polarity':''}


        jieba=ET.SubElement(sentence,'jieba')
        jieba.text=(cut)
'''







