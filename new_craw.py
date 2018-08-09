import requests
from bs4 import BeautifulSoup
import os
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
url='https://www.drugbank.ca/categories/DBCAT000041'
html=requests.get(url,headers=headers)
soup=BeautifulSoup(html.text,'lxml')
a=soup.select('div table tr td a')

#a=soup.select('#DataTables_Table_0 > tbody > tr:nth-child(1) > td:nth-child(1) > a')
print(len(a))
f1=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_link.txt','a')
f2=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_id.txt','a')
for i in a:
    if i['href'].startswith('/drugs/'):
        print(i['href'])
        print('https://www.drugbank.ca'+i['href'].strip())
        print(i['href'].strip().lstrip('/drugs/'))
        f1.writelines('https://www.drugbank.ca'+i['href'].strip()+'\n')
        f2.writelines(i['href'].strip().lstrip('/drugs/') + '\n')
f1.close()
f2.close()


