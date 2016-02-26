# -*-coding: utf-8 -*-
from django.db import models
from pymongo import MongoClient
import numpy

# Create your models here.




class phoneInfo(object):
    def __init__(self):
        self.client= MongoClient('10.120.26.22', 27017)

    def getOnePhoneInfo(self,name):
        db=self.client.project
        collection=db.cellphones

        phoneInfoList=[]
        for info in collection.find({'name':name}):
            phoneInfoList.append(info)


        return phoneInfoList

        client.close()

    def getPhoneInfoRecommand(self,name):
        db=self.client.project
        collection=db.cellphones

        aspList=['hardware','game','camera','battery','price','audio','shape','system']

        phoneAspScoreDic={}
        cosinSimilaritySortedList=[]
        phoneAndPriceDic={}

        for info in collection.find():
            phoneAndPriceDic[info['name']]=info['priceCellphone']
            phoneAspScore=[]
            for asp in aspList:
                if asp in info:
                    positiveAspScore=info[asp][0]
                    negativeAspScore=info[asp][1]
                    if positiveAspScore !=0 or negativeAspScore!=0:
                        aspScore=float(positiveAspScore*100)/float(positiveAspScore+negativeAspScore)
                        phoneAspScore.append(aspScore)
                    else:
                        phoneAspScore.append(100)
            phoneAspScoreDic[info['name']]=phoneAspScore

        targetPhoneAspScoreList=phoneAspScoreDic[name]
        cosinSimilarityDic={}
        for phone in phoneAspScoreDic:
            if phone !=name:
                comparePhoneAspScore=phoneAspScoreDic[phone]
                cosinDegree=phoneInfo().getDocDistance(targetPhoneAspScoreList,comparePhoneAspScore)
                cosinSimilarityDic[cosinDegree]=phone
        for score in sorted(cosinSimilarityDic.keys(),reverse=True):
            cosinSimilaritySortedDic={}
            cosinSimilaritySortedDic['name']=cosinSimilarityDic[score]
            cosinSimilaritySortedDic['price']=phoneAndPriceDic[cosinSimilarityDic[score]]
            cosinSimilaritySortedDic['url']='http://10.120.26.60:8000/phone/phone_info/?id='+cosinSimilarityDic[score]
            cosinSimilaritySortedDic['photo']='/static/img/'+cosinSimilarityDic[score]+'.png'
            cosinSimilaritySortedList.append(cosinSimilaritySortedDic.copy())

        return cosinSimilaritySortedList
        client.close()

    def getDocDistance(self,a,b):
        if numpy.linalg.norm(a)==0 or numpy.linalg.norm(b)==0:
            return -1
        return round(numpy.inner(a,b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b)), 4)

class Recommend(object):
    def __init__(self):
        self.client= MongoClient('10.120.26.22', 27017)

    def getRecommendPhone(self,asp):
        db=self.client.project
        collection=db.cellphones
        phoneInfoListDic={}
        sortDic={}
        sortedNameList=[]
        phoneTotalList=[]
        phoneInfoList=[]
        hightLevelPhoneList=[]
        mediumLevelPhoneList=[]
        recommand2AspectDic={'business':['hardware','battery'],'camera':['camera'],'game':['game'],'money':['price'],'music':['audio'],'shap':['shape']}

        for info in collection.find():
            #print info['name'],info['price']
            phoneTotalList.append(info)


        for phone in phoneTotalList:
            positiveCount=0
            negativeCount=0
            for aspect in recommand2AspectDic[asp]:
                if aspect in phone:
                    if phone[aspect][0]!=0 or phone[aspect][1]!=0:
                        #print phone['name'],aspect,phone[aspect]
                        positiveCount +=phone[aspect][0]
                        negativeCount +=phone[aspect][1]

            if positiveCount !=0 or negativeCount !=0:
                sortDic[float(positiveCount*100)/float(negativeCount+positiveCount)]=phone['name']
                #print phone['name'],positiveCount,negativeCount,float(positiveCount*100)/float(negativeCount+positiveCount)

        for sortedScore in sorted(sortDic.keys(),reverse=True):
            sortedNameList.append(sortDic[sortedScore])



        for phoneName in sortedNameList:
            for phone in phoneTotalList:
                if phone['name']==phoneName:
                    phoneInfoList.append(phone)

        for phone in phoneInfoList:
            phone['priceCellphone']=''.join(phone['priceCellphone'].split())
            if int(''.join(''.join(phone['priceCellphone'].split(',')).split()))>12000:
                hightLevelPhoneList.append(phone)
            elif int(''.join(''.join(phone['priceCellphone'].split(',')).split()))<=12000:
                mediumLevelPhoneList.append(phone)

        phoneInfoListDic['hightLevelPhoneList']=hightLevelPhoneList
        phoneInfoListDic['mediumLevelPhoneList']=mediumLevelPhoneList


        return phoneInfoListDic
        client.close()



