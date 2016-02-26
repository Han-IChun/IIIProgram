# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import math

f=open('label_num1.xml','r')
label_num1=bs(f.read(),'xml')
f.close()

f=open('label_num2.xml','r')
label_num2=bs(f.read(),'xml')
f.close()

categorys=['camera','software','shap','audio','smooth','battery','brand','screen','hardware','price','other']
listEmotion=('positive','negative','conflict','not_write','-')
dicEmotion={}
dicFinal={}

for ele in listEmotion:
    dicEmotion[ele]=0

for ele in categorys:
    dicFinal[ele]=dicEmotion.copy()

for ele in dicFinal:
    for i in dicFinal[ele]:
        dicFinal[ele][i]=dicEmotion.copy()


#f=open('test.txt','w')
#print len(label_num1.select('sentence'))

for i in range(0,len(label_num1.select('sentence'))):
    #print label_num1.select('sentence')[i]['reviewID']
    dicID1={}
    dicID2={}
    if label_num1.select('sentence')[i].select('aspectCategory')>0:
        for j in label_num1.select('sentence')[i].select('aspectCategory'):
            dicID1[j['category']]=j['polarity']
        #print dicID1


    if label_num2.select('sentence')[i].select('aspectCategory')>0:
        for j in label_num2.select('sentence')[i].select('aspectCategory'):
            dicID2[j['category']]=j['polarity']
        #print dicID2


    for category in categorys:
        if category in dicID1 and category in dicID2:
            dicFinal[category][dicID1[category]][dicID1[category]] +=1

        if category in dicID1 and category not in dicID2:
            dicFinal[category][dicID1[category]]['not_write'] +=1

        if category not in dicID1 and category in dicID2:
            dicFinal[category]['not_write'][dicID2[category]] +=1

        if category not in dicID1 and category not  in dicID2:
            dicFinal[category]['not_write']['not_write'] +=1
f=open('matrix.txtx','w')
for ele in categorys:
    firstlist=[dicFinal[ele]['positive']['positive'],dicFinal[ele]['positive']['negative'],dicFinal[ele]['positive']['-'],dicFinal[ele]['positive']['conflict'],dicFinal[ele]['positive']['not_write']]
    secondlist=[dicFinal[ele]['negative']['positive'],dicFinal[ele]['negative']['negative'],dicFinal[ele]['negative']['-'],dicFinal[ele]['negative']['conflict'],dicFinal[ele]['negative']['not_write']]
    thirdlist=[dicFinal[ele]['-']['positive'],dicFinal[ele]['-']['negative'],dicFinal[ele]['-']['-'],dicFinal[ele]['-']['conflict'],dicFinal[ele]['-']['not_write']]
    forthlist=[dicFinal[ele]['conflict']['positive'],dicFinal[ele]['conflict']['negative'],dicFinal[ele]['conflict']['-'],dicFinal[ele]['conflict']['conflict'],dicFinal[ele]['conflict']['not_write']]
    fifthlist=[dicFinal[ele]['not_write']['positive'],dicFinal[ele]['not_write']['negative'],dicFinal[ele]['not_write']['-'],dicFinal[ele]['not_write']['conflict'],dicFinal[ele]['not_write']['not_write']]


    first=[]
    second=[]
    third=[]
    forth=[]
    fifth=[]
    column=[0,0,0,0,0,0]
    col=0
    count1=0
    count2=0
    count3=0
    count4=0
    count5=0

    for j in range(0,5):
        count1+=firstlist[j]
        count2+=secondlist[j]
        count3+=thirdlist[j]
        count4+=forthlist[j]
        count5+=firstlist[j]

        first.append(str(firstlist[j]))
        second.append(str(secondlist[j]))
        third.append(str(thirdlist[j]))
        forth.append(str(forthlist[j]))
        fifth.append(str(fifthlist[j]))
        column[j]=str(firstlist[j]+secondlist[j]+thirdlist[j]+forthlist[j]+fifthlist[j])
        col+=firstlist[j]+secondlist[j]+thirdlist[j]+forthlist[j]+fifthlist[j]

    column[5]=str(col)
    firstline='{}\t{}\n'.format('\t'.join(first),count1)
    secondline='{}\t{}\n'.format('\t'.join(second),count2)
    thirdline='{}\t{}\n'.format('\t'.join(third),count3)
    forthline='{}\t{}\n'.format('\t'.join(forth),count4)
    fifthline='{}\t{}\n'.format('\t'.join(fifth),count5)

    ef=(count1*float(column[0])/float(column[5]))+(count2*float(column[1])/float(column[5]))+(count3*float(column[2])/float(column[5]))+(count4*float(column[3])/float(column[5]))+(count5*float(column[4])/float(column[5]))
    a=int(first[0])+int(second[1])+int(third[2])+int(forth[3])+int(fifth[4])
    K=float(a-ef)/(float(column[5])-ef)

    final='--------{}----------\n{}{}{}{}{}{}\nK={}\n'.format(ele,firstline,secondline,thirdline,forthline,fifthline,'\t'.join(column),K)

    f.write(final)
    print final
f.close()

'''
f=open('test.txt','w')
for i in range(0,len(label_num1.select('sentence'))):
    content='{}{}'.format(label_num1.select('sentence')[i],label_num2.select('sentence')[i])
    f.write(content)
f.close()

'''
