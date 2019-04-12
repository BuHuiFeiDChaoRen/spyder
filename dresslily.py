import  requests
from lxml import etree

class XpathSpider(object):
    def __init__(self):
        self.url = 'https://www.dresslily.com/new-products1.html?innerid=1818'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',"Connection":"close"
         }
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        # }
    def get_response(self,url):
        response = requests.get(url,headers=self.headers)
        data = response.content.decode()
        return data

    #获取当前页所有商品的链接
    def parse_list_url(self,data):
        xpath_data = etree.HTML(data)
        url_list = xpath_data.xpath('//a[@class="js_logsss_click_delegate_ps js-picture twoimgtip"]/@href')
        title_list = xpath_data.xpath('//a[@class="js_logsss_click_delegate_ps"]/text()')
        image_list = xpath_data.xpath('//img[@class="first-image lazyload"]/@data-original')
        return url_list,title_list,image_list

    #解析每个商品
    def parse_detail_data(self,data):
        xpath_one = etree.HTML(data)
        # sku_1=xpath_one.xpath('//em[@class="sku-show"]')
        sku = xpath_one.xpath('//em[@class="sku-show"]/text()')
        price = xpath_one.xpath('//span[@class="my-shop-price"]/@data-orgp')[0]
        color = xpath_one.xpath('//li[@class="js-sku item selected "]/@data-value')[0]
        size = xpath_one.xpath('//li[@class="js-sku item selected "]/@data-value')[1]
        image = xpath_one.xpath('//img[@data-index="0"]/@src')
        title = xpath_one.xpath('//img[@data-index="0"]/@alt')
        # product_description = xpath_one.xpath('//div[@class="xxkkk2"]/text()')
        description_title = xpath_one.xpath('//div[@class="xxkkk20"]/strong/text()')
        descripyion_text = xpath_one.xpath('//div[@class="xxkkk20"]/text()')
        descripyion_text = [i for i in descripyion_text if (i != '             ' and i != '\n            ')]
        dict_description = dict(zip(description_title, descripyion_text))


        # print(image)
        # print(title)
        # print(color)
        # print(price)
        # print(product_description)
        # print(dict_description)
        # print(title)
        return sku,price,color,image,title,dict_description

    def downloadimage(self,image):
        print("正在下载图片：")
        image_str = image[0]
        bendi = 'D:/图片/dresslily-new/'
        imagename = image_str.split('/')[-1]
        bendi_one = bendi + imagename
        print(bendi_one)
        img = requests.get(image_str,headers=self.headers)
        with open(bendi_one,'wb') as f:
            f.write(img.content)

    def main(self):
        url = self.url
        data = self.get_response(url)
        url_list,title_list,image_list= self.parse_list_url(data)
        # print(url_list[0])
        # print(title_list[0])
        print("okokokokokokok")
        # print(url_list)
        detail_data = self.get_response(url_list[0])
        sku,price,color,image,title,dict_description= self.parse_detail_data(detail_data)
        print(sku,price,color,image,title,dict_description)
        self.downloadimage(image_list)


XpathSpider().main()

