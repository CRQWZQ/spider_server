# -*- coding:utf-8 -*-
import re
import time
import json
import datetime

# import self as self
# from dask.distributed import Client
# from scrapy import Request, FormRequest
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from bs4 import BeautifulSoup as bs4
# from pyquery import PyQuery as pq
from selenium import webdriver
from multiprocessing.pool import Pool
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from mysqldbHelper import MysqldbHelper

__author__ = 'ZQ'

class BuyerTrade_Info(object):
    def __init__(self, url):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=option)
        # self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 2)
        self.db = MysqldbHelper()
        self.url = url

    # 获取淘宝订单页面
    def search_trade(self):
        try:

            # 获取授权登录的链接进行页面数据获取
            self.browser.get(self.url)
            time.sleep(2)
            # # 切换电脑账号登录
            # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_Quick2Static'))).click()
            # time.sleep(2)
            # action = ActionChains(browser)
            # time.sleep(2)
            # # 滑动鼠标尽可能让模拟人运行鼠标的行为
            # action.move_by_offset(random.randint(10, 60), random.randint(10, 60)).perform()
            # # 先使用自己账号进行登录测试
            # browser.find_element_by_id('TPL_username_1').clear()
            # username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1')))
            # action.move_by_offset(random.randint(10, 60), random.randint(10, 60)).perform()
            # username.send_keys(u'tb_*******')
            # username.send_keys(Keys.TAB)
            # time.sleep(2)
            # password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1')))
            # browser.find_element_by_id('TPL_password_1').clear()
            # password.click()
            # browser.find_element_by_id('TPL_password_1').send_keys('********')
            # time.sleep(1)
            # # 滑块验证
            # while True:
            #     try:
            #         # 定位滑块元素,如果不存在，则跳出循环
            #         show = browser.find_element_by_xpath("//*[@id='nocaptcha']")
            #         showval = show.value_of_css_property("display")
            #         if not show.is_displayed():
            #             break
            #         # 定位滑块元素
            #         source = browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
            #         time.sleep(1)
            #         action.click_and_hold(source).perform()
            #         for index in range(20):
            #             try:
            #                 action.move_by_offset(15, 0).perform() # 平行移动鼠标
            #                 # browser.save_screenshot('login-screeshot-i-' + str(index) + '.png')
            #             except Exception as e:
            #                 print(e)
            #                 break
            #
            #             if (index==19):
            #                 action.release()
            #                 time.sleep(1)
            #                 # browser.save_screenshot('login-screeshot-i-' + str(index) + '.png')
            #             else:
            #                 time.sleep(0.2)
            #                 time.sleep(0.2)
            #
            #         print(show.get_attribute("outerHTML"))
            #         time.sleep(2)
            #         # browser.save_screenshot('login-screeshot-0.png')
            #
            #         # # 定义鼠标拖放动作
            #         # ActionChains(browser).drag_and_drop_by_offset(source, 600, 0).perform()
            #         # # 等待JS认证运行，如果不等待容易报错
            #         time.sleep(2)
            #         # 查看是否认证成功，获取text值
            #         text = browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
            #         # 判断验证响应效果
            #         if text.text.startswith(u'验证通过'):
            #             print('成功滑动')
            #             break
            #         if text.text.startswith(u'请点击'):
            #             print('成功滑动')
            #             break
            #         if text.text.startswith(u'请按住'):
            #             continue
            #     except Exception as e:
            #         # 失败后重新刷新加载滑块模块
            #         action.move_by_offset(random.randint(100, 600), random.randint(100, 600)).perform()  # 平行移动鼠标
            #         browser.find_element_by_xpath("//*[@id='nocaptcha']/div/span/a").click()
            #         print(e)

            # 点击登录
            # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SubmitStatic'))).click()

            # 扫码等待
            while True:
                time.sleep(2)
                if self.is_login_sucess():
                    break
                elif self.is_QRCodeLogin_sucess():
                    continue
                else:
                    time.sleep(1)
                    continue

            self.browser.find_element_by_xpath('//*[@id="J_SiteNavMytaobao"]/div[1]/a/span').click()
            time.sleep(1)
            # 获取用户信誉 重复用户不会多次获取（后续优化用户是否存在数据库中，存在则只更新数据）
            self.get_contentInfo()

            # 获取所有订单信息 （页面还为全部解析完成）
            self.browser.find_element_by_xpath('//*[@id="bought"]').click()
            time.sleep(1)
            self.get_tradeInfo()
        except TimeoutException as e:
            print('超时异常', e)

    # 评价管理中获取用户誉
    def get_contentInfo(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="myRate"]').click()

            username = self.browser.find_element_by_xpath('//*[@id="J_LoginInfo"]/div[1]/a[1]').text
            xinyong = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/h4[2]/a[1]').text    # 累积信用积分
            xy_img = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/h4[2]/a[2]/img').get_attribute('src')     #信用等级砖展
            good_rate = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/p/strong').text    # 好评率
            week_good = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[2]/a').text    # 最近一周好评
            month_good = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[3]/a').text   # 最近一个月好评
            sex_months_good = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[4]/a').text  # 最近6个月好评
            sex_months_ago_good = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[5]/a').text  # 6个月前好评
            week_general = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[2]/a').text     # 最近一周中评
            month_general = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[3]/a').text    # 最近一个月中评
            sex_months_general = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[4]/a').text   # 最近6个月中评
            sex_months_ago_general = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[5]/a').text   # 6个月前中评
            week_bad = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[2]/a').text
            month_bad = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[3]/a').text
            sex_months_bad = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[4]/a').text
            sex_months_ago_bad = self.browser.find_element_by_xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[5]/a').text

            sql = "INSERT into reputation(tb_name,xinyong,xy_img,good_rate,week_good,month_good,sex_months_good," \
                  "sex_months_ago_good,week_general,month_general,sex_months_general,sex_months_ago_general,week_bad," \
                  "month_bad,sex_months_bad,sex_months_ago_bad)" \
                  " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.db.updateByParam(sql, (username, xinyong, xy_img, good_rate, week_good, month_good, sex_months_good,
                                   sex_months_ago_good, week_general, month_general, sex_months_general, sex_months_ago_general,
                                   week_bad, month_bad, sex_months_bad, sex_months_ago_bad))
        except Exception as e:
            print("get_contentInfo is error or insert info is repetition : %s " % e)
    # 订单信息获取
    def get_tradeInfo(self):
        try:
            # json.parse 内容正则匹配 ：JSON.parse\('(.*?)\'\)\;
            # 匹配mainOrders内容的正则表达式   ： \"mainOrders\":(.*?)\,\"page\"

            html = self.browser.page_source
            result = html.encode('utf-8').decode('unicode_escape') #页面内容先进行转码 Unicode编码转换一下
            # 正则匹配 订单信息列表详情
            regex = r'\"mainOrders\":(.*?)\,\"page\"'
            detail_data = re.search(regex, result)
            detail_data = detail_data.group(1)
            data_dict = json.loads(detail_data)
            for detail in data_dict:
                url_detail = detail.get('statusInfo').get('url')
                if url_detail:
                    url_detail = 'https:' + url_detail
                    a = re.search('tmall', url_detail)
                    b = re.search('tradearchive.taobao', url_detail)
                    c = re.search('trade.taobao', url_detail)

                    if a or b or c:
                        info_dict = {}  # 存放一部分信息

                        order_id = detail.get('id')
                        info_dict['order_id'] = order_id

                        store_url = detail.get('seller').get('shopUrl')
                        info_dict['store_url'] = 'https:' + store_url

                        store_name = detail.get('seller').get('shopName')
                        info_dict['store_name'] = store_name

                        ww_name = detail.get('seller').get('nick')
                        info_dict['ww_name'] = ww_name

                        trade_time = detail.get('orderInfo').get('createTime')
                        info_dict['trade_time'] = trade_time

                        if detail.get('payInfo').get('postFees'):
                            post_fee = detail.get('payInfo').get('postFees')[0].get('value')  # ￥0.00
                            info_dict['post_fee'] = re.match(r'￥(.*)', post_fee).group(1)
                        else:
                            info_dict['post_fee'] = ''

                        real_pay = detail.get('payInfo').get('actualFee')
                        info_dict['real_pay'] = real_pay

                        info_dict['goods'] = []

                        goods_list = detail.get('subOrders')
                        for single_goods in goods_list:
                            goods_dict = {}
                            goods_id = single_goods.get('itemInfo').get('id')
                            goods_dict['itemId'] = goods_id
                            goods_img = single_goods.get('itemInfo').get('pic')
                            if goods_img:
                                goods_dict['goods_img'] = 'https:' + goods_img
                            else:
                                goods_dict['goods_img'] = ''

                            goods_title = single_goods.get('itemInfo').get('title')
                            goods_dict['goods_title'] = goods_title

                            goods_url = single_goods.get('itemInfo').get('itemUrl')
                            if goods_url:
                                goods_dict['goods_url'] = 'https:' + goods_url
                            else:
                                goods_dict['goods_url'] = ''

                            if single_goods.get('itemInfo').get('skuText'):
                                for sku_index in range(len(single_goods.get('itemInfo').get('skuText'))):
                                    goods_sku1_name = single_goods.get('itemInfo').get('skuText')[sku_index].get('name')
                                    goods_sku1_value = single_goods.get('itemInfo').get('skuText')[sku_index].get('value')
                                    if goods_sku1_name and goods_sku1_value:
                                        goods_sku1 = goods_sku1_name + ':' + goods_sku1_value
                                        sku = 'goods_sku' + str(sku_index + 1)
                                        # 只插入2个sku
                                        if sku_index < 2:
                                            goods_dict[sku] = goods_sku1
                            if not goods_dict.get('goods_sku1'):
                                goods_dict['goods_sku1'] = ''
                            if not goods_dict.get('goods_sku2'):
                                goods_dict['goods_sku2'] = ''

                            goods_price = single_goods.get('priceInfo').get('realTotal')
                            goods_dict['goods_price'] = goods_price

                            goods_count = single_goods.get('quantity')
                            goods_dict['goods_count'] = goods_count

                            info_dict['goods'].append(goods_dict)

                            try:
                                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                sql1 ="insert into goods (goods_id, goods_title, goods_img, goods_url, order_id, goods_price, goods_count, goods_sku1, goods_sku2, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                self.db.updateByParam(sql1, (goods_dict['itemId'], goods_dict['goods_title'], goods_dict['goods_img'], goods_dict['goods_url'], info_dict['order_id'], goods_dict['goods_price'],
                                                       goods_dict['goods_count'], goods_dict['goods_sku1'], goods_dict['goods_sku2'], dt))
                            except Exception as e:
                                print('insert goods data is error: %s' % e)

                        goods_status = detail.get('statusInfo').get('text')
                        info_dict['goods_status'] = goods_status
                        try:
                            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            sql2 = "insert into orders_detail (order_id, store_name, store_url, ww_name, trade_time, post_fee, real_pay, goods_status, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            self.db.updateByParam(sql2, (info_dict['order_id'], info_dict['store_name'], info_dict['store_url'], info_dict['ww_name'], info_dict['trade_time'], info_dict['post_fee'], info_dict['real_pay'], info_dict['goods_status'], dt))
                        except Exception as e:
                            print('insert order_detail data is error: %s' % e)

            return True
        except Exception as e:
            print("get_tradeInfo is error:%s" % e)
            return False

    # 之前的页面解析  现已弃用
    def parse_orders(self, response):
        result = response.text
        data_dict = json.loads(result)

        # 在订单列表中获取所需数据
        for detail in data_dict.get('mainOrders'):
            url_detail = detail.get('statusInfo').get('url')
            if url_detail:
                url_detail = 'https:' + url_detail
                a = re.search('tmall', url_detail)
                b = re.search('tradearchive.taobao', url_detail)
                c = re.search('trade.taobao', url_detail)

                if a or b or c:
                    info_dict = {}  # 存放一部分信息

                    order_id = detail.get('id')
                    info_dict['order_id'] = order_id

                    store_url = detail.get('seller').get('shopUrl')
                    info_dict['store_url'] = 'https:' + store_url

                    store_name = detail.get('seller').get('shopName')
                    info_dict['store_name'] = store_name

                    ww_name = detail.get('seller').get('nick')
                    info_dict['ww_name'] = ww_name

                    trade_time = detail.get('orderInfo').get('createTime')
                    info_dict['trade_time'] = trade_time

                    if detail.get('payInfo').get('postFees'):
                        post_fee = detail.get('payInfo').get('postFees')[0].get('value')  # ￥0.00
                        info_dict['post_fee'] = re.match(r'￥(.*)', post_fee).group(1)

                    real_pay = detail.get('payInfo').get('actualFee')
                    info_dict['real_pay'] = real_pay

                    info_dict['goods'] = []

                    goods_list = detail.get('subOrders')
                    for single_goods in goods_list:
                        goods_dict = {}

                        goods_img = single_goods.get('itemInfo').get('pic')
                        if goods_img:
                            goods_dict['goods_img'] = 'https:' + goods_img
                        else:
                            goods_dict['goods_img'] = ''

                        goods_title = single_goods.get('itemInfo').get('title')
                        goods_dict['goods_title'] = goods_title

                        goods_url = single_goods.get('itemInfo').get('itemUrl')
                        if goods_url:
                            goods_dict['goods_url'] = 'https:' + goods_url
                        else:
                            goods_dict['goods_url'] = ''

                        if single_goods.get('itemInfo').get('skuText'):
                            for sku_index in range(len(single_goods.get('itemInfo').get('skuText'))):
                                goods_sku1_name = single_goods.get('itemInfo').get('skuText')[sku_index].get('name')
                                goods_sku1_value = single_goods.get('itemInfo').get('skuText')[sku_index].get('value')
                                if goods_sku1_name and goods_sku1_value:
                                    goods_sku1 = goods_sku1_name + ':' + goods_sku1_value
                                    sku = 'goods_sku' + str(sku_index + 1)
                                    # 只插入2个sku
                                    if sku_index < 2:
                                        goods_dict[sku] = goods_sku1
                        if not goods_dict.get('goods_sku1'):
                            goods_dict['goods_sku1'] = ''
                        if not goods_dict.get('goods_sku2'):
                            goods_dict['goods_sku2'] = ''

                        goods_price = single_goods.get('priceInfo').get('realTotal')
                        goods_dict['goods_price'] = goods_price

                        goods_count = single_goods.get('quantity')
                        goods_dict['goods_count'] = goods_count

                        info_dict['goods'].append(goods_dict)

                    goods_status = detail.get('statusInfo').get('text')
                    info_dict['goods_status'] = goods_status

    # 判断是否登录：（后续有链接也要弃用）
    def is_QRCodeLogin_sucess(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[3]/div[2]/p/span').text.startswith(u'扫一扫登录')
            return True
        except:
            return False

    # 判断是否登录账号：（后续有链接也要弃用）
    def is_login_sucess(self):
        try:
            self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[2]/a[1]').text != ''
            return True
        except:
            return False

    def call_close(self):
        self.browser.close()

def trade_spider_run(url):
    wn = BuyerTrade_Info(url)
    try:
        wn.search_trade()
    except Exception as e:
        print('请求出现错误，导致任务失败！', e)

    finally:
        wn.call_close()

def main(urls):
    pool = Pool(processes=5)
    for url in urls:
        result = pool.apply_async(trade_spider_run, (url, ))

    pool.close()
    pool.join()
    if result.successful():
        print('trade_spider_run is successful!')

if __name__ == '__main__':

    urls = ["https://login.taobao.com"] * 3
    main(urls)


