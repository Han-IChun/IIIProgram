# -*-coding: utf-8 -*-
import jieba
import json
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import re
import xml.etree.ElementTree as ET
import math
import lxml.etree as etree

class mongoDBNeed(object):
    global client
    global db
    global collection

    def making_connection(self,ip):
        client= MongoClient(ip, 27017)

    def connect_database(self,databasename):
        db=client.databasename

    def connect_collection(self,collectionname):
        collection=db.collectionname

    def connection_close(self):
        client.close()

    def mobilHTML2ArticlesJsonFormat(self,inputdir,file):
        articleDic={}
        oneArticleList=[]


        filename=file.decode('cp950')
        m= re.match('(.*).txt$',filename)
        n=re.search('/(\w+)$',inputdir)
        f=open(inputdir+'/'+filename,'r')
        soup=bs(f.read(),"html.parser")


        title=m.group(1)
        phone=n.group(1)


        for content in soup.select('article'):
            oneArticleDic={}

            date=content.select('.date')[0].text.split(' ')[0]
            author=''.join(content.select('.fn')[0].text.split())
            completeSentence=''
            if len(content.select('blockquote'))>0:
                totalContent=''.join(content.select('.single-post-content')[0].text.split())
                againContent=''.join(content.select('blockquote')[0].text.split())
                finalContent=totalContent.split(againContent)
                for sentence in finalContent:
                    if len(sentence)>0:
                        completeSentence=sentence
            else:
                finalContent=''.join(content.select('.single-post-content')[0].text.replace('\n',',').split())
                completeSentence=finalContent


            oneArticleDic['date']=date
            oneArticleDic['author']=author.encode('utf-8')
            oneArticleDic['completeSentence']=completeSentence.encode('utf-8')
            oneArticleDic['sentences']=[]
            oneArticleList.append(oneArticleDic)

        articleDic['phone']=phone.encode('utf-8')
        articleDic['title']=title.encode('utf-8')
        articleDic['oneArticle']=oneArticleList
        if articleDic !={}:
            return articleDic




class CRFPlus(object):

    def makeAspSet(self):

        aspSet=set()

        f=open('dic/asp_dic.txt','r')
        for line in f.readlines():
            word =line.split(' ')[0].strip().decode('utf-8')
            if word not in aspSet:
                aspSet.add(word)
        f.close()

        return aspSet

    def makeOpinionSet(self):

        opinionSet=set()

        f=open('dic/opinion_dic.txt','r')
        for line in f.readlines():
            word =line.split(' ')[0].strip().decode('utf-8')
            if word not in opinionSet:
                opinionSet.add(word)
        f.close()

        return opinionSet

    def makespeechDic(self):
        speechDic={}


        f=open('dic/asp_dic.txt','r')
        for line in f.readlines():
            word =line.split(' ')[0].strip().decode('utf-8')
            speech=line.split(' ')[1].strip().decode('utf-8')
            if word not in speechDic:
                speechDic[word]=speech
        f.close()

        f=open('dic/opinion_dic.txt','r')
        for line in f.readlines():
            word =line.split(' ')[0].strip().decode('utf-8')
            speech=line.split(' ')[1].strip().decode('utf-8')
            if word not in speechDic:
                speechDic[word]=speech
        f.close()


        f=open('dic/dict.txt.big','r')
        for line in f.readlines():
            word =line.split(' ')[0].strip().decode('utf-8')
            speech=line.split(' ')[2].strip().decode('utf-8')
            if word not in speechDic:
                speechDic[word]=speech
        f.close()

        return speechDic

    def setJiebaDic(self):
        jieba.set_dictionary('dic/dict.txt.big')
        jieba.load_userdict('dic/opinion_dic.txt')
        jieba.load_userdict('dic/userdict.txt')
        jieba.load_userdict('dic/asp_dic.txt')


    def makeCRFFormat(self,speechDic,aspSet,sentence,outputFileDir):


            fid=open(outputFileDir,'w')
        #for line in f.readlines():
        #   line=''.join(line.split())
            for wordCut in jieba.cut(sentence,HMM=False):
                speech=''
                inAspSet=''
                firstWord=wordCut
                lastWord=wordCut.encode('utf-8')
                wordCutLen=''


                if wordCut in speechDic:
                    speech=speechDic[wordCut]
                else:
                    speech='NA'

                if wordCut in aspSet:
                    inAspSet='T'
                else:
                    inAspSet='F'

                if len(wordCut)>=1:
                    firstWord=wordCut[0].encode('utf-8')
                    lastWord=wordCut[-1].encode('utf-8')

                if len(wordCut)<=2:
                    wordCutLen='Len<=2'
                else:
                    wordCutLen='Len>2'


                CRFFornat='{}\t{}\t{}\t{}\t{}\t{}\n'.format(wordCut.encode('utf-8'),speech,inAspSet,firstWord,lastWord,wordCutLen)
                fid.write(CRFFornat)
            fid.write('\n')
            fid.close()
        #f.close()


    def completeSentence2SentencesList(self,completeSentence):

        markSet=set(['?','!',','])
        sentencesList=[]

        for mark in markSet:
            completeSentence=re.sub(re.escape(mark),'\t',completeSentence)
        for subSentence in completeSentence.split():
            sentencesList.append(subSentence)

        return sentencesList


    def CRFCommand(self,command):
        os.system('E:&cd E:\Python\CRF++-0.58 &'+command)


