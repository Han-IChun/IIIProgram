# -*- coding: utf-8 -*-



import jieba
import os
import time
import math
import json


def text(filename,input_dir):         #文章整理成一行一篇文章
        f=open(input_dir+'/'+filename,'r')
        for w in f.readlines(): #readlines將整篇文存成一個list，一行為一個list元素
            if len(w)>1:    #去掉沒內容的行([])
                return ''.join(w.split())    #去空白
            #end if
        #end for

def cut_articleinline(input_dir): #將整理過一行一個評論的txt斷詞 load uesrdic 情緒字典 將stopword 去掉
    tStart=time.time() #計算所需時間(計時開始)
    jieba.set_dictionary('dic/dict.txt.big')  #設定繁中字典
    jieba.load_userdict('dic/userdic.txt')  #設定自定義字典
    jieba.load_userdict('dic/antusd.txt')  #設定自定義字典
    jieba.load_userdict('dic/negative.txt')  #設定自定義字典
    jieba.load_userdict('dic/positive.txt')  #設定自定義字典

    stopword_set=set()  #設一個空的set 裝 stopword
    f=open('dic/stopword.txt','r')  #開啟stopword txt檔
    for i in f.readlines(): #將stop word 一行一行讀出來
        stopword_set.add(i.strip()) #將stop word 加到stopword set 裡面
    f.close()

    fid=open('pmi/article_cut.txt','w')     #開要寫入斷詞結果的檔案
    try:
        for file in os.listdir(input_dir): #將要斷詞的資料夾裡的文章用 listdir 讀出來
            filename=file.decode('cp950') #將文章名稱用 cp950解碼
            f=open(input_dir+'/'+filename,'r')#把input_dir的文章讀進來
            #file=open('pmi/'+filename,'w')
            for line in f.readlines():
                list=[]
                for w in jieba.cut(''.join(line.split()).strip(),HMM=False):     #將讀進來的每一行用jieba斷開 且用for取出
                    if len(w)>0:#若w不是空字串
                        #if w.encode('utf-8') not in stopword_set: #如果斷出來的字不是stopword
                            list.append(w.strip().encode('utf-8')) #將w append到 list裡面

                #file.write('\t'.join(list)+'\n')
                fid.write('\t'.join(list)+'\n')   #斷完詞的內容用tab隔開和換行
            #file.close()
                #end for
            #end for
        #end for
    except Exception as e:
        print e
    finally:
        fid.close
    tEnd = time.time() #記時(時間結束)
    print 'cut_articleinline cost {} s'.format(tEnd-tStart)    #將經過時間print 出來

def cut(input_dir):  #斷詞

    tStart=time.time() #計算所需時間(計時開始)
    #jieba.set_dictionary('dic/dict.txt.big')  #設定繁中字典
    jieba.load_userdict('dic/userdic.txt')  #設定自定義字典
    jieba.load_userdict('dic/antusd.txt')  #設定自定義字典
    jieba.load_userdict('dic/negative.txt')  #設定自定義字典
    jieba.load_userdict('dic/positive.txt')  #設定自定義字典

    stopword_set=set()  #設一個空的set 裝 stopword
    f=open('dic/stopword.txt','r') #開啟stopword txt檔
    for i in f.readlines(): #將stop word 一行一行讀出來
        stopword_set.add(i.strip()) #將stop wor 加到stopword set 裡面
    f.close()

    fid=open('pmi/article_cut.txt','w')     #開斷詞後的檔案
    try:
        for file in os.listdir(input_dir):
            filename=file.decode('cp950')
            for w in jieba.cut(text(filename,input_dir)):     #將要處理的文章放到text裡整理過用jieba斷詞
                if w.encode('utf-8') not in stopword_set:
                    fid.write(w.encode('utf-8')+'\t')   #斷完詞的內容用tab隔開
            #end for
        #end for
            fid.write('\n') #每篇文章當成一行
    except Exception as e:
        print e
    finally:
        fid.close
    tEnd = time.time() #記時(時間結束)
    print 'cut cost {} s'.format(tEnd-tStart)    #將經過時間print 出來

