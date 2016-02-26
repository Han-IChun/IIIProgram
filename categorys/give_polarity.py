# -*- coding: utf-8 -*-

import json

list_total=[]
list=[]
word_list=[]

attribute_set=set(['B_A','I_A','E_A','A'])
opinion_set=set(['B_O','I_O','E_O','O'])

attribute_list=[]
opinion_list=[]

f=open('categorys_pmi.json','r')
categorys_pmi = json.loads(f.read().decode('utf8'))
f.close()

f=open('polarity.json','r')
polarity_count = json.loads(f.read().decode('utf8'))
f.close()

f=open('conll_output_Backup7.txt','r')
firstline=f.readline()

for line in f.readlines():
    if len(line)>1:
        word_list=[]
        word_list.append(line.strip().split('\t')[0]+'\t'+line.strip().split('\t')[3])
        list.append(word_list)
    elif len(line)==1:
        list_total.append(list)
        list=[]
f.close()


for i in list_total:#one sentence
    attribute_list=[]
    opinion_list=[]
    little_attribute_list=[]
    little_opinion_list=[]
    for j in i:
        j[0]=j[0].strip()
        if j[0].split('\t')[1] in attribute_set:
            if j[0].split('\t')[1]=='B_A':
                little_attribute_list.append(j[0])
            if j[0].split('\t')[1]=='I_A':
                little_attribute_list.append(j[0])
            if j[0].split('\t')[1]=='E_A':
                little_attribute_list.append(j[0])
                attribute_list.append(little_attribute_list)
                little_attribute_list=[]
            if j[0].split('\t')[1]=='A':
                little_attribute_list.append(j[0])
                attribute_list.append(little_attribute_list)
                little_attribute_list=[]

        if j[0].split('\t')[1] in opinion_set:
            if j[0].split('\t')[1]=='B_O':
                little_opinion_list.append(j[0])
            if j[0].split('\t')[1]=='I_O':
                little_opinion_list.append(j[0])
            if j[0].split('\t')[1]=='E_O':
                little_opinion_list.append(j[0])
                opinion_list.append(little_opinion_list)
                little_opinion_list=[]
            if j[0].split('\t')[1]=='O':
                little_opinion_list.append(j[0])
                opinion_list.append(little_opinion_list)
                little_opinion_list=[]
    attribute_categorys_count_dic={}
    opinion_categorys_count_dic={}


    if len(attribute_list)>0 or len(opinion_list)>0:
        sentence_attributes_categorys_set=set()
        sentence_opinions_categorys_dic={}
        for attribute_words in attribute_list:
            attribute_words_categorys_dic={}
            for attribute_word in attribute_words:
                attribute_word=attribute_word.split('\t')[0].decode('utf-8')
                categorys_pmi_dic={}
                if attribute_word in categorys_pmi and attribute_word!=u'的':
                    categorys_pmi_dic=categorys_pmi[attribute_word].copy()
                    max_pmi=categorys_pmi_dic[categorys_pmi_dic.keys()[0]]
                    max_pmi_category=categorys_pmi_dic.keys()[0]
                    for pmi in categorys_pmi_dic:
                        if categorys_pmi_dic[pmi]>max_pmi:
                            max_pmi=categorys_pmi_dic[pmi]
                            max_pmi_category=pmi
                    if max_pmi_category not in attribute_words_categorys_dic:
                        attribute_words_categorys_dic[max_pmi_category]=1
                    else:
                        attribute_words_categorys_dic[max_pmi_category] +=1
            for attributes_category in attribute_words_categorys_dic:
                most_category_count=max(attribute_words_categorys_dic.values())
                if attribute_words_categorys_dic[attributes_category]==most_category_count:
                    sentence_attributes_categorys_set.add(attributes_category)

        for opinon_words in opinion_list:
            opinion_words_categorys_dic={}
            for opinon_word in opinon_words:
                opinon_word=opinon_word.split('\t')[0].decode('utf-8')
                categorys_pmi_dic={}
                if opinon_word in categorys_pmi and opinon_word!=u'的':
                    categorys_pmi_dic=categorys_pmi[opinon_word].copy()
                    max_pmi=categorys_pmi_dic[categorys_pmi_dic.keys()[0]]
                    max_pmi_category=categorys_pmi_dic.keys()[0]
                    for pmi in categorys_pmi_dic:
                        if categorys_pmi_dic[pmi]>max_pmi:
                            max_pmi=categorys_pmi_dic[pmi]
                            max_pmi_category=pmi
                    if max_pmi_category not in opinion_words_categorys_dic:
                        opinion_words_categorys_dic[max_pmi_category]=1
                    else:
                        opinion_words_categorys_dic[max_pmi_category] +=1
            for opinion_category in opinion_words_categorys_dic:
                most_category_count=max(opinion_words_categorys_dic.values())
                if opinion_words_categorys_dic[opinion_category]==most_category_count:
                    if opinion_category not in sentence_opinions_categorys_dic:
                        sentence_opinions_categorys_dic[opinion_category]=set([opinon_word])
                    else:
                        if opinon_word not in sentence_opinions_categorys_dic[opinion_category]:
                            sentence_opinions_categorys_dic[opinion_category].add(opinon_word)
        print sentence_attributes_categorys_set,sentence_opinions_categorys_dic
        if len(sentence_attributes_categorys_set)==len(sentence_opinions_categorys_dic):
            for category in sentence_attributes_categorys_set:
                poalrity_dic={}
                if category in sentence_opinions_categorys_dic:
                    for opinion_word in sentence_opinions_categorys_dic[category]:
                        polarity_list=[]
                        if opinion_word in polarity_count[category]:
                            max_polarity_count=max(polarity_count[category][opinion_word].values())
                            for polarity in polarity_count[category][opinion_word]:
                                if polarity_count[category][opinion_word][polarity]==max_polarity_count:
                                    polarity_list.append(polarity)
                        if len(polarity_list)==1:
                            for polarity_in_polarity_list in polarity_list:
                                if polarity_in_polarity_list not in poalrity_dic:
                                    poalrity_dic[polarity_in_polarity_list] =1
                                else:
                                    poalrity_dic[polarity_in_polarity_list] +=1
                    max_polarity_count=max(poalrity_dic.values())
                    polarity_list=[]
                    for polarity_in_polarity_dic in poalrity_dic:
                        if poalrity_dic[polarity_in_polarity_dic]==max_polarity_count:
                            polarity_list.append(polarity_in_polarity_dic)
                    print category,polarity_list[0]







