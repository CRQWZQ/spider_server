# -*- coding:utf-8 -*-
import datetime

import buyertrade_taobao
from mysqldbHelper import MysqldbHelper

__author__ = 'ZQ'

class SelectExecutor(object):
    def __init__(self):
        self.db = MysqldbHelper()
        sql = 'select login_url from qr_code_login where status=1'
        self.urls = self.db.update(sql)

    def selectExecutor(self):

        if self.urls:
            print("startTime:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            buyertrade_taobao.main(self.urls)
            print("endTime:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("No job is waiting !")

def main():
    se = SelectExecutor()
    se.selectExecutor()