# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import DingDian.settings
import pymysql
import logging
from DingDian.proxyParser import checkProxy

logger = logging.getLogger(__name__)

class booksPipeline(object):

    def __init__(self):
        self.MYSQL = DingDian.settings.MYSQL
        self.con = pymysql.connect(
            host = self.MYSQL["MYSQL_HOST"],
            db = self.MYSQL["MYSQL_DBNAME"],
            user = self.MYSQL["MYSQL_USER"],
            passwd = self.MYSQL["MYSQL_PASSWD"],
            charset='utf8',
            use_unicode=True

        )

        self.cursor = self.con.cursor()

    def close_spider(self,spider):
        checkProxy.shutDown = True
        self.con.close()

    def process_item(self, item, spider):
        if item["type"] == "bookInfo":
            try:
                self.cursor.execute(
                    "insert into xs(name,id,chapterNew,author,charNum,updateTime,isEnd) values('%s',%d,'%s','%s',%d,'%s',%d)" % (
                    item["name"], item["id"],item["chapterNew"], item["author"], item["charNum"], item["updateTime"], item["isEnd"]))
                self.con.commit()
            except Exception as e:
                self.con.rollback()
                logger.error("[+]采集小说失败：\t" + item["name"])
                logger.error(e)
            return item
            
        if item["type"] == "chapterInfo":
            try:
                self.cursor.execute(
                   "insert into xscontent values(%d,'%s',%d,'%s')"% (item["id"], item["chapterName"], item["chapterNum"], item["content"]))
                self.con.commit()
            except Exception as e:
                self.con.rollback()
                logger.error("[+]采集小说失败：\t" + item["chapterName"])
                logger.error(e)
            return item