class generateNeedModel(object):

    def resetXMLJiebaTxet(self,inputdir):
        f=open(inputdir,'r')
        content=bs(f.read(),'xml')
        f.close()


        XMLDic={}
        sentenceDic={'polarity':'','jieba':'','asp':''}
        sentenceList=[]
        sentences=ET.Element('sentences')
        for ele in content.select('sentence'):
            polarity=ele['polarity']
            sentence=ele.select('text')[0].text


            aspDic={}
            for asp in ele.select('aspectCategory'):
                aspDic[asp['term']]=asp['polarity']


            sentenceList.append(sentence)

            sentenceDic['asp']=aspDic
            sentenceDic['polarity']=polarity
            sentenceDic['jieba']='\t'.join(jieba.cut(sentence,HMM=False))
            XMLDic[sentence]=sentenceDic.copy()

        for ele in sentenceList:

            sentence=ET.SubElement(sentences,'sentence')
            sentence.attrib={'polarity':XMLDic[ele]['polarity']}
            text=ET.SubElement(sentence,'text')
            text.text=ele

            aspectCategories=ET.SubElement(sentence,'aspectCategories')


            for asp in XMLDic[ele]['asp']:
                aspectCategory=ET.SubElement(aspectCategories,'aspectCategory')
                aspectCategory.attrib={'category':asp,'polarity':XMLDic[ele]['asp'][asp]}


            jieb=ET.SubElement(sentence,'jieba')

            jieb.text=(XMLDic[ele]['jieba'])


        tree=ET.ElementTree(sentences)
        ET.ElementTree(sentences).write('test.xml',encoding="UTF-8",xml_declaration=True)

    def categoryPmi(self,xmlfile,outputdir,*categorys):

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
            category.append(ele.encode('utf-8'))

        for ele in category:
            diccategory[ele]=emptydic.copy()
            dicnotcategory[ele]=emptydic.copy()
            categorys_dic[ele]=' '

        for i in soup.select('sentence'):
            if len(i.select('aspectCategory'))>0:
                for j in i.select('aspectCategory'):
                    filename=j['category'].encode('utf-8')
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

        for word in dictotal:
            dic=categorys_dic.copy()
            for ele in category:
                if word in diccategory[ele] and word in dicnotcategory[ele]:
                    category_pmi=math.log((float(diccategory[ele][word]*total)/float(dictotal[word]*category_count[ele])),2)
                    notcategory_pmi=math.log((float(dicnotcategory[ele][word]*total)/float(dictotal[word]*notcategory_count[ele])),2)

                    dic[ele]=category_pmi-notcategory_pmi
                elif word not in diccategory[ele] and word in dicnotcategory[ele]:
                    category_pmi=0
                    notcategory_pmi=math.log((float(dicnotcategory[ele][word]*total)/float(dictotal[word]*notcategory_count[ele])),2)
                    dic[ele]=category_pmi-notcategory_pmi
                elif word in diccategory[ele] and word not in dicnotcategory[ele]:

                    category_pmi=math.log((float(diccategory[ele][word]*total)/float(dictotal[word]*category_count[ele])),2)
                    notcategory_pmi=0
                    dic[ele]=category_pmi-notcategory_pmi


            dicfinal[word.encode('utf-8')]=dic.copy()

        f=open(outputdir,'w')
        json.dump(dicfinal,f,ensure_ascii=False)
        f.close()


    def generateAspword2asp(self,inputDir,outputDir):
        asp2OpiniodDic={}
        f=open(inputDir,'r')

        firstline=f.readline()
        for line in f.readlines():
            asp=line.split('\t')[0]
            for word in line.split('\t')[1].split(','):
                aspWord=word.strip()
                if aspWord not in asp2OpiniodDic:
                    asp2OpiniodDic[aspWord]=asp
        f.close()

        f=open(outputDir,'w')
        json.dump(asp2OpiniodDic,f,ensure_ascii=False)
        f.close()

    def categoryPolarityPmi(self,xmlfile,outputdir,*categorys):

        f=open(xmlfile,'r')
        soup=bs(f.read(),'xml')
        f.close()

        polarity_dic=['positive','negative']

        diccategory={}
        emptydic={}
        category=[]

        for ele in polarity_dic:
            emptydic[ele]=0

        for ele in categorys:
            category.append(ele.encode('utf-8'))
            diccategory[ele.encode('utf-8')]={}


        for i in soup.select('sentence'):
            if len(i.select('aspectCategory'))>0:
                for j in i.select('aspectCategory'):
                    filename=j['category']
                    polarity=j['polarity']
                    for ele in category:
                        if filename.encode('utf-8')==ele:
                            for k in i.select('jieba')[0].text.split('\t'):
                                if len(k)>0:
                                    if k not in diccategory[ele]:
                                        diccategory[ele][k.encode('utf-8')] =emptydic.copy()
                                        diccategory[ele][k.encode('utf-8')][polarity] +=1
                                    else:
                                        diccategory[ele][k.encode('utf-8')][polarity] +=1



        f=open(outputdir,'w')
        json.dump(diccategory,f,ensure_ascii=False)
        f.close()

    def generateAspword2OpinionPolarity(self,inputDir,outputDir):

        CRFPlus().setJiebaDic()
        aspSet=CRFPlus().makeAspSet()
        opinionSet=CRFPlus().makeOpinionSet()

        aspword2OpinionPolarityDic={}
        polarityDic={'positive':0,'negative':0}


        for file in os.listdir(inputDir):
            f=open(inputDir+'/'+file.decode('cp950'),'r')
            firstline=f.readline()
            for line in f.readlines():
                opinionList=[]
                aspList=[]
                line=line.strip()
                if len(line)>0:
                    sentence=''.join(line.split('\t')[0].split())
                    polarity=line.split('\t')[1]

                    for wordCut in jieba.cut(sentence,HMM=False):
                        print wordCut in opinionSet,wordCut
                        if wordCut in opinionSet:
                            opinionList.append(wordCut)
                        if wordCut in aspSet:
                            aspList.append(wordCut)
                    for aspWord in aspList:
                        aspWord=aspWord.encode('utf-8')
                        if aspWord not in aspword2OpinionPolarityDic:
                            aspword2OpinionPolarityDic[aspWord]={}

                        for opinionWord in opinionList:
                            opinionWord=opinionWord.encode('utf-8')
                            if opinionWord not in aspword2OpinionPolarityDic[aspWord]:
                                aspword2OpinionPolarityDic[aspWord][opinionWord]=polarityDic.copy()
                                aspword2OpinionPolarityDic[aspWord][opinionWord][polarity] =1
                            else:
                                #print aspWord,opinionWord,aspword2OpinionPolarityDic[aspWord][opinionWord],file,line
                                aspword2OpinionPolarityDic[aspWord][opinionWord][polarity] +=1
        f=open(outputDir,'w')
        json.dump(aspword2OpinionPolarityDic,f,ensure_ascii=False)
        f.close()

    def word2WordPloarityPmi(self,inputDir,outputDir):

        CRFPlus().setJiebaDic()

        word2WordPloarityPmi={}
        polarityDic={'positive':0,'negative':0}


        for file in os.listdir(inputDir):
            f=open(inputDir+'/'+file.decode('cp950'),'r')
            firstline=f.readline()
            for line in f.readlines():
                wordCutList=[]
                line=line.strip()
                if len(line)>0:
                    if len(line.split('\t'))>1:
                        sentence=''.join(line.split('\t')[0].split())
                        polarity=''.join(line.split('\t')[1].split())


                        for wordCut in jieba.cut(sentence,HMM=False):
                            wordCutList.append(wordCut.encode('utf-8'))
                        for i in wordCutList:
                            if i not in word2WordPloarityPmi:
                                word2WordPloarityPmi[i]={}
                                for j in wordCutList:
                                    if j not in word2WordPloarityPmi[i]:
                                        word2WordPloarityPmi[i][j]=polarityDic.copy()
                                        word2WordPloarityPmi[i][j][polarity]=1
                                    else:
                                        word2WordPloarityPmi[i][j][polarity]+=1
                            else:
                                for j in wordCutList:
                                    if j not in word2WordPloarityPmi[i]:
                                        word2WordPloarityPmi[i][j]=polarityDic.copy()
                                        word2WordPloarityPmi[i][j][polarity]=1
                                    else:
                                        word2WordPloarityPmi[i][j][polarity]+=1




        f=open(outputDir,'w')
        json.dump(word2WordPloarityPmi,f,ensure_ascii=False)
        f.close()


