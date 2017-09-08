#!usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pymysql.cursors
from jcrawler_comments.common import getNowDate


class DBManager(object):

    def __init__(self):
        self.conn = pymysql.connect(user='root', password='密码', db='wyy', charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)


    def insertData(self,SongModel_Arr,CommentModel_Arr,Song_Comment_Arr,currentId):
        try:
            with self.conn.cursor() as cursor:
                # 插入一条新纪录
                sql_Song = "INSERT INTO `Song` (`sid`,`name`,`link`,`artist`,`commentsNum`) VALUES (%s,%s,%s,%s,%s)"
                sql_Comment = "INSERT INTO `Comment` (`cid`,`content`,`userName`,`uid`,`likeNum`,`createDate`) VALUES (%s,%s,%s,%s,%s,%s)"
                sql_Song_Comment = "INSERT INTO `Song_Comment` (`sid`,`cid`) VALUES (%s,%s)"
                sql_has_been_completed = "INSERT INTO `has_been_completed` (`currentId`,`date`) VALUES (%s,%s)"
                cursor.executemany(sql_Song,SongModel_Arr)
                cursor.executemany(sql_Comment,CommentModel_Arr)
                cursor.executemany(sql_Song_Comment,Song_Comment_Arr)
                cursor.execute(sql_has_been_completed,(currentId,getNowDate()))
            self.conn.commit()
        finally:
            self.conn.close()