# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import re

res=requests.get('http://www.eprice.com.tw/mobile/intro/c01-p5163-acer-liquid-e600/')
res.encoding='utf-8'


soup=bs(res.text,"lxml")
first_price_url=soup.select('.btn-price-1st')[0]['href']
second_price_url=soup.select('.btn-price-2nd')[0]['href']

res=requests.get(second_price_url)
res.encoding='utf-8'
soup=bs(res.text,"lxml")

result_list=soup.select('.result-list')[0]
name=''.join(result_list.select('.item')[0].select('.product')[0].text.encode('utf-8').split('型號：')[1].split())
print name
for item in result_list.select('.item'):
    date=re.search(ur'\d+-?\d+-?\d+',item.select('.date')[0].text).group()
    price=''.join(item.select('.price')[0].text.split('$')[1].split(','))
    info='{}\t{}\n'.format(date,price)
    print info