class sentenceAspAndPolarity(object):


    def categorysPmi(self):
        f=open('json/categorysPmi.json','r')
        categorysPmi= json.loads(f.read().decode('utf-8'))
        f.close()
        return categorysPmi
    def categoryPolarityPmi(self):
        f=open('json/categoryPolarityPmi.json','r')
        categoryPolarityPmi= json.loads(f.read().decode('utf-8'))
        f.close()
        return categoryPolarityPmi

    def att2OpnDic(self):
        f=open('json/aspword2OpinionPolarity.json','r')
        att2OpnDic= json.loads(f.read().decode('utf-8'))
        f.close()
        return att2OpnDic

    def polarityPmi(self):
        f=open('json/word2PositiveNegativePmi.json','r')
        polarityPmi= json.loads(f.read().decode('utf-8'))
        f.close()
        return polarityPmi

    def att2CategoryDic(self):
        f=open('json/aspword2Asp.json','r')
        att2CategoryDic= json.loads(f.read().decode('utf-8'))
        f.close()
        return att2CategoryDic
    def word2WordPloarityPmi(self):
        f=open('json/word2WordPloarityPmi.json','r')
        word2WordPloarityPmi= json.loads(f.read().decode('utf-8'))
        f.close()
        return word2WordPloarityPmi

    def asp2Tag(self):
        f=open('json/asp2Tag.json','r')
        asp2TagDic= json.loads(f.read().decode('utf-8'))
        f.close()
        return asp2TagDic

    def wholeSentenceAttOpinList(self,attributeSet,opinionSet):
        wholeSentenceList=[]
        attributeList=[]
        opinionList=[]
        subAttributeList=[]
        subOpinionList=[]
        f=open('CRF++-0.58/conll_output.txt','r')
        for lines in f.readlines():
            lines=lines.strip()
            lineList=lines.split('\xef\xbb\xbf')
            if len(lineList)==2:
                line =lineList[1]
            else:
                line=lineList[0]
            if len(line.decode('utf-8'))>1:
                wholeSentenceList.append(line.split("\t")[0])
                if line.split('\t')[6] in attributeSet:
                    attWord=line.split('\t')[0]
                    attribute=line.split('\t')[6]
                    if attribute=='B_A':
                        subAttributeList.append(attWord)
                    if attribute=='I_A':
                        subAttributeList.append(attWord)
                    if attribute=='E_A':
                        subAttributeList.append(attWord)
                        attributeList.append(subAttributeList)
                        subAttributeList=[]
                    if attribute=='A':
                        subAttributeList.append(attWord)
                        attributeList.append(subAttributeList)
                        subAttributeList=[]
                if line.split('\t')[6] in opinionSet:
                    opinionWord=line.split('\t')[0]
                    opinion=line.split('\t')[6]
                    if opinion=='B_O':
                        subOpinionList.append(opinionWord)
                    if opinion=='I_O':
                        subOpinionList.append(opinionWord)
                    if opinion=='E_O':
                        subOpinionList.append(opinionWord)
                        opinionList.append(subOpinionList)
                        subOpinionList=[]
                    if opinion=='O':
                        subOpinionList.append(opinionWord)
                        opinionList.append(subOpinionList)
                        subOpinionList=[]
        listDic={'wholeSentenceList':wholeSentenceList,'attributeList':attributeList,'opinionList':opinionList}
        return listDic

    def oneOpinionWord2Polarity(self,att2OpnDic,polarityPmi,categoryPolarityPmi,opinionList,negativeSet,aspect,attWord):
        polarity=''
        if len(opinionList[0])==1:
            opinionWord=opinionList[0][0].decode('utf-8')

            if attWord in att2OpnDic and opinionWord in att2OpnDic[attWord]:

                polarity='positive'
                if att2OpnDic[attWord][opinionWord]['negative']>att2OpnDic[attWord][opinionWord]['positive']:
                    polarity='negative'

            elif opinionWord in categoryPolarityPmi[aspect]:

                polarity='positive'
                if categoryPolarityPmi[aspect][opinionWord]['negative']>categoryPolarityPmi[aspect][opinionWord]['positive']:
                    polarity='negative'

            elif opinionWord in polarityPmi:

                polarity='positive'
                if polarityPmi[opinionWord]['negative']>polarityPmi[opinionWord]['positive']:
                    polarity='negative'

        else:
            if ''.join(opinionList[0]).decode('utf-8') in att2OpnDic and ''.join(opinionList[0]).decode('utf-8') in att2OpnDic[attWord]:
                opinionWord=''.join(opinionList[0]).decode('utf-8')
                if att2OpnDic[attWord][opinionWord]['negative']>att2OpnDic[attWord][opinionWord]['positive']:
                    polarity='negative'

            elif ''.join(opinionList[0]).decode('utf-8') in categoryPolarityPmi[aspect]:
                opinionWord=''.join(opinionList[0]).decode('utf-8')
                polarity='positive'
                if categoryPolarityPmi[aspect][opinionWord]['negative']>categoryPolarityPmi[aspect][opinionWord]['positive']:
                    polarity='negative'

            elif ''.join(opinionList[0]).decode('utf-8') in polarityPmi:
                opinionWord=''.join(opinionList[0]).decode('utf-8')
                polarity='positive'
                if polarityPmi[opinionWord]['negative']>polarityPmi[opinionWord]['positive']:
                    polarity='negative'
            else:
                negativeCount=0
                for opinionWord in opinionList[0]:
                    opinionWord=opinionWord.decode('utf-8')
                    if opinionWord in negativeSet:
                        negativeCount +=1
                    elif attWord in att2OpnDic and opinionWord in att2OpnDic[attWord]:
                        polarity='positive'
                        if att2OpnDic[attWord][opinionWord]['negative']>att2OpnDic[attWord][opinionWord]['positive']:
                            polarity='negative'

                    elif opinionWord in categoryPolarityPmi[aspect]:
                        polarity='positive'
                        if categoryPolarityPmi[aspect][opinionWord]['negative']>categoryPolarityPmi[aspect][opinionWord]['positive']:
                            polarity='negative'
                    elif opinionWord in polarityPmi:
                        polarity='positive'
                        if polarityPmi[opinionWord]['negative']>polarityPmi[opinionWord]['positive']:
                            polarity='negative'

                if negativeCount%2==1:
                    if polarity=='positive':
                        polarity='negative'
                    else:
                        polarity='positive'
        return polarity

    def moreThanOneOpinionWord2Polarity(self,polarityPmi,categorysPmi,categoryPolarityPmi,opinionList,negativeSet,wholeSentenceList,aspect,attWord):
        polarity=''
        finalPmi=0
        wordPositionDic={}
        for position in range(0,len(wholeSentenceList)):
            wordPositionDic[wholeSentenceList[position]]=position
        attWordPosition=wordPositionDic[attWord.encode('utf-8')]

        for opinionWords in opinionList:
            subPmi=0
            if len(opinionWords)==1:
                opinionWord=opinionWords[0].decode('utf-8')
                distance=abs(wordPositionDic[opinionWord.encode('utf-8')]-attWordPosition)

                if opinionWord in categoryPolarityPmi[aspect]:

                    subPmiPolarity=categoryPolarityPmi[aspect][opinionWord]['positive']-categoryPolarityPmi[aspect][opinionWord]['negative']
                    polarityCount=categoryPolarityPmi[aspect][opinionWord]['positive']+categoryPolarityPmi[aspect][opinionWord]['negative']
                    subPmi=float(subPmiPolarity)/float(distance*polarityCount)

                elif opinionWord in polarityPmi and opinionWord in categorysPmi:

                    subPmiPolarity=polarityPmi[opinionWord]['positive']-polarityPmi[opinionWord]['negative']
                    subPmi=subPmiPolarity*(max(0,categorysPmi[opinionWord][aspect]))/distance

            else:
                negativeCount=0
                for opinionWord in opinionWords:
                    subSubPmi=0
                    opinionWordCount=0
                    opinionWord=opinionWord.decode('utf-8')
                    distance=abs(wordPositionDic[opinionWord.encode('utf-8')]-attWordPosition)
                    if opinionWord in negativeSet:
                        negativeCount +=1
                    elif opinionWord in categoryPolarityPmi[aspect]:
                        opinionWordCount+=1
                        subPmiPolarity=categoryPolarityPmi[aspect][opinionWord]['positive']-categoryPolarityPmi[aspect][opinionWord]['negative']
                        polarityCount=categoryPolarityPmi[aspect][opinionWord]['positive']+categoryPolarityPmi[aspect][opinionWord]['negative']
                        subSubPmi=subPmiPolarity/distance*polarityCount
                        subPmi+=subSubPmi
                    elif opinionWord in polarityPmi and opinionWord in categorysPmi:
                        opinionWordCount+=1
                        subPmiPolarity=polarityPmi[opinionWord]['positive']-polarityPmi[opinionWord]['negative']
                        subSubPmi=subPmiPolarity*(max(0,categorysPmi[opinionWord][aspect]))/distance
                        subPmi+=subSubPmi
                subPmi=subPmi/opinionWordCount
                if negativeCount%2==1:
                    subPmi=subPmi*(-1)
            finalPmi+=subPmi
            if finalPmi<0:
                polarity='negative'
            elif finalPmi>0:
                polarity='positive'

        return polarity





    def giveSentenceAspPolarity(self,att2CategoryDic,att2OpnDic,categorysPmi,polarityPmi,categoryPolarityPmi,wholeSentenceList,attributeList,opinionList):
        """
                這份程式在測用論文的方式取得句子的情緒
                分為三種情況：
                case1: 1by1,1by m,m by 1
                case2: 0 by 1, 0 by M:
                case3: m by m

                case1: 利用屬性詞對意見詞的極性字典與屬性詞對面向的字典，直接找出屬相詞的面向，跟他對意見詞的極性
                case2:aj4
                """
        aspList=[]
        aspDic={}
        polaritySet=('positive','negative','conflict')
        connectWordSet=(u'的',u'跟',u'和')
        negativeSet=(u'不',u'沒',u'不是',u'沒有',u'不算',u'不夠',u'不能',u'不行',u'不會')

        if len(attributeList)>0 and len(opinionList)>0:#屬性詞和意見詞都不為零
            if len(opinionList)==1:
                for attWords in attributeList:
                    for attWord in attWords:
                        aspect=''
                        polarity=' '
                        attWord=attWord.decode('utf-8')
                        if attWord not in connectWordSet:
                            if attWord in att2CategoryDic:
                                aspect=att2CategoryDic[attWord]

                                polarity=sentenceAspAndPolarity().oneOpinionWord2Polarity(att2OpnDic,polarityPmi,categoryPolarityPmi,opinionList,negativeSet,aspect,attWord)

                            elif attWord in categorysPmi:
                                maxPmi=max(categorysPmi[attWord].values())
                                for asp in categorysPmi[attWord]:
                                    if categorysPmi[attWord][asp]==maxPmi:
                                        aspect=asp
                                polarity=sentenceAspAndPolarity().oneOpinionWord2Polarity(att2OpnDic,polarityPmi,categoryPolarityPmi,opinionList,negativeSet,aspect,attWord)


                            if aspect not in aspDic:
                                if polarity in polaritySet:
                                    aspDic[aspect]=polarity
                            else:
                                if aspDic[aspect]!=polarity and polarity in polaritySet:
                                    aspDic[aspect]='conflict'


            else:
                for attWords in attributeList:
                    for attWord in attWords:
                        aspect=''
                        polarity=' '
                        attWord=attWord.decode('utf-8')
                        if attWord not in connectWordSet:
                            if attWord in att2CategoryDic:
                                aspect=att2CategoryDic[attWord]
                                polarity=sentenceAspAndPolarity().moreThanOneOpinionWord2Polarity(polarityPmi,categorysPmi,categoryPolarityPmi,opinionList,negativeSet,wholeSentenceList,aspect,attWord)

                            elif attWord in categorysPmi:
                                maxPmi=max(categorysPmi[attWord].values())
                                for asp in categorysPmi[attWord]:
                                    if categorysPmi[attWord][asp]==maxPmi:
                                        aspect=asp
                                        polarity=sentenceAspAndPolarity().moreThanOneOpinionWord2Polarity(polarityPmi,categorysPmi,categoryPolarityPmi,opinionList,negativeSet,wholeSentenceList,aspect,attWord)

                            if aspect not in aspDic:
                                if polarity in polaritySet:
                                    aspDic[aspect]=polarity
                            else:
                                if aspDic[aspect]!=polarity and polarity in polaritySet:
                                    aspDic[aspect]='conflict'

        elif len(attributeList)==0 and len(opinionList)>0:
            for opinionWords in opinionList:
                polarity=' '
                if len(opinionWords)==1:
                    aspect=''
                    opinionWord=opinionWords[0].decode('utf-8')
                    if opinionWord in categorysPmi:
                        maxPmi=max(categorysPmi[opinionWord].values())
                        for asp in categorysPmi[opinionWord]:
                            if categorysPmi[opinionWord][asp]==maxPmi:
                                aspect=asp
                        if opinionWord in categoryPolarityPmi[aspect]:
                            polarity='positive'
                            if categoryPolarityPmi[aspect][opinionWord]['negative']>categoryPolarityPmi[aspect][opinionWord]['positive']:
                                polarity='negative'

                        elif opinionWord in polarityPmi:
                            polarity='positive'
                            if polarityPmi[opinionWord]['negative']>polarityPmi[opinionWord]['positive']:
                                polarity='negative'

                        if aspect not in aspDic:
                            if polarity in polaritySet:
                                aspDic[aspect]=polarity
                        else:
                            if aspDic[aspect]!=polarity and polarity in polaritySet:
                                aspDic[aspect]='conflict'

                else:
                    negativeCount=0
                    for opinionWord in opinionWords:
                        aspect=''
                        opinionWord=opinionWord.decode('utf-8')
                        if opinionWord in negativeSet:
                            negativeCount +=1
                        elif opinionWord in categorysPmi:
                            maxPmi=max(categorysPmi[opinionWord].values())
                            for asp in categorysPmi[opinionWord]:
                                if categorysPmi[opinionWord][asp]==maxPmi:
                                    aspect=asp

                            if opinionWord in categoryPolarityPmi[aspect]:
                                polarity='positive'
                                if categoryPolarityPmi[aspect][opinionWord]['negative']>categoryPolarityPmi[aspect][opinionWord]['positive']:
                                    polarity='negative'
                            elif opinionWord in polarityPmi:
                                polarity='positive'
                                if polarityPmi[opinionWord]['negative']>polarityPmi[opinionWord]['positive']:
                                    polarity='negative'

                        if aspect not in aspDic:
                            if polarity in polaritySet:
                                aspDic[aspect]=polarity
                        else:
                            if aspDic[aspect]!=polarity and polarity in polaritySet:
                                aspDic[aspect]='conflict'
        aspList.append(aspDic)
        return aspList


