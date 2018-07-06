# -*- coding:utf-8 -*-
import time

import buyertrade_taobao
from mysqldbHelper import MysqldbHelper

__author__ = 'ZQ'

class SelectExecutor(object):
    def __init__(self):
        self.db = MysqldbHelper()
        sql = "SELECT `login_url`,`lg_token`,`user_name` FROM `lg_token_task` where `status`='success'"
        self.urls = self.db.select(sql)

    def selectExecutor(self):

        if self.urls:
            print("startTime:" + time.strftime("%Y-%m-%d %H:%M:%S"))
            # buyertrade_taobao.pool_main(self.urls)
            for url in self.urls:
                buyertrade_taobao.trade_spider_run(url)
            print("endTime:" + time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("No job is waiting !")

def main():
    se = SelectExecutor()
    se.selectExecutor()

if __name__ == '__main__':
    main()