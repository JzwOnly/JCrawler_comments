import requests
from bs4 import BeautifulSoup
import math
import random
import json
import time
import datetime
import sched
import re

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36"
   ]

random_16_arr = ['FFFFFFFFFFFFFFFF',
                 'S9qbXofYW6x02sdP',
                 '2oKxqSBw1tT1ZrDO',
                 'EytcyRO3qeEyHEGu',
                 'G8f2DKyMrqFcOoyA',
                 'Uwa8J7UIVTrMs7x7',
                 'pU6fPG2nEwmvW2h2',
                 'bUR7DfDe5FLHgG8x',
                 'ZRJcuql9B8gIY3Bi',
                 'yZog8GG0zPTGBWsp']
encSecKey_arr = ['257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c',
                 'cc402fb10fb291abb17ec72b9daba1346b726e0e83b3fc60fcdff98b6385405e637cd7605d403c5aea41e9148e636a2d166c9a5228a4c2c02a0448855915ce2f98a9c923769b81cd41f40b731ec0e1e7ae3c410f4dd9cb9ca5d2b60440cbbc4a67dbca4ce35d32240e08c04889a0e2dedb654b474e9de28173823437a004075f',
                 'aaa2f069413e62154999bf8e4af91891a503f816841351265a84440ae33e5b2f737b0ab5e1e8acd615316114581c137e53e5570bbf8617c7983dd81a990328f5d3c5db52a92cdb7f3e3206884d00112725733e6d0851bbcef3ccd3b888c904f6ede4027dd25a4983652981f7e15a386e0b204bfb6c5a7a5e97b97c8ebc06ddb6',
                 '2d354726db43808952709355a17568a6ad66b557ecd856a27d9ab85d3d16204427c8839d2d4dde7beed3388b8b429fe6ac1384504fde4a5e10db9b02c41fe76d91c525fb8dc20bec9b09191d5dbc1158e4269eabd95012431e02e82c0c228214d04cd17d6f7349d9742e37a74ca2a731d48dff811ac51f5dc1b2a1cb73166dac',
                 '49a8cc07b572c67287c5d97f959045e1070a096a55c9fbff3a37c3b64c9967da91c9d09051896bc0a9df80d0c40487ea595f8cb378e060fcbecb29bd877945f610a53ffb295cee7e0b63ac087b63a0329a272a4f5899177ce20d7b8510ebde0858109672374b01e68220eddff26983c18d56f84009c569141de3d3911c2fbb89',
                 'd2d2a3d7d739b21930871fbb7906890637e171f71e824032f9a2159f2e2994e5cd662a7eac14a57fa2ad1d52bb93b497ef1c7666f97f9c0398a134e3a2bab1572546e3ca8029f77a8ab819936ba7f87de965fa65018eb7ddc92ebdd32280a0edfa899e2fe52b871871dde639e77066a50209b15ac1aa90e960c446345eb741bf',
                 'b69f93a14adea7cac42d3cb41ad0ce0786cae56c680383ad38ce0dc56192d99c652b4e2c172c07b6fa964d7409a8728121fd531d4cd123140c2e040817ffd1490e2ce4577fff2b00a8b76bd3c9a44eb8df6458fdf76031f4549c18d8d43feeaf4cd5c97f5971411b63bb448b82b166cf873690cd447a5079d28d8332509c4f47',
                 '62d0b38787f7a19f8eba53d5d1990d171842f883329ed6f1d0b06458c7c433b1de2288fbeafa140d90303f3e60e27abadf8789c73d7df7ca7fbbb270cb4a50b261bd33d0c82b243bb80c566ddf07fca63b19cea9667bfb086ef48684d09dca195f13a6da5f5a8ddbf9b844dd5094522768dc7634cd9c405e3bcb8abc7bb97726',
                 '5ae1dfae8256c41d2a82d323ad2b2b09610e1f3a4e3cf9cb26810608ab24b56119185a307513e51df38d560feebfd8b9d959029a4cc863f72555a497d1288df9cb110a53059ff64804b2431a05e23acce7508c52f5a35433f474c40133394c2fd8407e3680dd2971d87d33ae378c0e71ec3e6f41258f8d48e66de5f266d6d3c7',
                 '4ce19672f98b060378b3361f000d706984e013bf6e9674bae8cbaccbcd0df5f026d51d740ccdc32093cc895136981508b218ee1d57c626d1868261e55e765564f4ae44dd81eaee1b2d062f7101175b2b7aa3158c6227d8a3fa04b19713ab0a6d734915b57b797f360ae4885f3591c6e19e59443c5129bd535202ea83faaaa06a']
ip_pool = []