'''
        aspList=[]

        if len(attributeList)>1 and len(opinionList)>1:  # case3
            aspDic={}
            for att_words in attributeList:
                for att_word in att_words:
                    att_word=att_word.decode('utf-8')
                    if att_word in categorysPmi:
                        distance=0
                        for opn_words in opinionList:
                            for opn_word in opn_words:
                                opn_word=opn_word.decode('utf-8')
                                if opn_word in polarityPmi:
                                    t_a=polarityPmi[opn_word].values() #get "att_wrods"'s positive and negtive score .  t_a=[0.0xxx, 0.xxxx]
                                    rating_pmi=t_a[0]-t_a[1]
                                    pol=categorysPmi[att_word].values()
                                    position=pol.index(max(pol))
                                    aspect= categorysPmi[att_word].keys()[position]
                                    t_o=categorysPmi[opn_word][aspect]
                                    distance+=float(rating_pmi)*max([0,t_o])/abs(wholeSentenceList.index(att_word.encode('utf-8'))-wholeSentenceList.index(opn_word.encode('utf-8')))
                            if distance>0:
                                polarity="positive"
                            else:
                                polarity="negtive"
                        if aspect not in aspDic:
                            aspDic[aspect]=polarity
                        print "Aspect:",aspect,"\t","Polarity:",polarity,"\t","Score:",distance
            aspList.append(aspDic)
            print "*******************************************************************************"


        elif len(attributeList)==0 and len(opinionList)!=0: # case 2
            aspDic={}
            for opn_words in opinionList:
                for opn_word in opn_words:
                    opn_word=opn_word.decode('utf-8')
                    if opn_word in categorysPmi and opn_word in polarityPmi:
                        categorys_bank = categorysPmi[opn_word]
                        position_c=categorys_bank.values().index(max(categorys_bank.values()))
                        polarity_bank = polarityPmi[opn_word]
                        position_p=polarity_bank.values().index(max(polarity_bank.values()))
                        t_a=polarityPmi[opn_word].values() #get "att_wrods"'s positive and negtive score .  t_a=[0.0xxx, 0.xxxx]

                        aspect=categorys_bank.keys()[position_c]
                        polarity=polarity_bank.keys()[position_p]
                        score=t_a[0]-t_a[1]

                        if aspect not in aspDic:
                            aspDic[aspect]=polarity
                        print "Aspect:",aspect,"\t","Polarity:",polarity,"\t","Score:",score
            aspList.append(aspDic)
            print "*******************************************************************************"

        elif len(attributeList)==0 and len(opinionList)==0: # empty set
            pass

        else:    # case 1
            aspDic={}
            for att_words in attributeList:
                for att_word in att_words:
                    att_word=att_word.decode('utf-8')
                    for opn_words in opinionList:
                        for opn_word in opn_words:
                            opn_word=opn_word.decode('utf-8')
                            if att_word in att2CategoryDic and att_word in att2OpnDic:
                                aspect=att2CategoryDic[att_word]
                                opn=att2OpnDic[att_word]
                                if opn_word in opn:
                                    t= opn[opn_word].values()
                                    polarity=t[0]-t[1]
                                    if polarity>0:
                                        polarity="positive"
                                    else:
                                        polarity="negtive"
                                    r=[float(t[0]+1)/float(t[0]+t[1]+2),float(t[1]+1)/float(t[0]+t[1]+2)]
                                    score =max(r)

                                if aspect not in aspDic:
                                    aspDic[aspect]=polarity
                                print "Aspect:",aspect,"\t","Polarity:",polarity,"\t","Score:",score
            aspList.append(aspDic)
            print "*******************************************************************************"

        return aspList
        '''


