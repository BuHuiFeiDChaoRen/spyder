import  requests
from lxml import etree
import time
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',"Connection":"close"
}


response = requests.get("https://www.rosegal.com/new-products/this-week/",headers=headers).content.decode()

xpath_data = etree.HTML(response)

# result =xpath_data.xpath('//a[@class ="f12"]/text()')
# print(result)

result = xpath_data.xpath('//a[@class="js_exposure logsss_event_cl js_goodsHoverImg"]/@href')
print(result)
for url_one in result:
    print(url_one)
    data = requests.get(url_one,headers=headers).content.decode()
    data_one = etree.HTML(data)
    title = data_one.xpath('//h1[@id="js_goodTitle"]/text()')
    sku = data_one.xpath('//div[@class="goods_sku f14 fr"]/text()')
    price = data_one.xpath('//span[@class="current_price"]/b[@class="my_shop_price"]/text()')
    image = data_one.xpath('//img[@id="js_bigImg"]/@src')
    color_size = data_one.xpath('//a[@class="itemAttr current "]/@title')
    color = color_size[0]
    size=color_size[1]
    descripyion_title= data_one.xpath('//div[@class="xxkkk20"]/strong/text()')
    descripyion_text = data_one.xpath('//div[@class="xxkkk20"]/text()')
    descripyion_text = [i for i in descripyion_text if (i !='             ' and i != '\n            ')]
    dict_description =dict(zip(descripyion_title,descripyion_text))

    print(dict_description)
    print(title,sku,price,color,size,image)
    break

print("正在下载图片")
bendi = 'D:/图片/rosegal-new/'
image_str = image[0]
file_name = image_str.split('/')[-1]
bendi_one = bendi + file_name
img = requests.get(image_str,headers=headers)
with open(bendi_one,'wb') as f:
    f.write(img.content)




