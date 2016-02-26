# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:41:28 2015

@author: BigData
"""
from bs4 import BeautifulSoup as bs
import os
import re
import traceback

def get_article_contentall(input_dir,output_dir,error_log):
    for file in os.listdir(input_dir):
        try :
            filename=file.decode('cp950')
            m= re.match('(.*).txt$',filename)
            #print m.group(1)            
            f=open(input_dir+'/'+filename,'r')
            soup=bs(f.read(),"html.parser")
            
            fid=open(output_dir+'/'+ m.group(1)+'.txt','w')
            for content in soup.select('article'):              
                #print content.select('.single-post-content')[0].text.encode('utf-8')
                str='{0}\n-------------------------------'.format(content.select('.single-post-content')[0].text.encode('utf-8'))
                fid.write(str)
            fid.close()
        except Exception as e:
            error=open(error_log,'a')
            error.write('{0}_{1}_{2}\n'.format(traceback,e,m.group(1).encode('utf-8')))
            error.close()

#路徑皆為相對路徑
#error_log檔名盡量包含廠牌及時間 ex Acer (Android)_20151213_errlog.txt
#get_article_contentall(想拿出內容的mobile01 HTML資料夾 ex'data/test',想放內容的資料夾 ex'data/content',errlog位置+.txt'data/err_log.txt')
get_article_contentall('data/test','data/content','data/err_log.txt')