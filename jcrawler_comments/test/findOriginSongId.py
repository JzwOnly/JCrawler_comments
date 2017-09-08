

from bs4 import BeautifulSoup
import requests

header = {
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host': 'music.163.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
def findOriginSongId():
    count = 0
    for index in range(33916,60000):
        url = 'http://music.163.com/song?id='+str(index)
        s = requests.session()
        try:
            s = BeautifulSoup(s.get(url, headers=header).content, "lxml")
            result = s.find('div',{'class':'m-lycifo'})
            if result == None:
                if s.find('div', {'class': 'n-for404'}) != None:
                    print(index,'404')
            else:
                print(index,'找到第一首歌')
                return index
        except requests.exceptions as e:
            print(e)
    print(count)
    return None


result = findOriginSongId()
if result != None:
    print('第一首歌id{0}'.format(result))