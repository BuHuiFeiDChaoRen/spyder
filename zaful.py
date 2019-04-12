import  requests
from lxml import etree
import json
class XpathSpider(object):
    def __init__(self):
        self.url = 'https://www.zaful.com/new-arrivals/date-2019-04-11/'
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
        url_list = xpath_data.xpath('//a[@class="logsss_event_cl"]/@href')
        title_list = xpath_data.xpath('//a[@class="logsss_event_cl"]/text()')
        time = xpath_data.xpath('//div[@class="category-top clearfix"]/h2/text()')[0]
        return url_list,title_list,time

    def parse_detail_data(self,data):
        xpath_one = etree.HTML(data)
        sku = xpath_one.xpath('//p[@class="sku"]/span/text()')
        title = xpath_one.xpath('//p[@class="js-goods-title goods-text"]/text()')
        price = xpath_one.xpath('//span[@class="shop-price my_shop_price"]/text()')
        color = xpath_one.xpath('//span[@class="big-color"]/a/@title')
        image = xpath_one.xpath('//span[@class="big-color"]/a/img/@src')
        size = xpath_one.xpath('//p[@class="js-sizeItem active "]/a/@title')
        description_title = xpath_one.xpath('//div[@class="xxkkk20"]/strong/text()')
        descripyion_text = xpath_one.xpath('//div[@class="xxkkk20"]/text()')
        descripyion_text = [i for i in descripyion_text if (i != '             ' and i != '\n            ')]
        dict_description = dict(zip(description_title, descripyion_text))
        return sku,title,price,color,image,size,dict_description


    def downloadimage(self,image):
        print("正在下载图片：")
        image_str = image[0]
        bendi = 'D:/图片/zaful-new/'
        imagename = image_str.split('/')[-1]
        bendi_one = bendi + imagename
        print(bendi_one)
        img = requests.get(image_str,headers=self.headers)
        with open(bendi_one,'wb') as f:
            f.write(img.content)

    def main(self):
        url = self.url
        data = self.get_response(url)
        url_list,title_list,time= self.parse_list_url(data)
        print(time)
        detail_data = self.get_response(url_list[0])
        sku,title,price,color,image,size,dict_description=self.parse_detail_data(detail_data)
        print(sku,title,price,color,image,size,dict_description)
        # self.downloadimage(image)

XpathSpider().main()