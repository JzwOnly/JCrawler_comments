#!usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pymysql.cursors
from jcrawler_comments.common import *
import time
import sched


def insertData(arr):
    """
    清空表数据(包括自增长id)
     TRUNCATE TABLE table
     truncate
    """
    conn = pymysql.connect(user='root', password='jiayoujzw2016', db='wyy', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            # 插入一条新纪录
            sql = "INSERT INTO `Song` (`sid`,`name`,`link`,`artist`,`commentsNum`) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,arr)
        conn.commit()
    finally:
        conn.close()

def insertComment():
    timeStr = timeStampToDateStr(1501143628280)
    timeDate = timeStampToDate(1501143628280)
    conn = pymysql.connect(user='root', password='jiayoujzw2016', db='wyy', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            # 插入一条新纪录
            sql = "INSERT INTO `Comment` (`cid`,`content`,`userName`,`uid`,`likeNum`,`createDate`) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(486926138,'好多人说这剧三观不正，导演估计是个小三，其实我的前半生这电视剧也就讲发生在上海的故事，要是在我们这儿啊，第一集陈俊生就被罗子君打死了，全剧终。','云村儿颜值担当',251506059,1056,timeDate))
        conn.commit()
    finally:
        conn.close()

#insertComment()
# 被调度触发的函数
def event_func():
    print("Current Time:", time.strftime("%y-%m-%d %H:%M:%S"))


def run_function():
    # 初始化sched模块的scheduler类
    s = sched.scheduler(time.time, time.sleep)
    # 设置一个调度,因为time.sleep()的时间是一秒,所以timer的间隔时间就是sleep的时间,加上enter的第一个参数
    s.enter(0, 2, event_func)
    s.run()


def timer1(sleepTime):
    while True:
        # sched模块不是循环的，一次调度被执行后就Over了，如果想再执行，可以使用while循环的方式不停的调用该方法
        run_function()
        time.sleep(sleepTime)

def sl():
    print('开始',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    time.sleep(5)
    print('结束',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def test():
    getIpPool()

test()