def checkdic(do_not_wanttochange,wanttochange):#檢查兩本 dic 將 wanttochange 字典裡跟 do_not_wanttochange 不重複的字 寫成一本新的字典
    dicset=set() #建一個空的set
    fid=open('dic/'+do_not_wanttochange,'r')
    for word in fid.readlines():
        dicset.add(word.strip())#將不想改的那本字典放到 dicset
    #end for
    fid.close()

    f=open('dic/'+wanttochange,'r')
    fid=open('dic/new_dic.txt','w')
    for word in f.readlines():#將要檢查的字典一行一行讀進來
        if word.strip() in dicset: #如果字沒有在dicset裡
            w='{}\n'.format(word.strip())
            fid.write(w)
    #end for
    fid.close()

def make_dic(): #將斷完詞的檔案做成字典，並計算所有字出現的頻率
    dic={}
    fid=open('pmi/article_cut.txt','r')
    for w in fid.read().split('\t'):    #將tab隔開的斷詞用split切開
        w=w.decode('utf-8').strip()     #將最後一個字的\n去掉
        if len(w)>0:    #怕有空白字元
            if w not in dic:    #如果字典沒有word就把word加到字典，把出現次數設為1
                dic[w] = 1
            else:       #如果word出現在字典裡面就把這個字的頻率+1
                dic[w] = dic[w] + 1
            #end if
        #end if
    #end for
    fid.close()
    return dic  #傳回dic

def vec():  #計算每個詞在每篇文章出現的次數
    tStart=time.time() #計算所需時間(計時開始)
    dic=make_dic()  #把make_dic做出來的字典指定給dic
    for i in dic:   #將字典清空
        dic[i]=0
    #end for
    f=open('pmi/word_vec.txt','w')
    f.write('\t'.join(dic.keys()).encode('utf-8')+'\n') #將dic的key用tab join起來存成 word_vec
    f.close()

    fid=open('pmi/article_cut.txt','r') #將之前斷完詞的結果讀近來(一行一篇文章的斷詞)
    file=open('pmi/count_vec.txt','a')#將給個詞在每篇文章出現的次數append到文件上
    for i in fid.readlines():#將斷詞的結果一行一行讀進來
        for w in i.split('\t'): #將每一行用tab切開
            w=w.decode('utf-8')
            if len(w)>0:
                if w in dic:#如果字再字典裡面，
                    dic[w] += 1
                #end if
            #end if
        #end for w
        list=[] #建一個空list
        for i in dic.values():#將每個 dic.value轉成str才能join
            list.append(str(i))
        #end for i
        file.write('\t'.join(list)+'\n')#將剛剛的list用tab join起來 並換行
        for i in dic:#將字典重新清空，計算下一篇文章的詞出現次數
            dic[i]=0
        #end for i
    print 'Total {} words'.format(len(list))
    #end for i
    file.close()
    fid.close()
    tEnd = time.time() #記時(時間結束)
    print 'vec cost {} s'.format(tEnd-tStart)    #將經過時間print 出來

