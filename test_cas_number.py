from lxml import etree
import requests
import urllib
from bs4 import BeautifulSoup

def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
url = 'https://www.drugbank.ca/drugs/DB00179'
html = requests.get(url, headers=headers)

s = etree.HTML(html.text)
for i in range(1,20):
    items = s.xpath('/html/body/main/div/div/dl/dt[' + str(i) + ']/text()')
    if items == None or items == []:
        continue
    else:
        for item in items:
            if item == "CAS number":
                print("CAS_number:", item)
                CAS_number_value=s.xpath('/html/body/main/div/div/dl/dd[' + str(i) + ']/text()')
                if CAS_number_value==None or CAS_number_value==[]:
                    CAS_number_value="None"
                else:
                    CAS_number_value = CAS_number_value[0].strip()
                print("CAS_number_value:",CAS_number_value)

            if item == "Weight":
                print("Weight:", item)
                Weight_value = s.xpath('/html/body/main/div/div/dl/dd[' + str(i) + ']/text()')
                if Weight_value == None or Weight_value == []:
                    Weight_value = "None"
                else:
                    Weight_value = Weight_value[0].strip()
                print("Weight_value:", Weight_value)


