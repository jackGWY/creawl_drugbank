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
import urllib
import pymysql
#注意图片存
#url='https://www.drugbank.ca/drugs/DB01050'


def craw_drugbank(url):
    conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase', charset='utf8')
    cursor = conn.cursor()
    data = requests.get(url).text
    s = etree.HTML(data)

    Name = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[1]/text()')
    if Name==[]:
        return "None"
    Name=Name[0].strip()

    if Name == None or Name == "":
        Name = "None"
    print("Name:", Name)

    drugbank_id = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[2]/text()')
    if drugbank_id==[]:
        return "None"
    drugbank_id=drugbank_id[0].split('  ')[0].strip()
    if drugbank_id == None or drugbank_id == "":
        drugbank_id = "None"
    print('drugbank_id:', drugbank_id)

    Type = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[3]/text()')
    if Type==[]:
        return "None"
    Type=Type[0].strip()
    if Type == None or Type == "":
        Type = "None"
    print('Type:', Type)

    Groups = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[4]/text()')
    if Groups==[]:
        return "None"
    Groups=Groups[0].strip()
    if Groups == None or Groups == "":
        Groups = "None"
    print('Groups:', Groups)

    Description = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[5]/p/text()')
    if Description==[]:
        return "None"
    Description=Description[0].strip()
    if Description == None or Description == "":
        Description = "None"
    print('Description:', Description)
    # Blob

    # CAS_number = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[18]/text()')[0].strip()
    # if CAS_number == None or CAS_number == "":
    #     CAS_number = "None"
    # print('CAS_number:', CAS_number)
    #
    # Weight = s.xpath('/html/body/main/div/div[4]/dl[1]/dd[19]/text()')[0].strip()
    # if Weight == None or Weight == "":
    #     Weight = "None"
    # print('Weight:', Weight)

    Pathways = s.xpath('//*[@id="drug-pathways"]/tbody/tr')
    if Pathways==[]:
        return "None"
    # print(Pathways)
    for div in Pathways:
        pathway_name = div.xpath('./td[1]/a/text()')[0].strip()
        if pathway_name == None or pathway_name == "":
            pathway_name = "None"
        print("pathway_name:", pathway_name)
        pathway_link = div.xpath('./td[1]/a/@href')[0].strip()
        if pathway_link == None or pathway_link == "":
            pathway_link = "None"
        print("pathway_link:", pathway_link)

    KEGG_Drug_name = s.xpath('/html/body/main/div/div[4]/dl[4]/dd[3]/dl/dd[2]/a/text()')
    if KEGG_Drug_name==[]:
        return "None"
    KEGG_Drug_name=KEGG_Drug_name[0].strip()
    if KEGG_Drug_name == None or KEGG_Drug_name == "":
        KEGG_Drug_name = "None"
    print('KEGG_Drug_name:', KEGG_Drug_name)

    KEGG_Drug_link = s.xpath('/html/body/main/div/div[4]/dl[4]/dd[3]/dl/dd[2]/a/@href')
    if KEGG_Drug_name==[]:
        return "None"
    KEGG_Drug_link=KEGG_Drug_link[0].strip()
    if KEGG_Drug_link == None or KEGG_Drug_link == "":
        KEGG_Drug_link = "None"
    print('KEGG_Drug_link:', KEGG_Drug_link)
    # 需要加入的参数
    f_drug = open('E:' + os.sep + 'paindatabase' + os.sep + 'creawl_drugbank'
                  + os.sep + 'KEGG_Drug_link.txt', 'a')
    f_drug.writelines(KEGG_Drug_name+" "+KEGG_Drug_link +" "+ drugbank_id+" "+url+'\n')
    f_drug.close()

    imgPath = 'https://www.drugbank.ca/structures/' + drugbank_id + '/thumb.svg'
    if os.path.exists(".." + os.sep + "pic" + os.sep + drugbank_id + ".svg"):
        f = open(".." + os.sep + "pic" + os.sep + drugbank_id + ".svg", 'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
    Structure = drugbank_id + '.svg'
    print(Structure)


    sqlInsert="replace into drugbank(Name ,drugbank_id ,Type ,Groups ,Description ," \
              "Structure ,CAS_number ,Weight,KEGG_Drug ,KEGG_Drug_link ) " \
              "VALUES (%(Name)s,%(drugbank_id)s,%(Type)s,%(Groups)s,%(Description)s,%(Structure)s,%(CAS_number)s,%(Weight)s),%(KEGG_Drug)s,%(KEGG_Drug_link)s"
    # value={"Name":Name,
    #        "drugbank_id":drugbank_id,
    #        "Type":Type,
    #        "Groups":Groups,
    #        "Description": Description,
    #        "Structure": Structure,
    #        "CAS_number": CAS_number,
    #        "Weight": Weight,
    #        "KEGG_Drug": KEGG_Drug_name,
    #        "KEGG_Drug_link": KEGG_Drug_link
    #
    # }
    #cursor.execute(sqlInsert, value)

    sql_pathway_table="replace into pathway_table(pathway_name,pathway_link,Name )" \
                      "VALUES (%(pathway_name)s,%(pathway_link)s,%(Name)s)"
    # value2={
    #     "pathway_name": pathway_name,
    #     "pathway_link": pathway_link,
    #     "Name": Name
    # }
    #cursor.execute(sql_pathway_table, value2)



    # 处理kegg链接过去的
    # KEGG_Drug_data=requests.get(KEGG_Drug_link).text
    # s2=etree.HTML(KEGG_Drug_data)

    #ATC_Codes = s.xpath('/html/body/main/div/div[4]/dl[4]/dd[4]/a')
    # print(Pathways)
    # for atc in ATC_Codes:
    #     ATC_link = atc.xpath('./@href')[0]
    #     ATC_link = 'https://www.drugbank.ca' + ATC_link
    #
    #     print(ATC_link)
    #     ATC = atc.xpath('./text()')[0].strip().replace(' ', '').replace('—', '_')
    #     if ATC == None or ATC == "":
    #         ATC = "None"
    #     print(ATC)
    #     #sql_ATC_Codes="replace into ATC_Codes(ATC ,ATC_link,Name ) VALUES (%(ATC)s,%(ATC_link)s,%(Name)s)"
    #     lis = atc.xpath('../ul[1]/li')
    #     for li in lis:
    #         ATC_li = li.xpath('./a/text()')[0].strip()
    #         if ATC_li == None or ATC_li == "":
    #             ATC_li = "None"
    #         print(ATC_li)
    #         ATC_li_link = li.xpath('./a/@href')[0]
    #         ATC_li_link = 'https://www.drugbank.ca' + ATC_li_link
    #         if ATC_li_link == None or ATC_li_link == "":
    #             ATC_li_link = "None"
    #         print(ATC_li_link)

if __name__ == '__main__':


    f1 = open('E:' + os.sep + 'paindatabase' + os.sep + 'creawl_drugbank' + os.sep + 'drugbank_id_distinc.txt', 'r')
    #url = 'https://www.drugbank.ca/drugs/DB01050'
    count_result=0
    for line in f1.readlines():
        #print(line.strip())
        url='https://www.drugbank.ca/drugs/'+line.strip()
        print("@@@@@@@@@@@@@@@")
        print("url:",url)
        return_tag=craw_drugbank(url)
        if return_tag!="None":
            count_result=count_result+1
    print(count_result)
    #craw_drugbank(url)