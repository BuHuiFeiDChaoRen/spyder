import  requests
from lxml import etree
import json
class XpathSpider(object):
    def __init__(self):
        self.url = 'https://www.fairyseason.com/products_new.htm?new_type=2019-04-11'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
         }
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        # }

    def get_response(self,url):
        response = requests.get(url)
        data = response.content.decode()
        return data




    def parse_list_url(self, data):
        print("正在解析单个网页内容")
        xpath_data = etree.HTML(data)
        url_list = xpath_data.xpath('//div[@class="dirInfo"]/a/@href')
        title_list = xpath_data.xpath('//div[@class="dirInfo"]/a/@title')
        time = xpath_data.xpath('//a[@class="active"]/@data')
        return url_list, title_list,time




    def parse_detail_data(self,data):
        xpath_one = etree.HTML(data)
        sku = xpath_one.xpath('//li[1]/span[@class="attr_name"][2]/text()')
        title = xpath_one.xpath('//div[@class="productInfoBox"]/h1/text()')
        price = xpath_one.xpath('//span[@class="dirPriceBig redClass"]/text()')
        color = xpath_one.xpath('//div[@nameattr="Color"]/span/@title')
        image = xpath_one.xpath('//img[@class="main_img"]/@src')
        size = xpath_one.xpath('//div[@nameattr="Size"]/span[@meta="128"]/@title')
        # //*[@id="describe"]/div/ul/li[2]/span[1]
        description_title = xpath_one.xpath('//span[@class="attr_name"]/text()')
        del description_title[:4]
        descripyion_text_1 = xpath_one.xpath('//span[@class="attr_val"]/text()')
        descripyion_text_1 = ''.join(descripyion_text_1)
        descripyion_text_1 = [i for i in descripyion_text_1.split("  ") if (i !="\r\n" and i !="") ]
        dict_description = []
        for i in range(len(description_title)):
            dict_description.append(description_title[i] + descripyion_text_1[i])
        return sku,title,price,color,image,size,dict_description


    def downloadimage(self,image):
        print("正在下载图片：")
        image_str = image[0]
        bendi = 'D:/图片/fairyseason-new/'
        imagename = image_str.split('/')[-1]
        bendi_one = bendi + imagename
        print(bendi_one)
        img = requests.get(image_str,headers=self.headers)
        with open(bendi_one,'wb') as f:
            f.write(img.content)



    def main(self):
        url = self.url
        data = self.get_response(url)
        url_list, title_list, time = self.parse_list_url(data)
        detail_data = self.get_response(url_list[0])
        sku,title,price,color,image,size ,dict_description= self.parse_detail_data(detail_data)
        print(time)
        print(sku,title,price,color,image,size,dict_description)
        self.downloadimage(image)


XpathSpider().main()