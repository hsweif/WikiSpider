import urllib
import urllib2
import chardet
import time
import re
import sys
import os
import HTMLParser
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")
from HTMLParser import HTMLParser
 
class MyHTMLParser(HTMLParser):
     def __init__(self):
         HTMLParser.__init__(self)
         self.link = ''
     def handle_starttag(self, tag, attrs):
         if tag == "a":
             if len(attrs) == 0: pass
             else:
                 for (variable, value)  in attrs:
                     if variable == "href":
                         self.link = value

class WikiSpider:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64)')
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.__headers]
        self.count = 0
        self.pageNumber = 0
        self.infoURL_list = []
        self.pageURL_list = []
        self.parser = MyHTMLParser()
        self.url_set = set([])
        self.content = '' 
    def openURL(self, url):
        #req = Request(url)
        #req.add_header('user-agent', 'fake-client')
        #response = urllib2.urlopen(req)
        #content = response.read()
        self.content = self.__opener.open(url).read()
        encoding = chardet.detect(self.content)['encoding']
        self.content = self.content.decode(encoding, 'ignore')
    def addURL(self, url):
        self.pageURL_list.append(url)
    def getInfo(self):
        path = os.path.abspath(".")
        path += '/Data/'
        with open('record.txt', "r+")as rc:
            num = int(rc.read())
        file_name = str(num)
        file_name += '.html'
        with open(path + file_name, "w")as f:
            soup = BeautifulSoup(self.content, "html.parser")
            info_list = str(soup.find_all('table', class_ = 'infobox biography vcard'))
            self.count = self.count + 1
            infobox_soup = BeautifulSoup(info_list, "html.parser")
            photo_num = 1 
            for item in infobox_soup.find_all('tr'):
                #print item.get_text()
                image = item.find_all('a', class_ = 'image')
                for i in image:
                    if i != None : 
                        image_url = i.img['src']
                        urllib.urlretrieve('https:' + image_url, path+'Photo/'+str(num)+'_'+str(photo_num)+'.jpg')
                        photo_num = photo_num + 1
                        f.write('Image Path:' + image_url + '\n')
                if item.th != None :
                    #print item.th.string
                    if item.th.string != None :
                        f.write('#' + item.th.string + '\n')
                    #classfied_info += item.th.string
                for i in item.find_all('td'):
                    tmp = i.get_text()
                    if tmp.find(r'\n') != -1:
                        tmp = tmp.replace(r'\n', r'|')
                        #tmp = tmp.replace(u'\xa0', u' ')
                        k = 0
                        if tmp != None :
                            while tmp[k] == '|':
                                k = k + 1
                            else :
                                t = tmp[0:k].replace(r'|', r'')
                                tt = tmp[-k:].replace(r'|', r'')
                                tmp = t + tmp[k:-k] + tt
                    f.write(tmp + '\n')
                f.write('\n')
        num = num + 1
        tmp = str(num)
        with open('record.txt', "w")as rc:
            rc.write(tmp)

    def urlAvailable(self, url):
        key_list = re.findall('https://en.wikipedia.org/wiki/([^:]*):', url) 
        for key in key_list:
            if key == 'Wikipedia':
                return False
            elif key == 'Help':
                return False
            elif key == 'Category':
                return False
            elif key == 'Template':
                return False
            elif key == 'User':
                return False
            elif key == 'Special':
                return False
            elif key == 'Talk':
                return False
            elif key == 'Portal':
                return False
            elif key == 'Category_talk':
                return False
        if url == 'https://en.wikipedia.org/wiki/Main_Page': 
            return False
        return True
    def getNextURL(self):
        page_list = re.findall('(<a\s*href\s*=\s*"/w/index.php[^"]*"[^>]*>next page</a>)', self.content)
        print page_list
        k = 0
        while page_list:
            original_list = re.findall('<a\s*href\s*="(/wiki[^"]*)"', self.content) 
            for url in original_list:
                tmp = 'https://en.wikipedia.org' 
                tmp += url
                if self.urlAvailable(tmp) and tmp not in self.url_set:
                    self.infoURL_list.append(tmp)
                    self.pageNumber = self.pageNumber + 1
                    self.url_set.add(tmp)
                    print 'no. ', self.pageNumber, tmp
            tmp = 'https://en.wikipedia.org' 
            self.parser.feed(page_list[0])
            tmp += self.parser.link
            self.openURL(tmp)
            k = k + 1
            print 'page', k, tmp
            page_list = re.findall('(<a\s*href\s*=\s*"/w/index.php[^"]*"\s*title\s*=\s*"[^"]*">next page</a>)', self.content)
    def isInfoPage(self):
        pattern = re.compile('<table\s*class\s*=\s*"infobox biography vcard"\s*[^>]*')
        match = pattern.search(self.content)
        if match:
            return True
        else:
            return False
    def startSearch(self):    
        for pageURL in self.pageURL_list:
            self.openURL(pageURL)
            self.getNextURL()
            if self.pageNumber > 14000:
                break
        for url in self.infoURL_list:
            if self.count > 10500:
                break
            else :
                self.openURL(url)
                if self.isInfoPage():  
                    print 'Got info, no.', self.count, ' ', url
                    self.getInfo()
                    self.infoURL_list.remove(url)
                else :
                    print 'No info', url
    
spider = WikiSpider()
#spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_actresses')
#spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_male_actors')
#spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_singers')
#spider.addURL('https://en.wikipedia.org/wiki/Category:20th-century_American_businesspeople')
#spider.addURL('https://en.wikipedia.org/wiki/Category:African-American_basketball_players')
#spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_writers')
#spider.addURL('https://en.wikipedia.org/wiki/Category:American_film_directors')
#spider.addURL('https://en.wikipedia.org/wiki/Category:21st-century_American_painters')
#spider.addURL('https://en.wikipedia.org/wiki/Category:Japanese_actresses')
#spider.addURL('https://en.wikipedia.org/wiki/Category:Japanese_male_actors')
#spider.addURL('https://en.wikipedia.org/wiki/Category:British_writers')
spider.addURL('https://en.wikipedia.org/wiki/Category:Japanese_female_singers')
spider.addURL('https://en.wikipedia.org/wiki/Category:South_Korean_female_singers')
spider.addURL('https://en.wikipedia.org/wiki/Category:South_Korean_male_singers')
spider.addURL('https://en.wikipedia.org/wiki/Category:British_actresses')
spider.startSearch()
print 'work done!!!!'
