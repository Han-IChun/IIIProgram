# -*- coding: utf-8 -*-
#get articl HTML

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

domain='http://www.mobile01.com/'


for file in os.listdir('../../iii_data/mobile01/data/article_url_list'):
    count=0
    error_log='../../iii_data/mobile01/data/'+file.split('_')[0]+'/error_log.txt'
    filename='../../iii_data/mobile01/data/article_url_list/'+file
    fid= open(filename,'r')
    for line in fid.readlines():
        try:
            count +=1
            print count,line.split('\t')[-1]
            rt=line.split('\t')[0].decode('utf-8')
            title=re.sub(r'[:/\\*?"|<>]','-',rt) #將不合法路徑字元用 '-'號取代
            dir='../../iii_data/mobile01/data/'+file.split('.')[0]+'/'+title+'.txt'

            browser = webdriver.Firefox()
            browser.get(line.split('\t')[-1])

            soup = BeautifulSoup(browser.page_source, "html.parser")

            f=open(dir, 'w')

            while len(soup.select('main')[0])>0:
                dic={}
                f.write(soup.select('main')[0].encode('utf-8'))
                time.sleep(0.5)


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
            print e
            '''
            error=open(error_log,'a')
            error.write('{0}_{1}_{2}\n'.format(traceback,e,line.split('@@')[-1]))
            error.close()
                '''
        finally:
            browser.quit()
    fid.close()
