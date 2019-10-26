import csv
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options=webdriver.ChromeOptions()
options.add_argument('--headers')


browser=webdriver.Chrome()
#显示等待
wait=WebDriverWait(browser,50)

def search(url):

    browser.get(url)

    time.sleep(3)
    #执行js,拖动窗口
    # h=document.body.scrollHeight
    for i in range(10):
        js1 = 'window.scrollTo(0,{}*document.body.scrollHeight/10)'.format(i)
        browser.execute_script(js1)
        time.sleep(2)
    #3.获取总页数

    total=wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="J_bottomPage"]/span[1]/a[9]'))
    )
    html=browser.page_source
    parse_html(html)

    return total.text
def next_page():
    #获取下一页
    #'//*[@id="J_bottomPage"]/span[1]/a[10]'
    next=wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="J_bottomPage"]/span[1]/a[10]'))
    )
    next.click()
    for i in range(10):
        js1 = 'window.scrollTo(0,{} * document.body.scrollHeight/10)'.format(i)
        browser.execute_script(js1)
        time.sleep(3)
    html=browser.page_source
    parse_html(html)
    # print(html)


def parse_html(html):
    tree=etree.HTML(html)
    goods_list=tree.xpath('//*[@id="plist"]/ul/li')
    result=[]
    # with open("jdhuawei", "a", encoding="utf8") as f:
    for goods in goods_list:
        #//*[@id="plist"]/ul/li[51]/div/div[4]/span/a[2]
        name=goods.xpath('./div/div[4]/a/em/text()')[0].strip()
        price = goods.xpath('./div/div[3]/strong[1]/i/text()')
        neicun=goods.xpath('./div/div[4]/span/a[2]/text()')
        pinlun = goods.xpath('./div/div[5]/strong/a/text()')
        img=goods.xpath('./div/div[1]/a/img/@src')
        title=goods.xpath('./div/div[7]/span/a/text()')
        data={
            'name':name,
            'price': price,
            'neicun':neicun,
            'pj': pinlun,
            'img':img,
            'title':title,
        }
        # print(data)
        result.append(data)
    with open("jdhuawei", "a", encoding="utf8") as f:
        for i in result:
            f.write(str(i)+'\n')


def main():
    url='https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_8557&sort=sort_rank_asc&trans=1&JL=3_%E5%93%81%E7%89%8C_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89#J_crumbsBar'
    total=search(url)
    # print(total)
    # for page in range(2,total):
    #     next_page()


if __name__ == '__main__':
    main()