import os
from lxml import etree
import requests
import time
import urllib
import pymysql

def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def craw_drugbank(url,drugbank_id):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    #time.sleep(10)
    data = requests.get(url, headers=headers).text
    s = etree.HTML(data)
    target_name_list = s.xpath(
        '//div[@class="bond-list-container targets"]/div[@class="bond-list"]/div[@class="bond card"]'
        '/div[@class="card-header"]/strong/a/text()')
    print("target_id_list:",target_name_list)
    target_link_list = s.xpath(
        '//div[@class="bond-list-container targets"]/div[@class="bond-list"]/div[@class="bond card"]'
        '/div[@class="card-header"]/strong/a/@href')
    print("target_link_list:",target_link_list)
    for target_link in target_link_list:
        target_link='https://www.drugbank.ca'+target_link
        print("target_link:",target_link)
        #time.sleep(10)
        data2 = requests.get(target_link, headers=headers).text
        s2 = etree.HTML(data2)
        target_name=s2.xpath('/html/body/main/div/div[1]/h1/text()')
        if target_name==[]:
            target_name="None"
        else:
            target_name=target_name[0].strip()
        print("target_name:",target_name)
        target_dict = {
            "target_name": target_name,
            "Kind": "None",
            "Organism": "None",
            "General_Function": "None",
            "Specific_Function": "None",
            "Gene_Name": "None",
            "Molecular_Weight": "None",
            "drugbank_id": drugbank_id,
            "Gene_sequence":"None"
        }
        for i in range(1,30):
            item=s2.xpath('/html/body/main/div/div[2]/dl[1]/dt['+str(i)+']/text()')
            if item==[]:
                continue
            else:item=item[0].strip()
            print("item:",item)
            if item=="Gene Name":
                Gene_Name=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if Gene_Name==[]:
                    Gene_Name="None"
                else:Gene_Name=Gene_Name[0].strip()
                print("Gene_Name:",Gene_Name)
                target_dict["Gene_Name"]=Gene_Name
            if item=="Organism":
                Organism=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if Organism==[]:
                    Organism="None"
                else:Organism=Organism[0].strip()
                print("Organism:",Organism)
                target_dict["Organism"] = Organism
            if item=="Molecular Weight":
                Molecular_Weight=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if Molecular_Weight==[]:
                    Molecular_Weight="None"
                else:Molecular_Weight=Molecular_Weight[0].strip()
                print("Molecular_Weight:",Molecular_Weight)
                target_dict["Molecular_Weight"] = Molecular_Weight
            if item=="Kind":
                Kind=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if Kind==[]:
                    Kind="None"
                else:Kind=Kind[0].strip()
                print("Kind:",Kind)
                target_dict["Kind"] = Kind
            if item=="Specific Function":
                Specific_Function=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if Specific_Function==[]:
                    Specific_Function="None"
                else:Specific_Function=Specific_Function[0].strip()
                print("Specific_Function:",Specific_Function)
                target_dict["Specific_Function"] = Specific_Function
            if item=="General Function":
                General_Function=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/text()')
                if General_Function==[]:
                    General_Function="None"
                else:General_Function=General_Function[0].strip()
                print("General_Function:",General_Function)
                target_dict["General_Function"] = General_Function
            if item=="Gene sequence":
                Gene_sequence=s2.xpath('/html/body/main/div/div[2]/dl[1]/dd['+str(i)+']/pre/text()')
                if Gene_sequence==[]:
                    Gene_sequence="None"
                else:Gene_sequence=Gene_sequence[0].strip()
                print("Gene_sequence :",Gene_sequence)
                target_dict["Gene_sequence"] = Gene_sequence
        conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase',
                               charset='utf8')
        target_cursor = conn.cursor()
        target_sql = "REPLACE INTO drugbank_target(target_name,Kind,Organism,General_Function,Specific_Function," \
                     "Gene_Name,Molecular_Weight,drugbank_id,Gene_sequence) VALUES (%(target_name)s,%(Kind)s,%(Organism)s," \
                     "%(General_Function)s,%(Specific_Function)s,%(Gene_Name)s,%(Molecular_Weight)s,%(drugbank_id)s,%(Gene_sequence)s)"
        try:
            target_cursor.execute(target_sql, target_dict)
            conn.commit()
            target_cursor.close()

        except Exception as e:
            print(e)
            conn.rollback()
            print("???????????????????????????????????????")
            time.sleep(10)


if __name__=="__main__":
    #url='https://www.drugbank.ca/drugs/DB00669'
    #craw_drugbank(url,drugbank_id="DB00669")
    f1 = open('drugbank_link2.txt', 'r')
    # url = 'https://www.drugbank.ca/drugs/DB01050'
    count_result = 0
    for line in f1.readlines():
        # print(line.strip())
        # line=line.split(" ")[3]
        if line == '\n':
            continue
        url = line.strip()
        str1=url
        str1=str1.replace("https://www.drugbank.ca/drugs/","")
        print("drugbank_id:",str1)
        # url='https://www.drugbank.ca/drugs/'+line.strip()
        print("@@@@@@@@@@@@@@@")
        print("url:", url)
        craw_drugbank(url,str1)
        count_result = count_result + 1
    print(count_result)