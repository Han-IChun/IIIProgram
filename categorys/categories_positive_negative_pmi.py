# -*- coding: utf-8 -*-


def category_pmi(xmlfile,*categorys):

    from bs4 import BeautifulSoup as bs
    import math
    import json
    import codecs

    f=open(xmlfile,'r')
    soup=bs(f.read(),'xml')
    f.close()

    polarity_dic=['positive','negative','conflict','-']

    diccategory={}
    emptydic={}
    category=[]
    dicfinal={}

    for ele in polarity_dic:
        emptydic[ele]=0

    for ele in categorys:
        category.append(ele)
        diccategory[ele]={}


    for i in soup.select('sentence'):
        if len(i.select('aspectCategory'))>0:
            for j in i.select('aspectCategory'):
                filename=j['category']
                polarity=j['polarity']
                for ele in category:
                    if filename==ele:
                        for k in i.select('jieba')[0].text.split('\t'):
                            if len(k)>0:
                                if k not in diccategory[ele]:
                                    diccategory[ele][k.encode('utf-8')] =emptydic.copy()
                                    diccategory[ele][k.encode('utf-8')][polarity] +=1
                                else:
                                    diccategory[ele][k.encode('utf-8')][polarity] +=1



    f=open('polarity.json','w')
    json.dump(diccategory,f,ensure_ascii=False)
    f.close()

    for ele in diccategory:
        for i in diccategory[ele]:
            for w in i.decode('utf-8'):
                if w==u'快':
                    print ele,i,diccategory[ele][i]




category_pmi('label_num1_final.xml','camera','software','shap','audio','smooth','battery','brand','screen','hardware','price','other')