class other(object):
    def __init__(self):
        self.client= MongoClient('10.120.26.22', 27017)
    def getTagSentenceDic(self,id,tag):
        articlesList=[]
        db=self.client.project
        collection=db.articles
        for oneArticle in collection.find({'phone':id}):
            if len(oneArticle['oneArticle'][0]['tags'])>0:
                for i in oneArticle['oneArticle'][0]['tags']:
                    if i==tag:
                        articleDic={}
                        articleDic['subsentenceList']=[]
                        date=oneArticle['oneArticle'][0]['date']
                        articleDic['date']=date
                        for sentence in oneArticle['oneArticle'][0]['sentences']:
                            subsentenceDic={}
                            for j in sentence:
                                if tag not in sentence[j][1]:
                                    subsentenceDic['subsentence']=j
                                    subsentenceDic['tag']='false'
                                elif tag  in sentence[j][1]:
                                    subsentenceDic['subsentence']=j
                                    subsentenceDic['tag']='true'
                                articleDic['subsentenceList'].append(subsentenceDic.copy())
                        articlesList.append(articleDic.copy())
        return articlesList

class percent(object):
    def __init__(self):
        self.client= MongoClient('10.120.26.22', 27017)
    def getRecommendPhone(self,asp,id):
        db=self.client.project
        collection=db.cellphones
        percentDic={'10':0,'20':0,'30':0,'40':0,'50':0,'60':0,'70':0,'80':0,'90':0,'100':0,'phoneScore':''}
        for info in collection.find():
            if asp in info:
                if info[asp][0] !=0 or info[asp][1] !=0:
                    score=float(info[asp][0]*100)/(info[asp][0]+info[asp][1])
                    if score>=0 and score <10:
                        percentDic['10']+=5
                    elif score>=10 and score <20:
                        percentDic['20']+=5
                    elif score>=20 and score <30:
                        percentDic['30']+=5
                    elif score>=30 and score <40:
                        percentDic['40']+=5
                    elif score>=40 and score <50:
                        percentDic['50']+=5
                    elif score>=50 and score <60:
                        percentDic['60']+=5
                    elif score>=60 and score <70:
                        percentDic['70']+=5
                    elif score>=70 and score <80:
                        percentDic['80']+=5
                    elif score>=80 and score <90:
                        percentDic['90']+=5
                    elif score>=90 and score <100:
                        percentDic['100']+=5
        for info in collection.find():
            if info['name']==id and asp in info :
                if info[asp][0] !=0 or info[asp][1] !=0:
                    score=float(info[asp][0]*100)/(info[asp][0]+info[asp][1])
                    percentDic['phoneScore']=score
        return percentDic



#other().getTagSentenceDic('A5',u'好用')
#Recommend().getRecommendPhone('money')
#percent().getRecommendPhone('price','A5')
#phoneInfo().getOnePhoneInfo('A9')
phoneInfo().getPhoneInfoRecommand('A5')

