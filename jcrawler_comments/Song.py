#!usr/bin/env python3
# -*- coding: utf-8 -*-
#

from jcrawler_comments.Comment import getJsonToCommentModel
from jcrawler_comments.Comment import get_comment
from jcrawler_comments.common import *

class Song(object):
    __slots__ = ('sid','name','link','artist','commentsNum','hotComments','proxie')

    def __init__(self, sid, name, link, artist, proxie):
        self.sid = int(sid)
        self.proxie = proxie
        self.name = name
        self.link = link
        self.artist = artist
        commentUrl = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0}?csrf_token='.format(sid)
        commentJson = get_comment(commentUrl,1,proxie)
        self.hotComments = getJsonToCommentModel(commentJson)
        self.commentsNum = int(commentJson['total'])



def songInfo(sid,proxie):
    url = 'http://music.163.com/song?id='+str(sid)
    s = requests.session()
    try:
        if proxie == None:
            s = BeautifulSoup(s.get(url,headers=getHeader('header'),timeout=10).content,'lxml')
        else:
            s = BeautifulSoup(s.get(url, proxies=proxie,headers=getHeader('header'),timeout=10).content,'lxml')
        songHtml = s.find('div',{'class':'m-lycifo'})
        if songHtml == None:
            if s.find('div', {'class': 'n-for404'}) != None:
                print('歌曲id:{0}'.format(sid), '404')
                return '404'
        else:
            name = songHtml.find('em',{'class':'f-ff2'}).text
            artist = songHtml.find('p',{'class':'des s-fc4'}).find('span')['title']
            songModel = Song(sid,name,url,artist,proxie)
            print('歌曲id：{0}《{1}》该歌曲评论数为：{2}, 热门评论数为：{3}'.format(songModel.sid,songModel.name,songModel.commentsNum,len(songModel.hotComments)))
            return songModel
    except Exception as e:
        print('Error',url,e)
        return None
