
Python3

使用:

    该爬虫使用requests+bs4 进行网易云音乐的热门评论，和歌曲信息
    使用mysql数据库
    数据库表结构
    1. 歌曲表
    ![image](http://github.com/JzwOnly/JCrawler_comments/docs/Song.png)
    2. 评论表
    ![image](http://github.com/JzwOnly/JCrawler_comments/docs/comment.png)
    3. 歌曲评论关联表
    ![image](http://github.com/JzwOnly/JCrawler_comments/docs/Song_Comment.png)
    4. 记录赚取到的id位置
    ![image](http://github.com/JzwOnly/JCrawler_comments/docs/has_been_completed.png)


    注意：记录抓取到的歌曲id位置表中，以100为基数，存储了抓取到的id位置，每抓取完100个id，存入一次数据库

    在运行setup.py文件之前
    1. 在DBManager中填入mysql数据库密码
    2. 根据上面的四张表结构进行创建表
    3. 手动去wyycomment.py 中
    line28: traversalSongId(起始id, 结束id) 修改这两个id，
    数据库中记录了上一个抓到的id（记不住了可以去`has_been_completed`中查看）
