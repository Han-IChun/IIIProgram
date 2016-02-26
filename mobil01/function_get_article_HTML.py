# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests.packages
import traceback
import time
import os
import re


def get_content(article_url_list,content_location):
    domain='http://www.mobile01.com/'
    date='-'.join(time.strftime("%d/%m/%Y").split('/'))
    count=0
    error_log=content_location+'/'+date+'error_log.txt'

    fid= open(article_url_list,'r')
    for line in fid.readlines():
        try:
            count +=1
            print count,line.split('\t')[-1]
            rt=line.split('\t')[0].decode('utf-8')
            title=re.sub(r'[:/\\*?"|<>]','-',rt) #將不合法路徑字元用 '-'號取代
            dir=content_location+'/'+title+'.txt'

            browser = webdriver.Firefox()
            browser.get(line.split('\t')[-1])

            soup = BeautifulSoup(browser.page_source, "html.parser")

            f=open(dir, 'w')

            while len(soup.select('main')[0])>0:
                dic={}
                f.write(soup.select('main')[0].encode('utf-8'))


                for page in soup.select('.pagination a'):
                    dic[page.text.encode('utf-8')]=page['href']
                    #print page['href']
                if '下一頁 ›.' in dic :
                    next_url=domain+dic['下一頁 ›.']
                    print next_url
                    browser.get(next_url)
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                else:
                    print 'LAST PAGE'
                    break
            f.close()
        except Exception as e:
            error=open(error_log,'a')
            error.write('{0}_{1}_{2}\n'.format(traceback,e,line.split('\t')[-1]))
            error.close()
        finally:
            browser.quit()
    fid.close()

#先pip install selenium和安裝firefoxt
#get_content('連接清單和python的相對位置 ex:data/GSmar (Android)_url.txt','欲儲存文章內容的資料夾 ex:data/GSmart (Android)')
get_content('data/HTC (Android)_url.txt','data/HTC (Android)')