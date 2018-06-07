# -*- coding:utf-8 -*-
import logging

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import SelectExecutor

__author__ = 'ZQ'

from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    SelectExecutor.main()

#logging 日志生成
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filename='logJob.txt', filemode='a')

executors = {
    'default': ThreadPoolExecutor(5),
    'processpool': ProcessPoolExecutor(3)
}

if __name__ == '__main__':
    scheduler = BlockingScheduler(executors=executors)
    scheduler.add_job(job, 'interval', minutes=1)
    scheduler._logger = logging
    scheduler.start()
