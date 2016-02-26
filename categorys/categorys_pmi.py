# -*- coding: utf-8 -*-
import json


def category_pmi(xmlfile,*categorys):

    from bs4 import BeautifulSoup as bs
    import math

    f=open(xmlfile,'r')
    soup=bs(f.read(),'xml')
    f.close()


    dictotal={}
    diccategory={}
    dicnotcategory={}
    emptydic={}
    categorys_dic={}
    category=[]
    dicfinal={}

    for ele in categorys:
        category.append(ele)

    for ele in category:
        diccategory[ele]=emptydic.copy()
        dicnotcategory[ele]=emptydic.copy()
        categorys_dic[ele]=' '

    for i in soup.select('sentence'):
        if len(i.select('aspectCategory'))>0:
            for j in i.select('aspectCategory'):
                filename=j['category']
                for ele in diccategory:
                    if filename==ele:
                        for k in i.select('jieba')[0].text.split('\t'):
                            if len(k)>0:
                                if k not in diccategory[ele]:
                                    diccategory[ele][k] =1
                                else:
                                    diccategory[ele][k] +=1
        for k in i.select('jieba')[0].text.split('\t'):
            if len(k)>0:
                if k not in dictotal:
                    dictotal[k] =1
                else:
                   dictotal[k] +=1

    for i in dicnotcategory :
        for j in diccategory:
            if i !=j:
                for k in diccategory[j]:
                    if k not in dicnotcategory[i]:
                        dicnotcategory[i][k] =0
                        dicnotcategory[i][k] +=diccategory[j][k]
                    else:
                        dicnotcategory[i][k] +=diccategory[j][k]

    total=len(dictotal.keys())
    category_count=categorys_dic.copy()
    notcategory_count=categorys_dic.copy()

    for ele in category:
        category_count[ele]=len(diccategory[ele].keys())
        notcategory_count[ele]=len(dicnotcategory[ele].keys())

    f=open('pmi.txt','w')
    for word in dictotal:
        dic=categorys_dic.copy()
        for ele in category:
            if word in diccategory[ele] and word in dicnotcategory[ele]:
                #print '1',word,ele,diccategory[ele][word],total,category_count[ele],dictotal[word]
                category_pmi=math.log((float(diccategory[ele][word]*total)/float(dictotal[word]*category_count[ele])),2)
                notcategory_pmi=math.log((float(dicnotcategory[ele][word]*total)/float(dictotal[word]*notcategory_count[ele])),2)
                #print word,dicnotcategory[ele][word],total,dictotal[word],notcategory_count[ele]
                dic[ele]=category_pmi-notcategory_pmi
            elif word not in diccategory[ele] and word in dicnotcategory[ele]:
                #print '2',word,ele,dicnotcategory[ele][word]
                category_pmi=0
                notcategory_pmi=math.log((float(dicnotcategory[ele][word]*total)/float(dictotal[word]*notcategory_count[ele])),2)
                dic[ele]=category_pmi-notcategory_pmi
            elif word in diccategory[ele] and word not in dicnotcategory[ele]:
                #print '3',word,ele,diccategory[ele][word]
                category_pmi=math.log((float(diccategory[ele][word]*total)/float(dictotal[word]*category_count[ele])),2)
                notcategory_pmi=0
                dic[ele]=category_pmi-notcategory_pmi
        valueslist=[]
        for values in dic.values():
            valueslist.append(str(values))
        pmi='{}\t{}\n'.format(word.encode('utf-8'),'\t'.join(valueslist))

        dicfinal[word.encode('utf-8')]=dic.copy()
        f.write(pmi)
    for l in dic:
        f.write(l+'\t')
    f.close()

    f=open('categorys_pmi.json','w')
    json.dump(dicfinal,f,ensure_ascii=False)
    f.close()




category_pmi('label_num1_final.xml','camera','software','shap','audio','smooth','battery','brand','screen','hardware','price','other')
#category_pmi('chinese_aspect_category_dataset.xml','food')