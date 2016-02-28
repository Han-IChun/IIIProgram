#  -*- coding: utf-8 -*-
from pymongo import MongoClient
import json

f=open('aspec.json','r')
aspect = json.loads(f.read().decode('utf8'))
f.close()
asp={"camera":[0,0],"game":[0,0],"shape":[0,0],"audio":[0,0],"price":[0,0],"hardware":[0,0],"system":[0,0],"battery":[0,0]}
tags_cellphon={}
client = MongoClient('localhost', 27017)
db = client.project
cursor = db.articles.find({"phone":"A9"})
for doc in cursor:
    article_number=len(doc.get("oneArticle"))
    for number in range(0,article_number):
        sentences=doc.get("oneArticle")[number].get("sentence")
        for sentence in iter(sentences):
            for keys,values in sentence.iteritems():
                for key, value in values[0].iteritems():
                    aspBig=aspect[key]
                    for i in range(0,len(aspBig)):
                        if value=="positive":
                            asp[aspBig[i]][0]+=1
                        else:
                            asp[aspBig[i]][1]+=1
    for tag, times in doc.get("tags").items():
        if tag in tags_cellphon:
            tags_cellphon[tag]+=times
        else:
            tags_cellphon[tag]=times

db.cellphones.update({'name' : "A9"},
                     {'$set' : {'camera' : asp['camera'],
                                'game' : asp['game'],
                                'shape' : asp['shape'],
                                'audio' : asp['audio'],
                                'price' : asp['price'],
                                'hardware' : asp['hardware'],
                                'battery' : asp['battery'],
                                'system' : asp['system'],
                                'tags':tags_cellphon
                                }})










client.close()