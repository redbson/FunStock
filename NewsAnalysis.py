# coding: utf-8

from bs4 import BeautifulSoup
from urllib2 import Request, urlopen


def DisguiseUrlOpen(url, headers = {'User-Agent':
                    'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20170203 Firefox/23.0'}):

    requst = Request( url = url, headers = headers)
    return urlopen(requst).read()


def GetNewsUrl( keyword, site = 'baidu', n = 500 ):

    def BaiduNewsConten( keyword, pn=0, rn=50):

        url = 'http://news.baidu.com/ns?word=%s&pn=%s&cl=2&ct=1&tn=news&rn=%s&ie=utf-8&bt=0&et=0' %( keyword, pn,rn)
        r = DisguiseUrlOpen(url)

        content = ''
        try:
            content = r.content.decode('utf8')
        except UnicodeDecodeError:
            content = r.content.decode('gbk')
        finally:
            return content

    def UrlExtract( keyword, site='baidu', n = 500):

        if site == 'baidu':
            contentList = [  BaiduNewsConten(keyword, (i-1)*50, 50)  for i in range(1,(n/50)+1)  ]
            soupList = map(BeautifulSoup, contentList)
            l = []

        for soup in soupList:
            div = soup.find_all('div', class_='result')
            l.extend([ d.a['href'] for d in div])

        return l

    return UrlExtract(keyword, site, n )


def GetNewsConten(url):

    def MaxLen(l):
        maxLen = 0
        result = None
        for i in l:
            if maxLen < len(i):
                maxLen = len(i)
                result = i
                # if maxLen == len(i): do someting
        return result

    r = DisguiseUrlOpen(url)

    try:
        content = r.content.decode('gbk')  # else gb2312
    except UnicodeDecodeError:
        content = r.content.decode('utf8') # else utf16

    #print(content)
    soup = BeautifulSoup(content)

    pSet = set([ p.parent for p in soup.find_all('p') ])
    newsContent = [ p.string for p in  MaxLen([p.find_all('p')  for p in pSet ])]


    s,t = '',''
    for sig in newsContent:
       s += ('%s' %sig).strip().replace(u'　','').replace('None','')

    for h in ['h1', 'h2', 'h3', 'h4']:
        if len(soup.find_all(h)) != 0:
            t = ('%s' %soup.find_all(h)[0].string).replace(u'　','').replace('\n','')
            return [t,s]
    return [t,s]


def GetNewsKeywords( h, c):
    pass

if __name__=="__main__":
    urlList =GetNewsUrl(u'银行')
    newsList  = [ GetNewsConten(url) for url in urlList]

    keyWordBag = [ GetNewsKeywords(news[0],news[1]) for news in newsList ]

