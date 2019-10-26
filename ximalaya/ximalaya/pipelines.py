# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from ximalaya.items import Siye_list, Ya_list
from ximalaya.settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE


class MySQLPipline():

    def __init__(self,user,password,host,port,database):
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        self.database=database

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DATABASE
        )


    def open_spider(self,spider):
        #获取连接和游标
        self.conn=pymysql.Connection(user=self.user,password=self.password,host=self.host,port=self.port,database=self.database)
        self.cursor=self.conn.cursor()
    def close_spider(self,spider):
        self.conn.close()

    def process_item(self,item,spider):
        if isinstance(item, Siye_list):
            #保存到mysql
            for data in item['xi_list']:
                sql1=f'insert into comic (xi_name,xi_username,xi_url) '\
                    f'values ("{data["name"]}","{data["username"]}","{data["url"]}")'
                self.cursor.execute(sql1)
                self.conn.commit()
        if isinstance(item, Ya_list):
            # 查询当前保存的漫画的id值
            sql3 = f'select id from comic where xi_name="{item["title"]}";'
            self.cursor.execute(sql3)
            comic_id = self.cursor.fetchone()[0]

            for data in item['ya_list']:
                sql2=f'insert into ya_chapter (ya_name,ya_url,comic_id)'\
                    f' values ("{data["name"]}","{data["url"]}",{comic_id})'
                self.cursor.execute(sql2)
                self.conn.commit()
        return item

