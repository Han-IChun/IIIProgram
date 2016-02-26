#company_list
import requests
from bs4 import BeautifulSoup as bs
domain='http://www.eprice.com.tw'
url='http://www.eprice.com.tw/mobile/product/'
res=requests.get(url)
res.encoding='utf-8'
soup =bs(res.text)
str=''
for manublock in soup.select('.manu-block'):
    for p in manublock.select('li'):
        url1= p.select('a')[0]['href']
        url_list=domain+url1
        str +=url_list+"\n"
print str
f=open('phone/list.txt','w')
f.write(str)
f.close()