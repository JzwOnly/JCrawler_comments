#!usr/bin/env python3
# -*- coding: utf-8 -*-
#

from jcrawler_comments.Song import songInfo
from jcrawler_comments.DBManager import DBManager
from time import sleep
from jcrawler_comments.common import radomSec,getIpPool,getAIp

netErrorId = []
firstSongId = 59867
flag = False
sec = 60*15

historyProxie = None

def changeHistoryProxie(value):
    global historyProxie
    historyProxie = value
def getHistoryProxie():
    global historyProxie
    return historyProxie

def main(wetherProxie=None):
    aimSong_Arr = []
    if wetherProxie:
        getIpPool()
    result = traversalSongId(244901,300001,wetherProxie=wetherProxie)
    if result[0] == 'success':
        print(result[2])
        aimSong_Arr = result[1]
    else:
        print(result[2])
    if len(netErrorId) > 0:
        print('由于网络错误，未分析的歌曲id',netErrorId)
def traversalSongId(startId, endId, max404Num=10000,wetherProxie=None):
    song_Arr = []
    id = startId
    print('开始抓取========================================================')
    proxie = None
    while id < endId:
        if wetherProxie:
            if getHistoryProxie() == None:
                proxie = getProxie()
            else:
                proxie = getHistoryProxie()
        getSong(id,song_Arr,proxie)
        # 当整万时，存一批数据到数据库
        if id % 100 == 0:
            print('抓取完100个id,导入一次数据库')
            SongModel_Arr,CommentModel_Arr,Song_Comment_Arr = upPakingModelsToArr(song_Arr)
            db = DBManager()
            db.insertData(SongModel_Arr,CommentModel_Arr,Song_Comment_Arr,id)
            song_Arr = []
        id += 1
        sleep(radomSec())
        print('进行下一个id抓取===================================================')
    return ('success',song_Arr,'{0}-{1}之间'.format(startId,endId))

def getSong(id,song_Arr,proxie):
    result = songInfo(id, proxie)
    if result == '404':
        print(id, '当前页面没有内容')
        if proxie != None:
            changeHistoryProxie(proxie)
    elif result == None:
        if proxie != None:
            print('网络错误,当前遍历id={0}'.format(id), '重新更换ip')
            getSong(id,song_Arr,getProxie())
        else:
            getSong(id,song_Arr,None)
        # netErrorId.append(id)
    else:
        song_Arr.append(result)
        if proxie != None:
            changeHistoryProxie(proxie)
            print('当前使用ip  ' ':' + proxie['http'])

def getProxie():
    # (scheme, ip) = getAIp()
    # proxie = {
    #     scheme: ip
    # }

    ip = getAIp()
    proxie = {
        'http':ip,
        'https':ip
    }

    # print('当前使用ip  ' ':' + ip)
    # proxie = {
    #     'https':'101.251.234.254:51238'
    # }
    # ip = getIpPool1()
    # proxie = {
    #     'http':ip,
    #     'https':ip
    # }
    return proxie
def upPakingModelsToArr(song_Arr):
    SongModel_Arr = []
    CommentModel_Arr = []
    Song_Comment_Arr = []
    for song in song_Arr:
        songTuple = (song.sid,song.name,song.link,song.artist,song.commentsNum)
        SongModel_Arr.append(songTuple)
        for hotComment in song.hotComments:
            hotCommentTuple = (hotComment.cid,hotComment.content,hotComment.username,hotComment.uid,hotComment.likeNum,hotComment.createDate)
            CommentModel_Arr.append(hotCommentTuple)
            song_commentTuple = (song.sid,hotComment.cid)
            Song_Comment_Arr.append(song_commentTuple)

    return tuple(SongModel_Arr),tuple(CommentModel_Arr),tuple(Song_Comment_Arr)

main()