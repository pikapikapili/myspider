
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysqlcunchu import get_conn, execute_sql, close_conn, execute1_sql

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)
# browser=webdriver.Chrome()
#显示等待
wait=WebDriverWait(browser,50)

def search(url):
    browser.get(url)
    for i in range(10):
        js1 = 'window.scrollTo(0,{}*document.body.scrollHeight/10)'.format(i)
        browser.execute_script(js1)
        # time.sleep(0.5)
    #3.获取总页数
    total=wait.until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[3]/nav/ul/li[7]/a/span'))
    )
    html=browser.page_source
    parse_html(html)
    return total.text


#获取书的页数
def searchlist(url,id):
    browser.get(url)
    for i in range(10):
        js1 = 'window.scrollTo(0,{}*document.body.scrollHeight/10)'.format(i)
        browser.execute_script(js1)
        # time.sleep(0.5)
    #3.获取总页数
    html = browser.page_source
    pare2(html,id)
    tree = etree.HTML(html)
    g_list = tree.xpath('//*[@id="anchor_sound_list"]/div[2]/div/nav/ul/li')
    text=len(g_list)

    return text

#所有书的下一页
def next_page(total,url):

    for i in range(2,total):
        new_url =url+'p{}/'.format(i)
        print(new_url)
        browser.get(new_url)
        time.sleep(1)
        html=browser.page_source
        parse_html(html)


#书籍里章节的下一页
def next1_page(id,text,url):

    for i in range(2,text):
        new_url =url+'/p{}/'.format(i)
        browser.get(new_url)
        # time.sleep(1)
        html=browser.page_source
        #获取每本书每页章节
        pare2(html,id)


def parse_html(html):
    tree=etree.HTML(html)
    goods_list=tree.xpath('//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[2]/ul/li')
    # goods_list=tree.xpath('//*[@id="award"]/main/div[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]')
    result=[]
    for goods in goods_list:
        #/div/a[1]/span
        name=goods.xpath('./div/a[1]/span[2]/text()')
        if not name:
            name=goods.xpath('./div/a[1]/span/text()')
        username = goods.xpath('./div/a[2]/text()')
        url=goods.xpath('./div/div/a/@href')
        data={
            'name':name[0],
            'username':username[0],
            'url':'https://www.ximalaya.com'+url[0]
        }
        # print(data)
        result.append(data)
    # 3. 数据保存
    save_result(result)
    #获取书籍章节
    xiya(result)


def save_result(data):
    # 将结果保存到pymysql
    conn = get_conn()
    for result in data:
        sql = f'''insert into comic (xi_name, xi_username, xi_url)
                  values ('{result["name"]}', '{result["username"]}', '{result["url"]}')'''
        # print(sql)
        conn.commit()
        execute_sql(sql, conn)
    close_conn(conn)

def pare2(html,id):
    tree = etree.HTML(html)
    goods_list = tree.xpath('//*[@id="anchor_sound_list"]/div[2]/ul/li')
    result = []
    for goods in goods_list:
        # /div/a[1]/span
        name = goods.xpath('./div[2]/a/span/text()')
        # if not name:
        #     name = goods.xpath('./div/a[1]/span/text()')

        url = goods.xpath('./div[2]/a/@href')
        data = {
            'name': name[0],
            'url':url[0],
            'id':id
        }
        # print(data)
        result.append(data)
        # 3. 数据保存
    save_result1(result)

def save_result1(data):
    # 将结果保存到pymysql
    conn = get_conn()
    for result in data:
        sql = f'''insert into ya_chapter (ya_name, ya_url, comic_id)
                      values ('{result["name"]}', '{result["url"]}', '{result["id"]}')'''
        # print(sql)
        conn.commit()
        execute_sql(sql, conn)
    close_conn(conn)

#遍历每本书
def xiya(result):

    for item in result:

        conn = get_conn()
        sql3 = f'select id from comic where xi_url="{item["url"]}";'
        conn.commit()
        id=execute1_sql(sql3, conn)

        list_url = item["url"]
        close_conn(conn)
        text = searchlist(list_url,id)
        # print(text)

        next1_page(id,text,list_url)


def main():
    url='https://www.ximalaya.com/youshengshu/wenxue/'
    total=search(url)
    total=int(total)

    next_page(total,url)
    # 获取章节



if __name__ == '__main__':
    main()