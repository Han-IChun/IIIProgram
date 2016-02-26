# -*-coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response

from models import phoneInfo
from models import Recommend
from models import other
from models import percent

# Create your views here.

def index (request):
    return render(request,'index.html')

def getTagSentence(request,tagAndId):
    if 'tagAndId' in request.GET:
        tagAndId=request.GET['tagAndId']

    tag=tagAndId.split('/')[0]
    id=tagAndId.split('/')[1]
    articlesList=other().getTagSentenceDic(id,tag)

    return render_to_response('other.html',locals())

def getPhoneInfo(request,id):
    if 'id' in request.GET:
        id=request.GET['id']
    aspSet=('hardware','game','camera','battery','price','audio','shape','system')
    phoneInfoList=phoneInfo().getOnePhoneInfo(id)

    returnCosinSimilaritySortedList=[]
    tagsList=[]
    tagDic={}
    aspectScore={}
    info=phoneInfoList[0]
    info['photo']='/static/img/'+id+'.png'

    spec=phoneInfoList[0]['spec']

    tagsSum=sum(info['tags'].values())
    for tag in info['tags']:
        tagDic['tag']=tag
        tagDic['count']=info['tags'][tag]*1000/tagsSum
        tagsList.append(tagDic.copy())

    for asp in aspSet:
        aspectScore[asp]=info[asp][0]*100/(info[asp][0]+info[asp][1])

    cosinSimilaritySortedList=phoneInfo().getPhoneInfoRecommand(id)
    for i in range(0,4):
        returnCosinSimilaritySortedList.append(cosinSimilaritySortedList[i])



    return render_to_response('phone_info.html',locals())

def getRecommend(request,asp):

    aspDic={'business':'業務機','camera':'愛拍照','game':'手遊族','money':'小資族','music':'愛音樂','shap':'重外型'}
    aspect=aspDic[asp]

    finalHightLevelPhoneList=[]
    finalMediumLevelPhoneList=[]

    phoneInfoListDic=Recommend().getRecommendPhone(asp)

    hightLevelPhoneList=phoneInfoListDic['hightLevelPhoneList']
    mediumLevelPhoneList=phoneInfoListDic['mediumLevelPhoneList']
    for info in hightLevelPhoneList:
        info['url']='http://10.120.26.60:8000/phone/phone_info/?id='+info['name']
        info['photo']='/static/img/'+info['name']+'.png'
    for info in mediumLevelPhoneList:
        info['url']='http://10.120.26.60:8000/phone/phone_info/?id='+info['name']
        info['photo']='/static/img/'+info['name']+'.png'


    for i in range(0,4):
        if len(hightLevelPhoneList)>i:
            finalHightLevelPhoneList.append(hightLevelPhoneList[i])
        if len(mediumLevelPhoneList)>i:
            finalMediumLevelPhoneList.append(mediumLevelPhoneList[i])

    return render_to_response('recommend.html',locals())

def getPercent(request,aspAndId):
    if 'aspAndId' in request.GET:
        aspAndId=request.GET['aspAndId']
    asp=aspAndId.split('/')[0]
    id=aspAndId.split('/')[1]
    percentDic=percent().getRecommendPhone(asp,id)
    return render_to_response('percent.html',locals())


#getPhoneInfo('iphone')
#getTagSentence('螢幕大/Z3')
#getRecommend('game')
#getPercent('system/A5')



