import requests
from bs4 import BeautifulSoup
import os
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
url='https://www.drugbank.ca/unearth/q?utf8=%E2%9C%93&searcher=drugs&query=backache'
html=requests.get(url,headers=headers)
soup=BeautifulSoup(html.text,'lxml')
a=soup.select('.hit-link a')

print(len(a))
print(a)
#E:\paindatabase\pubmed
#f=open("E:"+os.sep+"paindatabase"+os.sep+"pubmed"+os.sep+"backache.txt","w+")
sum=1
for i in a:
	#sum=1
	url="https://www.drugbank.ca"+i['href']
	print(url)
	html_2=requests.get(url,headers=headers)
	soup2=BeautifulSoup(html_2.text,'lxml')
	
	# string1='.rprt abstract'
	# title=soup2.select('.content'+' h1')
	# all=soup2.select('.abstr p')
	# pubmed_id=soup2.select('.rprtid dd')
	# print(pubmed_id[0].text)

	# #print(title)
	# dict1={}
	# dict1["pubmed_id"]=pubmed_id[0].text.strip()
	# dict1["url"]=url.strip()

	# for title1 in title:
	# 	print(title1.text)
	# 	dict1["title"]=title1.text.strip()

	# print("len(all):",len(all))
	# len_all=len(all)
	# if len_all>=4:
	# 		count=1
			
	# 		for j in all:
	# 			if count==1:
	# 				if j.text!="":
	# 					dict1["background"]=j.text.strip()
	# 				else:dict1["background"]="None"
					
	# 			if count==2:
	# 				if j.text!="":
	# 					dict1["methods"]=j.text.strip()
	# 				else:dict1["methods"]="None"
					
	# 			if count==3:
	# 				if j.text!="":
	# 					dict1["results"]=j.text.strip()
	# 				else:dict1["results"]="None"
					
	# 			if count==4:
	# 				if j.text!="":
	# 					dict1["conclusions"]=j.text.strip()
	# 				else:dict1["conclusions"]="None"
	# 			count+=1
	
	# else:
	# 	dict1["background"]="None"
	# 	dict1["methods"]="None"
	# 	dict1["results"]="None"
	# 	dict1["conclusions"]="None"
	# 	# content3=soup2.select('.abstr'+' p')
	# 	# print(len(content3))





	# #print(dict1)
	# list1=[]
	# list1.append(dict1["pubmed_id"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["title"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["background"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["methods"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["results"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["conclusions"].replace(u'\xa0', u'')+"\n")
	# list1.append(dict1["url"].replace(u'\xa0', u'')+"\n")

	# try:
	# 	f.writelines(list1)
	# except UnicodeError as uError:
	# 	continue
	# if sum>=7:
	# 	sum=1
	# 	break
	# sum+=1


	#break
#f.close()

