# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup as bs
import re
import time

domain='http://www.dcfever.com/phones/'
domain1='http://www.dcfever.com'
domain2='http://www.dcfever.com/phones/readreviews.php?{}'#進入使用心得頁面


res=requests.get('http://www.dcfever.com/phones/database.php')#手機資訊館首頁
res.encoding=('utf-8')#解決requests完有亂碼問題
soup=bs(res.text,"html.parser")
content=soup.select('.brand_matrix_wrap')[0]
for li in content.select('li'):#抓取company url
    company_url=domain+li.select('a')[0]['href']
    #print url
    res1=requests.get(company_url)#進入手機company頁面
    res1.encoding=('utf-8')
    soup1=bs(res1.text,"html.parser")

    content1=soup1.select('.section_header')[0]#建資料夾的名字
    dirname=''.join(content1.text.split())#將資料夾名字去空白
    print dirname
    os.mkdir('advantage/'+dirname)#建優點下公司的資料夾
    os.mkdir('shortcoming/'+dirname)#建缺點下公司的資料夾

    page_nums=soup1.select('.pages')[0]#計算手機公司的手機頁面總共幾頁
    for nums in range(1,len(page_nums)+1):#將手機頁面format頁數  取得手機公司的每頁手機頁面
        phone_page='{}{}{}'.format(company_url,'page=',nums)#一個公司可能有多張手機頁面(手機數太多)
        print '------------------------------------------\n'+phone_page+'\n----------------手機心得頁面--------------------'
        res1=requests.get(phone_page)#進入手機公司的每頁手機頁面
        res1.encoding=('utf-8')
        soup1=bs(res1.text,"html.parser")
        content1=soup1.select('.gadget_inner_wrap')[0]
        #print content[0]
        for model in content1.select('.gadget'):
            if int(model.select('.gadget_rating_counter')[0].text.split(' ')[0])>0:#如果手機的評論 >0才進入手機的頁面
                id=model.select('.model_no a')[0]['href'].split('?')#抓取那隻手機在網站的id
                url1=domain2.format(id[1])#將id和手機資訊的url連結
                print url1
                rt=''.join(model.select('.model_no')[0].text.split())#取手機名稱且去空白
                filename=re.sub(r'[:/\\*?"|<>]','-',rt) #將手機名稱的不合法路徑字元用 '-'號取代
                res2=requests.get(url1)#進入手機資訊頁面
                res2.encoding='utf-8'
                soup2=bs(res2.text,"html.parser")
                page=soup2.select('.pages')[0]
                list=[]#建立一個存手機評論url的list
                if len(page)>0:#如果手機有不只一頁評論
                    for i in page.select('a'):#取得每一頁評論的url
                        list.append(i['href'])#將url放進list裡面
                    #end for i in page.....
                f=open('advantage/'+dirname+'/'+filename+'.txt','w')#將每隻手機的優點寫入一個txt
                fid=open('shortcoming/'+dirname+'/'+filename+'.txt','w')#將每隻手機的缺點寫入一個txt
                for i in soup2.select('.review_point'):
                        dic={'優點:':'','缺點:':''}
                        #print i.select('.caption')[0].text,i.select('.text')[0].text
                        if i.select('.caption')[0].text.encode('utf-8') in dic:
                            text=''.join(i.select('.text')[0].text.strip().split()).encode('utf-8')
                            dic[i.select('.caption')[0].text.encode('utf-8')]= text
                            good='{}\n'.format(dic['優點:'])
                            bad='{}\n'.format(dic['缺點:'])
                            if good !='':
                                f.write(good)
                            if bad !='':
                                fid.write(bad)
                for i in range(0,len(list)-1):#將評論的每一頁頁數formate在評論頁面的url
                    next_page=domain1+list[i]#取得下一頁的url
                    time.sleep(1)#設定抓取間隔
                    res3=requests.get(next_page)#requests下一頁
                    res3.encoding='utf-8'
                    soup3=bs(res3.text,"html.parser")
                    for i in soup3.select('.review_point'):
                        dic={'優點:':'','缺點:':''}
                        #print i.select('.caption')[0].text,i.select('.text')[0].text
                        if i.select('.caption')[0].text.encode('utf-8') in dic:
                            text=''.join(i.select('.text')[0].text.strip().split()).encode('utf-8')
                            dic[i.select('.caption')[0].text.encode('utf-8')]= text
                            good='{}\n'.format(dic['優點:'])
                            bad='{}\n'.format(dic['缺點:'])
                            if good !='':
                                f.write(good)
                            if bad !='':
                                fid.write(bad)
                f.close()
                fid.close()

