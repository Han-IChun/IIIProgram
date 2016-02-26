#article url list
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver

domain='http://www.mobile01.com/'
str=''

fid= open('../../iii_data/mobile01/data/test.txt','r')
for line in fid.readlines():
    #browser = webdriver.Firefox()
    #browser.get(line.strip())
    res=requests.get(line.strip())
    #soup = bs(browser.page_source, "html.parser")
    soup=bs(res.text,"html.parser")

    if len (soup.select('#maincontent h2 '))>1:
        title=''.join(soup.select('#maincontent h2 ')[1].text.strip().split('/'))
    else:
        title=''.join(soup.select('#maincontent h2 ')[0].text.strip().split('/'))
    print title

    file_name='../../iii_data/mobile01/data/article_url_list/'+title+'_url.txt'
    f=open(file_name,'w')

    while(len(soup.select('.subject-text'))>1):
        forumlist=soup.select('.forumlist')[0]
        dic={}
        for tr in forumlist.select('tbody tr'):
            title=''.join(tr.select('.subject-text a')[0].text.strip().encode('utf-8').split())
            reply=''.join(tr.select('.reply')[0].text.strip().encode('utf-8').split())
            article_time=''.join(tr.select('.authur p')[0].text.strip().encode('utf-8').split())
            authur=''.join(tr.select('.authur p')[1].text.strip().encode('utf-8').split())
            href= ''.join(tr.select('.subject-text a')[0]['href'].strip().encode('utf-8').split())
            last_reply_time=''.join(tr.select('.latestreply p')[0].text.strip().encode('utf-8').split())
            last_reply_authur=''.join(tr.select('.latestreply p')[1].text.strip().encode('utf-8').split())
            url=domain+href
            info='{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(title,reply,article_time,authur,last_reply_time,last_reply_authur,url)+'\n'

            f.write(info)
            #print url

        for a in soup.select('.pagination a'):
            dic[a.text.strip().encode('utf-8')] = domain+a['href'].encode('utf-8')

        if '下一頁 ›.' in dic:
            next_url=dic['下一頁 ›.']
            print 'next page'
            print 'next_url = '+next_url
            time.sleep(0.5)
            #browser.get(line.strip())
            #soup = bs(browser.page_source, "html.parser")
            res=requests.get(next_url)
            soup=bs(res.text,"html.parser")
        else:
            print 'last page'
            break
    print 'complete'
    f.close()
#browser.quit()
fid.close()