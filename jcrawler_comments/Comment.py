#!usr/bin/env python3
# -*- coding: utf-8 -*-
#

from Crypto.Cipher import AES
import base64

from jcrawler_comments.common import *

class Comment(object):
    __slots__ = ('cid','content','username','uid','likeNum','createDate')

    def __init__(self, cid, content, username, uid, likeNum, createDate):
        self.cid = int(cid)
        self.content = content
        self.username = username
        self.uid = int(uid)
        self.likeNum = likeNum
        self.createDate = createDate



def get_comment(url,page,proxie):
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    index = math.floor(random.random()* len(random_16_arr))
    params = get_params(index,page)
    encSecKey = get_encSecKey(index)
    json_text = get_json(url, params, encSecKey,proxie)
    json_dict = json.loads(json_text)
    return json_dict

def get_params(index,page):
    forth_param = "0CoJUm6Qyw8W8jud"
    offset = str((page-1)*20)
    if page > 1:
        total = 'false'
    else:
        total = 'true'
    iv = "0102030405060708"
    offset = 'offset:'+offset
    total = ', total:'+total
    first_param = '{rid:"",' +offset+total+', limit:"20", csrf_token:""}'
    first_key = forth_param
    second_key = random_16_arr[index]
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey(index):
    encSecKey = encSecKey_arr[index]
    return encSecKey

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    encrypt_text = encrypt_text.decode('utf-8')
    return encrypt_text


def get_json(url, params, encSecKey,proxie):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    if proxie == None:
        response = requests.post(url, headers=getHeader('header'), data=data, timeout=10)
    else:
        response = requests.post(url, headers=getHeader('header'), data=data, proxies=proxie, timeout=10)
    return response.content

def getJsonToCommentModel(commentJson):
    comments_Arr = []

    if 'hotComments' in commentJson.keys() and len(commentJson['hotComments']) > 0:
        hotComments = commentJson['hotComments']
        for hotComment in hotComments:
            cid = hotComment['commentId']
            content = hotComment['content']
            username = hotComment['user']['nickname']
            uid = hotComment['user']['userId']
            likeNum = hotComment['likedCount']
            createDate = timeStampToDateStr((int(hotComment['time'])))
            commentModel = Comment(cid,content,username,uid,likeNum,createDate)
            comments_Arr.append(commentModel)
    else:
        print('暂时没有热门评论')
    return comments_Arr