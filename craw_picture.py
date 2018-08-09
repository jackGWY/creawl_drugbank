import re
import urllib.request
import os

#爬取网页html
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


html = getHtml("http://tieba.baidu.com/p/3205263090")
html = html.decode('UTF-8')

#获取图片链接的方法
def getImg(html):
    # 利用正则表达式匹配网页里的图片地址
    reg = r'src="([.*\S]*\.jpg)" pic_ext="jpeg"'
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    print("imglist",imglist)
    return imglist

imgList=getImg(html)
imgCount=0
#for把获取到的图片都下载到本地pic文件夹里，保存之前先在本地建一个pic文件夹
for imgPath in imgList:
    f=open(".."+os.sep+"pic"+os.sep+str(imgCount)+".jpg",'wb')
    f.write((urllib.request.urlopen(imgPath)).read())
    f.close()
    imgCount+=1
print("全部抓取完成")