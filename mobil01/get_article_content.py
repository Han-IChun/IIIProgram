# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import os
import re
import traceback

        
def get_article_content(input_dir,output_dir,error_log):
    for file in os.listdir(input_dir):
        try :
            filename=file.decode('cp950')
            m= re.match('(.*).txt$',filename)
            #print m.group(1)            
            f=open(input_dir+'/'+filename,'r')
            soup=bs(f.read(),"html.parser")
            
            for content in soup.select('article'):
                fid=open(output_dir+'/'+ m.group(1)+'_'+content.select('li')[0].select('span')[1].text+'.txt','w')
                #print content.select('.single-post-content')[0].text.encode('utf-8')
                fid.write(content.select('.single-post-content')[0].text.encode('utf-8'))
                fid.close()
        except Exception as e:
            error=open(error_log,'a')
            error.write('{0}_{1}_{2}\n'.format(traceback,e,m.group(1).encode('utf-8')))
            error.close()

#路徑皆為相對路徑
#error_log檔名盡量包含廠牌及時間 ex Acer (Android)_20151213_errlog.txt
#get_article_contentall(想拿出內容的mobile01 HTML資料夾 ex'data/test',想放內容的資料夾 ex'data/content',errlog位置+.txt'data/err_log.txt')
get_article_content('data/test','data/content','data/err_log.txt')


