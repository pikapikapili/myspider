import json
import re

from scrapy import Spider, Selector, Request
from scrapy_splash import SplashRequest,request

from ximalaya.items import Siye_list, Ya_list


class XlSpider(Spider):

    name='ximalaya'

    url='https://www.ximalaya.com/youshengshu/wenxue/'

    def start_requests(self):

        yield Request(url=self.url,callback=self.parse_comic_list)


    def parse_comic_list(self,response):

        # 回调方法，处理url地址所对应的响应内容
        sel=Selector(response)
        #获取所有页数
        comic_list=sel.xpath('//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[3]/nav/ul/li[7]/a/span/text()').extract_first()
        # print(comic_list)
        #获取每页的书
        for i in range(1,int(comic_list)+1):
            url_list='https://www.ximalaya.com/youshengshu/wenxue/'+'p{}/'.format(i)
            yield Request(url=url_list, callback=self.parse_comic)


    def parse_comic(self,response):

        sel=Selector(response)
        item=Siye_list()
        goods_list = sel.xpath('//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[2]/ul/li')
        # goods_list=sel.xpath('//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]')
        result = []
        for goods in goods_list:
            # /div/a[1]/span
            name = goods.xpath('./div/a[1]/span[2]/text()').extract()
            if not name:
                name = goods.xpath('./div/a[1]/span/text()').extract()
            username = goods.xpath('./div/a[2]/text()').extract()
            url = goods.xpath('./div/div/a/@href').extract()
            # item['name']=name[0],
            # item['username']=username[0]
            data = {
                'name': name[0],
                'username': username[0],
                'url': 'https://www.ximalaya.com' + url[0]
            }
            yield Request(url=data['url'], callback=self.parse_chapter)
            result.append(data)
        item['xi_list']=result
        yield item

    def parse_chapter(self,response):
        sel = Selector(response)

        g_list = sel.xpath('//*[@id="anchor_sound_list"]/div[2]/div/nav/ul/li')
        text = int(len(g_list))
        for i in range(text+1):
            new_url=response.url+'p{}/'.format(i)
            yield Request(url=new_url, callback=self.parse_chapter_list)
        # print(text)


    def parse_chapter_list(self,response):
        sel = Selector(response)
        goods_list = sel.xpath('//*[@id="anchor_sound_list"]/div[2]/ul/li')
        # goods_list = sel.xpath('//*[@id="anchor_sound_list"]/div[2]/ul/li[1]')
        result = []
        item = Ya_list()
        item['title']=sel.xpath('//*[@id="award"]/main/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/h1/text()').extract()[0]
        # print(item['title'])
        for goods in goods_list:
            name = goods.xpath('./div[2]/a/span/text()').extract()
            # if not name:
            #     name = goods.xpath('./div/a[1]/span/text()')

            url = goods.xpath('./div[2]/a/@href').extract()
            data = {
                'name': name[0],
                'url': 'https://www.ximalaya.com'+url[0],
            }
            # print(data)
            result.append(data)
        item['ya_list']=result
        yield item