#programing flow

def programingFlow(input_dir):
    client = MongoClient('10.120.26.22', 27017)
    db = client.project
    db.articles.drop()
    #db.cellphones.drop()


    speechDic=CRFPlus().makespeechDic()
    aspSet=CRFPlus().makeAspSet()

    asp2TagDic=sentenceAspAndPolarity().asp2Tag()

    att2CategoryDic=sentenceAspAndPolarity().att2CategoryDic()
    att2OpnDic=sentenceAspAndPolarity().att2OpnDic()
    categorysPmi=sentenceAspAndPolarity().categorysPmi()
    polarityPmi=sentenceAspAndPolarity().polarityPmi()
    categoryPolarityPmi=sentenceAspAndPolarity().categoryPolarityPmi()
    #word2WordPloarityPmi=sentenceAspAndPolarity().word2WordPloarityPmi()

    CRFPlus().setJiebaDic()

    attributeSet=set(['B_A','I_A','E_A','A'])
    opinionSet=set(['B_O','I_O','E_O','O'])

    for dir in os.listdir(input_dir):
        print dir
        inputdir=input_dir+'/'+dir
        for file in os.listdir(inputdir):
            try:
                articleDic=mongoDBNeed().mobilHTML2ArticlesJsonFormat(inputdir,file)
                for oneArticle in articleDic['oneArticle']:
                    tagDic={}
                    completeSentence=''.join(oneArticle['completeSentence'].split('.'))
                    sentencesList=CRFPlus().completeSentence2SentencesList(completeSentence)
                    for subSentence in sentencesList:
                        subSentenceDic={}
                        tagList=[]
                        CRFPlus().makeCRFFormat(speechDic,aspSet,subSentence,'CRF++-0.58/conll_test.txt')
                        CRFPlus().CRFCommand('crf_test -m model conll_test.txt > conll_output.txt')



                        listDic=sentenceAspAndPolarity().wholeSentenceAttOpinList(attributeSet,opinionSet)
                        wholeSentenceList=listDic['wholeSentenceList']
                        attributeList=listDic['attributeList']
                        opinionList=listDic['opinionList']



                        aspList=sentenceAspAndPolarity().giveSentenceAspPolarity(att2CategoryDic,att2OpnDic,categorysPmi,polarityPmi,categoryPolarityPmi,wholeSentenceList,attributeList,opinionList)

                        for asps in aspList:
                            for asp in asps:
                                polarity=asps[asp]
                                if asp in asp2TagDic and polarity in asp2TagDic[asp]:
                                    tag=asp2TagDic[asp][polarity]
                                    if tag not in tagList:
                                        tagList.append(tag)
                        for tag in tagList:
                            if tag not in tagDic:
                                tagDic[tag]=1
                            else:
                                tagDic[tag]+=1

                        aspList.append(tagList)
                        subSentenceDic[subSentence]=aspList
                        oneArticle['sentences'].append(subSentenceDic)
                        oneArticle['tags']=tagDic
                db.articles.insert_one(articleDic)
            except Exception as e:
                print e
    client.close()



