# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:33:10 2019

@author: Administrator
"""

import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup
import csv
import time


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',"Connection":"close"
}

def get_one_page(url):
    # try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    #   return None
    # except RequestException:
    #     return None
""
# def parse_one_page(html):
#     pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
#                          +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
#                          +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
#     items = re.findall(pattern, html)
#     print(items)

def storageLocalFile(path,data):
    findele = open(path,"wb")
    findele.write(data.encode())
    findele.close()

#最新商品页面爬取
def souphtml(html):
    soup = BeautifulSoup(html,'html.parser')  #python标准库，后面的是解析器类型
    link1 = soup.find_all('div',attrs={'class':'grid-item one-full'})
    #link = soup.find_all('a')
    #print(link1)
    # print(link)
    list_image=[]
    list_name=[]
    list_bianhao=[]
    list_price=[]
    list_href=[]

    for k in link1:
        #衣服照片
        image = k.find('img')
        lazy_src = image.get('lazy-src')
        list_image.append(str(lazy_src))

        #衣服名称
        goods_name =k.find('p')
        title = goods_name.get('title')
        list_name.append(str(title))

        #衣服id码
        id = image.get('id')
        list_bianhao.append(str(id)[9:])

        #衣服价格
        price = k.find('strong')
        shop_price = price.get_text()
        list_price.append(shop_price)

        href_a = k.find('a')
        href = href_a.get('href')
        list_href.append(href)


    # print(list_image)
    # print(list_name)
    # print(list_bianhao)
    # print(list_price)
    return list_image,list_name,list_bianhao,list_price,list_href

def souphtml_one(image,name,id,price,href):
    # print(href[0])
    # print(len(href))
    # for i in range(len(href)):
        # print(href[i])
        # print(type(href))

    for i in range(2):
        # print(href[i])
        url = 'https://www.floryday.com'+ href[i]
        print(url)
        html_one = requests.get(url,headers=headers)
        # if html_one.status_code == 200:
        #     print(html_one.text)
        soup = BeautifulSoup(html_one.text,'html.parser')
        link = soup.find('div',attrs={'class':'prodf-options'})
        span = link.find('span')
        color_1 = span.get('data-value')

        link2 = soup.find_all('div',attrs={'class':'grid-item item pc--one-half'})
        # print(link2)
        info =[]
        for tag in link2:
            span_info = tag.find('span')
            info_text = span_info.get_text()
            info.append(info_text)
        id_1 = id[i]
        name_1 = name[i]
        price_1 =price[i]
        href_1=href[i]
        image_1=image[i]
        print(id_1,name_1,price_1,href_1,image_1)

        data = {}
        data['sku码'], data['商品名称'], data['商品图片'], data['价格'], data['商品链接'],data['颜色'],data['商品详细信息']= id_1, name_1, image_1, price_1, href_1,color_1,info
        header = ['sku码','商品名称','商品图片','价格','商品链接','颜色','商品详细信息']
        with open('floryday_new-arrival.csv','a') as csvwrite:
            mywriter = csv.writer(csvwrite)
            text = []
            text.append(data['sku码'])
            text.append(data['商品名称'])
            text.append(data['商品图片'])
            text.append(data['价格'])
            text.append(data['商品链接'])
            text.append(data['颜色'])
            text.append(data['商品详细信息'])
            mywriter.writerow(text)
    csvwrite.close()



def writefile(image,name,id,price,href):
    data={}
    data['商品编号'],data['商品名称'],data['商品图片'],data['价格'],data['商品链接']=id,name,image,price,href
    header = ['商品编号','商品名称','商品图片','价格','商品链接']
    with open('text.csv','w') as csvwrite:
        mywriter = csv.writer(csvwrite,header)
        mywriter.writerow(data.keys())
        for i in range (len(data['商品编号'])):
            text =[]
            text.append(data['商品编号'][i])
            text.append(data['商品名称'][i])
            text.append(data['商品图片'][i])
            text.append(data['价格'][i])
            text.append(data['商品链接'][i])
            mywriter.writerow(text)
        csvwrite.close()

    #保存图片
    # dirurl ='D:/图片/images/'
    # for imageurl in data['商品图片']:
    #     time.sleep(10)
    #     img = requests.get('https:'+imageurl)
    #     filename = imageurl.split('/')[-1]
    #     fileurl = dirurl + filename
    #     with open(fileurl,'wb') as f:
    #         f.write(img.content)
    #         f.close()

def main():
    url = 'https://www.floryday.com/en/Fashion-r9877/new-arrival/'
    html = get_one_page(url)
    # parse_one_page(html)
    list_image,list_name,list_bianhao,list_price,list_href=souphtml(html)
    # writefile(list_image,list_name,list_bianhao,list_price,list_href)
    souphtml_one(list_image,list_name,list_bianhao,list_price,list_href)

    # path = "D:/资源/1.txt"
    # storageLocalFile(path,html)


if __name__ == '__main__':
    main()