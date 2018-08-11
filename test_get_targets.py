import os
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
url = 'https://www.drugbank.ca/drugs/DB01050'
html = requests.get(url, headers=headers)

targets_dict={}

result={}
s = etree.HTML(html.text)
target_id_list = s.xpath(
    '//div[@class="bond-list-container targets"]/div[@class="bond-list"]/div[@class="bond card"]/@id')
print("target_id_list:",target_id_list)
if target_id_list==None or target_id_list==[]:
    result["target_table"]="None"#标记有没有targets
else:
    for target_id in target_id_list:
        target_id = target_id.strip()
        # print(target_id)
        string_to_xpath = '//*[@id="BE0000262"]/div/strong/a/text()'
        str_to_replace = txt_wrap_by(r'"', r'"', string_to_xpath)
        # print("str_to_replace:",str_to_replace)
        string_to_xpath = string_to_xpath.replace(str_to_replace, target_id)
        target_name = s.xpath(string_to_xpath)
        target_name = list(set(target_name))
        # target_name=s.xpath('//*[@id='+str(target_id)+']/div[2]/strong/a/text()')错误定位方法
        print("target_name:", target_name)
        target_dict = {
            "target_name":"None",
            "Kind": "None",
            "Organism": "None",
            "General_Function": "None",
            "Specific_Function": "None",
            "Gene_Name": "None",
            "Molecular_Weight": "None",
            "drugbank_id":"None"
        }
        #第一个div
        for i in range(1, 4):
            string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                '/div[@class="col-sm-12 col-lg-5"]/dl/dt[' + str(i) + ']/text()'
            item = s.xpath(string_to_xpath)
            item = list(set(item))
            if item == None or item == []:#只要判断四个字段
                continue
            else:
                item=item[0].strip()
                print("item_1:", item)
                if item=="Kind":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-5"]/dl/dd[' + str(i) + ']/text()'
                    Kind_value=s.xpath(string_to_xpath)
                    Kind_value=Kind_value[0].strip()
                    print("Kind_value:",Kind_value)

                if item=="Organism":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-5"]/dl/dd[' + str(i) + ']/text()'
                    Organism_value=s.xpath(string_to_xpath)
                    Organism_value=Organism_value[0].strip()
                    print("Organism_value:",Organism_value)
        #另一个div
        for i in range(1, 7):
            string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                '/div[@class="col-sm-12 col-lg-7"]/dl/dt[' + str(i) + ']/text()'
            item = s.xpath(string_to_xpath)
            item = list(set(item))
            if item == None or item == []:#只要判断四个字段
                continue
            else:
                item=item[0].strip()
                print("item_2:", item)
                if item=="General Function":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(i) + ']/text()'
                    General_Function_value=s.xpath(string_to_xpath)
                    General_Function_value=General_Function_value[0].strip()
                    print("General_Function_value:",General_Function_value)

                if item=="Specific Function":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(i) + ']/text()'
                    Specific_Function_value=s.xpath(string_to_xpath)
                    Specific_Function_value=Specific_Function_value[0].strip()
                    print("Specific_Function_value:",Specific_Function_value)

                if item=="Gene Name":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(i) + ']/text()'
                    Gene_Name_value=s.xpath(string_to_xpath)
                    Gene_Name_value=Gene_Name_value[0].strip()
                    print("Gene_Name_value:",Gene_Name_value)
                if item=="Molecular Weight":
                    string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                    '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(i) + ']/text()'
                    Molecular_Weight_value=s.xpath(string_to_xpath)
                    Molecular_Weight_value=Molecular_Weight_value[0].strip()
                    print("Molecular_Weight_value:",Molecular_Weight_value)