programingFlow('../phone')









'''
generateNeedModel().generateAspword2asp('generateNeedModelData/aspWords2asp.txt','json/aspword2Asp.json')
generateNeedModel().generateAspword2OpinionPolarity('generateNeedModelData/asp','json/aspword2OpinionPolarity.json')
'''

'''
CRFPlus().CRFCommand('crf_test -m model conll_test.txt > conll_output.txt')
'''
'''
CRFPlus().setJiebaDic()
generateNeedModel().resetXMLJiebaTxet('generateNeedModelData/totalXML.xml')
'''
'''
generateNeedModel().categoryPmi('generateNeedModelData/finalXML.xml','json/categorysPmi.json',u'防手震',u'自拍',u'拍照攝影',u'對焦',u'設計質感',u'體積重量',u'音量',u'音質',u'操作經驗',u'換電池',u'續航力',u'機身發熱',u'螢幕尺寸',u'螢幕觸控',u'螢幕畫質',u'記憶體擴充',u'雙卡雙待',u'性價比',u'價位',u'軟體問題')
'''

'''
generateNeedModel().categoryPolarityPmi('generateNeedModelData/finalXML.xml','json/categoryPolarityPmi.json',u'防手震',u'自拍',u'拍照攝影',u'對焦',u'設計質感',u'體積重量',u'音量',u'音質',u'操作經驗',u'換電池',u'續航力',u'機身發熱',u'螢幕尺寸',u'螢幕觸控',u'螢幕畫質',u'記憶體擴充',u'雙卡雙待',u'性價比',u'價位',u'軟體問題')
'''
#generateNeedModel().word2WordPloarityPmi('generateNeedModelData/asp','json/word2WordPloarityPmi.json')