def wordtoword_vec():#將文章對詞的矩陣轉成詞對詞的次數並算pmi
    tStart=time.time() #計算所需時間(計時開始)

    f=open('pmi/word_vec.txt','r')  #開啟總共斷詞的txt
    title=f.readline().split('\t')  #將整行斷詞用tab切開
    dim=len(title)#計算總共有幾個詞
    f.close()

    f=open('pmi/count_vec.txt','r') #開啟每篇文章出現詞的次數的txt
    article_num=len(f.readlines())#計算總共的文章數
    f.close()
    print 'Total {} articles'.format(article_num)

    fid=open('pmi/wordtoword.txt','w')#將詞對詞的結果寫到wordtoword.txt裡
    for k in range(0,dim):  #詞A的範圍
        for i in range(1,dim-k):    #詞B的範圍
            count =0 #詞AB總共一起出現的次數
            wordA=0 #詞A出現的次數
            wordB=0 #詞B出現的次數
            f=open('pmi/count_vec.txt','r')#開啟每篇詞出現次數的txt
            for j in f.readlines(): #將每篇詞分行讀出來
                list=j.split('\t')  #將j 用tab切開放到list裡面
                if int(list[k])>0:  #如果詞A有出現
                    wordA +=1   #詞A次數+1
                #end if
                if int(list[k+i])>0:    #如果詞B有出現
                    wordB +=1   #詞B次數+1
                #end if
                if (int(list[k])>0 and int(list[k+i])>0): #如果詞A跟詞B都有出現
                    count +=1   #共同出現次數+1
                #end if
            # end for j
        #end for i
    #end for k
            f.close()
            pmi=(count*article_num)/(wordA*wordB) #算pmi (沒取log)
            sentence='{}\t{}\t{}\t{}\t{}\t{}\n'.format(title[k].strip(),title[k+i].strip(),wordA,wordB,count,pmi)  #將詞A 詞B 詞A出現次數 詞B出現次數 總共出現次數 pmi(沒log) formate 起來
                                                                                                            #strip 將最後一個換行符號消除
            fid.write(sentence)
    fid.close()
    tEnd = time.time() #記時(時間結束)
    print 'wordtoword_vec cost {} s'.format(tEnd-tStart)    #將經過時間print 出來

def pmi_insentence():
    start=time.time()
    stopword_set=set()
    f=open('dic/stopword.txt','r')
    for i in f.readlines():
        stopword_set.add(i.strip())
    f.close()

    fid=open('pmi/article_cut.txt','r')
    total_article=len(fid.readlines())
    fid.close()

    dic={}
    dicsingle={}

    fid=open('pmi/article_cut.txt','r')
    for w in fid.readlines():
        listset=set()
        list=[]
        wordlist=w.split('\t')
        for i in wordlist:
            i=i.decode('utf-8').strip()     #將最後一個字的\n去掉
            if len(i)>0 and i not in stopword_set:
                if i not in list:
                    listset.add(i)
        for i in listset:
            list.append(i)
            if i not in dicsingle:
                dicsingle[i]=1
            else:
                dicsingle[i] +=1
        for k in range(0,len(list)):  #詞A的範圍
            for j in range(1,len(list)-k):    #詞B的範圍
                word='{}\t{}'.format(list[k].encode('utf-8'),list[k+j].encode('utf-8'))
                if word not in dic:
                    dic[word]=1
                else:
                    dic[word]+=1
    f=open('pmi/pmi_insentence.txt','w')
    for ele in dic:
        countA=dicsingle[ele.split('\t')[0].decode('utf-8')]
        countB=dicsingle[ele.split('\t')[1].decode('utf-8')]
        countAB=dic[ele]
        pmi=float((countAB*total_article))/float((countA*countB))
        count='{}\t{}\t{}\t{}\t{}\n'.format(ele,countA,countB,countAB,pmi)
        f.write(count)
    f.close()
    fid.close()
    end=time.time()
    cost='{} costs{}s'.format('wordtoword_insentence',end-start)
    print cost

