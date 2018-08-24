# from lxml import etree
# import requests
# url='https://book.douban.com/top250'
# data=requests.get(url).text
# s=etree.HTML(data)
# file=s.xpath('//*[@id="content"]/div/div[1]/div/table[1]')
# for div in file:
# 	title =div.xpath("./tr/td[2]/div[1]/a/@title")
# 	score=div.xpath("./tr/td[2]/div[2]/span[2]/text()")
# 	print("{} {}".format(title[0],score[0]))
import os
from lxml import etree
import requests
import time
import urllib
import pymysql
#注意图片存
#url='https://www.drugbank.ca/drugs/DB01050'
def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def craw_drugbank(url):

    result={
    "drugbank_Name":"None",
    "drugbank_id":"None",
    "drugbank_Type":"None",
    "Groups":"None",
    "Description":"None",
    "Structure":"None",
    "CAS_number":"None",
    "Weight":"None",
    "has_Pathway_table":"None",
    "has_target_table":"None",
    "KEGG_Drug":"None",
    "KEGG_Drug_link":"None"
    }

    pathway_dict={"pathway_name":"None","pathway_link": "None","drugbank_id": "None"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase', charset='utf8')

    time.sleep(10)
    data = requests.get(url,headers=headers).text
    s = etree.HTML(data)
    drugbank_Name= s.xpath('/html/body/main/div/div[4]/dl[1]/dd[1]/text()')
    if drugbank_Name == None or drugbank_Name== []:
        drugbank_Name ="None"
    else:
        drugbank_Name = drugbank_Name[0].strip()
    print("drugbank_Name:", drugbank_Name )
    result["drugbank_Name"]=drugbank_Name
    drugbank_id = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[2]/text()')
    if drugbank_id == None or drugbank_id == []:
        drugbank_id = "None"
    else:
        drugbank_id = drugbank_id[0].split('  ')[0].strip()
    print('drugbank_id:', drugbank_id)
    result["drugbank_id"] = drugbank_id
    pathway_dict["drugbank_id"]=drugbank_id

    drugbank_Type= s.xpath('/html/body/main/div/div[4]/dl[1]/dd[3]/text()')
    if drugbank_Type == None or drugbank_Type == []:
        drugbank_Type = "None"
    else:
        drugbank_Type = drugbank_Type [0].strip()
    print('drugbank_Type:', drugbank_Type)
    result["drugbank_Type"]=drugbank_Type
    Groups = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[4]/text()')
    if Groups == None or Groups == []:
        Groups = "None"
    else:
        Groups = Groups[0].strip()
    print('Groups:', Groups)
    result["Groups"]=Groups
    Description = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[5]/p/text()')
    if Description == None or Description ==[]:
        Description = "None"
    else:
        Description = Description[0].strip()
    print('Description:', Description)
    result["Description"]=Description
    Pathways = s.xpath('//*[@id="drug-pathways"]/tbody/tr')
    if Pathways==None or Pathways==[]:
        result["has_Pathway_table"]="None"
        print("has_Pathway_table:None")

    else:
        result["has_Pathway_table"]="true"
        print("has_Pathway_table:true")

        for div in Pathways:
            pathway_name = div.xpath('./td[1]/a/text()')[0].strip()
            if pathway_name == None or pathway_name ==[]:
                pathway_name = "None"
            else:
                print("pathway_name:", pathway_name)
                pathway_dict["pathway_name"]=pathway_name
                pathway_link = div.xpath('./td[1]/a/@href')[0].strip()
                if pathway_link == None or pathway_link == []:
                    pathway_link = "None"
                    print("pathway_link = None")
                    pathway_dict["pathway_link"]=pathway_link
                else:
                    print("pathway_link:", pathway_link)
                    pathway_dict["pathway_link"]=pathway_link
    # print(Pathways)

    KEGG_Drug = s.xpath('/html/body/main/div/div[4]/dl[4]/dd[3]/dl/dd[2]/a/text()')
    if KEGG_Drug == None or KEGG_Drug == []:
        KEGG_Drug = "None"
    else:KEGG_Drug=KEGG_Drug[0].strip()
    print('KEGG_Drug:', KEGG_Drug)
    result["KEGG_Drug"]=KEGG_Drug

    KEGG_Drug_link = s.xpath('/html/body/main/div/div[4]/dl[4]/dd[3]/dl/dd[2]/a/@href')

    if KEGG_Drug_link == None or KEGG_Drug_link == []:
        KEGG_Drug_link = "None"
    else:KEGG_Drug_link=KEGG_Drug_link[0].strip()
    print('KEGG_Drug_link:', KEGG_Drug_link)
    result["KEGG_Drug_link"]=KEGG_Drug_link

    f_drug = open('KEGG_Drug_link.txt', 'a')
    f_drug.writelines(KEGG_Drug+" "+KEGG_Drug_link +" "+ drugbank_id+" "+url+'\n')
    f_drug.close()

    imgPath = 'https://www.drugbank.ca/structures/' + drugbank_id + '/thumb.svg'
    if not os.path.exists(".." + os.sep + "pic" + os.sep + drugbank_id + ".svg"):
        f = open(".." + os.sep + "pic" + os.sep + drugbank_id + ".svg", 'wb')
        time.sleep(10)
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
    Structure = drugbank_id + '.svg'
    print(Structure)
    result["Structure"]=Structure

    for i in range(1, 20):
        items = s.xpath('/html/body/main/div/div/dl/dt[' + str(i) + ']/text()')
        if items == None or items == []:
            continue
        else:
            for item in items:
                if item == "CAS number":
                    print("CAS_number:", item)
                    CAS_number_value = s.xpath('/html/body/main/div/div/dl/dd[' + str(i) + ']/text()')
                    if CAS_number_value == None or CAS_number_value == []:
                        CAS_number_value = "None"
                    else:
                        CAS_number_value = CAS_number_value[0].strip()
                    print("CAS_number_value:", CAS_number_value)
                    result["CAS_number"]=CAS_number_value

                if item == "Weight":
                    print("Weight:", item)
                    Weight_value = s.xpath('/html/body/main/div/div/dl/dd[' + str(i) + ']/text()')
                    if Weight_value == None or Weight_value == []:
                        Weight_value = "None"
                    else:
                        Weight_value = Weight_value[0].strip()
                    print("Weight_value:", Weight_value)
                    result["Weight"]=Weight_value
    #html = requests.get(url, headers=headers)

    target_id_list = s.xpath(
        '//div[@class="bond-list-container targets"]/div[@class="bond-list"]/div[@class="bond card"]/@id')
    print("target_id_list:", target_id_list)
    if target_id_list == None or target_id_list == []:
        result["has_target_table"] = "None"  # 标记有没有targets
        print("has_target_table:None")

    else:
        result["has_target_table"] = "true"
        print("has_target_table:true")
        for target_id in target_id_list:
            target_id = target_id.strip()
            # print(target_id)
            string_to_xpath = '//*[@id="BE0000262"]/div/strong/a/text()'
            str_to_replace = txt_wrap_by(r'"', r'"', string_to_xpath)
            # print("str_to_replace:",str_to_replace)
            string_to_xpath = string_to_xpath.replace(str_to_replace, target_id)
            target_name = s.xpath(string_to_xpath)
            target_name = list(set(target_name))
            if target_name==None or target_name==[]:
                target_name="None"
            else:target_name=target_name[0].strip()
            # target_name=s.xpath('//*[@id='+str(target_id)+']/div[2]/strong/a/text()')错误定位方法
            print("target_name:", target_name)
            target_dict = {
                "target_name": target_name,
                "Kind": "None",
                "Organism": "None",
                "General_Function": "None",
                "Specific_Function": "None",
                "Gene_Name": "None",
                "Molecular_Weight": "None",
                "drugbank_id": drugbank_id
            }
            # 第一个div
            for i in range(1, 4):
                string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                 '/div[@class="col-sm-12 col-lg-5"]/dl/dt[' + str(
                    i) + ']/text()'
                item = s.xpath(string_to_xpath)
                item = list(set(item))
                if item == None or item == []:  # 只要判断四个字段
                    continue
                else:
                    item = item[0].strip()
                    print("item_1:", item)
                    if item == "Kind":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-5"]/dl/dd[' + str(
                            i) + ']/text()'
                        Kind_value = s.xpath(string_to_xpath)
                        if Kind_value==None or Kind_value==[]:
                            Kind_value="None"
                        else:Kind_value = Kind_value[0].strip()

                        print("Kind_value:", Kind_value)
                        target_dict["Kind"]=Kind_value

                    if item == "Organism":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-5"]/dl/dd[' + str(
                            i) + ']/text()'
                        Organism_value = s.xpath(string_to_xpath)
                        if Organism_value==None or Organism_value==[]:
                            Organism_value="None"
                        else:Organism_value = Organism_value[0].strip()

                        print("Organism_value:", Organism_value)
                        target_dict["Organism"]=Organism_value
            # 另一个div
            for i in range(1, 7):
                string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                 '/div[@class="col-sm-12 col-lg-7"]/dl/dt[' + str(
                    i) + ']/text()'
                item = s.xpath(string_to_xpath)
                item = list(set(item))
                if item == None or item == []:  # 只要判断四个字段
                    continue
                else:
                    item = item[0].strip()
                    print("item_2:", item)
                    if item == "General Function":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(
                            i) + ']/text()'
                        General_Function_value = s.xpath(string_to_xpath)
                        if General_Function_value==None or General_Function_value==[]:
                            General_Function_value="None"
                        else:
                            General_Function_value = General_Function_value[0].strip()
                        print("General_Function_value:", General_Function_value)
                        target_dict["General_Function"]=General_Function_value

                    if item == "Specific Function":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(
                            i) + ']/text()'
                        Specific_Function_value = s.xpath(string_to_xpath)
                        if Specific_Function_value==None or Specific_Function_value==[]:
                            Specific_Function_value="None"
                        else:Specific_Function_value = Specific_Function_value[0].strip()

                        print("Specific_Function_value:", Specific_Function_value)
                        target_dict["Specific_Function"]=Specific_Function_value

                    if item == "Gene Name":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(
                            i) + ']/text()'
                        Gene_Name_value = s.xpath(string_to_xpath)
                        if Gene_Name_value==None or Gene_Name_value==[]:
                            Gene_Name_value="None"
                        else:Gene_Name_value = Gene_Name_value[0].strip()
                        print("Gene_Name_value:", Gene_Name_value)
                        target_dict["Gene_Name"]=Gene_Name_value
                    if item == "Molecular Weight":
                        string_to_xpath = '//*[@id="' + str(target_id) + '"]/div[@class="card-body"]/div[@class="row"]' \
                                                                         '/div[@class="col-sm-12 col-lg-7"]/dl/dd[' + str(
                            i) + ']/text()'
                        Molecular_Weight_value = s.xpath(string_to_xpath)
                        if Molecular_Weight_value==None or Molecular_Weight_value==[]:
                            Molecular_Weight_value="None"
                        else:Molecular_Weight_value = Molecular_Weight_value[0].strip()
                        print("Molecular_Weight_value:", Molecular_Weight_value)
                        target_dict["Molecular_Weight"]=Molecular_Weight_value
        target_cursor=conn.cursor()
        target_sql="REPLACE INTO drugbank_target(target_name,Kind,Organism,General_Function,Specific_Function," \
                   "Gene_Name,Molecular_Weight,drugbank_id) VALUES (%(target_name)s,%(Kind)s,%(Organism)s," \
                   "%(General_Function)s,%(Specific_Function)s,%(Gene_Name)s,%(Molecular_Weight)s,%(drugbank_id)s)"
        try:
            target_cursor.execute(target_sql, target_dict)
            conn.commit()
            target_cursor.close()

        except Exception as e:
            print(e)
            print("???????????????????????????????????????")
            time.sleep(10)
            conn.rollback()
    drugbank_sql="replace into drugbank(drugbank_Name,drugbank_id,drugbank_Type,Groups,Description," \
                 "Structure,CAS_number,Weight,has_Pathway_table,has_target_table,KEGG_Drug,KEGG_Drug_link)" \
                 "VALUES(%(drugbank_Name)s,%(drugbank_id)s,%(drugbank_Type)s,%(Groups)s,%(Description)s," \
                 "%(Structure)s,%(CAS_number)s,%(Weight)s,%(has_Pathway_table)s,%(has_target_table)s," \
                 "%(KEGG_Drug)s,%(KEGG_Drug_link)s)"
    drugbank_cursor=conn.cursor()
    try:
        drugbank_cursor.execute(drugbank_sql, result)
        conn.commit()
        drugbank_cursor.close()

    except Exception as e:
        print("???????????????????????????????????????")
        print(e)

        conn.rollback()
        time.sleep(10)
    sql_pathway="replace into pathway_table(pathway_name,pathway_link,drugbank_id)" \
                      "VALUES (%(pathway_name)s,%(pathway_link)s,%(drugbank_id)s)"
    pathway_cursor=conn.cursor()
    try:
        pathway_cursor.execute(sql_pathway, pathway_dict)
        conn.commit()
        pathway_cursor.close()

    except Exception as e:
        print("???????????????????????????????????????")
        print(e)
        conn.rollback()
        time.sleep(10)

def get_drugbank_link_exist():
    result=[]
    f=open("drugbank_link_exist.txt","r")
    for line in f.readlines():
        if line=="\n":
            continue
        result.append(line.strip())
    f.close()
    return result
if __name__ == '__main__':
    f1 = open('drugbank_link_distinc.txt', 'r')
    #url = 'https://www.drugbank.ca/drugs/DB01050'
    drugbank_link_exist_list=get_drugbank_link_exist()
    count_result=0
    for line in f1.readlines():
        #print(line.strip())
        #line=line.split(" ")[3]
        if line=='\n':
            continue
        url=line.strip()

        #url='https://www.drugbank.ca/drugs/'+line.strip()
        print("@@@@@@@@@@@@@@@")
        print("url:",url)
        if url in drugbank_link_exist_list:
            continue
        craw_drugbank(url)
        f_exist=open("drugbank_link_exist.txt","a")
        f_exist.write(url+"\n")
        f_exist.close()
        count_result=count_result+1
    print(count_result)
    #craw_drugbank(url)