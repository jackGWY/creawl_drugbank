import os
from lxml import etree
import requests
import time
import urllib
import pymysql

conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase',
                               charset='utf8')
cur1 = conn.cursor()
sql_drugbank = 'select * from drugbank'
cur1.execute(sql_drugbank)
drugbank_list=cur1.fetchall()
print("drugbank_list:",drugbank_list)
for drugInfo in drugbank_list:
    drugbank_id=drugInfo[1]
    print("drugbank_id:",drugbank_id)
    drugbank_url2='https://www.drugbank.ca/drugs/'+drugbank_id
    print("drugbank_url2:",drugbank_url2)

    cur2=conn.cursor()
    sql2='update drugbank set drugbank_url = "%s" WHERE drugbank_id = "%s"' %(drugbank_url2,drugbank_id)
    cur2.execute(sql2)
    try:
        cur2.execute(sql2)
        conn.commit()
        cur2.close()
    except Exception as e:
        print("???????????????????????????????????????")
        print(e)
        conn.rollback()
        time.sleep(10)