def wordtoword_matrix(): #將斷完詞的檔案做成字典，並計算所有字出現的頻率
    dic={}
    finaldic={}
    fid=open('pmi/article_cut.txt','r')
    for w in fid.read().split('\t'):    #將tab隔開的斷詞用split切開
        w=w.decode('utf-8').strip()     #將最後一個字的\n去掉
        if len(w)>0:    #怕有空白字元
            if w not in dic:    #如果字典沒有word就把word加到字典，把出現次數設為1
                dic[w] = 0
    fid.close()

    for ele in dic:
        finaldic[ele]=dic.copy()
    fid=open('pmi/article_cut.txt','r')

    for w in fid.readlines():
        w=w.strip().split('\t')
        for i in w:
            if len(i)>0:
                for j in w:
                    if len(j)>0:
                        finaldic[i.decode('utf-8')][j.decode('utf-8')] +=1

    fid.close()

    f=open('pmi/dic.txt','w')
    fid=open('pmi/word.txt','w')

    for ele in finaldic:
        f.write(ele.encode('utf-8')+'\t')
        for i in finaldic[ele]:
            word='{}\t'.format(finaldic[ele][i])
            f.write(word)
        f.write('\n')

    f.close()
    fid.close()

def stopword(): #將斷完詞的結果中的stopword去掉
    stopword_set=set()#建一個stopword set
    f=open('dic/stopword.txt','r')#開啟 stopword 字典
    for i in f.readlines():
        stopword_set.add(i.strip())#把stopword 加到set裡面
    f.close()
    f=open('pmi/test.txt','r')
    fid=open('pmi/new_test.txt','w')
    for line in f.readlines():
        if line.split('\t')[0].strip() not in stopword_set and line.split('\t')[1].strip().split():
            sentence='{}\t{}\t{}\n'.format(line.split('\t')[0].strip(),line.split('\t')[1].strip(),line.split('\t')[2].strip())
            fid.write(sentence)
    fid.close()
    f.close()

def inuserdict():
    userdic_set=set()
    f=open('dic/userdic.txt','r')
    for i in f.readlines():
        userdic_set.add(i.strip())
    f.close()
    f=open('pmi/test.txt','r')
    fid=open('pmi/in_userdic.txt','w')
    for line in f.readlines():
        if line.split('\t')[0] in userdic_set and line.split('\t')[1] in userdic_set:
            sentence='{}\t{}\t{}\n'.format(line.split('\t')[0],line.split('\t')[1],line.split('\t')[2].strip())
            fid.write(sentence)
    fid.close()
    f.close()

