# -*- coding: utf-8 -*-
#dic

import os
import re
from bs4 import BeautifulSoup as bs
dic={'尺寸':'','重量':'','SIM 卡規格':'','防水防塵':'','螢幕技術':'','作業系統':'','處理器':'','記憶體':'','儲存空間':'','記憶卡':'','通訊協定':'',
     '雙卡雙待':'','相機功能':'','多媒體':'','連結與網路':'','感應器':'','電池':'','顏色':'','其它':''}


for file in os.listdir('E:\iii\e-price\data\items'):
    filename=file.decode('cp950')
    m= re.match('(.*).txt$',filename)
    print filename

    f=open('E:\iii\e-price\data\items\\'+m.group(1)+'.txt','r')
    soup = bs(f.read(), "html.parser")
    for li in soup.select('li'):
        if len(li.select('label'))>0:
            if li.select('label')[0].text.strip().encode('utf-8') in dic:
                if len(li.select('div ul'))>0:
                    for li2 in li.select('div ul li'):
                        if len(li2.text.strip().encode('utf-8'))>0:
                            str= ''.join(li2.text.strip().encode('utf-8').split())
                            #print str
                            dic[li.select('label')[0].text.strip().encode('utf-8')] +=str+'__'
                    #print '---------------------------------------------'

                else:
                    dic[li.select('label')[0].text.strip().encode('utf-8')]= ''.join(li.select('div')[0].text.strip().encode('utf-8').split())
    content=open('E:\iii\e-price\data\item_content\\'+m.group(1)+'.txt','w')
    for i in dic:
        str='{0}\n{1}\n-----------------------\n'.format(i,dic[i])
        content.write(str)
    content.close()
    f.close()