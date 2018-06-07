# -*- coding:utf-8 -*-
import pymysql

__author__ = 'ZQ'

class MysqldbHelper:
    def getCon(self):
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='tb', port=3306, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            return conn
        except pymysql.Error as e:
            print('pymysql Error:%s' % e)


    def select(self,sql):
        try:
            con = self.getCon()
            print(con)
            cur = con.cursor(pymysql.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except pymysql.Error as e:
            print('pymysql Error:%s' % e)
        finally:
            cur.close()
            con.close()

    def update(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except pymysql.Error as e:
            print('pymysql Error:%s' % e)
        finally:
            cur.close()
            con.close()

    def updateByParam(self, sql, params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except pymysql.Error as e:
            con.rollback()
            print('pymysql Error:%s' % e)
        finally:
            cur.close()
            con.close()