def positive_and_negative_pmi():
    total_dic={}
    fid=open('../../iii_data/pmi/article_cut.txt','r')
    for w in fid.read().split('\t'):    #將tab隔開的斷詞用split切開
        w=''.join(w.decode('utf-8').split()).strip()     #將最後一個字的\n去掉
        if len(w)>0:    #怕有空白字元
            w=w.encode('utf-8')
            if w not in total_dic:    #如果字典沒有word就把word加到字典，把出現次數設為1
                total_dic[w] = 1
            else:
                total_dic[w] += 1
    fid.close()

    positive_dic={}
    fid=open('../../iii_data/pmi/good.txt','r')
    for w in fid.read().split('\t'):    #將tab隔開的斷詞用split切開
        w=''.join(w.decode('utf-8').split()).strip()     #將最後一個字的\n去掉
        if len(w)>0:    #怕有空白字元
            w=w.encode('utf-8')
            if w not in positive_dic:    #如果字典沒有word就把word加到字典，把出現次數設為1
                positive_dic[w] = 1
            else:
                positive_dic[w] += 1
    fid.close()

    negative_dic={}
    fid=open('../../iii_data/pmi/bad.txt','r')
    for w in fid.read().split('\t'):    #將tab隔開的斷詞用split切開
        w=''.join(w.decode('utf-8').split()).strip()     #將最後一個字的\n去掉
        if len(w)>0:    #怕有空白字元
            w=w.encode('utf-8')
            if w not in negative_dic:    #如果字典沒有word就把word加到字典，把出現次數設為1
                negative_dic[w] = 1
            else:
                negative_dic[w] += 1
    fid.close()


    word2PositiveNegativePmiDic={}
    polarityDic={'positive':0,'negative':0}
    positive_total=len(positive_dic.keys())
    negative_total=len(negative_dic.keys())
    total=len(total_dic.keys())

    f=open('../../iii_data/pmi/positive_and_negative_pmi.txt','w')

    for ele in total_dic:
        if ele in positive_dic and ele in negative_dic:
            positive_pmi=math.log((float(positive_dic[ele]*total)/float(total_dic[ele]*positive_total)),2)
            negative_pmi=math.log((float(negative_dic[ele]*total)/float(total_dic[ele]*negative_total)),2)
            pmi='{}\t{}\t{}\t{}\n'.format(ele,positive_pmi,negative_pmi,positive_pmi-negative_pmi)
            f.write(pmi)
            word2PositiveNegativePmiDic[ele]=polarityDic.copy()
            word2PositiveNegativePmiDic[ele]['positive']=positive_pmi
            word2PositiveNegativePmiDic[ele]['negative']=negative_pmi

        elif ele in positive_dic and ele not in negative_dic:
            positive_pmi=math.log((float(positive_dic[ele]*total)/float(total_dic[ele]*positive_total)),2)
            negative_pmi=0
            pmi='{}\t{}\t{}\t{}\n'.format(ele,positive_pmi,negative_pmi,positive_pmi-negative_pmi)
            f.write(pmi)
            word2PositiveNegativePmiDic[ele]=polarityDic.copy()
            word2PositiveNegativePmiDic[ele]['positive']=positive_pmi
            word2PositiveNegativePmiDic[ele]['negative']=negative_pmi
        elif ele not in positive_dic and ele in negative_dic:
            positive_pmi=0
            negative_pmi=math.log((float(negative_dic[ele]*total)/float(total_dic[ele]*negative_total)),2)
            pmi='{}\t{}\t{}\t{}\n'.format(ele,positive_pmi,negative_pmi,positive_pmi-negative_pmi)
            f.write(pmi)
            word2PositiveNegativePmiDic[ele]=polarityDic.copy()
            word2PositiveNegativePmiDic[ele]['positive']=positive_pmi
            word2PositiveNegativePmiDic[ele]['negative']=negative_pmi
    f.close()

    f=open('../../iii_data/pmi/word2PositiveNegativePmi.json','w')
    json.dump(word2PositiveNegativePmiDic,f,ensure_ascii=False)
    f.close()
def cutdicspace_and_removesameword(dic_name,new_dic_name): #整理字典 去除空白和重複的字
    f=open('dic/'+dic_name,'r') #開啟要檢查的字典
    dicset={}   #建一個空的dic來檢查重複的字
    fid=open('dic/'+new_dic_name,'w') #開一個檢查完後要寫入的字典
    for line in f.readlines(): #將字典的字讀出來#
        word=''.join(line.split()).strip() #把字去空白和換行符號
        if len(word)>0: #怕有空字串
            if word not in dicset:#如果字沒有在dicset裡(表示沒有重複) 則這個字的出現次數為1
                dicset[word] =1
            else:#若字已經出現過則次數加1
                dicset[word] +=1
    #end for line in ...
    for word in dicset: #將每個dic的字取出
        if dicset[word]>1:
            print word,dicset[word]
        word='{}\n'.format(word)
        fid.write(word)
    #end for word in ...

    fid.close()
    f.close()


#1
#cutdicspace_and_removesameword('negative.txt','new.txt')

#2
#stopword()

#3
#inuserdict()

#4
#cut('mobil01/data/test') #想斷詞的文章資料夾路徑
#wordtoword_insentence()

#5
#cut('mobil01/data/test') #想斷詞的文章資料夾路徑
#vec()
#wordtoword_vec()

#6
#checkdic('antusd.txt','stopword.txt')

#7
#cut_articleinline('test')
#pmi_insentence()

#8
#cut('test')
#cut_articleinline('test')
#wordtoword_matrix()

#9
#cut_articleinline('test')
#positive_and_negative_pmi()

positive_and_negative_pmi()