def getHeader(type):
    index = math.floor(random.random() * len(USER_AGENTS))
    if type == 'header':
        header = {
            'Referer': 'http://music.163.com/',
            'User-Agent': USER_AGENTS[index],
            'Host': 'music.163.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        return header
    elif type == 'ipHeader':
        header = {
            #'Referer': 'http://www.xicidaili.com/',
            # 'Referer':'http://www.89ip.cn/',
            'User-Agent': USER_AGENTS[index],
            'Host': 'www.xicidaili.com',
             #'Host':'www.89ip.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        return header
    elif type == 'checkIpHeader':
        header = {
            'User-Agent': USER_AGENTS[index],
            'Host': 'ip.chinaz.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        return header


def timeStampToDateStr(timeStap):
    timeArray = time.localtime(timeStap/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def timeStampToDate(timeStamp):
    aimDateTime = datetime.datetime.fromtimestamp(timeStamp/1000)
    return aimDateTime

def getNowDate():
    return datetime.datetime.now()

def radomSec():
    return random.randint(300,500)/100

class ScheduleTimer(object):

    def __init__(self,sleepTime,func):
        self.sleepTime = sleepTime
        self.func = func

    def __run_function(self):
        # 初始化sched模块的scheduler类
        s = sched.scheduler(time.time, time.sleep)
        # 设置一个调度,因为time.sleep()的时间是一秒,所以timer的间隔时间就是sleep的时间,加上enter的第一个参数
        s.enter(0, 2, self.func)
        s.run()

    def timer1(self):
        while True:
            # sched模块不是循环的，一次调度被执行后就Over了，如果想再执行，可以使用while循环的方式不停的调用该方法
            self.__run_function()
            time.sleep(self.sleepTime)


def getIp():
    ip_pool_Arr = []
    url = 'http://www.xicidaili.com/nn/'
    #url = 'http://www.bugng.com/gngn?page=0'
    s = requests.session()
    try:
        s = BeautifulSoup(s.get(url,headers=getHeader('ipHeader')).content,'lxml')
        # ip_arr = s.find('tbody',{'id':'target'}).find_all('tr')
        # for ipInfo in ip_arr:
        #     ip = ipInfo.find_all('td')[0].text
        #     port = ipInfo.find_all('td')[1].text
        #     ip_pool_Arr.append('{0}:{1}'.format(ip, port))
        # 1
        # ipHtml = s.find('p').text.split('<br/>')[0].replace('\r','').replace('\n','').replace(' ','')
        # ipArrTemp = ipHtml.split('\t')
        # ipArr = ipArrTemp[1:len(ipArrTemp)-1][::2]
        # ip_pool_Arr = ipArr
        #2 http://www.xicidaili.com/nn/
        ipList = s.find('table',{'id':'ip_list'}).find_all('tr')[1:]
        for ip in ipList:
            ipInfoList = ip.find_all('td')
            ip_pool_Arr.append('{0}:{1}'.format(ipInfoList[1].text,ipInfoList[2].text))
        # 3
        # temp = s.find('p').text
        # ipArrStr = temp[1:len(temp) - 1].replace('\\', '')
        # ipJson = json.loads(ipArrStr)['rows']
        # for ipInfo in ipJson:
        #     ip_pool_Arr.append('{0}:{1}'.format(ipInfo['ip'], ipInfo['port']))

    except Exception as e:
        print('Error',e)
        return None
    print('########################################完成ip获取总共{0}个'.format(len(ip_pool_Arr)))
    return ip_pool_Arr

def checkAvailableIp(ip_pool_Arr,index=None):
    availableIp_Arr = []
    url = 'http://ip.chinaz.com/getip.aspx'
    for ip in ip_pool_Arr:
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url, headers=getHeader('checkIpHeader'),proxies={'http':ip,'https':ip},timeout=5).content, 'lxml')
            ipWhere = s.find('p')
            onlyIp = re.match('(.*?):\d+$',ip)[1]
            if ipWhere != None:
                if onlyIp in ipWhere.text:
                    print('availableIP: ', ip, ipWhere.text)
                    availableIp_Arr.append(ip)
                else:
                    print('未知错误ip',ipWhere.text)
                    pass
        except Exception as e:
            print('Error ip:',ip)
    print('########################################完成第{0}次可用ip校验,可用ip共:{1}个'.format(index,len(availableIp_Arr)))
    return availableIp_Arr
def getIpPool1():
    ip_arr = checkAvailableIp(getIp())
    if len(ip_arr) > 0:
        index = math.floor(random.random() * len(ip_arr))
    else:
        getIpPool1()
    return ip_arr[index]
def getIpPool():
    print('开始', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    global ip_pool
    ip_arr = checkAvailableIp(getIp())
    # # 重复10次，保证该ip池稳定可用
    # for index in range(0,10):
    #     ip_arr = checkAvailableIp(ip_arr,index)
    if len(ip_pool) > 0:
        for index in range(0, 2):
            ip_pool = checkAvailableIp(ip_pool,index)
        ip_pool.extend(ip_arr)
    else:
        ip_pool = ip_arr
    print('结束', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def getAIp():
    if len(ip_pool) > 0:
        index = math.floor(random.random() * len(ip_pool))
        return ip_pool[index]

