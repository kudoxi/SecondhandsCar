import requests
from multiprocessing import Queue
from threading import Thread
from SecondhandsCar.settings import HEADERS
import random
from selenium import webdriver
from lxml import etree
import pymongo

class GoodsSpider(object):
    def __init__(self):
        self.headers = HEADERS
        self.get_page()
        self.conn = pymongo.MongoClient('127.0.0.1',27017)
        self.mydb = self.conn.SecondhandsCar
        self.myset = self.mydb.lastgoods
        self.detail_urlq = Queue()


    #获取页码
    def get_pagenum(self):
        url = 'http://www.mechadvisor.com/index.php?m=Lianmai&c=Production&a=ajax_goods'
        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.page_source
        driver.quit()
        parse_html = etree.HTML(html)
        pagenum = parse_html.xpath("//ul[@class='pagination']//a[@class='end']/text()")
        if len(pagenum) > 0:
            return int(pagenum[0])
        else:
            return 0

    #获取页面
    def get_page(self):
        pn = 1#self.get_pagenum()
        if pn > 0:
            for i in range(2):
                url = 'https://car.autohome.com.cn/2sc/china/a0_0msdgscncgpi1ltocsp{}ex/'.format(i)
                header=random.choice(HEADERS)
                res = requests.get(url,headers=header)
                html = res.text
                print(i)
                self.parase_page(html)

    #解析页面
    def parase_page(self,html):
        parase_html = etree.HTML(html)
        lis = parase_html.xpath("//div[@class='piclist']/ul/li")
        if len(lis)>0:
            k = 0
            for i in lis:
                if len(i.xpath('./@infoid')) == 0:
                    continue
                carid = i.xpath('./@infoid')[0]
                href = i.xpath("./div[@class='pic']/a/@href")[0]
                img_src = i.xpath("./div[@class='pic']/a/img/@src")[0]
                title = i.xpath("./div[@class='title']/a/text()")[0]
                price_million = i.xpath("./div[@class='detail']/div[@class='detail-r']/span/text()")[0]
                mileage = i.xpath("./div[@class='detail']/div[@class='detail-l']/p[1]/text()")[0]
                register_date = i.xpath("./div[@class='detail']/div[@class='detail-l']/p[2]/text()")[0]
                print({
                    'href':href,
                    'img_src':img_src,
                    'title':title,
                    'price_million':price_million,
                    'mileage':mileage,
                    'register_date':register_date,
                    'carid':carid
                })
                k+=1

    #获取子页面
    def get_detail_page(self):
        if self.detail_urlq:
            pass
            #获取车辆信息

            #获取车主信息　手机号，地址，联系人

            #点击进入店铺，查看用户的营业执照，可能要掉用ＡＩ图片文字识别

    #存入数据库
    def save_page(self):
        pass

    #当前爬取的最后一个id存到mongodb里
    def save_id(self):
        pass

if __name__ == "__main__":
    gs = GoodsSpider()