
Python3

使用mysql数据库，使用mysql数据库

歌曲表
![歌曲表](https://github.com/JzwOnly/JCrawler_comments/blob/master/docs/Song.png)

评论表
![评论表](https://github.com/JzwOnly/JCrawler_comments/blob/master/docs/comment.png)

歌曲评论关联表
![歌曲评论关联表](https://github.com/JzwOnly/JCrawler_comments/blob/master/docs/Song_Comment.png)

记录抓取位置表
![记录抓取位置表](https://github.com/JzwOnly/JCrawler_comments/blob/master/docs/has_been_completed.png)

使用:

    该爬虫使用requests+bs4 进行网易云音乐的热门评论，和歌曲信息
    注意：记录抓取到的歌曲id位置表中，以100为基数，存储了抓取到的id位置，每抓取完100个id，存入一次数据库

    在运行setup.py文件之前
    1. 在DBManager中填入mysql数据库密码
    2. 根据上面的四张表结构进行创建表
    3. 手动去wyycomment.py 中
    line28: traversalSongId(起始id, 结束id) 修改这两个id，
    数据库中记录了上一个抓到的id（记不住了可以去`has_been_completed`中查看）
