#company url list
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
domain='http://www.mobile01.com/'
str=''

res=requests.get('http://www.mobile01.com/forumlist.php?f=16')
soup=bs(res.text,"html.parser")
tablelist=soup.select('.tablelist')[0]
for subject in tablelist.select('.subject-text'):
    str += domain+subject.select('a')[0]['href']+"\n"
#print str

f=open('mobil01/company_url_list.txt','w')
f.write(str)
f.close()